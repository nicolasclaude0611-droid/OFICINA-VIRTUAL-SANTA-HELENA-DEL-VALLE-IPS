#!/usr/bin/env python3
"""Arma los 3 reels tutorial (fuentes/reel1.html, reel2.html, reel3.html).

Versión 2 (pedido de Nicolas): la pantalla del celular ya no es una grabación en vivo. Son imágenes limpias de
cada estado de la página (assets/est/) y el desplazamiento lo hace el video, así queda totalmente fluido.
Cada reel tiene un diseño distinto. La duración de cada escena sale de su voz.
Uso: python3 gen.py  → copiar fuentes/reelN.html a index.html y renderizar.
"""
import json, os, subprocess, html

AQUI = os.path.dirname(os.path.abspath(__file__))
PAUSA, FINAL = 0.3, 2.4
WA = open(os.path.join(AQUI, 'assets/r2-whatsapp.txt'), encoding='utf-8').read().strip()
WA = WA.replace('Paciente Ejemplo', 'Helenita').replace('0000000000', '1065000000').replace('01/01/2000', '30/10/2006')
WA = WA.split('\n\nAutorizo')[0]
EST = json.load(open(os.path.join(AQUI, 'assets/est/meta.json')))
P = json.load(open(os.path.join(AQUI, 'assets/est/pos.json')))
CSS_W, CSS_H, HEAD = 390, 844, 76
# Formulario de peticiones, quejas o reclamos con el agendador cerrado (medido en la captura del reel 3)
PQ = {'sug': (217, 11232), 'nombre': (195, 11398), 'doc': (195, 11599), 'cel': (195, 11699),
      'asunto': (195, 12000), 'msg': (195, 12305), 'check': (58, 12408), 'submit': (195, 12588)}


def dur(path):
    p = os.path.join(AQUI, path)
    if not os.path.exists(p):
        return None
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
                                capture_output=True, text=True).stdout)


def esc(t):
    return html.escape(t)


BASE = '''@font-face { font-family: "Bricolage Grotesque"; src: url("assets/fonts/bricolage.woff2") format("woff2"); font-weight: 200 800; }
@font-face { font-family: "Figtree"; src: url("assets/fonts/figtree.woff2") format("woff2"); font-weight: 300 900; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: "Figtree", sans-serif; }
.cel { position: absolute; border-radius: 64px; background: #0A2233; box-shadow: 0 34px 80px rgba(0,0,0,.28); }
.pantalla { position: absolute; left: 14px; top: 14px; overflow: hidden; border-radius: 52px; background: #fff; }
.pag { position: absolute; left: 0; top: 0; }
.tira { position: absolute; left: 0; opacity: 0; }
.capa { position: absolute; left: 0; top: 0; }
.toque { position: absolute; left: 0; top: 0; width: 78px; height: 78px; margin: -39px 0 0 -39px; border-radius: 50%; border: 7px solid #FFE81A; background: rgba(255,232,26,.25); opacity: 0; }
.tarjeta { position: absolute; left: 20px; right: 20px; border-radius: 26px; background: #fff; box-shadow: 0 18px 44px rgba(10,34,51,.3); padding: 24px 24px 28px; font-size: 22px; color: #0A2233; line-height: 1.35; opacity: 0; }
.tarjeta h4 { font-size: 25px; margin-bottom: 12px; color: #06709A; }
.tarjeta .fila { border-bottom: 1px solid #e3eaef; padding: 7px 0; }
.tarjeta .fila b { color: #4A6171; font-weight: 600; margin-right: 8px; }
.burbuja { background: #e9f6ee; border-radius: 18px; padding: 14px 16px; white-space: pre-line; font-size: 20px; }
.anim { position: absolute; left: 0; top: 0; }
.final { position: absolute; inset: 0; opacity: 0; }
'''


