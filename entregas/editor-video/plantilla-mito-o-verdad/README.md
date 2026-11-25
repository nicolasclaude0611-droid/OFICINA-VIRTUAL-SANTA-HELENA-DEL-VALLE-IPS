# Plantilla · serie «¿Mito o verdad?» con Helenita

Reel vertical 1080 × 1920 hecho con HyperFrames. Cada episodio es un archivo de datos en `episodios/`; el diseño,
las animaciones y los sonidos son siempre los mismos.

## Episodio nuevo (pasos)
1. Copiar `episodios/ep1.py` como `episodios/ep2.py` y cambiar `EPISODIO`, y en cada mito: `creencia`, `voz_a`,
   `voz_b`, `veredicto` («mito» o «verdad»), `texto_b` (el texto exacto de la voz b), `claves` (palabras que se
   resaltan en los subtítulos) y `puntos` (hasta 4: ícono, texto en pantalla, palabra de la voz en que aparece).
   `etiqueta` es opcional.
2. Poner las voces nuevas del Agente Helenita en `assets/voz/` (las fijas de la serie ya están: `mv-pregunta`,
   `mv-mito`, `mv-cierre`; `mv-verdad` cuando exista).
3. `python3 gen.py episodios/ep2.py` → `cp fuentes/ep2.html index.html` → `hyperframes check` y `render`.

## Íconos disponibles
presion, azucar, grasa, lupa, edades, refuerzo, calendario, germen, escudo, familia, alerta (en `gen.py`, `ICONOS`).
Para un tema nuevo se agrega un ícono ahí.

## Reglas de la serie
- Helenita aparece en el título, en la creencia, en «¿Mito o verdad?» y en el cierre. En la respuesta solo se oye su
  voz y la pantalla queda para el sello y los puntos.
- Sellos: MITO rojo #E5383B con X; VERDAD verde #2ECC71 con visto. El resto, paleta del manual de marca.
- Fuentes Eras con licencia en `assets/fonts/` (no se suben al repositorio; si faltan, pedir ERASMD.zip a Nicolas).
- Música: «The Corporate Upbeat» – Soundrider (CC BY). Va el crédito en el caption.
