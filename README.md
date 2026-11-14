# Oficina virtual · Santa Helena del Valle IPS

Equipo de agentes de IA que trabajan en **Claude Code en la nube**. Cada agente tiene su propia sesión y su
rol; le escribes directamente a la sesión del agente que necesites.

| Agente | Para qué |
|---|---|
| **JARVIS** | Cerebro de la oficina: la dirige, mantiene reglas y roles, crea agentes y resuelve lo técnico |
| Agente Coordinador | Organiza pendientes e ideas y te dice a qué agente pasarle cada cosa |
| Agente Creativo Instagram | Posts, carruseles, historias, portadas e imágenes |
| Agente Editor de Video | Todos los reels y videos: edición y animación con HyperFrames |
| Agente Copies Redes | Captions, ganchos, guiones de reels y calendarios de contenido |
| Agente Textos Web y SEO | Artículos de blog, textos de la web y correos |
| Agente Administrador Web | Crea y actualiza la página web |
| Agente Helenita | Animaciones y voces de Helenita, y su catálogo |
| Agente Propuestas Comerciales (temporal) | Propuesta de negocio de la web para la gerencia |

## Estructura
- `CLAUDE.md` — reglas comunes para todos los agentes.
- `equipo.md` — quién hace qué.
- `agentes/` — la descripción de cada rol.
- `marca/marca.md` — resumen de la marca para los agentes; `marca/contexto-completo.md` — documento completo.
- `marca/img/` — logo, margarita con la S, Helenita y fotos de las sedes; logos en alta calidad en `marca/img/logos/`.
- `pendientes/` — lista de pendientes que lleva el Coordinador.
- `entregas/` — lo que entrega cada agente.
- `sesiones.md` — directorio de sesiones para los mensajes directos.
- `referencias/` — posts y videos de referencia que envía el dueño, con su análisis.
- La página web vive en otro repositorio: [`santa-helena`](https://github.com/nicolasclaude0611-droid/santa-helena), publicada en https://santahelenadelvalleips.com/ (Hostinger).
- El material aprobado se archiva en Google Drive (ver `CLAUDE.md`).

## Agregar un agente nuevo
Copia uno de los archivos de `agentes/`, cambia la misión y agrégalo a `equipo.md`. Luego abre una sesión
nueva y dile: "Eres el agente de `agentes/<archivo>.md`".

Basado en la idea de [Agentes IA 3D](https://github.com/ederland/Agentes_IA_3D) (MIT).
