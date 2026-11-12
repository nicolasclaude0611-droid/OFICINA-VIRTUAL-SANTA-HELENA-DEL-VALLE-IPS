#!/usr/bin/env python3
"""Arma los 3 reels tutorial (reel1.html, reel2.html, reel3.html) a partir de los guiones.

Cada escena: voz de Helenita, tramo de la grabación de la página (marcas en assets/grab/rN.json),
animación de Helenita, texto de la franja y subtítulo. La duración de cada escena sale de su voz.
Uso: python3 gen.py   (luego: npx hyperframes render -c reel1.html ...)
"""
import json, os, subprocess, html

AQUI = os.path.dirname(os.path.abspath(__file__))
FPS_CHARS = 14.0  # si falta una voz, se estima con 14 caracteres por segundo
PAUSA = 0.3      # aire después de cada frase
FINAL = 2.4       # tarjeta final con el logo
WA = open(os.path.join(AQUI, 'assets/r2-whatsapp.txt'), encoding='utf-8').read().strip()

def dur(path):
    p = os.path.join(AQUI, path)
    if not os.path.exists(p):
        return None
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
                         capture_output=True, text=True).stdout
    return float(out)

# (voz, texto dicho, franja, animación, tramo de la grabación [ini, fin] o marca, extra)
REELS = {
 1: dict(gancho='Así se usa nuestra página', escenas=[
   ('tut-r1-e1', '¡Hola! Le muestro cómo usar la página nueva de Santa Helena del Valle IPS.', 'Así se usa nuestra página', 'saludar', ('e1', 'e2'), None),
   ('tut-r1-e2', 'Arriba está el menú: servicios, sedes, preguntas frecuentes y PQRS.', 'Menú: Servicios · Sedes · Preguntas · PQRS', 'hablar', ('e2', 'e3'), None),
   ('tut-r1-e3', 'Para pedir una cita, toque Agendar cita.', 'Agendar cita', 'invitar', ('e3', 'e4'), None),
   ('tut-r1-e4', 'En Servicios elija un área y vea lo que ofrecemos.', 'Servicios por áreas', 'hablar', ('e4', 'e5'), None),
   ('tut-r1-e5', 'En Sedes encontrará el mapa, las direcciones, los horarios y cómo llegar.', 'Sedes: mapa, direcciones y horarios', 'senalar', ('e5', 'e6'), None),
   ('tut-r1-e6', 'Y en PQRS puede enviar una petición, queja, reclamo, sugerencia o felicitación.', 'PQRS: petición, queja, reclamo, sugerencia o felicitación', 'pensar', (25.0, 'e7'), None),
   ('tut-r1-e7', 'Si necesita ayuda, toque mi carita abajo.', '¿Dudas? Toque a Helenita', 'pulgar', ('e7', 'fin'), 'fab'),
 ]),
 2: dict(gancho='Pida su cita en 3 pasos', escenas=[
   ('tut-r2-e1', '¡Hola! Hoy le muestro cómo pedir su cita.', 'Pida su cita en 3 pasos', 'saludar', ('e1', 'e2'), None),
   ('tut-r2-e2', 'Toque el botón Agendar cita.', 'Agendar cita', 'invitar', ('e2', 'e3'), None),
   ('pagina-paso1', 'Para comenzar, elija la sede donde desea ser atendido.', '1 · Elija la sede', 'senalar', ('e3', 'e4'), None),
   ('pagina-paso2', 'Muy bien. Ahora, elija el servicio que necesita.', '2 · Elija el servicio', 'hablar', ('e4', 'e5'), None),
   ('pagina-paso3', 'Por último, escriba los datos del paciente.', '3 · Datos del paciente', 'hablar', ('e5', 'e6'), None),
   ('tut-r2-e6', 'Acepte la autorización y toque Pedir esta cita.', 'Marque la autorización y toque «Pedir esta cita»', 'senalar', ('e6', 'e7'), None),
   ('pagina-listo', '¡Listo! Su mensaje ya está en WhatsApp. Solo debe enviarlo.', 'El mensaje queda listo en WhatsApp', 'pulgar', ('e7', 'e8'), 'whatsapp'),
   ('tut-r2-e8', 'Nuestro equipo le confirmará la fecha y la hora por WhatsApp.', 'La IPS le confirma fecha y hora por WhatsApp', 'reposo', ('e8', 'fin'), None),
 ]),
 3: dict(gancho='¿Quiere enviarnos una queja o sugerencia?', escenas=[
   ('tut-r3-e1', '¡Hola! Hoy le muestro cómo enviar una petición, queja o sugerencia.', '¿Quiere enviarnos una queja o sugerencia?', 'saludar', ('e1', 'e2'), None),
   ('tut-r3-e2', 'Toque PQRS en el menú.', 'PQRS', 'invitar', ('e2', 'e3'), None),
   ('tut-r3-e3', 'Elija el tipo de solicitud y escriba sus datos de contacto.', '1 · Tipo de solicitud y sus datos', 'hablar', ('e3', 'e4'), None),
   ('tut-r3-e4', 'Cuéntenos qué ocurrió, con fecha, sede y servicio.', '2 · Cuéntenos qué ocurrió', 'hablar', ('e4', 'e5'), None),
   ('tut-r3-e5', 'Toque Preparar correo y se abrirá el mensaje listo.', '3 · Preparar correo', 'senalar', ('e5', 'e7'), None),
   ('tut-r3-e6', 'Revíselo y envíelo: llega a atención al usuario, con copia a Calidad.', 'Envíelo a siau@santahelenadelvalleips.com (copia: calidad@)', 'hablar', (21.5, 23.0), 'correo'),
   ('tut-r3-e7', 'Respondemos dentro de los términos de ley, hasta quince días hábiles.', 'Respuesta: hasta 15 días hábiles', 'pensar', (8.0, 8.5), 'nota15'),
   ('tut-r3-e8', 'Gracias por ayudarnos a mejorar.', 'Su opinión nos ayuda a mejorar', 'empatia', None, 'logo'),
 ]),
}

