#!/usr/bin/env python3
"""Reel vertical «Nuestra página web» para pacientes → fuentes/reel.html.

Guion aprobado: entregas/editor-video/2026-11-12-guion-reel-pacientes-pagina.md.
Pantalla del celular hecha con imágenes limpias de cada estado (assets/est/) y movida por el video: fluida.
«Antes» = capturas de la página anterior (31-oct-2026), en pequeño y sin críticas.
Uso: python3 gen.py  → copiar fuentes/reel.html a index.html y renderizar.
"""
import json, os, subprocess, html

AQUI = os.path.dirname(os.path.abspath(__file__))
EST = json.load(open(os.path.join(AQUI, 'assets/est/meta.json')))
P = json.load(open(os.path.join(AQUI, 'assets/est/pos.json')))
CSS_W, CSS_H, HEAD = 390, 844, 76
PAUSA = 0.35


def dur(path):
    p = os.path.join(AQUI, path)
    if not os.path.exists(p):
        return None
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
                                capture_output=True, text=True).stdout)


esc = html.escape
TL, AUD, EXTRA = [], [], []
n_toque = 0


class Cel:
    def __init__(self, x, y, S):
        self.x, self.y, self.S, self.k = x, y, S, S / CSS_W
        self.SH = round(CSS_H * self.k)
        self.tiras, self.cur, self.scroll, self.toques = [], None, 0, []

    def px(self, v):
        return round(v * self.k, 2)

    def mostrar(self, tira, t, fundido=0.15):
        if tira not in self.tiras:
            self.tiras.append(tira)
        if self.cur == tira:
            return
        if self.cur is None:
            TL.append(f'tl.set("#t-{tira}", {{opacity:1}}, {t:.2f});')
        else:
            TL.append(f'tl.fromTo("#t-{tira}", {{opacity:0}}, {{opacity:1, duration:{fundido}, ease:"none", immediateRender:false}}, {t:.2f});')
            TL.append(f'tl.to("#t-{self.cur}", {{opacity:0, duration:0.01}}, {t + fundido:.2f});')
        self.cur = tira

    def desplazar(self, y, t, d, ease='power2.inOut'):
        if d <= 0:
            TL.append(f'tl.set("#pag", {{y:{-self.px(y)}}}, {t:.2f});')
        else:
            TL.append(f'tl.fromTo("#pag", {{y:{-self.px(self.scroll)}}}, {{y:{-self.px(y)}, duration:{d:.2f}, ease:"{ease}", immediateRender:false}}, {t:.2f});')
        self.scroll = y

    def tocar(self, x, ypag, t):
        global n_toque
        n_toque += 1
        i = n_toque
        self.toques.append(f'<div class="toque" id="tq{i}"></div>')
        TL.append(f'tl.set("#tq{i}", {{x:{self.px(x)}, y:{self.px(ypag - self.scroll)}}}, 0);')
        TL.append(f'tl.fromTo("#tq{i}", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.18, ease:"power2.out", immediateRender:false}}, {t:.2f});')
        TL.append(f'tl.to("#tq{i}", {{opacity:0, scale:1.5, duration:0.35, ease:"power1.out"}}, {t + 0.22:.2f});')
        AUD.append(f'<audio id="clic{i}" class="clip" src="assets/sfx/click-soft.mp3" data-start="{t + 0.05:.2f}" data-duration="0.35" data-track-index="{15 + i % 3}" data-volume="0.35"></audio>')

    def html(self):
        tiras = ''.join(f'<img class="tira" id="t-{n}" src="assets/est/{n}.png" alt="" style="top:{self.px(EST[n]["y0"])}px;width:{self.S}px" />' for n in self.tiras)
        nt = EST['notiTira']
        noti = (f'<div id="noti-ventana" style="left:{self.px(nt["track_x"])}px;top:{self.px(nt["track_y"])}px;width:{self.px(370)}px;height:{self.px(nt["h_css"])}px">'
                f'<img id="noti-tira" src="assets/est/noti-tira.png" alt="" style="width:{self.px(nt["w_css"])}px" /></div>')
        return f'''<div class="cel" id="cel" style="left:{self.x}px;top:{self.y}px;width:{self.S + 28}px;height:{self.SH + 28}px">
  <div class="pantalla" id="pantalla" style="width:{self.S}px;height:{self.SH}px">
    <div class="pag" id="pag" style="width:{self.S}px">{tiras}{noti}</div>
    <img class="capa" id="antes-pant" src="assets/antes/inicio-movil.png" alt="" style="width:{self.S}px" />
    <img class="capa" id="cab" src="assets/est/header.png" alt="" style="width:{self.S}px;opacity:0" />
    {''.join(self.toques)}
  </div>
</div>'''


