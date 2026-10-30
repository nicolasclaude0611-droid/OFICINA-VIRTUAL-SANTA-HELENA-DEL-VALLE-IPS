# Oficina virtual · Santa Helena del Valle IPS

Equipo de agentes de IA que trabajan en **Claude Code en la nube**. Cada agente tiene su propia sesión y su
rol; le escribes directamente a la sesión del agente que necesites.

| Agente | Para qué |
|---|---|
| Agente Coordinador | Organiza pendientes e ideas y te dice a qué agente pasarle cada cosa |
| Agente Creativo Instagram | Posts, carruseles, historias, imágenes y videos cortos |
| Agente Editor de Video | Edita videos grabados: cortes, audio, subtítulos, formato vertical |
| Agente Copies Redes | Captions, ganchos, guiones de reels y calendarios de contenido |
| Agente Textos Web y SEO | Artículos de blog, textos de la web y correos |
| Agente Administrador Web | Crea y actualiza la página web |

## Estructura
- `CLAUDE.md` — reglas comunes para todos los agentes.
- `equipo.md` — quién hace qué.
- `agentes/` — la descripción de cada rol.
- `marca/marca.md` — datos e identidad de la IPS. **Complétalo**: es lo que más mejora el trabajo.
- `pendientes/` — lista de pendientes que lleva el Coordinador.
- `entregas/` — lo que entrega cada agente.
- `web/` — la página web.

## Agregar un agente nuevo
Copia uno de los archivos de `agentes/`, cambia la misión y agrégalo a `equipo.md`. Luego abre una sesión
nueva y dile: "Eres el agente de `agentes/<archivo>.md`".

Basado en la idea de [Agentes IA 3D](https://github.com/ederland/Agentes_IA_3D) (MIT).
