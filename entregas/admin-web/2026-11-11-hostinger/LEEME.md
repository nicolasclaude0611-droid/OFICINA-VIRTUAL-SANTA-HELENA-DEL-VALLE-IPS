# Web nueva para Hostinger · 11 nov 2026

**Archivo:** `web-nueva-santa-helena.zip` (3,8 MB, 43 archivos en la raíz del ZIP, sin carpeta contenedora).
Código fuente: repositorio `santa-helena`, rama `web-hostinger`.
**Versión 2 (11 nov 2026):** `.htaccess` corregido para convivir con las carpetas de otros sistemas de la IPS en `public_html`.

## Qué trae
- La página (index, política de datos, términos, 404), estilos, código, imágenes, fotos, Helenita y voces.
- `.htaccess`, hecho para NO afectar las carpetas de otros sistemas (mesadeayuda, citas, control, nube, 2018, Backup2018…):
  - https obligatorio y sin www: en todo el dominio (las carpetas con su propio `.htaccess` conservan sus reglas).
  - Cabeceras de seguridad (CSP para Google Maps, Google Fonts y wa.me) y caché: solo en los archivos de la página nueva.
  - Redirecciones 301 del WordPress viejo y página 404: solo si la dirección no existe, y nunca dentro de una carpeta existente.
  - No cambia `DirectoryIndex`, `Options` ni `ErrorDocument`, que se heredarían a las subcarpetas.
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
Con Apache y carpetas de ejemplo (mesadeayuda con su propio `.htaccess`, citas, nube, Backup2018, y restos de WordPress):
siguen sirviendo su `index.php`/archivos sin cabeceras nuevas ni redirecciones; la portada muestra la página nueva aunque
haya un `index.php` viejo; redirecciones, https, sin www, 404 y caché funcionan. Con la política de
seguridad activa, en celular y computador: sin bloqueos; cargan letras, mapa, Helenita y páginas legales.

## Para montarlo (lo guía JARVIS)
1. Antes de tocar nada, sacar copia de seguridad del WordPress desde el panel de Hostinger.
2. No mover las carpetas de los sistemas de la IPS. Antes de extraer, revisar que en `public_html` no existan ya
   archivos o carpetas con estos nombres (se sobrescribirían): `index.html`, `404.html`, `politica-de-datos.html`,
   `terminos.html`, `styles.css`, `script.js`, `legal.css`, `robots.txt`, `sitemap.xml`, `img/`, `fotos/`, `media/`, `helenita/`.
   El `.htaccess` actual del WordPress se reemplaza (guardarlo en la copia de seguridad).
3. Subir el ZIP a `public_html` y extraerlo ahí. Activar SSL si no está.
4. Los archivos del WordPress que queden en la raíz (index.php, wp-admin…) siguen accesibles; conviene retirarlos cuando
   se confirme que no se usan.

## Para decidir
- El sitio viejo tiene páginas institucionales que desaparecen (derechos y deberes de los pacientes, actas de
  reunión, política de participación social, cumplimiento de circular, encuestas FOMAG, registros COVID). Hoy
  redirigen a la portada. Confirmar con Nicolas si alguna debe seguir publicada (algunas pueden ser obligatorias
  para una IPS).