def voz(nombre, ini, texto, pista=10):
    d = dur(f'assets/voz/{nombre}.mp3')
    if d is None:
        return len(texto) / 14.0, True
    AUD.append(f'<audio id="voz-{nombre}" class="clip" src="assets/voz/{nombre}.mp3" data-start="{ini:.2f}" data-duration="{d - 0.04:.2f}" data-track-index="{pista}" data-volume="1"></audio>')
    return d, False


def anim(nombre, ini, d, tag, clase='anim'):
    out, n = [], 0
    while d - n * 5.0 > 0.05:
        seg = min(5.0, d - n * 5.0)
        out.append(f'<video id="a-{tag}-{n}" class="{clase} clip" src="assets/helenita/{nombre}.webm" data-start="{ini + n * 5.0:.2f}" data-duration="{seg:.2f}" data-track-index="3" muted playsinline></video>')
        n += 1
    return out


def construir():
    C = Cel(291, 430, 470)
    W = P['wizard'] - HEAD - 10
    titulos, anims, faltan = [], [], []
    t = 0.0

    def titulo(i, texto, ini, d, ahora=True):
        etq = '<span class="ahora">Ahora</span>' if ahora else ''
        titulos.append(f'<div class="tit" id="tit{i}">{etq}{esc(texto)}</div>')
        TL.append(f'tl.fromTo("#tit{i}", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.35, ease:"power3.out", immediateRender:false}}, {ini:.2f});')
        TL.append(f'tl.to("#tit{i}", {{opacity:0, y:-20, duration:0.2}}, {ini + d - 0.2:.2f});')

    def sub(i, texto, ini, d):
        titulos.append(f'<div class="sub" id="sub{i}">{esc(texto)}</div>')
        TL.append(f'tl.fromTo("#sub{i}", {{opacity:0, y:16}}, {{opacity:1, y:0, duration:0.3, immediateRender:false}}, {ini + 0.1:.2f});')
        TL.append(f'tl.to("#sub{i}", {{opacity:0, duration:0.18}}, {ini + d - 0.18:.2f});')

    def antes(img, ini, d):
        TL.append(f'tl.set("#antes-img", {{attr:{{src:"assets/antes/{img}.png"}}}}, {ini:.2f});')
        TL.append(f'tl.fromTo("#antes", {{opacity:0, x:40}}, {{opacity:1, x:0, duration:0.4, ease:"power3.out", immediateRender:false}}, {ini + 0.3:.2f});')
        TL.append(f'tl.to("#antes", {{opacity:0, x:40, duration:0.25}}, {ini + d - 0.3:.2f});')

    def guia(nombre, ini, d, tag):
        anims.extend(anim(nombre, ini, d, tag))

    # ---- 0 · Antes → Ahora (sin voz) ----
    d0 = 3.2
    titulos.append('<div class="tit" id="tit0">Nuestra página se renovó</div>')
    TL.append('tl.set("#tit0", {opacity:1}, 0);')
    TL.append(f'tl.to("#tit0", {{opacity:0, y:-20, duration:0.2}}, {d0 - 0.2:.2f});')
    C.mostrar('top', 0)
    TL.append('tl.fromTo("#brillo", {opacity:0, x:0}, {opacity:1, x:420, duration:0.5, ease:"power2.in", immediateRender:false}, 1.1);')
    TL.append('tl.to("#brillo", {opacity:0, x:640, duration:0.35, ease:"power2.out"}, 1.6);')
    TL.append('tl.to("#antes-pant", {opacity:0, duration:0.35}, 1.45);')
    TL.append('tl.to("#cab", {opacity:1, duration:0.35}, 1.45);')
    TL.append('tl.to("#etq-cel", {opacity:0, duration:0.25}, 1.4);')
    TL.append('tl.fromTo("#etq-ahora", {opacity:0}, {opacity:1, duration:0.3, immediateRender:false}, 1.55);')
    TL.append('tl.to("#etq-ahora", {opacity:0, duration:0.3}, 3.0);')
    AUD.append('<audio id="brillo-sfx" class="clip" src="assets/sfx/sparkle.mp3" data-start="1.15" data-duration="1.8" data-track-index="14" data-volume="0.45"></audio>')
    AUD.append('<audio id="wh0" class="clip" src="assets/sfx/whoosh.mp3" data-start="1.05" data-duration="1.2" data-track-index="16" data-volume="0.3"></audio>')
    t = d0

    # ---- 1 · Helenita de la página saluda ----
    d, f = voz('pagina-saludo', t + 0.1, '¡Hola! Soy Helenita. Con gusto le acompaño a agendar su cita.', 11)
    d1 = round(d + PAUSA, 2)
    titulo(1, 'Helenita le habla', t, d1)
    TL.append(f'tl.set("#cel", {{transformOrigin:"60% 100%"}}, {t:.2f});')
    TL.append(f'tl.to("#cel", {{scale:1.1, duration:0.9, ease:"power3.inOut"}}, {t + 0.2:.2f});')
    TL.append(f'tl.to("#cel", {{scale:1, duration:0.6, ease:"power3.inOut"}}, {t + d1 - 0.6:.2f});')
    t += d1

    # ---- 2 · Helenita grande, con boca (V3) ----
    d, f = voz('boca-v3', t, 'boca')
    d2 = round(8.2 + 0.2, 2)
    titulos.append('<div class="tit" id="tit2">Hola, soy Helenita</div>')
    TL.append(f'tl.fromTo("#tit2", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.35, immediateRender:false}}, {t + 3.3:.2f});')
    TL.append(f'tl.to("#tit2", {{opacity:0, duration:0.2}}, {t + d2 - 0.2:.2f});')
    TL.append(f'tl.to("#cel", {{x:250, scale:0.62, transformOrigin:"100% 50%", duration:0.6, ease:"power3.inOut"}}, {t:.2f});')
    TL.append(f'tl.to("#cel", {{x:0, scale:1, duration:0.6, ease:"power3.inOut"}}, {t + d2 - 0.5:.2f});')
    TL.append(f'tl.to("#guia", {{opacity:0, duration:0.25}}, {t:.2f});')
    TL.append(f'tl.to("#guia", {{opacity:1, duration:0.3}}, {t + d2 - 0.2:.2f});')
    EXTRA.append(f'<div id="grande1" class="grande"><video id="boca1" class="clip" src="assets/helenita/boca-v3.webm" data-start="{t:.2f}" data-duration="8.2" data-track-index="4" muted playsinline></video></div>')
    TL.append(f'tl.fromTo("#grande1", {{opacity:0, x:-80, scale:0.9}}, {{opacity:1, x:0, scale:1, duration:0.5, ease:"back.out(1.4)", immediateRender:false}}, {t:.2f});')
    TL.append(f'tl.to("#grande1", {{opacity:0, x:-60, duration:0.35}}, {t + 8.0:.2f});')
    AUD.append(f'<audio id="brillo2" class="clip" src="assets/sfx/sparkle.mp3" data-start="{t:.2f}" data-duration="1.5" data-track-index="14" data-volume="0.35"></audio>')
    t += d2

    escenas = [
        ('rp-e3', 'Desde su celular o computador, en nuestra página puede hacer todo esto.', 'Todo desde su celular o computador', 'hablar', None),
        ('rp-e4', 'Pida su cita en tres pasos: la sede, el servicio y sus datos. El mensaje le queda listo en WhatsApp.', 'Su cita en 3 pasos', 'senalar', 'citas'),
        ('v5', 'Todo es claro, se ve bien en el celular y los servicios están ordenados por áreas.', 'Servicios por áreas', 'hablar', None),
        ('rp-e6', 'Encuentre nuestras tres sedes, con su mapa y su horario.', '3 sedes con mapa y horario', 'senalar', None),
        ('rp-e7', 'Lea nuestras noticias, campañas y guías paso a paso.', 'Noticias y guías', 'pensar', None),
        ('rp-e8', 'Y envíenos sus peticiones, quejas o reclamos: el correo queda listo para enviar.', 'Peticiones, quejas o reclamos', 'pulgar', 'pqrs'),
    ]
    for j, (vz, texto, tit, an, ant) in enumerate(escenas, 3):
        dv, falta = voz(vz, t + 0.15, texto)
        faltan += [vz] if falta else []
        d = round(dv + PAUSA, 2)
        ini = t
        f = lambda x: ini + x * d
        titulo(j, tit, ini, d, ahora=(j != 3))
        sub(j, texto, ini, d)
        guia(an, ini, d, f'e{j}')
        if ant:
            antes(ant, ini, d)
        if j == 3:
            C.desplazar(560, f(0.05), 0.8 * d, 'sine.inOut')
        if j == 4:
            C.tocar(P['cta']['x'], P['cta']['y'] + C.scroll, f(0.06))
            C.desplazar(W, f(0.12), 0.25 * d)
            C.mostrar('w1', f(0.38), 0.05)
            C.tocar(P['sedeVdp']['x'], P['sedeVdp']['y'], f(0.42)); C.mostrar('w1s', f(0.46))
            C.tocar(P['next1']['x'], P['next1']['y'], f(0.58)); C.mostrar('w2', f(0.63))
            C.tocar(P['fcat']['x'], P['fcat']['y'], f(0.7)); C.mostrar('w2a', f(0.74))
            C.tocar(P['serv1']['x'], P['serv1']['y'], f(0.8)); C.mostrar('w2s', f(0.84))
            C.tocar(P['next2']['x'], P['next2']['y'], f(0.9)); C.mostrar('w3', f(0.94))
        if j == 5:
            C.mostrar('top', ini, 0.12)
            C.desplazar(2808, ini, 0.3 * d)
            C.tocar(300, 3214, f(0.55)); C.mostrar('serv-apoyo', f(0.6))
        if j == 6:
            C.mostrar('mid', ini, 0.12)
            C.desplazar(6456, f(0.02), 0.45 * d)
            C.desplazar(6700, f(0.6), 0.35 * d)
        if j == 7:
            C.mostrar('noti1', ini, 0.15)
            C.desplazar(3748, ini, 0)
            TL.append(f'tl.set("#noti-ventana", {{opacity:1}}, {ini:.2f});')
            TL.append(f'tl.fromTo("#noti-tira", {{x:0}}, {{x:{-C.px(868)}, duration:{0.8 * d:.2f}, ease:"power1.inOut", immediateRender:false}}, {f(0.12):.2f});')
            TL.append(f'tl.set("#noti-ventana", {{opacity:0}}, {ini + d:.2f});')
        if j == 8:
            TL.append(f'tl.fromTo("#pantalla", {{filter:"blur(0px)"}}, {{filter:"blur(10px)", duration:0.12, immediateRender:false}}, {ini - 0.1:.2f});')
            C.mostrar('pqrs0', ini, 0.1)
            C.desplazar(10640, ini + 0.02, 0)
            TL.append(f'tl.to("#pantalla", {{filter:"blur(0px)", duration:0.25}}, {ini + 0.05:.2f});')
            C.desplazar(11300, f(0.15), 0.35 * d)
            C.desplazar(12100, f(0.55), 0.3 * d)
            C.tocar(195, 12588, f(0.9))
        t += d

    # ---- 9 · Cierre con boca (V8, voz rehecha «Cesar») ----
    dv, falta = voz('boca-v8', t + 0.3, 'boca')
    faltan += ['boca-v8 (voz rehecha)'] if falta else []
    d9 = 8.4
    TL.append(f'tl.fromTo("#fondo-azul", {{opacity:0}}, {{opacity:1, duration:0.5, immediateRender:false}}, {t:.2f});')
    TL.append(f'tl.to(["#cel", "#guia", "#antes"], {{opacity:0, y:80, duration:0.4, ease:"power2.in"}}, {t:.2f});')
    EXTRA.append(f'<div id="grande2" class="grande"><video id="boca2" class="clip" src="assets/helenita/boca-v8.webm" data-start="{t + 0.3:.2f}" data-duration="8.04" data-track-index="4" muted playsinline></video></div>')
    TL.append(f'tl.fromTo("#grande2", {{opacity:0, y:80}}, {{opacity:1, y:0, duration:0.5, ease:"power3.out", immediateRender:false}}, {t + 0.2:.2f});')
    TL.append(f'tl.to("#grande2", {{opacity:0, duration:0.3}}, {t + 8.25:.2f});')
    titulos.append('<div class="cierre" id="cie1">Veinte años cuidando a las familias del Cesar y La Guajira.</div><div class="cierre am" id="cie2">¡La salud, nuestro compromiso!</div>')
    TL.append(f'tl.fromTo("#cie1", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.4, immediateRender:false}}, {t + 1.7:.2f});')
    TL.append(f'tl.fromTo("#cie2", {{opacity:0, y:30, scale:0.9}}, {{opacity:1, y:0, scale:1, duration:0.45, ease:"back.out(1.6)", immediateRender:false}}, {t + 6.1:.2f});')
    TL.append(f'tl.to(["#cie1", "#cie2"], {{opacity:0, duration:0.3}}, {t + 8.25:.2f});')
    t += d9
    fin = round(t, 2)
    total = round(fin + 2.6, 2)
    TL.append(f'tl.fromTo("#final", {{opacity:0}}, {{opacity:1, duration:0.4, immediateRender:false}}, {fin:.2f});')
    TL.append(f'tl.fromTo("#final img", {{scale:0.8}}, {{scale:1, duration:0.6, ease:"back.out(1.6)", immediateRender:false}}, {fin:.2f});')
    AUD.append(f'<audio id="pop" class="clip" src="assets/sfx/pop.mp3" data-start="{fin:.2f}" data-duration="0.7" data-track-index="14" data-volume="0.3"></audio>')
    AUD.append(f'<audio id="musica" class="clip" src="assets/bgm/the-corporate-upbeat.mp3" data-start="0" data-duration="{total:.2f}" data-media-start="12" data-track-index="12" data-volume="0.07" data-fade-in="0.4" data-fade-out="1.8"></audio>')

    css = open(os.path.join(AQUI, 'estilo.css'), encoding='utf-8').read()
    doc = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{css}</style>