class Reel:
    def __init__(self, n, fondo, musica_ini):
        self.n, self.t, self.tl, self.audios = n, 0.0, [], []
        self.fondo, self.musica_ini = fondo, musica_ini
        self.tiras, self.cur, self.scroll, self.ntap, self.toques = [], None, 0, 0, []

    def celular(self, x, y, S):
        self.S, self.k, self.cx, self.cy = S, S / CSS_W, x, y
        self.SH = round(CSS_H * self.k)

    def px(self, v):
        return round(v * self.k, 2)

    def mostrar(self, tira, t, fundido=0.15):
        """Cambia el estado de la página con un fundido corto (mismo encuadre, sin saltos)."""
        if tira not in self.tiras:
            self.tiras.append(tira)
        if self.cur == tira:
            return
        if self.cur is None:
            self.tl.append(f'tl.set("#t-{tira}", {{opacity:1}}, {t:.2f});')
        else:
            self.tl.append(f'tl.fromTo("#t-{tira}", {{opacity:0}}, {{opacity:1, duration:{fundido}, ease:"none", immediateRender:false}}, {t:.2f});')
            self.tl.append(f'tl.to("#t-{self.cur}", {{opacity:0, duration:0.01}}, {t + fundido:.2f});')
        self.cur = tira

    def desplazar(self, y, t, d, ease='power2.inOut'):
        if d <= 0:
            self.tl.append(f'tl.set("#pag", {{y:{-self.px(y)}}}, {t:.2f});')
        else:
            self.tl.append(f'tl.fromTo("#pag", {{y:{-self.px(self.scroll)}}}, {{y:{-self.px(y)}, duration:{d:.2f}, ease:"{ease}", immediateRender:false}}, {t:.2f});')
        self.scroll = y

    def tocar(self, x, ypag, t):
        """Círculo amarillo donde se toca (coordenadas de la página) y un clic suave."""
        self.ntap += 1
        i = self.ntap
        self.toques.append(f'<div class="toque" id="tq{i}"></div>')
        self.tl.append(f'tl.set("#tq{i}", {{x:{self.px(x)}, y:{self.px(ypag - self.scroll)}}}, 0);')
        self.tl.append(f'tl.fromTo("#tq{i}", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.18, ease:"power2.out", immediateRender:false}}, {t:.2f});')
        self.tl.append(f'tl.to("#tq{i}", {{opacity:0, scale:1.5, duration:0.35, ease:"power1.out"}}, {t + 0.22:.2f});')
        self.audios.append(f'<audio id="clic{i}" class="clip" src="assets/sfx/click-soft.mp3" data-start="{t + 0.05:.2f}" data-duration="0.35" data-track-index="{15 + i % 3}" data-volume="0.35"></audio>')

    def capa(self, cid, t_on, t_off, fundido=0.2):
        self.tl.append(f'tl.fromTo("#{cid}", {{opacity:0}}, {{opacity:1, duration:{fundido}, immediateRender:false}}, {t_on:.2f});')
        if t_off is not None:
            self.tl.append(f'tl.to("#{cid}", {{opacity:0, duration:{fundido}}}, {t_off:.2f});')

    def acercar(self, escala, fx, fy, t, d=0.6):
        """Acercamiento suave del celular hacia un punto de su pantalla."""
        self.tl.append(f'tl.set("#cel", {{transformOrigin:"{14 + self.px(fx)}px {14 + self.px(fy)}px"}}, {t:.2f});')
        self.tl.append(f'tl.to("#cel", {{scale:{escala}, duration:{d}, ease:"power3.inOut"}}, {t:.2f});')

    def desenfoque(self, t):
        self.tl.append(f'tl.fromTo("#pantalla", {{filter:"blur(0px)"}}, {{filter:"blur(10px)", duration:0.12, immediateRender:false}}, {t - 0.1:.2f});')
        self.tl.append(f'tl.to("#pantalla", {{filter:"blur(0px)", duration:0.25}}, {t + 0.04:.2f});')

    def html_celular(self, extra=''):
        tiras = ''.join(f'<img class="tira" id="t-{n}" src="assets/est/{n}.png" alt="" style="top:{self.px(EST[n]["y0"])}px;width:{self.S}px" />' for n in self.tiras)
        fab = EST['fab']
        return f'''<div class="cel" id="cel" style="left:{self.cx}px;top:{self.cy}px;width:{self.S + 28}px;height:{self.SH + 28}px">
  <div class="pantalla" id="pantalla" style="width:{self.S}px;height:{self.SH}px">
    <div class="pag" id="pag" style="width:{self.S}px">{tiras}</div>
    <img class="capa" id="cab" src="assets/est/header.png" alt="" style="width:{self.S}px" />
    <img class="capa" id="menu" src="assets/est/menu.png" alt="" style="width:{self.S}px;opacity:0" />
    <img class="capa" id="fab" src="assets/est/fab.png" alt="" style="left:{self.px(fab['x'])}px;top:{self.px(fab['y'])}px;width:{self.px(fab['width'])}px;opacity:0" />
    {extra}
    {''.join(self.toques)}
  </div>
</div>'''

    def escena(self, voz, texto):
        vpath = f'assets/voz/{voz}.mp3'
        dv = dur(vpath)
        falta = dv is None
        dv = dv or len(texto) / 14.0
        d = round(dv + PAUSA, 2)
        ini = round(self.t, 2)
        if not falta:
            self.audios.append(f'<audio id="voz-{voz}" class="clip" src="{vpath}" data-start="{ini + 0.15:.2f}" data-duration="{dv - 0.06:.2f}" data-track-index="10" data-volume="1"></audio>')
        self.t += d
        return ini, d, falta

    def helenita(self, anim, ini, d, tag):
        out, n = [], 0
        while d - n * 5.0 > 0.05:
            seg = min(5.0, d - n * 5.0)
            out.append(f'<video id="a-{tag}-{n}" class="anim clip" src="assets/helenita/{anim}.webm" data-start="{ini + n * 5.0:.2f}" data-duration="{seg:.2f}" data-track-index="3" muted playsinline></video>')
            n += 1
        return out

    def cierre(self, fin):
        self.tl.append(f'tl.fromTo("#final", {{opacity:0}}, {{opacity:1, duration:0.4, immediateRender:false}}, {fin:.2f});')
        self.tl.append(f'tl.fromTo("#final img", {{scale:0.8}}, {{scale:1, duration:0.6, ease:"back.out(1.6)", immediateRender:false}}, {fin:.2f});')
        self.audios.append(f'<audio id="pop" class="clip" src="assets/sfx/pop.mp3" data-start="{fin:.2f}" data-duration="0.7" data-track-index="14" data-volume="0.3"></audio>')

    def documento(self, css, cuerpo, total):
        self.audios.append(f'<audio id="musica" class="clip" src="assets/bgm/the-corporate-upbeat.mp3" data-start="0" data-duration="{total:.2f}" data-media-start="{self.musica_ini}" data-track-index="11" data-volume="0.07" data-fade-in="0.4" data-fade-out="1.5"></audio>')
        return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{BASE}