CSS = '''
@font-face { font-family: "Bricolage Grotesque"; src: url("assets/fonts/bricolage.woff2") format("woff2"); font-weight: 200 800; }
@font-face { font-family: "Figtree"; src: url("assets/fonts/figtree.woff2") format("woff2"); font-weight: 300 900; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #EFF4F7; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #EFF4F7; font-family: "Figtree", sans-serif; }
#fondo-arco { position: absolute; left: -260px; top: 900px; width: 900px; height: 900px; border-radius: 50%; background: #dbe8f0; }
.franja { position: absolute; left: 60px; top: 190px; width: 960px; min-height: 200px; padding: 34px 44px 38px 64px; border-radius: 36px; background: #0A2233; color: #fff; font-family: "Bricolage Grotesque", sans-serif; font-weight: 600; letter-spacing: -0.035em; line-height: 1.02; display: flex; align-items: center; opacity: 0; }
.franja::before { content: ""; position: absolute; left: 30px; top: 40px; bottom: 40px; width: 10px; border-radius: 5px; background: #FFE81A; }
#cel { position: absolute; left: 500px; top: 440px; width: 528px; height: 1110px; border-radius: 62px; background: #0A2233; box-shadow: 0 30px 70px rgba(10,34,51,.25); }
#pantalla { position: absolute; left: 14px; top: 14px; width: 500px; height: 1082px; border-radius: 50px; overflow: hidden; background: #fff; }
.grab { position: absolute; left: 0; top: 0; width: 500px; height: 1082px; object-fit: cover; object-position: top; }
.globo { position: absolute; left: 40px; top: 450px; width: 440px; padding: 30px 32px; border-radius: 30px; background: #fff; color: #0A2233; font-size: 38px; font-weight: 600; line-height: 1.22; box-shadow: 0 16px 40px rgba(10,34,51,.14); opacity: 0; }
.globo::after { content: ""; position: absolute; left: 150px; bottom: -22px; border: 22px solid transparent; border-top-color: #fff; border-bottom: 0; }
#hele { position: absolute; left: -70px; top: 830px; width: 720px; height: 720px; }
.anim { position: absolute; left: 0; top: 0; width: 720px; height: 720px; }
.tarjeta { position: absolute; left: 24px; right: 24px; border-radius: 26px; background: #fff; box-shadow: 0 18px 44px rgba(10,34,51,.28); padding: 26px 26px 30px; font-size: 23px; color: #0A2233; line-height: 1.35; opacity: 0; }
.tarjeta h4 { font-size: 26px; margin-bottom: 14px; color: #06709A; }
.tarjeta .fila { border-bottom: 1px solid #e3eaef; padding: 8px 0; }
.tarjeta .fila b { color: #4A6171; font-weight: 600; margin-right: 8px; }
.burbuja { background: #e9f6ee; border-radius: 18px; padding: 16px 18px; white-space: pre-line; font-size: 21px; }
#pie { position: absolute; left: 0; top: 1600px; width: 1080px; text-align: center; font-size: 34px; font-weight: 700; color: #06709A; opacity: 0; }
#final { position: absolute; inset: 0; background: #FBFCFD; opacity: 0; }
#final img { position: absolute; left: 190px; top: 620px; width: 700px; }
#final p { position: absolute; left: 0; top: 1060px; width: 1080px; text-align: center; font-size: 42px; font-weight: 700; color: #0A2233; }
#final span { display: block; margin-top: 18px; font-size: 34px; font-weight: 600; color: #06709A; }
#toque { position: absolute; left: 963px; top: 1480px; width: 90px; height: 90px; margin: -45px 0 0 -45px; border-radius: 50%; border: 6px solid #FFE81A; opacity: 0; }
'''

