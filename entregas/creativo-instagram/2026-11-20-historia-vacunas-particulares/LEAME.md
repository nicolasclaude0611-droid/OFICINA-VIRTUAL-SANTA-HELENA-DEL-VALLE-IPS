# Historia semanal · Vacunas particulares (plantilla reutilizable)

Encargo directo del Agente Copies Redes con textos aprobados por Nicolas
(`entregas/copies-redes/2026-11-20-historia-vacunas-particulares.md`, rama agente/copies-redes). Borrador para aprobación.

- **Variación A lista** en `A/`: `pantalla-1.png`, `pantalla-2.png`, `pantalla-3.png` (1080 × 1920, en imagen, no video,
  por decisión de Nicolas). Helenita: pantalla 1 con la mano abierta («invitar»), pantalla 2 sin Helenita (lista en
  una sola columna), pantalla 3 haciendo el corazón. `vista-general.png`: resumen.
- **WhatsApp 301 655 3822: exclusivo de esta historia semanal.** No usar en otras piezas.
- Estilo del **manual de identidad** (degradado azul, logo con contorno blanco, letra Eras, amarillo solo en el botón
  y acentos). Zona segura: el texto importante queda entre ~250 px arriba y la franja de abajo.

## Cómo sacar otra semana (B1 influenza, B2 varicela y herpes zóster, B3 VPH)
1. Textos: `plantilla/textos.js` (un bloque por variación; para cambiar un texto, solo se edita ahí).
2. Ejecutar `bash plantilla/crear-imagenes.sh B1` (o B2, B3). Crea la carpeta `B1/` con los 3 PNG.
   Necesita las fuentes Eras instaladas (no se guardan aquí por licencia) y Node con Playwright.
- `plantilla/historia.html?v=A&p=1` muestra cada pantalla en el navegador. Helenita: cuadros existentes, sin gasto de créditos.
- Sin la línea «No necesita orden médica» (la quitó Nicolas el 20 nov).
