# Web nueva para Hostinger · 11 nov 2026

**Archivo:** `web-nueva-santa-helena.zip` (3,8 MB, 43 archivos en la raíz del ZIP, sin carpeta contenedora).
Código fuente: repositorio `santa-helena`, rama `web-hostinger` (commit 877b49f).

## Qué trae
- La página (index, política de datos, términos, 404), estilos, código, imágenes, fotos, Helenita y voces.
- `.htaccess`: https obligatorio, sin www, cabeceras de seguridad (CSP que permite Google Maps, Google Fonts y wa.me),
  caché de imágenes y videos, compresión, página 404 y redirecciones 301 del WordPress viejo.
- `robots.txt`, `sitemap.xml`, canonical y metadatos para redes con `img/compartir.jpg`.
- Todas las direcciones son relativas o apuntan a https://santahelenadelvalleips.com/ (ninguna a github.io).

## Redirecciones del sitio viejo
- `/solicitud-de-citas/` (enlace del Instagram), `/solicitud-de-citasbk/`, `/citasdondoctor/` → `/#agendar`
- Páginas de servicios (medicina general, enfermería, ginecología, pediatría, nutrición, psicología, laboratorio,
  citología, control prenatal, etc.) → `/#servicios`
- `/acercadenosotros/`, `/valores-corporativos/`, `/estructura-organizacional/` → `/#nosotros`
- `/contactos/` → `/#sedes`
- Resto de páginas viejas, noticias, categorías y rutas de WordPress (`/wp-admin/`, `/wp-login.php`, `/feed/`…) → portada.

## Probado
Con Apache (igual que Hostinger): redirecciones, https, sin www, 404, cabeceras y caché. Con la política de
seguridad activa, en celular y computador: sin bloqueos; cargan letras, mapa, Helenita y páginas legales.

## Para montarlo (lo guía JARVIS)
1. Antes de tocar nada, sacar copia de seguridad del WordPress desde el panel de Hostinger.
2. Vaciar `public_html` (o mover el WordPress a otra carpeta) para que no queden archivos viejos expuestos.
3. Subir el ZIP a `public_html` y extraerlo ahí. Activar SSL si no está.

## Para decidir
- El sitio viejo tiene páginas institucionales que desaparecen (derechos y deberes de los pacientes, actas de
  reunión, política de participación social, cumplimiento de circular, encuestas FOMAG, registros COVID). Hoy
  redirigen a la portada. Confirmar con Nicolas si alguna debe seguir publicada (algunas pueden ser obligatorias
  para una IPS).
