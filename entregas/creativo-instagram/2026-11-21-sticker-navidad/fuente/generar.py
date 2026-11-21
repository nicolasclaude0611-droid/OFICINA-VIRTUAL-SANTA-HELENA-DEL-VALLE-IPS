#!/usr/bin/env python3
"""Genera sticker.html (sticker de Navidad 13 x 13 cm + 3 mm de sangrado, 1606 x 1606 px a 300 ppp).
Ilustraciones (árbol, muñeco de nieve, regalos, luces, nieve) dibujadas aquí en SVG, estilo plano con volumen."""
import math, random
from pathlib import Path

W = 1606
AQUI = Path(__file__).parent

# ---------- árbol ----------
def arbol(x, y, s=1.0):
    def tier(cx, y0, y1, hw, n, g):
        bump = 30
        p = f'M{cx},{y0} Q{cx+hw*0.45},{y0+(y1-y0)*0.55} {cx+hw},{y1} '
        for i in range(n):
            xa = cx + hw - (2*hw)*(i/n); xb = cx + hw - (2*hw)*((i+1)/n)
            p += f'Q{(xa+xb)/2},{y1+bump} {xb},{y1} '
        p += f'Q{cx-hw*0.45},{y0+(y1-y0)*0.55} {cx},{y0}Z'
        return f'<path d="{p}" fill="url(#{g})"/>'
    cx = 230
    capas = [(40, 210, 120, 4), (110, 320, 165, 5), (190, 430, 205, 6), (280, 540, 240, 7)]
    sombra = ''.join(tier(cx, y0+14, y1+14, hw+6, n, 'arbS') for y0, y1, hw, n in reversed(capas))
    frente = ''.join(tier(cx, y0, y1, hw, n, 'arbG') for y0, y1, hw, n in reversed(capas))
    guirn = ''.join(f'<path d="M{cx-a},{yy} Q{cx},{yy+44} {cx+b},{yy-22}" fill="none" stroke="#C8382D" stroke-width="7" stroke-linecap="round"/>'
                    for a, b, yy in [(70, 80, 160), (115, 125, 270), (160, 165, 385), (200, 205, 495)])
    bolas = ''
    for bx, by, r, c in [(195, 175, 17, 'r'), (285, 228, 11, 'o'), (150, 250, 11, 'o'), (250, 300, 20, 'r'), (120, 345, 12, 'o'),
                         (300, 360, 12, 'o'), (205, 400, 11, 'o'), (330, 420, 22, 'r'), (110, 440, 18, 'r'), (230, 470, 12, 'o'),
                         (60, 520, 13, 'o'), (175, 530, 21, 'r'), (300, 525, 12, 'o'), (400, 520, 18, 'r'), (260, 120, 10, 'o')]:
        g = 'bolaR' if c == 'r' else 'bolaO'
        bolas += f'<circle cx="{bx}" cy="{by}" r="{r}" fill="url(#{g})"/><circle cx="{bx-r*0.35:.1f}" cy="{by-r*0.35:.1f}" r="{r*0.28:.1f}" fill="#fff" opacity=".7"/>'
    estrella_pts = []
    for k in range(10):
        a = -math.pi/2 + k*math.pi/5; rr = 46 if k % 2 == 0 else 19
        estrella_pts.append(f'{cx+rr*math.cos(a):.1f},{22+rr*math.sin(a):.1f}')
    estrella = (f'<polygon points="{" ".join(estrella_pts)}" fill="url(#oro)" stroke="#E0A800" stroke-width="2" stroke-linejoin="round"/>'
                + ''.join(f'<line x1="{cx}" y1="22" x2="{p.split(",")[0]}" y2="{p.split(",")[1]}" stroke="#F9E27A" stroke-width="2" opacity=".8"/>' for p in estrella_pts[::2]))
    tronco = f'<path d="M{cx-30},540 L{cx+30},540 L{cx+36},640 L{cx-36},640Z" fill="#3E2A1E"/><path d="M{cx+8},540 L{cx+30},540 L{cx+36},640 L{cx+14},640Z" fill="#2E1F16"/>'
    brillo = f'<ellipse cx="{cx}" cy="330" rx="300" ry="330" fill="url(#halo)"/>'
    return f'<g transform="translate({x} {y}) scale({s})">{brillo}{tronco}{sombra}{frente}{guirn}{bolas}{estrella}</g>'

