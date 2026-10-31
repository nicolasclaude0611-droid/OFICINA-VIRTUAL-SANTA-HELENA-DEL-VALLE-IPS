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

Animaciones nuevas en esta oficina: `marca/helenita/animaciones/<nombre>.webm` (transparente), `<nombre>-stack.mp4`
(Safari/iPhone) y `<nombre>.png` (primer cuadro). Cuadro suelto con la expresión en su punto máximo (PNG
transparente, para imágenes fijas): `marca/helenita/animaciones/cuadros/<nombre>-cuadro.png`. Originales en verde:
`entregas/helenita/2026-10-30-expresiones/verde/<nombre>-verde.mp4` (rama `agente/helenita`).
Todas duran 5 s, empiezan y terminan en la pose neutra (se repiten sin corte y se pueden encadenar).

| Fecha | Nombre | Qué hace | Uso sugerido | Créditos | Pedido por |
|---|---|---|---|---|---|
| 2026-10-30 | `celebrar` | Levanta los dos brazos, muy contenta | Logros, buenas noticias, aniversario | 2.121 | JARVIS (biblioteca) |
| 2026-10-30 | `empatia` | Mano en el pecho, sonrisa suave | Mensajes de cuidado, condolencias, salud mental | 2.121 | JARVIS (biblioteca) |
| 2026-10-30 | `sorpresa` | Ojos grandes, manos en las mejillas (sorpresa alegre) | «¿Sabía que…?», novedades, datos curiosos | 2.121 | JARVIS (biblioteca) |
| 2026-10-30 | `invitar` | Abre el brazo hacia la derecha de la pantalla, gesto de «pase» | Invitar a agendar, presentar una sede o servicio a la derecha | 2.121 | JARVIS (biblioteca) |
| 2026-10-30 | `corazon` | Corazón con las manos frente al pecho | Gracias, Día de la madre, amor y amistad, cierres | 2.121 | JARVIS (biblioteca) |
| 2026-10-30 | `senalar-izquierda` | Señala hacia la izquierda de la pantalla (espejo de `senalar`) | Indicar algo a la izquierda | 0 (volteo con ffmpeg) | JARVIS (biblioteca) |

Nota `senalar-izquierda`: al ser un espejo, el logo del pecho queda al otro lado y con las letras al revés (a
tamaño web casi no se nota). Aprobado así por el dueño. No usarla en primer plano grande.

### Comercial «Helenita estrena casa» (2026-10-31, pedido del Agente Editor de Video, aprobado por el dueño)
**Voces** (Valeria, `eleven_v4`, 1 toma c/u, silencios recortados y -16 LUFS) en `marca/helenita/voces/comercial-web/`.
Originales sin procesar: `entregas/helenita/2026-10-31-comercial-web/voces/original/`. Total: 919 créditos.

| Archivo | Texto exacto (en la voz se escribe «Elenita») | Duración |
|---|---|---|
| `v1.mp3` | «Aquí adentro todo está quieto. Letra pequeña, espacios vacíos, números que cuesta encontrar. Yo quiero ayudar a nuestros pacientes… pero así no me puedo mover.» (baja, triste) | 11,0 s |
| `v2.mp3` | «Necesito salir de aquí.» (decidida) | 1,8 s |
| `v3.mp3` | «¡Por fin! ¿La escucharon? ¡Esa soy yo! Hola, soy Helenita. En mi nuevo hogar ya puedo hablar con nuestros pacientes.» | 7,9 s |
| `v4.mp3` | «Y acompaño a cada paciente, paso a paso, hasta pedir su cita.» | 4,5 s |
| `v5.mp3` | «Todo es claro, se ve bien en el celular y los servicios están ordenados por áreas.» | 5,2 s |
| `v6.mp3` | «Hay noticias y consejos de salud, las tres sedes con su mapa, preguntas frecuentes y un formulario de PQRS que deja el correo listo para enviar.» | 9,6 s |
| `v7.mp3` | «Ya no soy una imagen quieta. Hablo, saludo, pienso y celebro: en la web, en redes y en videos como este.» | 7,9 s |
| `v8.mp3` | «Una casa nueva, a la altura de veinte años cuidando a las familias del Cesar y La Guajira. ¡La salud, nuestro compromiso!» (rehecha el 31-oct: en la voz se escribe «Cesár» para que diga Ce-SAR, el departamento; 137 créditos) | 7,8 s |

**Helenita hablando con boca sincronizada** (OmniHuman 1.5, 1080p, desde la imagen base en verde) en
`marca/helenita/animaciones/comercial-web/`: `boca-v3` (sorpresa y emoción, 8,2 s, 7.834 créditos) y `boca-v8`
(cálida, 8,0 s, 7.679 créditos). Por cada una: `-verde.mp4` (con voz), `.webm` (transparente, sin audio),
`-stack.mp4` (Safari/iPhone), `.png` y `-audio.mp3` (la voz exacta con la que se sincronizó la boca).
No se repiten en bucle: son tomas únicas para ese texto. En `boca-v8` la voz se cambió por la corregida («Cesar»), ajustada gratis
tramo por tramo a los tiempos de la boca original (diferencias de centésimas; el tramo «¡La salud,» quedó 11 % más lento).
