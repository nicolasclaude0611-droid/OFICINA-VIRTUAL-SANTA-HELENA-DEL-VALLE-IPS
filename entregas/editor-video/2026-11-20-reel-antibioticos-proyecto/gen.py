#!/usr/bin/env python3
"""Reel «¿Cómo funcionan los antibióticos?» (Semana Mundial de Concientización sobre la Resistencia a los
Antimicrobianos). Motion graphics hechos con HTML/SVG + GSAP para HyperFrames. Escribe fuentes/reel.html.

- La duración de cada escena sale de su voz (assets/voz/abx2-eN.mp3). Si falta una voz, se estima (14 car./s).
- Los subtítulos van palabra por palabra: los tiempos salen de las pausas de la voz (silencedetect).
- Colores: paleta oficial del manual (fondo en degradado azul, #1894D1, #FFF212, #FFCC29, blanco) y los colores
  propios de los personajes que Nicolas aprobó en el guion (bacteria naranja, virus violeta, etc.).
- Fuentes Eras (con licencia): assets/fonts/*.TTF, ignoradas por git. Nunca se suben al repositorio.
Uso: python3 gen.py  → cp fuentes/reel.html index.html → hyperframes check / render.
"""
import os, re, subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))

# Colores
AZ, AM, OC, BL = '#1894D1', '#FFF212', '#FFCC29', '#FFFFFF'
NAVY = '#0A2233'
BAC, VIR, GRIS, ROJO, VERDE = '#FF9F1C', '#A66BFF', '#B8C2CC', '#E5383B', '#2ECC71'

ESC = [
    ('abx2-e1', '¿Los antibióticos sirven para la gripa? En esta Semana Mundial de Concientización sobre la Resistencia a los Antimicrobianos, le explicamos cómo funcionan.', 'saludar', ['antibióticos', 'gripa?', 'Semana', 'Mundial']),
    ('abx2-e2', 'Hay varios tipos de gérmenes que pueden enfermarnos; los más comunes son las bacterias y los virus.', 'hablar', ['bacterias', 'virus.']),
    ('abx2-e3', 'Las bacterias son seres vivos muy pequeños. Cuando entran al cuerpo, se multiplican y pueden causar infecciones.', 'senalar', ['multiplican', 'infecciones.']),
    ('abx2-e4', 'El antibiótico las ataca: las elimina o no las deja multiplicarse, y así ayuda al cuerpo a recuperarse.', 'hablar', ['elimina', 'multiplicarse,']),
    ('abx2-e5', 'Los virus son distintos: causan enfermedades como la gripa y el resfriado, y los antibióticos no sirven contra ellos.', 'pensar', ['gripa', 'resfriado,', 'sirven']),
    ('abx2-e6', 'Por eso solo su médico puede decidir si usted necesita un antibiótico, cuál y por cuántos días.', 'senalar', ['médico', 'cuál', 'días.']),
    ('abx2-e7', 'Si se toman cuando no hacen falta, o se dejan a medias, algunas bacterias sobreviven.', 'empatia', ['falta,', 'medias,', 'sobreviven.']),
    ('abx2-e8', 'Esas bacterias se multiplican y se vuelven resistentes: el antibiótico ya no las puede eliminar.', 'hablar', ['resistentes:', 'eliminar.']),
    ('abx2-e9', 'Así, una infección común puede volverse más difícil de tratar.', 'pensar', ['común', 'difícil']),
    ('abx2-e10', 'Por eso, no se automedique, no use sobrantes ni medicinas de otra persona, y siga el tratamiento como su médico se lo indicó.', 'senalar', ['automedique,', 'sobrantes', 'tratamiento']),
    ('abx2-e11', 'En esta semana mundial, cuidar los antibióticos es cuidar la salud de todos.', 'corazon', ['antibióticos', 'todos.']),
    ('abx2-e12', '¿Qué tema de salud quiere que le expliquemos? Cuéntenos en los comentarios.', 'pulgar', ['comentarios.']),
]

AUD, TL, HTML = [], [], []
PISTAS = {}  # pista -> último fin (para no encimar audios en la misma pista)


def dur(path):
    p = os.path.join(AQUI, path)
    if not os.path.exists(p):
        return None
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
                                capture_output=True, text=True).stdout)