# ---------- muñeco de nieve ----------
def munieco(x, y, s=1.0):
    gris, crema = '#DCD9D2', '#FBF4E4'
    return f'''<g transform="translate({x} {y}) scale({s})">
<defs><clipPath id="cuerpoMn"><ellipse cx="180" cy="420" rx="160" ry="150"/><circle cx="185" cy="225" r="108"/></clipPath></defs>
<path d="M58,330 L-20,262 M-2,277 L-24,240 M-2,277 L-44,268" stroke="#6B4226" stroke-width="11" stroke-linecap="round" fill="none"/>
<path d="M305,320 L380,250 M362,267 L372,228 M362,267 L402,262" stroke="#6B4226" stroke-width="11" stroke-linecap="round" fill="none"/>
<g clip-path="url(#cuerpoMn)"><rect x="0" y="100" width="360" height="480" fill="{gris}"/>
<ellipse cx="208" cy="400" rx="140" ry="138" fill="{crema}"/><circle cx="205" cy="212" r="92" fill="{crema}"/></g>
<path d="M92,288 Q185,330 282,282 L290,316 Q186,370 86,322Z" fill="#C8382D"/><path d="M86,322 Q186,370 290,316 L288,330 Q186,385 88,338Z" fill="#9E2A22"/>
<path d="M122,300 Q110,360 112,430 L150,432 Q150,370 160,312Z" fill="#C8382D"/><path d="M112,430 L150,432 L150,440 L112,438Z" fill="#9E2A22"/>
''' + ''.join(f'<line x1="{xx}" y1="438" x2="{xx}" y2="456" stroke="#C8382D" stroke-width="4"/>' for xx in range(116, 150, 7)) + f'''
<circle cx="168" cy="210" r="13" fill="#3B2A20"/><circle cx="238" cy="198" r="13" fill="#3B2A20"/><circle cx="172" cy="205" r="4" fill="#fff"/><circle cx="242" cy="193" r="4" fill="#fff"/>
<path d="M200,228 Q235,224 286,232 Q240,250 204,250 Q190,242 200,228Z" fill="#D9803C"/><path d="M204,250 Q240,250 286,232 Q245,246 206,246Z" fill="#B8642B"/>
<path d="M175,262 Q205,290 240,262" stroke="#3B2A20" stroke-width="6" fill="none" stroke-linecap="round"/>
<circle cx="205" cy="390" r="14" fill="#3B2A20"/><circle cx="208" cy="450" r="14" fill="#3B2A20"/>
<g transform="rotate(-18 190 120)"><ellipse cx="190" cy="140" rx="118" ry="22" fill="#23253A"/><path d="M118,138 L128,30 Q190,10 252,30 L262,138Z" fill="#2E3048"/>
<path d="M128,30 Q190,10 252,30 L248,50 Q190,30 132,50Z" fill="#3A3D58"/><path d="M122,108 L258,108 L261,132 L119,132Z" fill="#C8382D"/></g>
</g>'''

# ---------- regalo ----------
def regalo(x, y, w, h, c1, c2, cinta):
    lid = 30
    return f'''<g transform="translate({x} {y})">
<rect x="0" y="{lid-4}" width="{w}" height="{h}" rx="6" fill="{c1}"/><rect x="{w*0.62}" y="{lid-4}" width="{w*0.38}" height="{h}" rx="6" fill="{c2}" opacity=".5"/>
<rect x="-8" y="0" width="{w+16}" height="{lid}" rx="7" fill="{c1}" stroke="rgba(0,0,0,.12)" stroke-width="3"/>
<rect x="{w/2-11}" y="0" width="22" height="{h+lid-4}" fill="{cinta}"/><rect x="-8" y="{lid/2-8}" width="{w+16}" height="0" fill="{cinta}"/>
<path d="M{w/2},2 C{w/2-60},-50 {w/2-62},10 {w/2},2 M{w/2},2 C{w/2+60},-50 {w/2+62},10 {w/2},2" fill="{cinta}" stroke="{cinta}" stroke-width="10" stroke-linejoin="round"/>
<circle cx="{w/2}" cy="2" r="10" fill="{cinta}"/></g>'''

def luces():
    def quad(p0, p1, p2, t): return [(1-t)**2*p0[i] + 2*(1-t)*t*p1[i] + t*t*p2[i] for i in (0, 1)]
    cols = ['#E0342B', '#F4C430', '#2FA24F']; out = ''; n = 0
    for a, b, c in [((-20, 66), (400, 220), (803, 92)), ((803, 92), (1206, 220), (1626, 66))]:
        out += f'<path d="M{a[0]},{a[1]} Q{b[0]},{b[1]} {c[0]},{c[1]}" fill="none" stroke="#0A2233" stroke-width="5"/>'
        for k in range(1, 9):
            x, yy = quad(a, b, c, k/9); col = cols[n % 3]; n += 1
            out += (f'<g transform="translate({x:.0f} {yy:.0f})"><circle cy="22" r="34" fill="{col}" opacity=".22"/>'
                    f'<rect x="-8" y="-4" width="16" height="13" rx="3" fill="#56656F"/><ellipse cy="24" rx="14" ry="20" fill="{col}"/>'
                    f'<ellipse cx="-5" cy="17" rx="4" ry="8" fill="#fff" opacity=".6"/></g>')
    return out