html, body, #root {{ background: {self.fondo}; }}
{css}</style>
</head>
<body>
<!-- Reel tutorial {self.n} · generado con gen.py (cambiar gen.py y volver a correrlo) -->
<div id="root" data-composition-id="reel{self.n}" data-start="0" data-duration="{total:.2f}" data-width="1080" data-height="1920" data-layout-allow-overflow>
{cuerpo}
{chr(10).join(self.audios)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(self.tl)}
window.__timelines["reel{self.n}"] = tl;
</script>
</body>
</html>
'''


def entrada(R, sel, i, ini, d, desde='{opacity:0, y:24}', hasta='{opacity:1, y:0, duration:0.32, ease:"power3.out"'):
    if i == 1:
        R.tl.append(f'tl.set({sel}, {{opacity:1}}, 0);')
    else:
        R.tl.append(f'tl.fromTo({sel}, {desde}, {hasta}, immediateRender:false}}, {ini:.2f});')
    R.tl.append(f'tl.to({sel}, {{opacity:0, duration:0.18}}, {ini + d - 0.18:.2f});')


# ============ REEL 1 · Recorrido · azul oscuro, capítulos numerados ============
def reel1():
    R = Reel(1, '#0A2233', 4)
    R.celular(470, 300, 540)
    css = '''
