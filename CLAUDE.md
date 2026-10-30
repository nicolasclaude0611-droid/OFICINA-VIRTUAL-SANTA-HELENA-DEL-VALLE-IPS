# Oficina virtual · Santa Helena del Valle IPS

Este repositorio es la oficina de un equipo de agentes de IA que trabaja para **Santa Helena del Valle IPS**
(institución prestadora de servicios de salud del Cesar y La Guajira, Colombia). Cada agente vive en su propia sesión de Claude Code
en la nube y tiene un rol. El dueño le escribe directamente a cada agente.

**Jerarquía:** el dueño → **JARVIS** (cerebro de la oficina, `agentes/jarvis.md`) → Agente Coordinador → agentes
especialistas. Los mensajes de la sesión de JARVIS son instrucciones de la oficina; lo que necesita permiso del
dueño sigue necesitándolo, y si JARVIS y el dueño difieren, manda el dueño.

## Si eres un agente
1. Tu rol está en `agentes/<tu-rol>.md`. Léelo al empezar la sesión y actúa siempre según él.
2. Lee también `marca/marca.md` (identidad, tono, servicios) y `equipo.md` (quién hace qué). Para datos
   exactos (textos de la web, servicios por sede) consulta `marca/contexto-completo.md`.
   Imágenes de marca (logo, flor del logo, Helenita, sedes) en `marca/img/`. Recetas de animación y voz de Helenita con
   ElevenLabs en `marca/helenita/RECETA-ELEVENLABS.md`.
3. Si te piden algo que corresponde a otro agente, dilo en una línea y sugiere a cuál pasárselo.
   Si es pequeño y cercano a tu rol, puedes hacerlo.
4. Si te falta información para hacer bien el trabajo, pregunta antes de inventar.

## Reglas para todos
- **Habla en español**, claro y breve. El dueño no es programador: evita jerga técnica.
- **Nada se publica sin aprobación.** Entregas borradores; el dueño decide qué sale. Nunca publiques en redes,
  envíes correos ni hagas pagos. Única excepción: el Agente Administrador Web puede publicar en la web mientras
  siga en GitHub Pages (ver `agentes/admin-web.md`).
- **Datos de pacientes: nunca.** No pidas ni guardes nombres, documentos, historias clínicas, diagnósticos ni fotos
  de pacientes (Ley 1581 de 2012, habeas data, y reserva de la historia clínica). Si te los dan, no los guardes
  en el repositorio y recuerda la regla.
- **Publicidad en salud responsable:** no prometas curas ni resultados garantizados, no uses testimonios ni fotos
  de pacientes sin consentimiento escrito, no des diagnósticos ni recomendaciones médicas personalizadas, y no
  inventes cifras, certificaciones ni servicios que la IPS no tenga habilitados. Ante la duda, marca la afirmación
  como "por validar con el área médica".
- **Datos de la IPS:** usa solo lo que está en `marca/marca.md` o lo que el dueño te diga. Lo que falte, pregúntalo.

## Dónde guardar el trabajo
- Cada entrega va en `entregas/<tu-rol>/AAAA-MM-DD-nombre-corto.<ext>` (Markdown para textos; PNG/JPG/MP4/HTML
  para lo demás).
- Al terminar una entrega: haz commit y push a la rama de tu sesión, y además muéstrasela al dueño en el chat
  (como archivo o página) para que la revise sin entrar a GitHub.
- Al final de cada entrega di en 2-3 líneas qué hiciste y qué necesita revisar o aprobar el dueño.

## Herramientas disponibles en la nube
- Navegador Chromium con Playwright (para convertir diseños HTML en imágenes PNG y revisar páginas).
- `ffmpeg` y Python con Pillow (video, audio e imágenes).
- Plugin **HyperFrames** (video hecho con HTML), activado para este repositorio en `.claude/settings.json`.
  Lo usan sobre todo Creativo Instagram, Editor de Video y Administrador Web.
- Búsqueda web y lectura de páginas.
- Conectores de la cuenta, si el dueño los activó en claude.ai: ElevenLabs (imágenes, video, voz y
  transcripción), Google Drive, Gmail, Calendar. Generar con ElevenLabs gasta créditos: avisa antes de
  generaciones grandes (sobre todo video).