def tramos_voz(path, d):
    """Tramos con voz (inicio, fin) según las pausas."""
    r = subprocess.run(['ffmpeg', '-i', os.path.join(AQUI, path), '-af', 'silencedetect=noise=-38dB:d=0.16', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', r)]
    fin = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', r)]
    sil = list(zip(ini, fin + [d] * (len(ini) - len(fin))))
    tr, t = [], 0.0
    for a, b in sil:
        if a - t > 0.08:
            tr.append((t, a))
        t = b
    if d - t > 0.08:
        tr.append((t, d))
    return tr


def tiempos_palabras(texto, d, audio):
    """Lista de (palabra, t) relativa al inicio de la voz."""
    pal = texto.split()
    peso = [len(p) + 1.5 for p in pal]
    # frases separadas por puntuación
    frases, cur = [], []
    for i, p in enumerate(pal):
        cur.append(i)
        if p[-1] in ',.:?!;':
            frases.append(cur); cur = []
    if cur:
        frases.append(cur)
    tr = tramos_voz(audio, d) if audio else []
    if tr and len(tr) > len(frases):  # une los tramos separados por las pausas más cortas
        while len(tr) > len(frases):
            k = min(range(len(tr) - 1), key=lambda j: tr[j + 1][0] - tr[j][1])
            tr[k:k + 2] = [(tr[k][0], tr[k + 1][1])]
    out = [0.0] * len(pal)
    if tr and len(tr) == len(frases):
        grupos = list(zip(frases, tr))
    else:
        a, b = (tr[0][0], tr[-1][1]) if tr else (0.05, d - 0.1)
        grupos = [(list(range(len(pal))), (a, b))]
    for idx, (a, b) in grupos:
        tot = sum(peso[i] for i in idx)
        t = a
        for i in idx:
            out[i] = t
            t += (b - a) * peso[i] / tot
    return list(zip(pal, out))


def pista_libre(ini, fin, base, n):
    for k in range(base, base + n):
        if PISTAS.get(k, -1) <= ini - 0.02:
            PISTAS[k] = fin
            return k
    PISTAS[base] = fin
    return base


def sfx(nombre, t, d=0.6, vol=0.3):
    k = pista_libre(t, t + d, 20, 8)
    AUD.append(f'<audio id="sfx{len(AUD)}" class="clip" src="assets/sfx/{nombre}.mp3" data-start="{t:.2f}" data-duration="{d:.2f}" data-track-index="{k}" data-volume="{vol}"></audio>')


def pop(sel, t, d=0.45, sonido=True, desde='{opacity:0,scale:0.4}', ease='back.out(1.8)'):
    TL.append(f'tl.fromTo("{sel}", {desde}, {{opacity:1,scale:1,x:0,y:0,rotation:0,duration:{d},ease:"{ease}",immediateRender:false}}, {t:.2f});')
    if sonido:
        sfx('pop', t, 0.5, 0.22)


def a(sel, props, t):
    TL.append(f'tl.to("{sel}", {props}, {t:.2f});')


# ---------- dibujos (SVG) ----------
def bacteria(id_, x, y, w=150, rot=0, extra=''):
    h = w * 0.58
    return (f'<div id="{id_}" class="obj bac {extra}" style="left:{x}px;top:{y}px;width:{w}px;height:{h:.0f}px;--r:{rot}deg">'
            f'<svg viewBox="0 0 150 87"><rect x="5" y="5" width="140" height="77" rx="38" fill="{BAC}" stroke="#FFE2B8" stroke-width="5"/>'
            f'<circle cx="38" cy="30" r="6" fill="#E07B00"/><circle cx="112" cy="58" r="7" fill="#E07B00"/><circle cx="96" cy="26" r="4" fill="#E07B00"/>'
            f'<circle cx="62" cy="42" r="6" fill="{NAVY}"/><circle cx="88" cy="42" r="6" fill="{NAVY}"/>'
            f'<path d="M64 58 Q75 66 86 58" stroke="{NAVY}" stroke-width="4" fill="none" stroke-linecap="round"/></svg></div>')


def escudo_svg(color=GRIS, borde='#FFFFFF', dentro=''):
    return (f'<svg viewBox="0 0 100 120"><path d="M50 6 L92 22 V58 C92 86 72 104 50 114 C28 104 8 86 8 58 V22 Z" fill="{color}" stroke="{borde}" stroke-width="6" stroke-linejoin="round"/>{dentro}</svg>')


def bac_escudo(id_, x, y, w=150):
    return (f'<div id="{id_}" class="obj" style="left:{x}px;top:{y}px;width:{w + 40}px;height:{w * 0.58 + 40:.0f}px">'
            + bacteria(id_ + 'b', 0, 0, w).replace('class="obj bac ', 'class="bac fija ')
            + f'<div class="esc-g" id="{id_}s" style="left:{w - 40}px;top:{w * 0.58 - 50:.0f}px;width:80px;height:96px">{escudo_svg()}</div></div>')


def virus(id_, x, y, w=140, extra=''):
    puntas = ''.join(
        f'<line x1="{70 + 42 * __import__("math").cos(k * 0.785):.1f}" y1="{70 + 42 * __import__("math").sin(k * 0.785):.1f}" x2="{70 + 62 * __import__("math").cos(k * 0.785):.1f}" y2="{70 + 62 * __import__("math").sin(k * 0.785):.1f}" stroke="#E3D1FF" stroke-width="7" stroke-linecap="round"/>'
        f'<circle cx="{70 + 64 * __import__("math").cos(k * 0.785):.1f}" cy="{70 + 64 * __import__("math").sin(k * 0.785):.1f}" r="7" fill="{VIR}" stroke="#E3D1FF" stroke-width="3"/>'
        for k in range(8))
    return (f'<div id="{id_}" class="obj vir {extra}" style="left:{x}px;top:{y}px;width:{w}px;height:{w}px">'
            f'<svg viewBox="0 0 140 140">{puntas}<circle cx="70" cy="70" r="44" fill="{VIR}" stroke="#E3D1FF" stroke-width="5"/>'
            f'<circle cx="56" cy="62" r="6" fill="{NAVY}"/><circle cx="84" cy="62" r="6" fill="{NAVY}"/>'
            f'<path d="M58 84 Q70 78 82 84" stroke="{NAVY}" stroke-width="4" fill="none" stroke-linecap="round"/></svg></div>')


def capsula(id_, x, y, w=220, rot=-20):
    return (f'<div id="{id_}" class="obj cap" style="left:{x}px;top:{y}px;width:{w}px;height:{w * 0.42:.0f}px;--r:{rot}deg">'
            f'<svg viewBox="0 0 220 92"><path d="M46 6 H110 V86 H46 A40 40 0 0 1 46 6 Z" fill="{AZ}" stroke="#FFFFFF" stroke-width="6"/>'
            f'<path d="M110 6 H174 A40 40 0 0 1 174 86 H110 Z" fill="{AM}" stroke="#FFFFFF" stroke-width="6"/>'
            f'<rect x="34" y="20" width="50" height="12" rx="6" fill="#FFFFFF" opacity="0.55"/></svg></div>')


def equis(id_, x, y, w=200):
    return (f'<div id="{id_}" class="obj equis" style="left:{x}px;top:{y}px;width:{w}px;height:{w}px">'
            f'<svg viewBox="0 0 100 100"><path d="M18 18 L82 82 M82 18 L18 82" stroke="{ROJO}" stroke-width="15" stroke-linecap="round"/></svg></div>')


def visto(id_, x, y, w=80):
    return (f'<div id="{id_}" class="obj visto" style="left:{x}px;top:{y}px;width:{w}px;height:{w}px">'
            f'<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="{VERDE}"/><path d="M28 52 L44 68 L74 34" stroke="#FFFFFF" stroke-width="11" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')


def etiqueta(id_, x, y, texto, color=BL, cls=''):
    return f'<div id="{id_}" class="obj tag {cls}" style="left:{x}px;top:{y}px;border-color:{color};color:{color}">{texto}</div>'


def nota(id_, x, y, w, texto):
    return f'<div id="{id_}" class="obj nota" style="left:{x}px;top:{y}px;width:{w}px">{texto}</div>'


CUERPO = (f'<svg viewBox="0 0 360 560"><g fill="rgba(255,255,255,0.07)" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round">'
          '<circle cx="180" cy="72" r="58"/>'
          '<path d="M100 150 H260 Q300 150 304 196 L318 360 Q320 382 300 384 Q284 386 280 364 L268 250 L262 540 H196 L186 380 H174 L164 540 H98 L92 250 L80 364 Q76 386 60 384 Q40 382 42 360 L56 196 Q60 150 100 150 Z"/></g></svg>')

MEDICO = (f'<svg viewBox="0 0 300 480"><g stroke="#FFFFFF" stroke-width="6" stroke-linejoin="round">'
          f'<circle cx="150" cy="70" r="54" fill="#F2D3B3"/>'
          f'<path d="M96 40 Q150 -6 204 40 Q190 22 150 22 Q110 22 96 40 Z" fill="{NAVY}"/>'
          f'<path d="M60 150 Q70 128 110 128 H190 Q230 128 240 150 L262 470 H38 Z" fill="#FFFFFF"/>'
          f'<path d="M110 128 L150 230 L190 128" fill="{AZ}"/>'
          f'<path d="M150 230 V470" stroke="{AZ}" stroke-width="5"/></g>'
          f'<path d="M118 136 Q96 230 150 262 Q204 230 182 136" fill="none" stroke="{NAVY}" stroke-width="7" stroke-linecap="round"/>'
          f'<circle cx="150" cy="268" r="16" fill="{AZ}" stroke="{NAVY}" stroke-width="5"/>'
          f'<rect x="186" y="300" width="44" height="54" rx="8" fill="{AZ}"/></svg>')


def persona(x, y, s, color):
    return (f'<g transform="translate({x},{y}) scale({s})" fill="{color}" stroke="#FFFFFF" stroke-width="5">'
            '<circle cx="50" cy="34" r="30"/><path d="M8 170 V104 Q8 72 50 72 Q92 72 92 104 V170 Z"/></g>')


FAMILIA = ('<svg viewBox="0 0 360 230">' + persona(10, 40, 1.12, AZ) + persona(130, 98, 0.78, OC) + persona(232, 40, 1.12, '#5DB8E6') + '</svg>')

ESCUDO_INSIGNIA = escudo_svg(AZ, '#FFFFFF', capsula_svg := (
    f'<g transform="translate(26 44) rotate(-25 24 14)"><path d="M14 4 H24 V28 H14 A12 12 0 0 1 14 4 Z" fill="#FFFFFF"/>'
    f'<path d="M24 4 H34 A12 12 0 0 1 34 28 H24 Z" fill="{AM}"/></g>'))


def construir():
    t = 0.25
    falt = []
    escenas = []
    for i, (nom, texto, anim, claves) in enumerate(ESC):
        ruta = f'assets/voz/{nom}.mp3'
        d = dur(ruta)
        if d is None:
            falt.append(nom)
            d = len(texto) / 14.0
            pal = tiempos_palabras(texto, d, None)
        else:
            pal = tiempos_palabras(texto, d, ruta)
            AUD.append(f'<audio id="voz{i + 1}" class="clip" src="{ruta}" data-start="{t + 0.15:.2f}" data-duration="{d - 0.03:.2f}" data-track-index="{2 + i % 2}" data-volume="1"></audio>')
        extra = 2.6 if i == len(ESC) - 1 else 0.5
        ini, fin = t, t + 0.15 + d + extra
        escenas.append(dict(n=i + 1, ini=ini, fin=fin, voz=t + 0.15, d=d, pal=pal, claves=claves, anim=anim))
        t = fin
    total = t

    def W(e, palabra, k=0):
        """Momento (absoluto) en que la voz dice esa palabra."""
        hits = [tt for p, tt in e['pal'] if p.lower().strip('¿?,.:!¡').startswith(palabra.lower())]
        return e['voz'] + (hits[k] if len(hits) > k else hits[-1] if hits else 0)

    # ---------- subtítulos palabra por palabra ----------
    SUB = []
    for e in escenas:
        pal = e['pal']
        bloques, cur, largo = [], [], 0
        for j, (p, tt) in enumerate(pal):
            if cur and largo + len(p) > 40:
                bloques.append(cur); cur, largo = [], 0
            cur.append(j); largo += len(p) + 1
            if p[-1] in '.?:' and largo > 14:
                bloques.append(cur); cur, largo = [], 0
        if cur:
            bloques.append(cur)
        for b, idx in enumerate(bloques):
            bid = f's{e["n"]}-{b}'
            spans = ''.join(f'<span id="{bid}-{j}" class="w{" k" if pal[j][0] in e["claves"] else ""}">{pal[j][0]}</span> ' for j in idx)
            SUB.append(f'<div id="{bid}" class="sub">{spans}</div>')
            t0 = e['voz'] + pal[idx[0]][1]
            t1 = e['voz'] + pal[bloques[b + 1][0]][1] if b + 1 < len(bloques) else e['fin'] - 0.15
            TL.append(f'tl.set("#{bid}", {{opacity:1}}, {t0 - 0.02:.2f});')
            TL.append(f'tl.set("#{bid}", {{opacity:0}}, {t1 - 0.02:.2f});')
            for j in idx:
                TL.append(f'tl.fromTo("#{bid}-{j}", {{opacity:0.0,y:14}}, {{opacity:1,y:0,duration:0.16,ease:"power2.out",immediateRender:false}}, {e["voz"] + pal[j][1] - 0.04:.2f});')

    # ---------- Helenita ----------
    HEL = []
    CON_H = {1, 10, 11, 12}
    for e in escenas:
        if e['n'] not in CON_H:
            continue
        d = e['fin'] - e['ini']
        n = 0
        while d - n * 5.0 > 0.05:
            seg = min(5.0, d - n * 5.0)
            HEL.append(f'<video id="h{e["n"]}-{n}" class="anim clip" src="assets/helenita/{e["anim"]}.webm" data-start="{e["ini"] + n * 5.0:.2f}" data-duration="{seg:.2f}" data-track-index="5" muted playsinline></video>')
            n += 1
    TL.append('tl.fromTo("#guia", {opacity:0, y:120}, {opacity:1, y:0, duration:0.6, ease:"power3.out", immediateRender:false}, 0.15);')
    TL.append(f'tl.to("#guia", {{opacity:0, y:260, duration:0.45, ease:"power2.in"}}, {escenas[0]["fin"] - 0.45:.2f});')
    TL.append(f'tl.to("#guia", {{opacity:1, y:0, duration:0.55, ease:"power3.out"}}, {escenas[9]["ini"]:.2f});')

    # ---------- escenas ----------
    for e in escenas:
        n, ini, fin = e['n'], e['ini'], e['fin']
        if n > 1:
            TL.append(f'tl.fromTo("#e{n}", {{opacity:0}}, {{opacity:1,duration:0.3,immediateRender:false}}, {ini:.2f});')
            sfx('whoosh-short', ini - 0.05, 0.5, 0.18)
        else:
            TL.append(f'tl.set("#e1", {{opacity:1}}, 0);')
        if n < len(escenas):
            TL.append(f'tl.to("#e{n}", {{opacity:0,duration:0.28}}, {fin - 0.28:.2f});')

    E = {e['n']: e for e in escenas}
    H = {}

    # 1 · gancho e insignia
    e = E[1]
    H[1] = (f'<div id="ins-g" class="obj" style="left:90px;top:560px;width:900px;height:330px">'
            f'<div class="ins-esc">{ESCUDO_INSIGNIA}</div>'
            f'<div class="ins-txt"><b>SEMANA MUNDIAL DE CONCIENTIZACIÓN</b><span>sobre la Resistencia a los Antimicrobianos</span><i>18 – 24 NOV</i></div></div>'
            + capsula('c1', 150, 960, 230, -15) + virus('v1', 690, 925, 170)
            + '<div id="q1" class="obj preg" style="left:470px;top:930px">?</div>'
            + nota('n1', 500, 1190, 430, '<b>Antimicrobianos:</b> medicinas contra gérmenes. Los antibióticos son un tipo de ellos.'))
    pop('#ins-g', 0.3, 0.6)
    pop('#c1', 0.9, desde='{opacity:0,x:-260,rotation:-60}', ease='power3.out')
    pop('#v1', 1.1, desde='{opacity:0,x:260,scale:0.5}', ease='back.out(1.6)')
    pop('#q1', W(e, 'gripa'), 0.4)
    TL.append(f'tl.to("#q1", {{scale:1.18,yoyo:true,repeat:5,duration:0.32,ease:"sine.inOut"}}, {W(e, "gripa") + 0.45:.2f});')
    TL.append(f'tl.to("#ins-g", {{scale:1.05,yoyo:true,repeat:1,duration:0.3}}, {W(e, "Semana"):.2f});')
    pop('#n1', W(e, 'Antimicrobianos') + 0.2, 0.5)
    t_enc = W(e, 'explicamos')
    a('#ins-g', f'{{opacity:0,scale:0.4,y:-330,duration:0.55,ease:"power3.in"}}', t_enc - 0.1)
    pop('#insignia', t_enc + 0.3, 0.45, sonido=False)
    TL.append(f'tl.to(["#c1","#v1","#q1"], {{y:-300,duration:0.7,ease:"power3.inOut"}}, {t_enc + 0.1:.2f});')

    # 2 · bacterias y virus
    e = E[2]
    bs = [(150, 610, 200, -10), (410, 650, 170, 15), (650, 600, 200, 8)]
    vs = [(170, 1000, 190), (445, 1050, 170), (700, 1000, 190)]
    H[2] = (''.join(bacteria(f'b2-{k}', x, y, w, r) for k, (x, y, w, r) in enumerate(bs))
            + ''.join(virus(f'v2-{k}', x, y, w) for k, (x, y, w) in enumerate(vs))
            + etiqueta('t2b', 395, 790, 'BACTERIAS', BAC) + etiqueta('t2v', 455, 1245, 'VIRUS', VIR)
            + '<div id="vs2" class="obj vs" style="left:478px;top:880px">VS</div>')
    for k in range(3):
        pop(f'#b2-{k}', W(e, 'tipos') - 0.2 + k * 0.12, sonido=(k == 0), desde='{opacity:0,y:-200}', ease='power3.out')
        pop(f'#v2-{k}', W(e, 'gérmenes') - 0.2 + k * 0.12, sonido=(k == 0), desde='{opacity:0,y:200}', ease='power3.out')
    TL.append(f'tl.to(["#b2-0","#b2-1","#b2-2"], {{scale:1.15,duration:0.25,yoyo:true,repeat:1}}, {W(e, "bacterias"):.2f});')
    TL.append(f'tl.to(["#v2-0","#v2-1","#v2-2"], {{scale:1.15,duration:0.25,yoyo:true,repeat:1}}, {W(e, "virus"):.2f});')
    pop('#t2b', W(e, 'bacterias') - 0.05, sonido=False)
    pop('#t2v', W(e, 'virus') - 0.05, sonido=False)
    pop('#vs2', W(e, 'enfermarnos'), 0.4)

    # 3 · cuerpo y multiplicación
    e = E[3]
    pos8 = [(450, 760), (560, 760), (450, 830), (560, 830), (450, 900), (560, 900), (505, 970), (505, 690)]
    H[3] = ('<div id="cuerpo" class="obj" style="left:330px;top:560px;width:420px;height:653px">' + CUERPO + '</div>'
            + bacteria('b3-0', 60, 700, 120, 0)
            + ''.join(bacteria(f'b3-{k + 1}', x, y, 80, (k * 37) % 50 - 25) for k, (x, y) in enumerate(pos8))
            + '<div id="cnt3" class="obj cnt" style="left:800px;top:640px">×2</div>'
            + etiqueta('t3', 770, 790, 'SE<br>MULTIPLICAN', BAC)
            + nota('n3', 330, 1240, 420, 'Pueden causar <b>infecciones</b>'))
    pop('#cuerpo', e['ini'] + 0.2, 0.6, sonido=False)
    pop('#b3-0', W(e, 'bacterias'), desde='{opacity:0,x:-200}', ease='power3.out')
    t_ent = W(e, 'entran')
    a('#b3-0', '{x:385,y:58,scale:0.667,duration:0.8,ease:"power2.inOut"}', t_ent - 0.1)
    a('#b3-0', '{opacity:0,duration:0.1}', W(e, 'multiplican') - 0.05)
    tm = W(e, 'multiplican')
    for g, (cnt, idx) in enumerate([('×2', [0, 1]), ('×4', [2, 3]), ('×8', [4, 5, 6, 7])]):
        for k in idx:
            pop(f'#b3-{k + 1}', tm - 0.05 + g * 0.55, 0.35, sonido=(k == idx[0]))
        if g == 0:
            pop('#cnt3', tm - 0.05, 0.35, sonido=False)
        else:
            TL.append(f'tl.set("#cnt3", {{textContent:"{cnt}"}}, {tm - 0.05 + g * 0.55:.2f});')
            TL.append(f'tl.fromTo("#cnt3", {{scale:1.4}}, {{scale:1,duration:0.3,immediateRender:false}}, {tm - 0.05 + g * 0.55:.2f});')
    pop('#t3', tm + 0.4, sonido=False)
    pop('#n3', W(e, 'infecciones') - 0.1)

    # 4 · el antibiótico ataca
    e = E[4]
    grid = [(150 + (k % 4) * 200, 610 + (k // 4) * 260) for k in range(8)]
    rompe = [0, 2, 5, 7]
    H[4] = (''.join(bacteria(f'b4-{k}', x, y, 130, (k * 29) % 40 - 20) for k, (x, y) in enumerate(grid))
            + ''.join(f'<div id="p4-{k}" class="obj pausa" style="left:{grid[k][0] + 95}px;top:{grid[k][1] - 30}px">❚❚</div>' for k in range(8) if k not in rompe)
            + ''.join(f'<div id="x4-{k}" class="obj chispa" style="left:{grid[k][0] + 15}px;top:{grid[k][1] - 25}px">✸</div>' for k in rompe)
            + capsula('c4', -300, 1000, 240, -10)
            + etiqueta('t4a', 140, 1000, 'ELIMINA', AM) + etiqueta('t4b', 500, 1000, 'NO SE MULTIPLICAN', AM))
    for k in range(8):
        pop(f'#b4-{k}', e['ini'] + 0.15 + k * 0.06, 0.35, sonido=(k == 0))
    ta = W(e, 'antibiótico')
    pop('#c4', ta - 0.1, 0.4, sonido=False, desde='{opacity:0}', ease='none')
    TL.append(f'tl.to("#c4", {{x:720,y:-265,rotation:15,duration:0.9,ease:"power2.inOut"}}, {ta:.2f});')
    sfx('whoosh', ta, 0.6, 0.2)
    te = W(e, 'elimina')
    for j, k in enumerate(rompe):
        pop(f'#x4-{k}', te + j * 0.1, 0.3, sonido=(j == 0))
        a(f'#b4-{k}', '{opacity:0,scale:0.2,rotation:90,duration:0.35,ease:"power2.in"}', te + j * 0.1)
        a(f'#x4-{k}', '{opacity:0,scale:1.6,duration:0.4}', te + j * 0.1 + 0.35)
    pop('#t4a', te + 0.2, sonido=False)
    tq = W(e, 'multiplicarse')
    for j, k in enumerate([k for k in range(8) if k not in rompe]):
        pop(f'#p4-{k}', tq - 0.2 + j * 0.08, 0.3, sonido=(j == 0))
        a(f'#b4-{k}', '{filter:"saturate(0.35)",duration:0.4}', tq - 0.2)
    pop('#t4b', tq + 0.2, sonido=False)
    a('#c4', '{y:-285,scale:1.15,duration:0.5,yoyo:true,repeat:1}', W(e, 'recuperarse') - 0.3)

    # 5 · contra los virus no sirve
    e = E[5]
    H[5] = (virus('v5', 600, 680, 260) + capsula('c5', 60, 760, 240, -5) + equis('x5', 430, 640, 280)
            + etiqueta('t5g', 560, 590, 'GRIPA', VIR) + etiqueta('t5r', 760, 590, 'RESFRIADO', VIR)
            + etiqueta('t5', 110, 1000, 'CONTRA LOS VIRUS NO SIRVEN', ROJO, 'grande'))
    pop('#v5', W(e, 'virus'), 0.5)
    pop('#c5', W(e, 'distintos') - 0.1, desde='{opacity:0,x:-260}', ease='power3.out')
    pop('#t5g', W(e, 'gripa'), 0.35)
    pop('#t5r', W(e, 'resfriado'), 0.35)
    tn = W(e, 'antibióticos')
    TL.append(f'tl.to("#c5", {{x:330,duration:0.45,ease:"power2.in"}}, {tn - 0.2:.2f});')
    TL.append(f'tl.to("#c5", {{x:40,rotation:-40,duration:0.6,ease:"back.out(2)"}}, {tn + 0.25:.2f});')
    TL.append(f'tl.to("#v5", {{scale:1.08,duration:0.15,yoyo:true,repeat:1}}, {tn + 0.22:.2f});')
    sfx('click-soft', tn + 0.22, 0.4, 0.35)
    pop('#x5', W(e, 'sirven') - 0.1, 0.4)
    pop('#t5', W(e, 'sirven') + 0.2, sonido=False)

    # 6 · solo su médico decide
    e = E[6]
    lista = [('¿Es una bacteria?', 'antibiótico'), ('¿Cuál antibiótico?', 'cuál'), ('¿Cuántos días?', 'días')]
    H[6] = ('<div id="med" class="obj" style="left:70px;top:590px;width:330px;height:528px">' + MEDICO + '</div>'
            + '<div id="lst6" class="obj tarjeta" style="left:440px;top:620px;width:560px">'
            + '<div class="tit">SOLO SU MÉDICO DECIDE</div>'
            + ''.join(f'<div id="l6-{k}" class="fila">{txt}</div>' for k, (txt, _) in enumerate(lista)) + '</div>')
    pop('#med', W(e, 'médico') - 0.2, 0.55)
    pop('#lst6', W(e, 'decidir') - 0.2, 0.45)
    for k, (_, p) in enumerate(lista):
        pop(f'#l6-{k}', W(e, p) - 0.15, 0.35, desde='{opacity:0,x:40}', ease='power3.out')

    # 7 · mal uso: a medias
    e = E[7]
    cal = ''.join(f'<div class="dia" id="d7-{k}"><small>DÍA {k + 1}</small><span class="mini">{"●" if k < 3 else ""}</span></div>' for k in range(7))
    sobre = [(160, 990), (330, 1020), (500, 985), (670, 1025), (820, 990), (590, 1100)]
    H[7] = (f'<div id="cal7" class="obj cal" style="left:60px;top:600px;width:960px"><div class="tit">TRATAMIENTO: 7 DÍAS</div><div class="dias">{cal}</div></div>'
            + '<div id="corte7" class="obj corte" style="left:478px;top:660px;height:210px"></div>'
            + etiqueta('t7a', 560, 880, 'SE DEJA A MEDIAS', ROJO)
            + etiqueta('t7b', 80, 880, 'SIN NECESIDAD', ROJO)
            + ''.join(bacteria(f'b7-{k}', x, y, 120, (k * 23) % 40 - 20) for k, (x, y) in enumerate(sobre))
            + etiqueta('t7c', 470, 1230, 'ALGUNAS SOBREVIVEN', BAC))
    pop('#cal7', e['ini'] + 0.15, 0.5)
    for k in range(3):
        a(f'#d7-{k}', '{backgroundColor:"rgba(24,148,209,0.55)",duration:0.25}', e['ini'] + 0.5 + k * 0.25)
    pop('#t7b', W(e, 'falta'), 0.35)
    pop('#corte7', W(e, 'medias') - 0.3, 0.3, desde='{opacity:0,scaleY:0}', ease='power2.out')
    for k in range(3, 7):
        a(f'#d7-{k}', '{opacity:0.3,duration:0.3}', W(e, 'medias') - 0.2)
    pop('#t7a', W(e, 'medias'), sonido=False)
    for k in range(6):
        pop(f'#b7-{k}', W(e, 'algunas') - 0.6 + k * 0.05, 0.3, sonido=(k == 0))
    for k in [0, 1, 3, 4]:
        a(f'#b7-{k}', '{opacity:0,scale:0.2,duration:0.35}', W(e, 'sobreviven') - 0.2)
    TL.append(f'tl.to(["#b7-2","#b7-5"], {{scale:1.2,duration:0.3,yoyo:true,repeat:3}}, {W(e, "sobreviven") + 0.1:.2f});')
    pop('#t7c', W(e, 'sobreviven') + 0.15, sonido=False)

    # 8 · resistentes
    e = E[8]
    res = [(470, 690), (640, 760), (480, 870), (700, 900), (560, 1000), (820, 640)]
    H[8] = (bacteria('b8-a', 520, 800, 140) + bacteria('b8-b', 690, 830, 140)
            + ''.join(bac_escudo(f'r8-{k}', x, y, 130) for k, (x, y) in enumerate(res))
            + capsula('c8', -280, 760, 220, 0)
            + etiqueta('t8', 560, 1110, 'RESISTENTES', GRIS, 'grande')
            + nota('n8', 500, 1220, 430, 'No es usted quien se vuelve resistente: <b>son las bacterias</b>.'))
    pop('#b8-a', e['ini'] + 0.15, 0.4)
    pop('#b8-b', e['ini'] + 0.25, 0.4, sonido=False)
    tm = W(e, 'multiplican')
    a('#b8-a', '{opacity:0,duration:0.2}', tm)
    a('#b8-b', '{opacity:0,duration:0.2}', tm)
    for k in range(6):
        TL.append(f'tl.set("#r8-{k}s", {{opacity:0}}, 0);')
        pop(f'#r8-{k}', tm + k * 0.12, 0.35, sonido=(k % 2 == 0))
    tr = W(e, 'resistentes')
    for k in range(6):
        pop(f'#r8-{k}s', tr - 0.2 + k * 0.08, 0.3, sonido=(k == 0), desde='{opacity:0,scale:2.2}', ease='back.out(2)')
    pop('#t8', tr + 0.2, sonido=False)
    pop('#n8', tr + 0.6, 0.45, sonido=False)
    te = W(e, 'antibiótico')
    pop('#c8', te - 0.3, 0.2, sonido=False, desde='{opacity:0}', ease='none')
    TL.append(f'tl.to("#c8", {{x:640,duration:0.5,ease:"power2.in"}}, {te - 0.2:.2f});')
    TL.append(f'tl.to("#c8", {{x:330,rotation:-50,duration:0.6,ease:"back.out(2)"}}, {te + 0.3:.2f});')
    sfx('click-soft', te + 0.3, 0.4, 0.35)

    # 9 · más difícil de tratar
    e = E[9]
    H[9] = ('<div id="k9a" class="obj caja" style="left:70px;top:640px;width:400px;height:400px">'
            + bacteria('b9a', 125, 150, 150).replace('class="obj bac ', 'class="bac fija ') + '<div class="tit">INFECCIÓN COMÚN</div></div>'
            + '<div id="fl9" class="obj flecha" style="left:478px;top:780px">➜</div>'
            + '<div id="k9b" class="obj caja fuerte" style="left:610px;top:620px;width:420px;height:440px">'
            + bac_escudo('b9b', 110, 150, 160).replace('class="obj"', 'class="fija"') + '<div class="tit">MÁS DIFÍCIL DE TRATAR</div></div>')
    pop('#k9a', W(e, 'infección') - 0.2, 0.45)
    pop('#fl9', W(e, 'puede'), 0.35, desde='{opacity:0,x:-60}', ease='power3.out')
    pop('#k9b', W(e, 'volverse'), 0.5)
    TL.append(f'tl.to("#k9b", {{scale:1.06,yoyo:true,repeat:3,duration:0.3,ease:"sine.inOut"}}, {W(e, "difícil"):.2f});')

    # 10 · tres reglas
    e = E[10]
    reglas = [('No se automedique', 'automedique'), ('No use sobrantes ni medicinas de otra persona', 'sobrantes'),
              ('Siga el tratamiento como su médico lo indicó', 'tratamiento')]
    H[10] = ('<div id="lst10" class="obj tarjeta ancha" style="left:50px;top:590px;width:980px"><div class="tit">RECUERDE</div>'
             + ''.join(f'<div class="regla" id="r10-{k}"><span class="caja-v" id="cv10-{k}"></span><span>{txt}</span></div>' for k, (txt, _) in enumerate(reglas))
             + '</div>'
             + ''.join(visto(f'v10-{k}', 92, 718 + k * 120, 84) for k in range(3))
             + ''.join(f'<div id="pc10-{k}" class="obj popc">{c}</div>' for k, c in enumerate(['NO SE<br>AUTOMEDIQUE', 'NO USE<br>SOBRANTES', 'SIGA EL<br>TRATAMIENTO'])))
    pop('#lst10', e['ini'] + 0.15, 0.5)
    for k, (_, p) in enumerate(reglas):
        tp = W(e, p)
        pop(f'#pc10-{k}', tp - 0.65, 0.45, desde='{opacity:0,scale:0.1}', ease='back.out(1.7)')
        TL.append(f'tl.to("#pc10-{k}", {{x:-420,y:{-760 + k * 120},scale:0.35,opacity:0,duration:0.5,ease:"power2.in"}}, {tp + 0.45:.2f});')
        pop(f'#r10-{k}', tp + 0.85, 0.3, sonido=False, desde='{opacity:0.25}', ease='none')
        pop(f'#v10-{k}', tp + 0.85, 0.4, sonido=False, desde='{opacity:0,scale:0}', ease='back.out(2.5)')
        sfx('chime', tp + 0.85, 1.0, 0.25)

    # 11 · cuidar a todos
    e = E[11]
    H[11] = ('<div id="esc11" class="obj escudo-g" style="left:270px;top:560px;width:540px;height:648px">' + escudo_svg('rgba(24,148,209,0.35)', '#FFFFFF') + '</div>'
             + '<div id="fam11" class="obj" style="left:360px;top:760px;width:360px;height:230px">' + FAMILIA + '</div>'
             + nota('n11', 510, 1230, 420, 'Cuidar los antibióticos es cuidar <b>la salud de todos</b>'))
    pop('#esc11', e['ini'] + 0.15, 0.6)
    pop('#fam11', W(e, 'cuidar') - 0.1, 0.5)
    TL.append(f'tl.to("#esc11", {{scale:1.04,yoyo:true,repeat:3,duration:0.5,ease:"sine.inOut"}}, {W(e, "cuidar", 1):.2f});')
    pop('#n11', W(e, 'salud') - 0.2, 0.45, sonido=False)
    TL.append(f'tl.to("#insignia", {{scale:1.12,yoyo:true,repeat:1,duration:0.3}}, {W(e, "semana"):.2f});')

    # 12 · cierre
    e = E[12]
    H[12] = ('<img id="logo12" class="obj" src="assets/img/logo-lema.png" alt="Santa Helena del Valle IPS" style="left:225px;top:420px;width:580px" />'
             + '<div id="pr12" class="obj pr12">¿Qué tema de salud le explicamos ahora?</div>'
             + '<div id="com12" class="obj comenta">COMENTA ▼</div>'
             + '<div id="www12" class="obj www">www.santahelenadelvalleips.com</div>')
    a('#insignia', '{opacity:0,duration:0.3}', e['ini'] - 0.1)
    pop('#logo12', e['ini'] + 0.2, 0.6)
    pop('#pr12', W(e, 'tema') - 0.2, 0.4, sonido=False, desde='{opacity:0,y:30}', ease='power3.out')
    pop('#com12', W(e, 'comentarios') - 0.3, 0.5)
    TL.append(f'tl.to("#com12", {{scale:1.07,yoyo:true,repeat:5,duration:0.35,ease:"sine.inOut"}}, {W(e, "comentarios") + 0.3:.2f});')
    pop('#www12', W(e, 'comentarios') + 0.3, 0.4, sonido=False, desde='{opacity:0,y:20}', ease='power3.out')

    CAJA = {2: (150, 890, 600, 1310), 3: (60, 1090, 560, 1330), 4: (140, 960, 580, 1060), 5: (60, 1060, 590, 1070),
            6: (70, 1050, 590, 1118), 7: (60, 1020, 600, 1290), 8: (40, 1010, 620, 1360), 9: (70, 1030, 620, 1060)}

    def lienzo(k):
        if k not in CAJA:
            return ''
        x0, x1, y0, y1 = CAJA[k]
        sc = min(1040 / (x1 - x0), 1000 / (y1 - y0), 1.35)
        tx, ty = 540 - sc * (x0 + x1) / 2, 1050 - sc * (y0 + y1) / 2
        return f' style="transform:translate({tx:.0f}px,{ty:.0f}px) scale({sc:.3f})"'
    escs = ''.join(f'<div class="esc" id="e{k}"><div class="lienzo"{lienzo(k)}>{H[k]}</div></div>' for k in sorted(H))

    AUD.append(f'<audio id="musica" class="clip" src="assets/bgm/the-corporate-upbeat.mp3" data-start="0" data-duration="{total:.2f}" data-media-start="4" data-track-index="12" data-volume="0.055" data-fade-in="0.5" data-fade-out="2"></audio>')

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
<!-- Reel antibióticos · generado con gen.py -->
<div id="root" data-composition-id="reel" data-start="0" data-duration="{total:.2f}" data-width="1080" data-height="1920" data-layout-allow-overflow>
<div id="fondo"></div>
<img id="flor" src="assets/img/flor.png" alt="" />
<div id="puntos"></div>
{escs}
<div id="insignia"><div class="ins-pill"><span class="ins-mini">{ESCUDO_INSIGNIA}</span>SEMANA MUNDIAL DE CONCIENTIZACIÓN · 18–24 NOV</div></div>
{chr(10).join(SUB)}
<div id="guia">{''.join(HEL)}</div>
{chr(10).join(AUD)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
tl.fromTo("#flor", {{rotation:0}}, {{rotation:40, duration:{total:.2f}, ease:"none", immediateRender:false}}, 0);
{chr(10).join(TL)}
window.__timelines["reel"] = tl;
</script>
</body>
</html>
'''
    open(os.path.join(AQUI, 'fuentes/reel.html'), 'w', encoding='utf-8').write(doc)
    print(f'reel.html · {total:.1f} s · voces que faltan: {falt}')
    for e in escenas:
        print(f'  e{e["n"]}: {e["ini"]:.1f}–{e["fin"]:.1f}')


construir()
