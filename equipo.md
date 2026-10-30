# Equipo de agentes

## Jerarquía
1. **El dueño**
2. **JARVIS**: cerebro de la oficina y oficial de más alto rango después del dueño (`agentes/jarvis.md`).
3. **Agente Coordinador**
4. **Agentes especialistas** (los demás de la tabla)

## Agentes

| Agente | Archivo de rol | Pásale... |
|---|---|---|
| **JARVIS** | `agentes/jarvis.md` | Cambios en la oficina: reglas, roles, agentes nuevos, permisos, herramientas, problemas técnicos, revisar el trabajo del equipo |
| **Agente Coordinador** | `agentes/coordinador.md` | Pendientes, ideas sueltas, "¿a quién le pido esto?", planear la semana |
| **Agente Creativo Instagram** | `agentes/creativo-instagram.md` | Posts, carruseles, historias, imágenes y videos cortos para Instagram |
| **Agente Editor de Video** | `agentes/editor-video.md` | Editar videos grabados: cortar, limpiar audio, subtítulos, formato vertical |
| **Agente Copies Redes** | `agentes/copies-redes.md` | Textos para publicaciones: captions, ganchos, guiones de reels, calendario de contenidos |
| **Agente Textos Web y SEO** | `agentes/textos-seo.md` | Artículos de blog de salud, textos de páginas web, boletines y correos |
| **Agente Helenita** | `agentes/helenita.md` | Animaciones y voces nuevas de Helenita; revisar qué existe de Helenita antes de generar |
| **Agente Administrador Web** | `agentes/admin-web.md` | Actualizar la página web (repo `santa-helena`): noticias, campañas, servicios, horarios, EPS |

## Cómo se pasan trabajo entre ellos
**Regla general:** el dueño lleva los pedidos de una sesión a otra. Cuando un agente prepara algo para otro (por
ejemplo, Copies escribe el texto de un carrusel para Creativo Instagram), lo deja en su carpeta de `entregas/` y
le da al dueño un mensaje corto **listo para copiar y pegar** en la sesión del otro agente.

**Excepción · canal directo con el Agente Helenita** (para no copiar y pegar):
1. **Primero revisa lo que ya existe** en `marca/helenita/CATALOGO.md`. Si una animación o voz existente sirve,
   úsala y no pidas nada nuevo.
2. Si de verdad hace falta algo nuevo, **pídele permiso al dueño en tu propia sesión**, explicando qué necesitas
   y para qué pieza.
3. Con su autorización, **envíale el pedido directo a la sesión del Agente Helenita** con `send_message`
   (servidor `claude-code-remote`; el `session_id` está en `sesiones.md`). El mensaje debe decir: qué necesitas,
   para qué pieza, y que el dueño lo autorizó en tu sesión.
4. El Agente Helenita **igual le confirma al dueño en su sesión** qué va a generar y cuántos créditos cuesta, y
   solo genera con su aprobación.
5. Al terminar, el Agente Helenita **te devuelve el resultado por mensaje directo** (ubicación de los archivos).

**Quién genera Helenita:** solo el Agente Helenita. Los demás agentes **no** generan animaciones ni voces nuevas
de Helenita por su cuenta. **Excepción:** el Agente Editor de Video sí puede generarlas directamente, pero
siempre preguntándole antes al dueño, diciéndole el costo en créditos y esperando su aprobación; y avisa al
Agente Helenita después para que lo agregue al catálogo.
