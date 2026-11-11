# skill-voz-clonada

Una skill para Claude Code que escribe guiones **con tu forma de hablar**, más un script que los convierte en **voz en off con tu clon de voz local** eligiendo la mejor toma de cada línea.

## Qué hay

| Ruta | Qué es |
|---|---|
| `skill/voz-propia/SKILL.md` | La skill: ficha de tu voz (plantilla para completar), reglas para escribir texto que un clon lee bien, cierre (CTA) y checklist |
| `scripts/gen_voz.py` | Genera la voz línea por línea, verifica cada toma con whisper, une todo y masteriza a -16 LUFS. Devuelve `tiempos.json` para sincronizar el video |
| `ejemplos/guion_ejemplo.txt` | Guion de ejemplo en el formato que espera el script |

## Cómo funciona

1. **La skill escribe.** Claude arma el guion con tu ficha: una línea por bloque de 12-25 palabras, números en letras, ninguna afirmación que termine en "qué" o "cómo" (el clon la entonaría como pregunta).
2. **El script genera.** Cada línea es una llamada a tu servidor TTS con tu audio de referencia. Si tenés whisper.cpp, transcribe cada toma, la compara con el texto y prueba otra semilla si no coincide o sale demasiado rápida.
3. **Resultado:** `voz_master.wav` listo para el video y `tiempos.json` con inicio y fin de cada línea (sirve para subtítulos y cortes).

## Requisitos

- Python 3.10+, `ffmpeg`/`ffprobe` y `curl` en el PATH.
- Un servidor TTS de clonación local con `POST /generate` que acepte `text`, `language`, `ref_audio`, `ref_text`, `seed`, `num_step`, `guidance_scale`, `duration` y `effect_preset` (por ejemplo, uno basado en OmniVoice). Si el tuyo usa otros campos, adaptá el `curl` del script.
- Opcional: [whisper.cpp](https://github.com/ggerganov/whisper.cpp) para verificar las tomas.

## Uso

```bash
# 1. Instalar la skill en Claude Code
cp -r skill/voz-propia ~/.claude/skills/

# 2. Completar la sección "Ficha de la voz" de SKILL.md con tus patrones

# 3. Generar la voz
REF=mi_muestra.wav RT="texto exacto que digo en la muestra" \
WHISPER_CLI=/ruta/whisper-cli WHISPER_MODEL=/ruta/ggml-large-v3-turbo-q5_0.bin \
python scripts/gen_voz.py ejemplos/guion_ejemplo.txt salida
```

Más rápido (una toma por línea): `SEMILLAS=7 UMBRAL=0.90`. Las líneas con números suelen salir marcadas como "REVISAR" porque whisper escribe cifras: escuchalas igual.

## Privacidad y uso responsable

- **Nunca subas tu muestra de voz ni audios generados**: con eso cualquiera clona tu voz. El `.gitignore` ya excluye los formatos de audio.
- Usá el clon solo con tu propia voz o con permiso explícito de la persona.

## Licencia

MIT