#brillo { position: absolute; left: 380px; top: 160px; width: 900px; height: 900px; border-radius: 50%; background: radial-gradient(circle, rgba(5,150,200,.35), rgba(5,150,200,0) 65%); }
#marca { position: absolute; left: 60px; top: 150px; width: 250px; }
.cap { position: absolute; left: 60px; top: 300px; width: 380px; opacity: 0; }
.cap .num { display: inline-block; font-family: "Bricolage Grotesque"; font-weight: 700; font-size: 34px; color: #0A2233; background: #FFE81A; border-radius: 30px; padding: 6px 20px; }
.cap h2 { margin-top: 22px; font-family: "Bricolage Grotesque"; font-weight: 600; font-size: 60px; line-height: 1.0; letter-spacing: -0.035em; color: #fff; }
.cap p { margin-top: 26px; font-size: 36px; line-height: 1.25; font-weight: 600; color: #bfe6f4; }
#hele { position: absolute; left: -90px; top: 980px; width: 580px; height: 580px; }
#hele .anim { width: 580px; height: 580px; }
.final { background: #0A2233; }
.final img { position: absolute; left: 190px; top: 700px; width: 700px; }
.final p { position: absolute; left: 0; top: 1150px; width: 1080px; text-align: center; font-size: 40px; font-weight: 700; color: #FFE81A; }
'''
    escenas = [
        ('tut-r1-e1', '¡Hola! Le muestro cómo usar la página nueva de Santa Helena del Valle IPS.', 'Así se usa nuestra página', 'saludar'),
        ('tut-r1-e2', 'Arriba está el menú: servicios, sedes, preguntas frecuentes y peticiones, quejas o reclamos.', 'El menú', 'hablar'),
        ('tut-r1-e3', 'Para pedir una cita, toque Agendar cita.', 'Agendar cita', 'invitar'),
        ('tut-r1-e4', 'En Servicios elija un área y vea lo que ofrecemos.', 'Servicios por áreas', 'hablar'),
        ('tut-r1-e5', 'En Sedes encontrará el mapa, las direcciones, los horarios y cómo llegar.', 'Sedes y mapa', 'senalar'),
        ('tut-r1-e6', 'Y aquí puede enviarnos sus peticiones, quejas o reclamos, y también sugerencias o felicitaciones.', 'Peticiones, quejas y reclamos', 'pensar'),
        ('tut-r1-e7', 'Si necesita ayuda, toque mi carita abajo.', '¿Dudas? Toque a Helenita', 'pulgar'),
    ]
    textos, anims, faltan = [], [], []
    R.mostrar('top', 0)
    for i, (voz, dicho, titulo, anim) in enumerate(escenas, 1):
        ini, d, falta = R.escena(voz, dicho)
        faltan += [voz] if falta else []
        f = lambda x: ini + x * d
        textos.append(f'<div class="cap" id="cap{i}"><span class="num">{i:02d} / {len(escenas):02d}</span><h2>{esc(titulo)}</h2><p>{esc(dicho)}</p></div>')
        entrada(R, f'"#cap{i}"', i, ini, d, '{opacity:0, x:-40}', '{opacity:1, x:0, duration:0.35, ease:"power3.out"')
        anims += R.helenita(anim, ini, d, f'e{i}')
        if i == 2:
            R.tocar(P['menuBtn']['x'], P['menuBtn']['y'], f(0.08)); R.capa('menu', f(0.14), ini + d - 0.15)
        if i == 3:
            R.tocar(P['cta']['x'], P['cta']['y'], f(0.2)); R.tocar(P['cta']['x'], P['cta']['y'], f(0.6))
        if i == 4:
            R.desplazar(2808, f(0.04), 0.45 * d)
            R.tocar(300, 3214, f(0.62)); R.mostrar('serv-apoyo', f(0.66))
        if i == 5:
            R.mostrar('mid', ini, 0.15)
            R.desplazar(6456, f(0.03), 0.42 * d)
            R.desplazar(6700, f(0.55), 0.35 * d)
        if i == 6:
            R.desenfoque(ini)
            R.mostrar('pqrs0', ini, 0.1)
            R.desplazar(10640, ini + 0.02, 0)
            R.desplazar(11000, f(0.45), 0.45 * d)
        if i == 7:
            R.capa('fab', ini + 0.05, None)
            fb = EST['fab']
            cx, cy = fb['x'] + fb['width'] / 2, fb['y'] + fb['height'] / 2
            R.tocar(cx, R.scroll + cy, f(0.3)); R.tocar(cx, R.scroll + cy, f(0.65))
    fin = round(R.t, 2)
    total = round(fin + FINAL, 2)
    R.cierre(fin)
    cuerpo = f'''<div id="brillo"></div>
<img id="marca" src="assets/img/logo-lema.png" alt="Santa Helena del Valle IPS" />
{R.html_celular()}
{chr(10).join(textos)}
<div id="hele">{''.join(anims)}</div>
<div class="final" id="final"><img src="assets/img/logo-lema.png" alt="" /><p>santahelenadelvalleips.com</p></div>'''
    return R.documento(css, cuerpo, total), total, faltan


# ============ REEL 2 · Pedir cita · claro, marcador de 3 pasos y acercamientos ============
def reel2():
    R = Reel(2, '#FBFCFD', 30)
    R.celular(276, 410, 500)
    css = '''
#titulo { position: absolute; left: 0; top: 130px; width: 1080px; text-align: center; font-family: "Bricolage Grotesque"; font-weight: 600; font-size: 56px; letter-spacing: -0.035em; color: #0A2233; }
#pasos { position: absolute; left: 190px; top: 220px; width: 700px; height: 130px; }
#pasos .linea { position: absolute; left: 60px; right: 60px; top: 34px; height: 6px; background: #dfe7ec; border-radius: 3px; }
#relleno { position: absolute; left: 60px; top: 34px; height: 6px; width: 580px; background: #FFE81A; border-radius: 3px; transform-origin: 0 50%; }
.paso { position: absolute; top: 0; width: 120px; text-align: center; }
.paso i { display: block; margin: 0 auto; width: 74px; height: 74px; border-radius: 50%; background: #fff; border: 5px solid #dfe7ec; font-style: normal; font-family: "Bricolage Grotesque"; font-weight: 700; font-size: 36px; line-height: 64px; color: #5d6f7c; }
.paso i.on { background: #FFE81A; border-color: #FFE81A; color: #0A2233; }
.paso i.ok { background: #0A2233; border-color: #0A2233; color: #FFE81A; }
.paso b { display: block; margin-top: 8px; font-size: 28px; color: #4A6171; }
.sub { position: absolute; left: 90px; top: 1525px; width: 900px; padding: 22px 34px; border-radius: 30px; background: #0A2233; color: #fff; text-align: center; font-size: 38px; font-weight: 600; line-height: 1.22; opacity: 0; }
.sub::before { content: ""; position: absolute; left: 50%; top: -12px; width: 60px; height: 8px; margin-left: -30px; border-radius: 4px; background: #FFE81A; }
#hele { position: absolute; left: -150px; top: 1000px; width: 540px; height: 540px; }
#hele .anim { width: 540px; height: 540px; }
.final { background: #FBFCFD; }
.final img { position: absolute; left: 190px; top: 700px; width: 700px; }
.final p { position: absolute; left: 0; top: 1120px; width: 1080px; text-align: center; font-size: 40px; font-weight: 700; color: #06709A; }
'''
    escenas = [
        ('tut-r2-e1', '¡Hola! Hoy le muestro cómo pedir su cita.', 'saludar', 0),
        ('tut-r2-e2', 'Toque el botón Agendar cita.', 'invitar', 0),
        ('pagina-paso1', 'Para comenzar, elija la sede donde desea ser atendido.', 'senalar', 1),
        ('pagina-paso2', 'Muy bien. Ahora, elija el servicio que necesita.', 'hablar', 2),
        ('pagina-paso3', 'Por último, escriba los datos del paciente.', 'hablar', 3),
        ('tut-r2-e6', 'Acepte la autorización y toque Pedir esta cita.', 'senalar', 3),
        ('pagina-listo', '¡Listo! Su mensaje ya está en WhatsApp. Solo debe enviarlo.', 'pulgar', 4),
        ('tut-r2-e8', 'Nuestro equipo le confirmará la fecha y la hora por WhatsApp.', 'reposo', 4),
    ]
    textos, anims, faltan = [], [], []
    R.mostrar('top', 0)
    R.tl.append('tl.set("#relleno", {scaleX:0}, 0);')
    paso_actual = 0
    W = P['wizard'] - HEAD - 10
    for i, (voz, dicho, anim, paso) in enumerate(escenas, 1):
        ini, d, falta = R.escena(voz, dicho)
        faltan += [voz] if falta else []
        f = lambda x: ini + x * d
        textos.append(f'<div class="sub" id="sub{i}">{esc(dicho)}</div>')
        entrada(R, f'"#sub{i}"', i, ini, d)
        anims += R.helenita(anim, ini, d, f'e{i}')
        if paso != paso_actual:
            for j in range(1, 4):
                cls = 'ok' if j < paso else ('on' if j == paso else '')
                R.tl.append(f'tl.set("#p{j}", {{className:"{cls}"}}, {ini:.2f});')
            R.tl.append(f'tl.to("#relleno", {{scaleX:{min(1.0, (paso - 1) / 2):.2f}, duration:0.45, ease:"power2.out"}}, {ini:.2f});')
            paso_actual = paso
        if i == 2:
            R.tocar(P['cta']['x'], P['cta']['y'], f(0.1))
            R.desplazar(W, f(0.2), 0.6 * d)
        if i == 3:
            R.mostrar('w1', ini, 0.05)
            R.acercar(1.12, 195, P['sedeVdp']['y'] - W, f(0.02), 0.5)
            R.tocar(P['sedeVdp']['x'], P['sedeVdp']['y'], f(0.35)); R.mostrar('w1s', f(0.4))
            R.tocar(P['next1']['x'], P['next1']['y'], f(0.78)); R.mostrar('w2', f(0.84))
        if i == 4:
            R.tocar(P['fcat']['x'], P['fcat']['y'], f(0.12)); R.mostrar('w2a', f(0.2))
            R.tocar(P['serv1']['x'], P['serv1']['y'], f(0.48)); R.mostrar('w2s', f(0.54))
            R.tocar(P['next2']['x'], P['next2']['y'], f(0.8)); R.mostrar('w3', f(0.86))
        if i == 5:
            R.tocar(P['f-nombre']['x'], P['f-nombre']['y'], f(0.12)); R.mostrar('w3n', f(0.18))
            R.tocar(P['f-doc']['x'], P['f-doc']['y'], f(0.36)); R.mostrar('w3d', f(0.42))
            R.desplazar(W + 380, f(0.55), 0.3 * d)
            R.tocar(P['f-cel']['x'], P['f-cel']['y'], f(0.86)); R.mostrar('w3t', f(0.9))
        if i == 6:
            R.desplazar(W + 760, f(0.0), 0.3 * d)
            R.tocar(P['check']['x'], P['check']['y'], f(0.38)); R.mostrar('w3c', f(0.43))
            R.tocar(P['submit']['x'], P['submit']['y'], f(0.75)); R.mostrar('wL', f(0.8), 0.02)
        if i == 7:
            R.acercar(1.0, 195, 400, ini, 0.4)
            R.desplazar(1700, f(0.0), 0.3 * d)
            R.capa('wa', f(0.33), ini + d - 0.15, 0.3)
        if i == 8:
            R.desplazar(1560, f(0.0), 0.25 * d)
            R.acercar(1.15, 195, 260, f(0.25), 0.6)
    fin = round(R.t, 2)
    total = round(fin + FINAL, 2)
    R.cierre(fin)
    wa = f'<div class="tarjeta" id="wa" style="top:{R.px(250)}px"><h4>Su mensaje en WhatsApp</h4><div class="burbuja">{esc(WA)}</div></div>'
    pasos = ''.join(f'<div class="paso" style="left:{x}px"><i id="p{j}">{j}</i><b>{t}</b></div>' for j, (x, t) in enumerate([(0, 'Sede'), (290, 'Servicio'), (580, 'Datos')], 1))
    cuerpo = f'''<div id="titulo">Pida su cita en 3 pasos</div>
<div id="pasos"><div class="linea"></div><div id="relleno"></div>{pasos}</div>
{R.html_celular(wa)}
<div id="hele">{''.join(anims)}</div>
{chr(10).join(textos)}
<div class="final" id="final"><img src="assets/img/logo.png" alt="" /><p>santahelenadelvalleips.com</p></div>'''
    return R.documento(css, cuerpo, total), total, faltan


# ============ REEL 3 · Peticiones, quejas o reclamos · azul, Helenita en círculo ============
def reel3():
    R = Reel(3, 'linear-gradient(160deg, #06709A 0%, #0A2233 70%)', 60)
    R.celular(301, 600, 450)
    css = '''
#circulo { position: absolute; left: 60px; top: 200px; width: 300px; height: 300px; border-radius: 50%; overflow: hidden; background: #FFE81A; box-shadow: 0 0 0 10px rgba(255,255,255,.18); }
#circulo .anim { width: 620px; height: 620px; left: -160px; top: -40px; }
.etq { position: absolute; left: 400px; top: 196px; font-weight: 700; color: #0A2233; background: #FFE81A; padding: 8px 22px; border-radius: 26px; opacity: 0; }
.bur { position: absolute; left: 400px; top: 262px; width: 620px; padding: 26px 30px; border-radius: 30px; background: #fff; color: #0A2233; font-size: 37px; font-weight: 600; line-height: 1.22; opacity: 0; }
.bur::before { content: ""; position: absolute; left: -20px; top: 40px; border: 20px solid transparent; border-right-color: #fff; border-left: 0; }
.final { background: linear-gradient(160deg, #06709A 0%, #0A2233 70%); }
.final img { position: absolute; left: 190px; top: 700px; width: 700px; }
.final p { position: absolute; left: 0; top: 1130px; width: 1080px; text-align: center; font-size: 40px; font-weight: 700; color: #FFE81A; }
'''
    escenas = [
        ('tut-r3-e1', '¡Hola! Hoy le muestro cómo enviar una petición, queja o sugerencia.', '¿Una queja o sugerencia?', 'saludar'),
        ('tut-r3-e2', 'Toque Peticiones, quejas o reclamos en el menú.', 'Abra el menú', 'invitar'),
        ('tut-r3-e3', 'Elija el tipo de solicitud y escriba sus datos de contacto.', 'Paso 1 · Tipo y datos', 'hablar'),
        ('tut-r3-e4', 'Cuéntenos qué ocurrió, con fecha, sede y servicio.', 'Paso 2 · Qué ocurrió', 'hablar'),
        ('tut-r3-e5', 'Toque Preparar correo y se abrirá el mensaje listo.', 'Paso 3 · Preparar correo', 'senalar'),
        ('tut-r3-e6', 'Revíselo y envíelo: llega a atención al usuario, con copia a Calidad.', 'Para: siau@santahelenadelvalleips.com', 'hablar'),
        ('tut-r3-e7', 'Respondemos dentro de los términos de ley, hasta quince días hábiles.', 'Respuesta: hasta 15 días hábiles', 'pensar'),
        ('tut-r3-e8', 'Gracias por ayudarnos a mejorar.', 'Su opinión nos ayuda a mejorar', 'empatia'),
    ]
    textos, anims, faltan = [], [], []
    R.mostrar('top', 0)
    for i, (voz, dicho, etq, anim) in enumerate(escenas, 1):
        ini, d, falta = R.escena(voz, dicho)
        faltan += [voz] if falta else []
        f = lambda x: ini + x * d
        size = 30 if len(etq) < 30 else 25
        textos.append(f'<div class="etq" id="etq{i}" style="font-size:{size}px">{esc(etq)}</div><div class="bur" id="bur{i}">{esc(dicho)}</div>')
        entrada(R, f'["#etq{i}", "#bur{i}"]', i, ini, d, '{opacity:0, y:16}', '{opacity:1, y:0, duration:0.3, ease:"back.out(1.5)"')
        anims += R.helenita(anim, ini, d, f'e{i}')
        if i == 2:
            R.tocar(P['menuBtn']['x'], P['menuBtn']['y'], f(0.08)); R.capa('menu', f(0.14), f(0.68))
            R.tocar(P['menuPQRS']['x'], P['menuPQRS']['y'], f(0.55))
            R.desenfoque(f(0.7))
            R.mostrar('pqrs0', f(0.7), 0.08)
            R.desplazar(10640, f(0.7), 0)
        if i == 3:
            R.desplazar(11050, f(0.0), 0.28 * d)
            R.tocar(*PQ['sug'], f(0.34)); R.mostrar('p1', f(0.39))
            R.tocar(*PQ['nombre'], f(0.56)); R.mostrar('p2', f(0.62))
            R.desplazar(11400, f(0.7), 0.2 * d)
            R.tocar(*PQ['cel'], f(0.9)); R.mostrar('p3', f(0.94))
        if i == 4:
            R.desplazar(11760, f(0.0), 0.28 * d)
            R.tocar(*PQ['asunto'], f(0.34)); R.mostrar('p4', f(0.4))
            R.tocar(*PQ['msg'], f(0.62)); R.mostrar('p5', f(0.68))
        if i == 5:
            R.desplazar(12060, f(0.0), 0.25 * d)
            R.tocar(*PQ['check'], f(0.3)); R.mostrar('p6', f(0.35))
            R.tocar(*PQ['submit'], f(0.55)); R.mostrar('p7', f(0.6), 0.02)
            R.desplazar(12300, f(0.68), 0.28 * d)
        if i == 6:
            R.capa('correo', f(0.05), ini + d - 0.12, 0.3)
        if i == 7:
            R.mostrar('pqrs0', ini + 0.05, 0.25)
            R.desplazar(10640, ini + 0.05, 0)
            R.acercar(1.3, 195, 200, f(0.15), 0.6)
        if i == 8:
            R.tl.append(f'tl.to("#cel", {{opacity:0, y:60, duration:0.35, ease:"power2.in"}}, {ini:.2f});')
    fin = round(R.t, 2)
    total = round(fin + FINAL - 1.2, 2)
    R.cierre(fin - 1.2)
    filas = [('Para:', 'siau@santahelenadelvalleips.com'), ('CC:', 'calidad@santahelenadelvalleips.com'),
             ('Asunto:', 'PQRS · Sugerencia · Ejemplo de sugerencia')]
    fl = ''.join(f'<div class="fila"><b>{a}</b>{esc(b)}</div>' for a, b in filas)
    texto_c = 'Señores\nSistema de Información y Atención al Usuario (SIAU)\nSanta Helena del Valle IPS\n\nCordial saludo. Por medio de este correo presento una sugerencia…'
    correo = f'<div class="tarjeta" id="correo" style="top:{R.px(170)}px;font-size:19px"><h4>Su correo, listo para enviar</h4>{fl}<div class="burbuja" style="background:#EFF4F7;margin-top:12px;font-size:18px">{esc(texto_c)}</div></div>'
    cuerpo = f'''{R.html_celular(correo)}
<div id="circulo">{''.join(anims)}</div>
{chr(10).join(textos)}
<div class="final" id="final"><img src="assets/img/logo-lema.png" alt="" /><p>santahelenadelvalleips.com</p></div>'''
    return R.documento(css, cuerpo, total), total, faltan


os.makedirs(os.path.join(AQUI, 'fuentes'), exist_ok=True)
for n, fn in ((1, reel1), (2, reel2), (3, reel3)):
    doc, total, faltan = fn()
    open(os.path.join(AQUI, f'fuentes/reel{n}.html'), 'w', encoding='utf-8').write(doc)
    print(f'reel{n}.html · {total:.1f} s · voces que faltan: {faltan}')
