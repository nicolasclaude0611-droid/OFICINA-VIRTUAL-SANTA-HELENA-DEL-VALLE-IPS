# Catálogo de Helenita

> Lo mantiene el **Agente Helenita**. Antes de pedir o generar algo nuevo, revisa aquí si ya existe.
> "Web" = repositorio público `nicolasclaude0611-droid/santa-helena` (rama `main`).

## Animaciones (todas sin fondo, se repiten sin corte, 5 s)
Cada una tiene en la web: `media/helenita/<nombre>.webm` (transparente), `<nombre>-stack.mp4` (Safari/iPhone)
y `<nombre>.png` (primer cuadro). El PNG también está en esta oficina, en `marca/img/helenita/`.
Original en verde: `helenita/fuentes/<nombre>-verde.mp4` (web).

| Nombre | Qué hace | Uso sugerido |
|---|---|---|
| `saludar` | Saluda con la mano derecha, sonríe | Inicio, bienvenida, presentaciones |
| `reposo` | Respira, parpadea, sonríe (quieta) | Espera, fondo de cualquier pieza |
| `hablar` | Habla y explica con la mano abierta | Explicaciones, consejos, guías |
| `pensar` | Se toca el mentón, piensa y sonríe | Preguntas frecuentes, "¿sabía que…?" |
| `senalar` | Señala hacia la derecha de la pantalla | Indicar un botón, texto o dato a la derecha |
| `pulgar` | Pulgar arriba, guiña el ojo | Confirmaciones, cierres, "¡listo!" |

Variantes:
- **Navidad (prueba, sin publicar):** `saludar` con gorro, en `media/helenita/navidad/` (web). Herramienta:
  `marca/helenita/tools/gorro.py`. El dueño avisará cuándo aplicarlo a las 6 y programarlo para diciembre.

Imagen base en verde para generar nuevas: `helenita/fuentes/helenita-base-verde.png` (web).
Referencias de apariencia: `marca/img/helenita/helenita-referencia.jpg` (cuerpo) y `helenita-closeup.jpg` (rostro).

## Voces (Valeria - Friendly Woman, `eleven_v4`)
En la web, `media/voz/`:

| Archivo | Texto exacto |
|---|---|
| `saludo.mp3` | «¡Hola! Soy Helenita. Con gusto le acompaño a agendar su cita.» |
| `paso1.mp3` | «Para comenzar, elija la sede donde desea ser atendido.» |
| `paso2.mp3` | «Muy bien. Ahora, elija el servicio que necesita.» |
| `paso3.mp3` | «Por último, escriba los datos del paciente.» |
| `listo.mp3` | «¡Listo! Su mensaje ya está en WhatsApp. Solo debe enviarlo.» |

## Piezas hechas con Helenita
- `entregas/editor-video/2026-10-30-prueba-helenita-logo.mp4` (rama `agente/editor-video`): video de prueba de
  10 s presentando el logo (saludar, señalar, pulgar), sin voz.

## Nuevas (agregadas por el Agente Helenita)
_Formato: fecha · archivo · qué hace o texto exacto · créditos gastados · para qué pieza/agente._