def esc(t): return html.escape(t)

def construir(n):
    R = REELS[n]
    marcas = json.load(open(os.path.join(AQUI, f'assets/grab/r{n}.json')))
    vid_dur = dur(f'assets/grab/r{n}.mp4')
    t = 0.0
    partes, tl, audios = [], [], []
    franja_ids = []
    for i, (voz, dicho, franja, anim, tramo, extra) in enumerate(R['escenas'], 1):
        vpath = f'assets/voz/{voz}.mp3'
        d_voz = dur(vpath) or len(dicho) / FPS_CHARS
        d = round(d_voz + PAUSA, 2)
        ini = round(t, 2)
        sid = f'e{i}'
        # voz
        if os.path.exists(os.path.join(AQUI, vpath)):
            audios.append(f'<audio id="voz-{sid}" class="clip" src="{vpath}" data-start="{ini + 0.2:.2f}" data-duration="{d_voz - 0.06:.2f}" data-track-index="10" data-volume="1"></audio>')
        # grabación
        if tramo:
            a, b = tramo
            a = marcas[a] if isinstance(a, str) else a
            b = marcas[b] if isinstance(b, str) else b
            if isinstance(tramo[1], str) and tramo[1] != 'fin':
                b -= 0.8  # quita la espera final, para que el siguiente paso aparezca con la siguiente voz
            b = min(b, vid_dur - 0.05)
            seg = max(0.3, b - a)
            rate = max(0.08, min(1.6, seg / d))
            partes.append(f'<video id="grab-{sid}" class="grab clip" src="assets/grab/r{n}.mp4" data-start="{ini:.2f}" data-duration="{d:.2f}" data-media-start="{a:.2f}" data-playback-rate="{rate:.3f}" data-track-index="2" muted playsinline></video>')
        # animación
        partes.append(f'<video id="anim-{sid}" class="anim clip" src="assets/helenita/{anim}.webm" data-start="{ini:.2f}" data-duration="{min(d, 5.0):.2f}" data-track-index="3" muted playsinline></video>')
        if d > 5.0:
            partes.append(f'<video id="anim-{sid}b" class="anim clip" src="assets/helenita/{anim}.webm" data-start="{ini + 5.0:.2f}" data-duration="{d - 5.0:.2f}" data-track-index="3" muted playsinline></video>')
        # franja y globo
        size = 76 if len(franja) <= 26 else (62 if len(franja) <= 44 else 50)
        partes.append(f'<div class="franja" id="franja-{sid}" style="font-size:{size}px">{esc(franja)}</div>')
        partes.append(f'<div class="globo" id="globo-{sid}">{esc(dicho)}</div>')
        if i == 1:  # el primer cuadro ya se ve completo (portada del reel)
            tl.append(f'tl.fromTo(["#franja-{sid}", "#globo-{sid}"], {{opacity:1}}, {{opacity:1, duration:0.01}}, 0);')
        else:
            tl.append(f'tl.fromTo("#franja-{sid}", {{opacity:0, y:-24}}, {{opacity:1, y:0, duration:0.35, ease:"power3.out"}}, {ini:.2f});')
            tl.append(f'tl.fromTo("#globo-{sid}", {{opacity:0, scale:0.9, y:20}}, {{opacity:1, scale:1, y:0, duration:0.3, ease:"back.out(1.7)"}}, {ini + 0.1:.2f});')
        tl.append(f'tl.to(["#franja-{sid}", "#globo-{sid}"], {{opacity:0, duration:0.2, ease:"power2.in"}}, {ini + d - 0.2:.2f});')
        # extras dentro del celular
        if extra == 'whatsapp':
            partes.append(f'<div class="tarjeta" id="extra-{sid}" style="top:330px"><h4>Su mensaje en WhatsApp</h4><div class="burbuja">{esc(WA.split(chr(10)+chr(10)+"Autorizo")[0])}</div></div>')
            tl.append(f'tl.fromTo("#extra-{sid}", {{opacity:0, y:120}}, {{opacity:1, y:0, duration:0.45, ease:"power3.out"}}, {ini + 0.5:.2f});')
            tl.append(f'tl.to("#extra-{sid}", {{opacity:0, duration:0.25}}, {ini + d - 0.25:.2f});')
        if extra == 'correo':
            filas = [('Para:', 'siau@santahelenadelvalleips.com'), ('CC:', 'calidad@santahelenadelvalleips.com'), ('Asunto:', 'PQRS · Sugerencia · Ejemplo de sugerencia')]
            cuerpo = 'Señores\nSistema de Información y Atención al Usuario (SIAU)\nSanta Helena del Valle IPS\n\nCordial saludo. Por medio de este correo presento una sugerencia…'
            fl = ''.join(f'<div class="fila"><b>{a}</b>{esc(b)}</div>' for a, b in filas)
            partes.append(f'<div class="tarjeta" id="extra-{sid}" style="top:260px"><h4>Su correo, listo para enviar</h4>{fl}<div class="burbuja" style="background:#EFF4F7;margin-top:14px">{esc(cuerpo)}</div></div>')
            tl.append(f'tl.fromTo("#extra-{sid}", {{opacity:0, y:120}}, {{opacity:1, y:0, duration:0.45, ease:"power3.out"}}, {ini + 0.2:.2f});')
            tl.append(f'tl.to("#extra-{sid}", {{opacity:0, duration:0.25}}, {ini + d - 0.25:.2f});')
        if extra == 'fab':
            tl.append(f'tl.fromTo("#toque", {{opacity:0, scale:0.5}}, {{opacity:1, scale:1.15, duration:0.5, ease:"power2.out", repeat:3, yoyo:true}}, {ini + 0.6:.2f});')
        if extra == 'logo':
            tl.append(f'tl.fromTo("#cel", {{opacity:1}}, {{opacity:0, duration:0.3}}, {ini:.2f});')
            tl.append(f'tl.fromTo("#logo-esc", {{opacity:0, scale:0.8}}, {{opacity:1, scale:1, duration:0.5, ease:"back.out(1.6)"}}, {ini + 0.2:.2f});')
        audios.append(f'<audio id="wh-{sid}" class="clip" src="assets/sfx/whoosh-short.mp3" data-start="{max(0, ini - 0.08):.2f}" data-duration="0.6" data-track-index="{12 + i % 2}" data-volume="0.22"></audio>')
        t += d
    fin_ini = round(t, 2)
    total = round(t + FINAL, 2)
    logo_esc = ''
    if any(e[5] == 'logo' for e in R['escenas']):
        logo_esc = '<img id="logo-esc" src="assets/img/logo.png" alt="" style="position:absolute;left:500px;top:620px;width:540px;opacity:0" />'
    tl.append(f'tl.fromTo("#final", {{opacity:0}}, {{opacity:1, duration:0.4}}, {fin_ini:.2f});')
    tl.append(f'tl.fromTo("#final img", {{scale:0.8}}, {{scale:1, duration:0.6, ease:"back.out(1.6)"}}, {fin_ini:.2f});')
    audios.append(f'<audio id="musica" class="clip" src="assets/bgm/the-corporate-upbeat.mp3" data-start="0" data-duration="{total:.2f}" data-media-start="4" data-track-index="11" data-volume="0.07" data-fade-in="0.5" data-fade-out="1.5"></audio>')
    audios.append(f'<audio id="pop-final" class="clip" src="assets/sfx/pop.mp3" data-start="{fin_ini:.2f}" data-duration="0.7" data-track-index="14" data-volume="0.3"></audio>')
    graba = [p for p in partes if 'class="grab' in p or 'class="tarjeta' in p]
    anims = [p for p in partes if 'class="anim' in p]
    textos = [p for p in partes if 'class="franja' in p or 'class="globo' in p]
    doc = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<!-- Reel tutorial {n} · generado con gen.py (no editar a mano: cambiar gen.py y volver a correrlo) -->
