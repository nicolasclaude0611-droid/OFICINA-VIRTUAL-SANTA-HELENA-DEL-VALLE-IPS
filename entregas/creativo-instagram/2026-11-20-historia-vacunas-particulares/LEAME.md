# Historia semanal · Vacunas particulares (plantilla reutilizable)

Encargo directo del Agente Copies Redes con textos aprobados por Nicolas
(`entregas/copies-redes/2026-11-20-historia-vacunas-particulares.md`, rama agente/copies-redes). Borrador para aprobación.

- **Variación A lista** en `A/`: `pantalla-1.mp4`, `pantalla-2.mp4`, `pantalla-3.mp4` (1080 × 1920, 7 s cada una,
  Helenita animada con «invitar», sin voz) y las mismas pantallas en PNG sin Helenita. `vista-general.png`: resumen.
- **WhatsApp 301 655 3822: exclusivo de esta historia semanal.** No usar en otras piezas.
- Estilo del **manual de identidad** (degradado azul, logo con contorno blanco, letra Eras, amarillo solo en el botón
  y acentos). Zona segura: el texto importante queda entre ~250 px arriba y la franja de abajo.

## Cómo sacar otra semana (B1 influenza, B2 varicela y herpes zóster, B3 VPH)
1. Textos: `plantilla/textos.js` (un bloque por variación; para cambiar un texto, solo se edita ahí).
2. Ejecutar `bash plantilla/crear-videos.sh B1` (o B2, B3). Crea la carpeta `B1/` con los 3 PNG y los 3 MP4.
   Necesita las fuentes Eras instaladas (no se guardan aquí por licencia), Node con Playwright y ffmpeg.
- `plantilla/historia.html?v=A&p=1` muestra cada pantalla en el navegador. Helenita se agrega con ffmpeg
  (`plantilla/img/invitar.webm`, animación existente, sin gasto de créditos).
