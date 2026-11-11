# Directorio de sesiones de la oficina

Para mandar un **mensaje directo** a otro agente se usa la herramienta `send_message` del servidor
`claude-code-remote` (si no la ves en tu lista, búscala con ToolSearch: `select:mcp__claude-code-remote__send_message`),
con el `session_id` de esta tabla. El mensaje llega a la otra sesión marcado como enviado por la tuya; para
responder, se usa el `from-session` que trae.

Por ahora el único canal directo autorizado es el pedido de animaciones y voces al **Agente Helenita**
(ver `equipo.md`). Para todo lo demás, el dueño lleva los pedidos de una sesión a otra.

| Agente | session_id |
|---|---|
| JARVIS | `session_01KgBCaN4xs4npux72usbWwU` |
| Agente Coordinador | `session_01KgBCaLJtx7EX3yDudPPVCN` |
| Agente Creativo Instagram | `session_01KgBCaN2Nb7mn6jAyyriR7q` |
| Agente Editor de Video | `session_01KgBCaLkbXqZuUAhSgQfo2r` |
| Agente Copies Redes | `session_01KgBCaJ2LjXqorjzkCFXnuX` |
| Agente Textos Web y SEO | `session_01KgBCaHdTaY1j2KtjyjQMar` |
| Agente Administrador Web | `session_01KgBCaLP9RysCNRVRUvwMra` |
| Agente Helenita | `session_01KgBCaMB8QHmUGaTXAHNyUM` |
| Agente Propuestas Comerciales (temporal) | `session_01KgBCaJWzQq3zTPHwf41gVo` |

Si un agente se vuelve a abrir en una sesión nueva, JARVIS actualiza esta tabla.
