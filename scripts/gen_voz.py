"""Genera una voz en off con un clon de voz local, línea por línea, eligiendo la mejor toma.

Uso:
  REF=muestra.wav RT="texto exacto de la muestra" python gen_voz.py guion.txt carpeta_salida

Guion: una línea = un bloque (12-25 palabras); línea en blanco = cambio de idea (pausa más larga).
Salida: voz.wav (unión cruda), voz_master.wav (masterizada a -16 LUFS) y tiempos.json (inicio/fin por línea).

Variables de entorno:
  REF, RT          (obligatorias) audio de referencia de tu voz y su transcripción exacta
  TTS_URL          servidor TTS con POST /generate (default http://127.0.0.1:3900/generate)
  WHISPER_CLI      ruta a whisper-cli (whisper.cpp) para verificar cada toma; si falta, no verifica
  WHISPER_MODEL    modelo ggml de whisper
  SEMILLAS         semillas a probar por línea (default "7,11,23,31,47"); "7" = una sola toma, más rápido
  UMBRAL           parecido mínimo texto/whisper para aceptar una toma (default 0.97)
  MODO=bloques|frases, PRESET=raw|broadcast, CUT=nuevo|viejo, MASTER=1|0, DUR=silabas|no, GS=2.0, STEPS=32, SHELF=4
"""
import os, re, sys, json, subprocess, difflib

E = os.environ.get
REF, RT = E("REF"), E("RT")
if not REF or not RT:
    sys.exit("Faltan REF (audio de referencia) y RT (su transcripción). Ver el encabezado del script.")
URL = E("TTS_URL", "http://127.0.0.1:3900/generate")
W, M = E("WHISPER_CLI"), E("WHISPER_MODEL")
SEEDS = [int(s) for s in E("SEMILLAS", "7,11,23,31,47").split(",")]
UMBRAL = float(E("UMBRAL", "0.97"))
MODO, PRESET, CUTM, MASTER, DUR = E("MODO", "bloques"), E("PRESET", "raw"), E("CUT", "nuevo"), E("MASTER", "1"), E("DUR", "silabas")
GS, STEPS = E("GS", "2.0"), E("STEPS", "32")
CUTS = {
    "viejo": "silenceremove=start_periods=1:start_threshold=-35dB,areverse,silenceremove=start_periods=1:start_threshold=-35dB,areverse",
    "nuevo": "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03,areverse,"
             "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,"
             "afade=t=in:d=0.012,areverse,afade=t=in:d=0.03,areverse",
}
MASTER_AF = ("highpass=f=75,equalizer=f=250:t=q:w=1.0:g=-2,equalizer=f=3200:t=q:w=1.2:g=2.5,"
             "highshelf=f=6000:g=" + E("SHELF", "4") + ",deesser=i=0.4:m=0.5:f=0.5:s=o,"
             "acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,"
             "alimiter=limit=0.89:level=false,loudnorm=I=-16:TP=-1.5:LRA=7")

guion, D = sys.argv[1], os.path.abspath(sys.argv[2])
os.makedirs(D, exist_ok=True)
T = open(guion, encoding="utf-8").read().strip()

# Unidades de generación y la pausa que va DESPUÉS de cada una
if MODO == "frases":
    fr = [f.strip() for f in re.findall(r"[^.!?]+[.!?]?", " ".join(T.split())) if f.strip()]
    units = [(f, float(E("PAUSA", "0.32"))) for f in fr]
else:
    units, lines = [], T.splitlines()
    for i, l in enumerate(lines):
        if not l.strip():
            continue
        nxt = lines[i + 1] if i + 1 < len(lines) else "x"
        units.append((l.strip(), 0.50 if not nxt.strip() else 0.25))

sil = lambda s: len(re.findall(r"[aeiouáéíóúü]+", s.lower()))
norm = lambda s: re.sub(r"[^a-z0-9ñáéíóú]", "", s.lower())
dur_of = lambda p: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


