---
name: voz-propia
description: "Use for text that will be spoken or signed as the creator: voice-over scripts for a local voice clone, explanations and pitches in their own speech style. Holds the creator's speech profile (ficha), the rules for writing text a voice clone reads well, the CTA rules and a pre-delivery checklist. NOT for hooks/cuts, captions/hashtags or video editing."
---

# Voz propia

Skill para escribir guiones **con el estilo de habla de un creador** y que **un clon de voz local los lea bien**.
Tiene tres partes: la ficha de cómo habla la persona (se completa una vez), las reglas para escribir para el clon (medidas, sirven para cualquiera) y el checklist.

## 1. Ficha de la voz (completar con tus datos)

Cómo armarla: grabá 4-6 audios improvisados (charla, explicar algo, vender algo), transcribilos con whisper y anotá patrones, **no contenido**. Después leé en voz alta 2-3 guiones escritos con la ficha y anotá cada palabra que cambiás al leer: eso es lo más valioso.

Plantilla (reemplazá los ejemplos):
- **Variedad y trato:** p. ej. rioplatense con "vos". Si con clientes mezclás "vos" y "usted", elegir uno por texto.
- **Saludo propio:** tu muletilla de apertura. Usarla como máximo en 1 de cada 2 videos seguidos, y nunca en un pitch.
- **Arranque típico:** ¿le hablás a alguien concreto? ¿corregís algo? Anotá 2-3 frases reales.
- **Repetición para remarcar:** si repetís frases ("es una locura, es una locura"), una por guion, en el punto fuerte.
- **Contraste con número:** "no fueron 4 ni 5, fueron 38". Escala de lo esperable a lo enorme.
- **Cómo explicás:** p. ej. A vs B y bajar a lo práctico.
- **Conectores y muletillas:** lista corta. Tope: 1 de cada una cada ~50 palabras; exagerarlas suena a parodia.
- **Palabras que no son tuyas:** lo que la IA tiende a poner y vos no decís. Prohibidas.
- **Frases armadas en voz alta:** preferir la forma larga y llana ("es lo que", "porque") a la elíptica.

## 2. Reglas al escribir

- Frases de 6-14 palabras, conservando tus conectores.
- Nada de lenguaje de gurú: "descubrí el poder de…", "en este video te voy a enseñar", "sin más preámbulos", "game changer".
- Pitch a cliente: primero el resultado para el negocio (más gente, más ventas), el proceso después y corto.
- Cifras: nunca inventar números como si fueran reales.

## 3. Cierre (CTA)

Todo video termina con **un pedido que cambia**, pegado a la última idea (con punto en el medio el clon se traba):
- **Mandáselo** (por defecto; los envíos son lo que más empuja el alcance): "Mandáselo al que te dijo que C++ era un monstruo."
- **Guardalo** (videos que explican): "Guardalo, que el día que te trabes con punteros lo vas a buscar."
- **Te leo** (opinión): "¿Vos qué le preguntarías? Dejámelo abajo."
- **Sigue la serie** (solo si hay próximo capítulo real): sin fecha, haciendo desear la parte siguiente.
- Una acción, ≤ 12 palabras, que nombra algo **del propio video**. Rotar el tipo.
- Prohibido: "seguime para más", "dale like", "activá la campanita", "comentá INFO".

## 4. Escribir para el clon de voz

El clon copia bien el tono; lo que lo delata es el armado del texto.

**Bloques, no frases sueltas**
- Una línea del guion = un bloque = una llamada al motor: 1 a 3 frases, 12 a 25 palabras (4 a 7 s).
- **Línea en blanco = cambio de idea** (pausa 0,5 s). Líneas seguidas = misma idea (0,25 s).
- Ninguna frase de menos de 6 palabras va sola en una línea: sola sale atropellada. El saludo va con la primera frase; el remate corto, con la frase que remata.
- No más de 3 frases cortas seguidas: suena a telegrama.

**Puntuación (el clon la obedece)**
- Punto = bajada y pausa. Coma = pausa corta.
- Preguntas con "¿…?" completas. **Una afirmación no termina en "quién", "cómo", "qué", "cuál", "dónde"**: el clon la sube como pregunta.
- Sin "...", paréntesis, comillas ni "¡!" en cadena. Toda línea termina en punto, "?" o "!".

**Números y palabras difíciles**
- Números **siempre en letras** y como los decís ("cuatro millones ocho", nunca "4.8").
- Verbos donde el acento cambia el sentido (gano/ganó) no van al final de la frase.
- Si una palabra falla dos veces, cambiala o escribila como suena. Inglés y siglas como suenan.
- Nombres propios difíciles: escribilos como se pronuncian (en pantalla van bien escritos).

**Largo**
- Ritmo de referencia ~3,6 palabras/s ≈ 6 sílabas/s contando pausas. 15 s ≈ 55 palabras; 30 s ≈ 110; 45 s ≈ 160.
- Duración estimada por línea: sílabas ÷ 6,6 + 0,3 s por punto interno.

**Energía**
- Arriba del guion, qué referencia de audio usar (p. ej. `charla` o `arriba`). El clon copia la energía de la muestra, no la del texto: los "!" no lo hacen gritar.

## 5. Checklist antes de entregar
- [ ] ¿Lo dirías en un audio? Leelo en voz alta mentalmente.
- [ ] ¿Trato consistente (vos/usted)? ¿Muletillas dentro del tope?
- [ ] ¿Cero frases de gurú y cero cifras inventadas?
- [ ] ¿Largo = segundos × 3,6 palabras (±10 %)?
- [ ] ¿Una línea por bloque de 12-25 palabras, sin frases cortas solas?
- [ ] ¿Ninguna afirmación termina en quién/cómo/qué? ¿Números en letras?
- [ ] ¿Dice qué referencia de audio usar?
- [ ] ¿Cierra con un pedido que nombra algo del video y no repite el anterior?
- [ ] ¿El arranque es distinto al del video anterior?

Para generar el audio: `scripts/gen_voz.py` (ver README).