def nieve():
    random.seed(11); out = ''
    for i in range(190):
        x = random.uniform(0, W); y = random.uniform(140, 1420); r = random.choice([3, 4, 5, 6, 7, 9])
        if 120 < x < 1490 and 170 < y < 900: continue          # zona del logo y el texto: sin nieve
        out += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" opacity="{random.uniform(.35,.85):.2f}"/>'
    for x, y, s in [(70, 300, 1), (1530, 360, .8), (60, 960, .7), (1540, 880, 1.1), (940, 960, .7)]:
        brazos = ''.join(f'<line x1="0" y1="0" x2="{18*math.cos(a):.1f}" y2="{18*math.sin(a):.1f}"/>' for a in [k*math.pi/3 for k in range(6)])
        out += f'<g transform="translate({x} {y}) scale({s})" stroke="#fff" stroke-width="3.5" stroke-linecap="round" opacity=".85">{brazos}</g>'
    return out

suelo = ('<path d="M0,1440 Q260,1380 560,1450 Q860,1520 1150,1430 Q1400,1370 1606,1420 L1606,1606 L0,1606Z" fill="#fff"/>'
         '<path d="M0,1500 Q420,1450 820,1515 Q1220,1580 1606,1490 L1606,1606 L0,1606Z" fill="#E6F1FA"/>')
defs = '''<defs>
<linearGradient id="arbG" x1="0" x2="1"><stop offset="0" stop-color="#3F7D66"/><stop offset=".55" stop-color="#2F5F50"/><stop offset="1" stop-color="#244A3F"/></linearGradient>
<linearGradient id="arbS" x1="0" x2="1"><stop offset="0" stop-color="#1F4136"/><stop offset="1" stop-color="#18352C"/></linearGradient>
<radialGradient id="bolaR" cx=".35" cy=".35"><stop offset="0" stop-color="#F0605A"/><stop offset=".6" stop-color="#D6342C"/><stop offset="1" stop-color="#A11F1B"/></radialGradient>
<radialGradient id="bolaO" cx=".35" cy=".35"><stop offset="0" stop-color="#FFF1A6"/><stop offset=".6" stop-color="#F4C430"/><stop offset="1" stop-color="#D49A12"/></radialGradient>
<linearGradient id="oro" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE680"/><stop offset="1" stop-color="#F2B90F"/></linearGradient>
<radialGradient id="halo"><stop offset="0" stop-color="#FFF3B0" stop-opacity=".35"/><stop offset="1" stop-color="#FFF3B0" stop-opacity="0"/></radialGradient>
</defs>'''

fondo = f'<svg class="capa" viewBox="0 0 {W} {W}">{defs}{nieve()}{arbol(1060, 935, 0.9)}</svg>'
frente = (f'<svg class="capa" viewBox="0 0 {W} {W}">{suelo}{munieco(560, 1000, 0.92)}'
          f'{regalo(1000, 1430, 120, 95, "#D6342C", "#A11F1B", "#F4C430")}{regalo(1395, 1405, 105, 105, "#2FA24F", "#1E7A39", "#E0342B")}'
          f'{regalo(860, 1452, 95, 80, "#F4C430", "#D49A12", "#D6342C")}{luces()}</svg>')

html = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Sticker Navidad</title><style>
@font-face{{font-family:"Lobster";src:url(img/lobster.woff2) format("woff2")}}
@page{{size:13.6cm 13.6cm;margin:0}}
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{background:#fff}}
#s{{width:{W}px;height:{W}px;position:relative;overflow:hidden;background:linear-gradient(170deg,#004BAD 0%,#1A6DBD 40%,#1894D1 78%,#4CAFDC 100%);font-family:"Eras Demi ITC",sans-serif}}
svg.capa{{position:absolute;left:0;top:0;width:{W}px;height:{W}px}}
.logo{{position:absolute;left:50%;top:190px;width:430px;transform:translateX(-50%)}}
h1{{position:absolute;left:0;right:0;top:470px;text-align:center;font-family:"Lobster";font-weight:400;font-size:170px;line-height:1;color:#FFF212;text-shadow:0 6px 0 #C8382D,0 14px 24px rgba(0,0,0,.25)}}
.msg{{position:absolute;left:150px;right:150px;top:690px;text-align:center;color:#fff;font-size:48px;line-height:1.32}}
.hel{{position:absolute;left:105px;top:905px;height:780px}}
.corte{{position:absolute;left:35px;top:35px;width:{W-70}px;height:{W-70}px;border:3px dashed #ff00a8;display:none}}
body.conCorte .corte{{display:block}}
</style></head><body><section id="s">
{fondo}
<img class="hel" src="img/helenita-corazon-gorro.png">
{frente}
<img class="logo" src="img/logo-con-lema-transparente.png">
<h1>¡Feliz Navidad!</h1>
<p class="msg">Santa Helena del Valle IPS les desea que la magia de la Navidad ilumine cada rincón de su hogar y llene su corazón de gratitud, alegría y esperanza.</p>
<div class="corte"></div>
</section></body></html>'''
(AQUI / 'sticker.html').write_text(html)
print('ok')