<div id="root" data-composition-id="reel{n}" data-start="0" data-duration="{total:.2f}" data-width="1080" data-height="1920" data-layout-allow-overflow>
  <div id="fondo-arco"></div>
  <div id="cel"><div id="pantalla">
    {chr(10).join('    ' + p for p in graba)}
  </div></div>
  <div id="toque"></div>
  {logo_esc}
  <div id="hele">
    {chr(10).join('    ' + p for p in anims)}
  </div>
  {chr(10).join('  ' + p for p in textos)}
  <div id="final"><img src="assets/img/logo.png" alt="Santa Helena del Valle IPS" /><p>¡La salud, nuestro compromiso!<span>santahelenadelvalleips.com</span></p></div>
  {chr(10).join('  ' + a for a in audios)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tl)}
window.__timelines["reel{n}"] = tl;
</script>
</body>
</html>
'''
    os.makedirs(os.path.join(AQUI, 'fuentes'), exist_ok=True)
    open(os.path.join(AQUI, f'fuentes/reel{n}.html'), 'w', encoding='utf-8').write(doc)
    faltan = [e[0] for e in R['escenas'] if not os.path.exists(os.path.join(AQUI, f'assets/voz/{e[0]}.mp3'))]
    print(f'reel{n}.html · {total:.1f} s · voces que faltan: {len(faltan)}')

for n in REELS:
    construir(n)
