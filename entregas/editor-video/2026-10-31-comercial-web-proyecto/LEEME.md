# Comercial «Helenita estrena casa» · proyecto HyperFrames

Video interno para los directivos (88 s, horizontal 1920×1080). Compara la página web vieja con la nueva.
Guion aprobado por el dueño: `../2026-10-31-guion-comercial-web.md` (versión 3).

## Escenas (`compositions/`)
| Archivo | Tiempo | Qué pasa |
|---|---|---|
| `encerrada.html` | 0–16,4 s | Página vieja en gris dentro de un monitor; Helenita quieta en un recuadro. Grietas, temblor y la página estalla como vidrio (dibujado sobre un lienzo) |
| `ahora.html` | 16–23,2 s | Aparece la página nueva; acercamiento a la Helenita de la página mientras saluda con su voz. «Antes: quieta. Ahora: habla.» |
| `hola.html` | 23–31,6 s | Helenita del video habla (V3) junto a la página |
| `agendar.html` | 31,6–49 s | «Antes: varios números» → agendador de la página nueva con la voz de la Helenita de la página |
| `claro.html` | 49–55,6 s | Servicios en computador y la página en celular |
| `mosaico.html` | 55,6–66 s | Noticias, sedes y mapa, preguntas frecuentes, PQRS |
| `viva.html` | 66–74,8 s | «Helenita está viva»: 6 expresiones del catálogo |
| `cierre.html` | 74,8–88 s | Helenita habla (V8) y cierre con el logo |

En `hola.html` y `cierre.html` Helenita habla con la boca al ritmo de su voz (`assets/helenita/boca-v3.webm` y
`boca-v8.webm`, del Agente Helenita). Con ellas se usa la voz exacta de la sincronización (`assets/voz/boca-v3.mp3` y
`boca-v8.mp3`), no `v3`/`v8`, para que la boca no se desfase. La V8 ya dice «Cesar» (corrección del dueño).

## Material
- **Voces** (`assets/voz/`): `v1`, `v2`, `v4`–`v7`, `boca-v3` y `boca-v8` las generó el Agente Helenita (ElevenLabs, Valeria). `pagina-*.mp3` son las
  voces que ya usa la página web.
- **Grabaciones** (`assets/grab/`): hechas con el navegador el 31-oct-2026. En el agendador se usaron **datos
  inventados** («Paciente de ejemplo», documento 1000000000), no datos de pacientes.
- **Música** (licencia Creative Commons Atribución 3.0, permite uso comercial dando crédito):
  - «The Corporate Upbeat», Soundrider/Dope, Jamendo (pista 1670594).
  - «Wingspan», Blue Dot Sessions, Jamendo (pista 1365390).
- **Efectos de sonido:** los que trae HyperFrames y los de Pixabay de la prueba anterior (`assets/sfx/CREDITS.md`).

## Volver a exportar
`npx hyperframes render --quality delivery --video-frame-format png -o renders/comercial.mp4` dentro de esta carpeta.
