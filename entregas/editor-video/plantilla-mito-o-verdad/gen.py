#!/usr/bin/env python3
"""PLANTILLA de la serie «¿Mito o verdad?» con Helenita (reel 9:16, 1080×1920, HyperFrames).

Uso:  python3 gen.py episodios/ep1.py   → escribe fuentes/ep1.html
      cp fuentes/ep1.html index.html     → hyperframes check / render
Para un episodio nuevo solo se copia episodios/ep1.py, se cambian los textos, voces y puntos, y se ponen las
voces en assets/voz/. Ver README.md.

- Voces reutilizables de la serie: mv-pregunta, mv-mito, mv-verdad, mv-cierre (assets/voz/).
- La duración sale de las voces; si falta una, se estima (14 caracteres por segundo).
- Helenita aparece en el título, en cada creencia y en la pregunta, y en el cierre. Durante la respuesta se
  oye solo su voz y la pantalla queda libre para el sello y los puntos (pedido de Nicolas, 19-nov-2026).
- Colores: paleta del manual (degradado azul, #1894D1, #FFF212, #FFCC29, blanco) + sellos MITO rojo y VERDAD verde.
- Fuentes Eras (con licencia) en assets/fonts/*.TTF, ignoradas por git: nunca se suben al repositorio.
"""
import os, re, sys, runpy, subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
AZ, AM, OC, NAVY = '#1894D1', '#FFF212', '#FFCC29', '#0A2233'
ROJO, VERDE, VIR = '#E5383B', '#2ECC71', '#A66BFF'
WHATSAPP = '311 339 8988'
WEB = 'www.santahelenadelvalleips.com'
TEXTOS_FIJOS = {'mv-pregunta': '¿Mito o verdad?', 'mv-mito': '¡Mito!', 'mv-verdad': '¡Verdad!',
                'mv-cierre': 'Si tiene dudas, agende su cita por WhatsApp.'}

AUD, TL, PISTAS = [], [], {}


# ---------- utilidades de audio y tiempos ----------
def dur(path):
    p = os.path.join(AQUI, path)
    if not os.path.exists(p):
        return None
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
                                capture_output=True, text=True).stdout)