</head>
<body>
<!-- Reel «Nuestra página web» para pacientes · generado con gen.py -->
<div id="root" data-composition-id="reel" data-start="0" data-duration="{total:.2f}" data-width="1080" data-height="1920" data-layout-allow-overflow>
<div id="fondo-azul"></div>
<div id="halo"></div>
<div class="etq antes" id="etq-cel">Antes</div><div class="etq" id="etq-ahora">Ahora</div>
{C.html()}
<div id="brillo"></div>
<div id="antes"><span class="etq antes">Antes</span><img id="antes-img" src="assets/antes/citas.png" alt="" /></div>
<div id="guia">{''.join(anims)}</div>
{''.join(EXTRA)}
{chr(10).join(titulos)}
<div class="final" id="final"><img src="assets/img/logo.png" alt="Santa Helena del Valle IPS" /><p>santahelenadelvalleips.com</p></div>
{chr(10).join(AUD)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(TL)}
window.__timelines["reel"] = tl;
</script>
</body>
</html>
'''
    os.makedirs(os.path.join(AQUI, 'fuentes'), exist_ok=True)
    open(os.path.join(AQUI, 'fuentes/reel.html'), 'w', encoding='utf-8').write(doc)
    print(f'reel.html · {total:.1f} s · voces que faltan: {faltan}')


construir()