def escuchar(wav):
    """Transcribe la toma con whisper.cpp; None si no está configurado."""
    if not (W and M and os.path.exists(W)):
        return None
    w16 = wav[:-4] + "_16.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-ar", "16000", "-ac", "1", w16], check=True)
    return subprocess.run([W, "-m", M, "-l", "es", "-nt", "-np", "-f", w16], capture_output=True, text=True).stdout.strip()


parts, tl, t = [], [], 0.0
for i, (txt, pausa) in enumerate(units):
    best = None
    for seed in SEEDS:
        crudo, out = os.path.join(D, f"_c{i}_{seed}.wav"), os.path.join(D, f"_f{i}_{seed}.wav")
        cmd = ["curl", "-s", "-m", "300", "-X", "POST", URL, "-F", f"text={txt}", "-F", "language=es",
               "-F", f"ref_audio=@{REF}", "-F", f"ref_text={RT}", "-F", f"num_step={STEPS}", "-F", f"seed={seed}",
               "-F", f"guidance_scale={GS}", "-F", f"effect_preset={PRESET}", "-o", crudo]
        if DUR == "silabas":
            internos = len(re.findall(r"[.!?](?=\s)", txt))
            cmd[-2:-2] = ["-F", f"duration={round(sil(txt) / 6.6 + 0.30 * internos + 0.35, 2)}"]
        subprocess.run(cmd, check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", crudo, "-af", CUTS[CUTM], "-ar", "24000", "-ac", "1", out], check=True)
        oido = escuchar(out)
        if oido is None:
            r, oido = 1.0, ""
        else:
            r = difflib.SequenceMatcher(None, norm(txt), norm(oido)).ratio()
            if re.search(r"\d", oido):  # whisper escribe números con cifras: no castigar por eso
                r = max(r, difflib.SequenceMatcher(None, re.sub(r"\d", "", norm(txt)), re.sub(r"\d", "", norm(oido))).ratio())
        vel = sil(txt) / max(dur_of(out), 0.1)
        score = r - (0.05 if vel > 8.0 else 0)
        if not best or score > best[0]:
            best = (score, out, oido, r, vel, seed)
        if r >= UMBRAL and vel <= 8.0:
            break
    _, out, oido, r, vel, seed = best
    d = dur_of(out)
    tl.append({"i": i, "inicio": round(t, 2), "fin": round(t + d, 2), "texto": txt, "oido": oido,
               "parecido": round(r, 2), "silabas_s": round(vel, 1), "semilla": seed})
    parts.append(out)
    t += d
    if i < len(units) - 1:
        s = os.path.join(D, f"_sil_{pausa}.wav")
        if not os.path.exists(s):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(pausa), s], check=True)
        parts.append(s)
        t += pausa

lst = os.path.join(D, "_l.txt")
with open(lst, "w", encoding="utf-8") as fh:
    for p in parts:
        fh.write("file '" + p + "'\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", os.path.join(D, "voz.wav")], check=True)
if MASTER == "1":
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(D, "voz.wav"), "-af", MASTER_AF, "-ar", "48000", "-c:a", "pcm_s16le",
                    os.path.join(D, "voz_master.wav")], check=True)
json.dump({"config": dict(MODO=MODO, PRESET=PRESET, CUT=CUTM, MASTER=MASTER, DUR=DUR, GS=GS, STEPS=STEPS), "tiempos": tl},
          open(os.path.join(D, "tiempos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(round(t, 2), "s", round(len(T.split()) / t, 2), "pal/s")
for x in tl:
    if x["parecido"] < UMBRAL or x["silabas_s"] > 8.0:
        print("REVISAR", x["inicio"], x["parecido"], x["silabas_s"], "síl/s |", x["oido"][:80])
for f in os.listdir(D):
    if f.startswith("_"):
        os.remove(os.path.join(D, f))