def tramos_voz(path, d):
    r = subprocess.run(['ffmpeg', '-i', os.path.join(AQUI, path), '-af', 'silencedetect=noise=-38dB:d=0.16', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', r)]
    fin = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', r)]
    tr, t = [], 0.0
    for a, b in zip(ini, fin + [d] * (len(ini) - len(fin))):
        if a - t > 0.08:
            tr.append((t, a))
        t = b
    if d - t > 0.08:
        tr.append((t, d))
    return tr


def tiempos_palabras(texto, d, audio):
    pal = texto.split()
    peso = [len(p) + 1.5 for p in pal]
    frases, cur = [], []
    for i, p in enumerate(pal):
        cur.append(i)
        if p[-1] in ',.:?!;':
            frases.append(cur); cur = []
    if cur:
        frases.append(cur)
    tr = tramos_voz(audio, d) if audio else []
    while tr and len(tr) > len(frases):
        k = min(range(len(tr) - 1), key=lambda j: tr[j + 1][0] - tr[j][1])
        tr[k:k + 2] = [(tr[k][0], tr[k + 1][1])]
    grupos = list(zip(frases, tr)) if tr and len(tr) == len(frases) else \
        [(list(range(len(pal))), (tr[0][0], tr[-1][1]) if tr else (0.05, d - 0.1))]
    out = [0.0] * len(pal)
    for idx, (a, b) in grupos:
        tot, t = sum(peso[i] for i in idx), a
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


def pop(sel, t, d=0.45, sonido=True, desde='{opacity:0,scale:0.4}', hasta='opacity:1,scale:1,x:0,y:0,rotation:0', ease='back.out(1.8)'):
    TL.append(f'tl.fromTo("{sel}", {desde}, {{{hasta},duration:{d},ease:"{ease}",immediateRender:false}}, {t:.2f});')
    if sonido:
        sfx('pop', t, 0.5, 0.22)


class Voz:
    """Una voz colocada en el tiempo, con sus palabras para subtítulos y anclas."""
    def __init__(self, nombre, texto, t, claves=()):
        ruta = f'assets/voz/{nombre}.mp3'
        d = dur(ruta)
        self.falta = d is None
        self.d = d if d else max(0.8, len(texto) / 14.0)
        self.t, self.texto, self.claves = t, texto, list(claves)
        self.pal = tiempos_palabras(texto, self.d, None if self.falta else ruta)
        if not self.falta:
            k = pista_libre(t, t + self.d, 2, 3)
            AUD.append(f'<audio id="v-{nombre}-{len(AUD)}" class="clip" src="{ruta}" data-start="{t:.2f}" data-duration="{self.d - 0.03:.2f}" data-track-index="{k}" data-volume="1"></audio>')
        self.nombre = nombre

    @property
    def fin(self):
        return self.t + self.d

    def W(self, palabra, k=0):
        hits = [tt for p, tt in self.pal if p.lower().strip('¿?¡!,.:;').startswith(palabra.lower())]
        return self.t + (hits[k] if len(hits) > k else hits[-1] if hits else 0)


# ---------- subtítulos palabra por palabra ----------
SUB = []


def subtitulos(v, hasta):
    pal = v.pal
    bloques, cur, largo = [], [], 0
    for j, (p, _) in enumerate(pal):
        if cur and largo + len(p) > 40:
            bloques.append(cur); cur, largo = [], 0
        cur.append(j); largo += len(p) + 1
        if p[-1] in '.?:' and largo > 14:
            bloques.append(cur); cur, largo = [], 0
    if cur:
        bloques.append(cur)

    def palabra(p, clave):
        if not clave:
            return p
        m = re.match(r'^([¿¡]*)(.*?)([,.:;?!]*)$', p)
        return f'{m.group(1)}<b class="k">{m.group(2)}</b>{m.group(3)}'
    for b, idx in enumerate(bloques):
        bid = f's{len(SUB)}'
        SUB.append(f'<div id="{bid}" class="sub">' + ''.join(
            f'<span id="{bid}-{j}" class="w">{palabra(pal[j][0], pal[j][0] in v.claves)}</span> ' for j in idx) + '</div>')
        t0 = v.t + pal[idx[0]][1]
        t1 = v.t + pal[bloques[b + 1][0]][1] if b + 1 < len(bloques) else hasta
        TL.append(f'tl.set("#{bid}", {{opacity:1}}, {t0 - 0.02:.2f});')
        TL.append(f'tl.set("#{bid}", {{opacity:0}}, {t1 - 0.02:.2f});')
        for j in idx:
            TL.append(f'tl.fromTo("#{bid}-{j}", {{opacity:0,y:14}}, {{opacity:1,y:0,duration:0.16,ease:"power2.out",immediateRender:false}}, {v.t + pal[j][1] - 0.04:.2f});')


# ---------- íconos (SVG 100×100) ----------
def _c(inner, fondo='#FFFFFF'):
    return f'<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="48" fill="{fondo}"/>{inner}</svg>'


def _persona(x, y, s, color):
    return (f'<g transform="translate({x},{y}) scale({s})" fill="{color}">'
            '<circle cx="10" cy="7" r="7"/><path d="M0 34 V22 Q0 15 10 15 Q20 15 20 22 V34 Z"/></g>')


ICONOS = {
    'presion': _c(f'<path d="M50 78 C20 58 18 38 30 30 C40 24 48 30 50 36 C52 30 60 24 70 30 C82 38 80 58 50 78 Z" fill="{ROJO}"/>'
                  '<path d="M24 50 H38 L43 40 L50 60 L55 48 H76" fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>'),
    'azucar': _c(f'<path d="M50 18 C62 38 72 50 72 62 A22 22 0 0 1 28 62 C28 50 38 38 50 18 Z" fill="{AZ}"/>'
                 '<rect x="40" y="56" width="20" height="5" rx="2" fill="#fff"/><rect x="47.5" y="48.5" width="5" height="20" rx="2" fill="#fff"/>'),
    'grasa': _c(f'<path d="M50 18 C62 38 72 50 72 62 A22 22 0 0 1 28 62 C28 50 38 38 50 18 Z" fill="{OC}"/>'
                '<circle cx="42" cy="60" r="5" fill="#fff" opacity="0.8"/><circle cx="56" cy="68" r="4" fill="#fff" opacity="0.8"/>'),
    'lupa': _c(f'<circle cx="44" cy="44" r="18" fill="none" stroke="{AZ}" stroke-width="8"/>'
               f'<path d="M57 57 L74 74" stroke="{AZ}" stroke-width="10" stroke-linecap="round"/>'
               f'<path d="M36 44 L42 50 L53 38" fill="none" stroke="{VERDE}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'),
    'edades': _c(_persona(18, 44, 0.75, OC) + _persona(38, 30, 1.2, AZ) + _persona(66, 38, 0.95, '#5DB8E6')),
    'refuerzo': _c(f'<g transform="rotate(-45 50 50)"><rect x="24" y="42" width="44" height="16" rx="4" fill="{AZ}"/>'
                   f'<rect x="68" y="47" width="14" height="6" fill="{NAVY}"/><rect x="18" y="38" width="6" height="24" rx="2" fill="{NAVY}"/>'
                   f'<rect x="10" y="47" width="8" height="6" fill="{NAVY}"/></g>'
                   f'<circle cx="74" cy="28" r="13" fill="{VERDE}"/><path d="M74 21 V35 M67 28 H81" stroke="#fff" stroke-width="4.5" stroke-linecap="round"/>'),
    'calendario': _c(f'<rect x="22" y="26" width="56" height="50" rx="8" fill="#fff" stroke="{AZ}" stroke-width="5"/>'
                     f'<rect x="22" y="26" width="56" height="14" rx="6" fill="{AZ}"/>'
                     f'<path d="M34 20 V32 M66 20 V32" stroke="{NAVY}" stroke-width="5" stroke-linecap="round"/>'
                     f'<text x="50" y="68" text-anchor="middle" font-family="Eras Bold" font-size="22" fill="{NAVY}">1 AÑO</text>'),
    'germen': _c(''.join(f'<circle cx="{50 + 30 * __import__("math").cos(k * 0.785):.1f}" cy="{50 + 30 * __import__("math").sin(k * 0.785):.1f}" r="5" fill="{VIR}"/>' for k in range(8))
                 + f'<circle cx="50" cy="50" r="22" fill="{VIR}"/><circle cx="43" cy="47" r="3.5" fill="{NAVY}"/><circle cx="57" cy="47" r="3.5" fill="{NAVY}"/>'),
    'escudo': _c(f'<path d="M50 16 L76 26 V48 C76 66 64 78 50 84 C36 78 24 66 24 48 V26 Z" fill="{AZ}"/>'
                 '<path d="M38 50 L47 59 L63 41" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'),
    'familia': _c(f'<path d="M50 12 L82 24 V48 C82 70 68 82 50 90 C32 82 18 70 18 48 V24 Z" fill="{AZ}" opacity="0.25"/>'
                  + _persona(26, 40, 0.95, AZ) + _persona(43, 50, 0.7, OC) + _persona(56, 40, 0.95, '#5DB8E6')),
    'alerta': _c(f'<path d="M50 18 L82 76 H18 Z" fill="{OC}" stroke="{OC}" stroke-width="6" stroke-linejoin="round"/>'
                 f'<rect x="46" y="38" width="8" height="22" rx="3" fill="{NAVY}"/><circle cx="50" cy="67" r="4.5" fill="{NAVY}"/>'),
}

SELLO_X = f'<svg viewBox="0 0 100 100"><path d="M22 22 L78 78 M78 22 L22 78" stroke="#fff" stroke-width="16" stroke-linecap="round"/></svg>'
SELLO_V = f'<svg viewBox="0 0 100 100"><path d="M18 54 L40 76 L82 28" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/></svg>'


# ---------- construcción ----------
def construir(ruta_ep):
    ep = runpy.run_path(ruta_ep)
    n_ep, mitos = ep['EPISODIO'], ep['MITOS']
    N = len(mitos)
    H, HEL, faltan = [], [], []
    tramos_h = []  # (inicio, fin, animación) en que Helenita está en pantalla

    # Título
    t = 0.0
    H.append(f'<div class="esc" id="e0"><div id="tit" class="obj"><div class="tit-sello">¿MITO O<br>VERDAD?</div>'
             f'<div class="tit-ep">EPISODIO {n_ep}</div></div></div>')
    TL.append('tl.set("#e0", {opacity:1}, 0);')
    pop('#tit', 0.15, 0.6, desde='{opacity:0,scale:2.2,rotation:-12}', hasta='opacity:1,scale:1,rotation:-4', ease='back.out(1.4)')
    sfx('whoosh', 0.1, 0.6, 0.3)
    t = 1.7
    tramos_h.append((0.0, t, 'saludar'))
    TL.append(f'tl.to("#e0", {{opacity:0,x:-160,duration:0.3,ease:"power2.in"}}, {t - 0.3:.2f});')

    for i, m in enumerate(mitos):
        k = i + 1
        ini = t
        sid = f'e{k}'
        es_mito = m['veredicto'] == 'mito'
        va = Voz(m['voz_a'], m['creencia'], ini + 0.45)
        vp = Voz('mv-pregunta', TEXTOS_FIJOS['mv-pregunta'], va.fin + 0.3, ['¿Mito', 'verdad?'])
        t_cuenta = vp.fin + 0.05
        tv = t_cuenta + 0.85
        nv = 'mv-mito' if es_mito else 'mv-verdad'
        vv = Voz(nv, TEXTOS_FIJOS[nv], tv + 0.05, ['¡Mito!' if es_mito else '¡Verdad!'])
        vb = Voz(m['voz_b'], m['texto_b'], vv.fin + 0.35, m.get('claves', []))
        fin = vb.fin + 1.5  # tiempo para leer el último punto
        for v in (va, vp, vv, vb):
            if v.falta:
                faltan.append(v.nombre)
        subtitulos(va, vp.t)
        subtitulos(vp, tv)
        subtitulos(vv, vb.t)
        subtitulos(vb, fin - 0.15)

        puntos = m['puntos']
        lineas = -(-len(m['creencia']) // 24)
        borde = 560 + (88 + lineas * 78) * 0.82  # borde inferior de la tarjeta ya reducida
        y_sello, y_etq, y_ptos = borde - 40, borde + 35, borde + 170
        filas = ''.join(f'<div class="pto" id="{sid}-p{j}"><span class="ico">{ICONOS[ic]}</span><span class="ptxt">{txt}</span></div>'
                        for j, (ic, txt, _) in enumerate(puntos))
        etq = m.get('etiqueta')
        sello = (f'<div id="{sid}-ver" class="obj sello {"rojo" if es_mito else "verde"}" style="top:{y_sello:.0f}px"><span class="sico">{SELLO_X if es_mito else SELLO_V}</span>'
                 f'{"MITO" if es_mito else "VERDAD"}</div>')
        H.append(f'<div class="esc" id="{sid}">'
                 f'<div id="{sid}-num" class="obj num">MITO {k} DE {N}</div>'
                 f'<div id="{sid}-card" class="obj creencia"><span class="comi">“</span>{m["creencia"]}<span class="comi">”</span></div>'
                 f'<div id="{sid}-preg" class="obj preg"><span class="reloj"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="none" stroke="rgba(10,34,51,0.25)" stroke-width="12"/>'
                 f'<circle id="{sid}-arco" cx="50" cy="50" r="40" fill="none" stroke="{NAVY}" stroke-width="12" stroke-dasharray="251.3" stroke-dashoffset="0" transform="rotate(-90 50 50)"/></svg></span>¿MITO O VERDAD?</div>'
                 + sello
                 + (f'<div id="{sid}-etq" class="obj etq" style="top:{y_etq:.0f}px"><span>{etq[0]}</span></div>' if etq else '')
                 + f'<div class="ptos n{len(puntos)}" style="top:{y_ptos + (40 if len(puntos) <= 2 else 0):.0f}px">{filas}</div></div>')

        # entrada de la escena
        TL.append(f'tl.fromTo("#{sid}", {{opacity:0,x:160}}, {{opacity:1,x:0,duration:0.45,ease:"power3.out",immediateRender:false}}, {ini - 0.05:.2f});')
        sfx('whoosh-short', ini - 0.05, 0.5, 0.2)
        TL.append(f'tl.to("#{sid}", {{opacity:0,x:-160,duration:0.32,ease:"power2.in"}}, {fin - 0.3:.2f});')
        # progreso en la insignia
        TL.append(f'tl.to("#dot{k}", {{backgroundColor:"{AM}",scale:1.25,duration:0.3}}, {ini + 0.1:.2f});')
        TL.append(f'tl.to("#dot{k}", {{scale:1,duration:0.2}}, {ini + 0.4:.2f});')
        pop(f'#{sid}-num', ini + 0.1, 0.4, sonido=False, desde='{opacity:0,y:-30}', ease='power3.out')
        pop(f'#{sid}-card', ini + 0.2, 0.5)
        # pregunta y cuenta
        pop(f'#{sid}-preg', vp.t - 0.1, 0.45, desde='{opacity:0,scale:0.3,rotation:-20}', hasta='opacity:1,scale:1,rotation:-3')
        TL.append(f'tl.fromTo("#{sid}-arco", {{strokeDashoffset:0}}, {{strokeDashoffset:251.3,duration:0.8,ease:"none",immediateRender:false}}, {t_cuenta:.2f});')
        sfx('click-soft', t_cuenta, 0.3, 0.3)
        sfx('click-soft', t_cuenta + 0.4, 0.3, 0.3)
        # veredicto: la tarjeta sube, la pregunta se va y el sello cae
        TL.append(f'tl.to("#{sid}-preg", {{opacity:0,scale:0.6,duration:0.25}}, {tv - 0.05:.2f});')
        TL.append(f'tl.to("#{sid}-card", {{y:-70,scale:0.82,duration:0.45,ease:"power3.inOut"}}, {tv - 0.1:.2f});')
        TL.append(f'tl.to("#{sid}-num", {{y:-60,opacity:0,duration:0.3}}, {tv - 0.1:.2f});')
        pop(f'#{sid}-ver', tv, 0.4, sonido=False, desde='{opacity:0,scale:2.6,rotation:-25}', hasta='opacity:1,scale:1,rotation:-8', ease='power4.in')
        TL.append(f'tl.to("#{sid}-card", {{x:-8,duration:0.06,yoyo:true,repeat:3}}, {tv + 0.4:.2f});')
        sfx('click-soft', tv + 0.38, 0.4, 0.5)
        sfx('chime' if not es_mito else 'whoosh-short', tv + 0.38, 0.6, 0.25)
        # puntos al ritmo de la voz
        for j, (_, _, ancla) in enumerate(puntos):
            pop(f'#{sid}-p{j}', vb.W(ancla) - 0.25, 0.45, desde='{opacity:0,x:80}', ease='power3.out')
        if etq:
            pop(f'#{sid}-etq', vb.W(etq[1]) - 0.15, 0.4, sonido=False, desde='{opacity:0,scale:0.4,rotation:-10}', hasta='opacity:1,scale:1,rotation:-4')
        # Helenita: creencia (hablar) y pregunta (pensar); sale durante la respuesta
        tramos_h.append((ini, vp.t - 0.1, 'hablar'))
        tramos_h.append((vp.t - 0.1, tv + 0.2, 'pensar'))
        t = fin

    # Cierre
    ini = t
    vc = Voz('mv-cierre', TEXTOS_FIJOS['mv-cierre'], ini + 0.5, ['dudas,', 'WhatsApp.'])
    if vc.falta:
        faltan.append('mv-cierre')
    fin = vc.fin + 3.0
    subtitulos(vc, fin - 0.1)
    H.append(f'<div class="esc" id="ec"><img id="c-logo" class="obj" src="assets/img/logo-lema.png" alt="Santa Helena del Valle IPS" />'
             f'<div id="c-txt" class="obj ctxt">Si tiene dudas, <b>agende su cita</b></div>'
             f'<div id="c-wa" class="obj wa"><svg viewBox="0 0 32 32"><path fill="#fff" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6a10.6 10.6 0 0 1-5.4-1.5l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7 0a8.7 8.7 0 0 1-4.3-3.7c-.3-.6.3-.5.9-1.7a.6.6 0 0 0 0-.5l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6a1.2 1.2 0 0 0-.9.4 3.6 3.6 0 0 0-1.1 2.7 6.3 6.3 0 0 0 1.3 3.3 14.4 14.4 0 0 0 5.5 4.9c2 .9 2.8.9 3.8.8a3.3 3.3 0 0 0 2.2-1.5 2.7 2.7 0 0 0 .2-1.5c-.1-.2-.3-.3-.6-.4z"/></svg>WhatsApp {WHATSAPP}</div>'
             f'<div id="c-web" class="obj cweb">{WEB}</div></div>')
    TL.append(f'tl.fromTo("#ec", {{opacity:0,x:160}}, {{opacity:1,x:0,duration:0.45,ease:"power3.out",immediateRender:false}}, {ini - 0.05:.2f});')
    TL.append(f'tl.to("#insignia", {{opacity:0,duration:0.3}}, {ini - 0.1:.2f});')
    pop('#c-logo', ini + 0.15, 0.6)
    pop('#c-txt', vc.W('agende') - 0.2, 0.4, sonido=False, desde='{opacity:0,y:30}', ease='power3.out')
    pop('#c-wa', vc.W('WhatsApp') - 0.2, 0.5)
    TL.append(f'tl.to("#c-wa", {{scale:1.06,yoyo:true,repeat:5,duration:0.35,ease:"sine.inOut"}}, {vc.W("WhatsApp") + 0.4:.2f});')
    pop('#c-web', vc.W('WhatsApp') + 0.3, 0.4, sonido=False, desde='{opacity:0,y:20}', ease='power3.out')
    tramos_h.append((ini, fin, 'invitar'))
    total = fin

    # Helenita: videos encadenados por tramo, y entra/sale cuando hay un hueco
    for a, b, anim in tramos_h:
        n = 0
        while (b - a) - n * 5.0 > 0.05:
            seg = min(5.0, (b - a) - n * 5.0)
            HEL.append(f'<video id="h{len(HEL)}" class="anim clip" src="assets/helenita/{anim}.webm" data-start="{a + n * 5.0:.2f}" data-duration="{seg:.2f}" data-track-index="5" muted playsinline></video>')
            n += 1
    TL.append('tl.fromTo("#guia", {opacity:0,y:120}, {opacity:1,y:0,duration:0.6,ease:"power3.out",immediateRender:false}, 0.1);')
    previo = 0.0
    for a, b, _ in tramos_h:
        if a - previo > 0.3:  # hubo un hueco: sale y vuelve a entrar
            TL.append(f'tl.to("#guia", {{opacity:0,y:260,duration:0.4,ease:"power2.in"}}, {previo - 0.05:.2f});')
            TL.append(f'tl.to("#guia", {{opacity:1,y:0,duration:0.5,ease:"power3.out"}}, {a - 0.1:.2f});')
        previo = b

    AUD.append(f'<audio id="musica" class="clip" src="assets/bgm/the-corporate-upbeat.mp3" data-start="0" data-duration="{total:.2f}" data-media-start="4" data-track-index="12" data-volume="0.05" data-fade-in="0.5" data-fade-out="2"></audio>')

    dots = ''.join(f'<i id="dot{k + 1}"></i>' for k in range(N))
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
<!-- ¿Mito o verdad? · episodio {n_ep} · generado con gen.py -->
<div id="root" data-composition-id="reel" data-start="0" data-duration="{total:.2f}" data-width="1080" data-height="1920" data-layout-allow-overflow>
<div id="fondo"></div>
<img id="flor" src="assets/img/flor.png" alt="" />
<div id="puntos"></div>
{''.join(H)}
<div id="insignia"><div class="ins-pill">¿MITO O VERDAD? · EP. {n_ep}<span class="dots">{dots}</span></div></div>
{chr(10).join(SUB)}
<div id="guia">{''.join(HEL)}</div>
{chr(10).join(AUD)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
tl.fromTo("#flor", {{rotation:0}}, {{rotation:40, duration:{total:.2f}, ease:"none", immediateRender:false}}, 0);
tl.fromTo("#insignia", {{opacity:0,y:-20}}, {{opacity:1,y:0,duration:0.4,immediateRender:false}}, 1.6);
{chr(10).join(TL)}
window.__timelines["reel"] = tl;
</script>
</body>
</html>
'''
    nombre = os.path.splitext(os.path.basename(ruta_ep))[0]
    salida = os.path.join(AQUI, f'fuentes/{nombre}.html')
    open(salida, 'w', encoding='utf-8').write(doc)
    print(f'{nombre}.html · {total:.1f} s · voces que faltan: {sorted(set(faltan))}')


if __name__ == '__main__':
    construir(sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, 'episodios/ep1.py'))
