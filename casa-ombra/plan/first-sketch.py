"""Casa Ombra first-floor sketch -> SVG. Same coordinates and scale as the ground-floor sketch (see model2.py)."""
import sys

S, OX, OY = 36, 483, 300
W, H = 2400, 1350
INK = '#111'
G = '#9a9a9a'
LAT = '#9a6a35'
o = []

def X(v): return OX + v * S
def Y(v): return OY + v * S

def dash_attr(dash): return f'stroke-dasharray="{dash}"' if dash else ''

def line(a, b, c, d, w=2, col=INK, dash=''):
    o.append(f'<line x1="{X(a):.1f}" y1="{Y(b):.1f}" x2="{X(c):.1f}" y2="{Y(d):.1f}" stroke="{col}" stroke-width="{w}" {dash_attr(dash)} stroke-linecap="square"/>')

def wall(a, b, c, d): line(a, b, c, d, 10)
def iwall(a, b, c, d): line(a, b, c, d, 5)

def glass(a, b, c, d):
    line(a, b, c, d, 8, INK)
    line(a, b, c, d, 4, '#fff')

def rect(x, y, w, h, fill='none', st=INK, sw=1.5, dash='', rx=0):
    o.append(f'<rect x="{X(x):.1f}" y="{Y(y):.1f}" width="{w*S:.1f}" height="{h*S:.1f}" rx="{rx}" fill="{fill}" stroke="{st}" stroke-width="{sw}" {dash_attr(dash)}/>')

def poly(pts, fill='none', st=INK, sw=1.5, dash=''):
    p = ' '.join(f'{X(x):.1f},{Y(y):.1f}' for x, y in pts)
    o.append(f'<polygon points="{p}" fill="{fill}" stroke="{st}" stroke-width="{sw}" {dash_attr(dash)}/>')

def txt(x, y, s, size=22, weight=700, col=INK, ls='.12em', anchor='middle'):
    o.append(f'<text x="{X(x):.1f}" y="{Y(y):.1f}" font-size="{size}" font-weight="{weight}" letter-spacing="{ls}" fill="{col}" text-anchor="{anchor}">{s}</text>')

def sub(x, y, s, size=14, col='#555'): txt(x, y, s, size, 400, col, '.06em')

def gap(a, b, c, d): line(a, b, c, d, 13, '#fff')

def door_h(x0, y, wd, hinge='l', swing='s'):
    gap(x0, y, x0 + wd, y)
    hx = x0 if hinge == 'l' else x0 + wd
    ex = x0 + wd if hinge == 'l' else x0
    sy = 1 if swing == 's' else -1
    line(hx, y, hx, y + sy * wd, 2)
    sweep = 1 if (hinge == 'l') == (swing == 'n') else 0
    o.append(f'<path d="M{X(hx):.1f} {Y(y + sy*wd):.1f} A {wd*S:.1f} {wd*S:.1f} 0 0 {1 - sweep} {X(ex):.1f} {Y(y):.1f}" fill="none" stroke="{INK}" stroke-width="1.1" stroke-dasharray="5 4"/>')

def door_v(x, y0, wd, hinge='t', swing='e'):
    gap(x, y0, x, y0 + wd)
    hy = y0 if hinge == 't' else y0 + wd
    ey = y0 + wd if hinge == 't' else y0
    sx = 1 if swing == 'e' else -1
    line(x, hy, x + sx * wd, hy, 2)
    sweep = 1 if (hinge == 't') == (swing == 'e') else 0
    o.append(f'<path d="M{X(x + sx*wd):.1f} {Y(hy):.1f} A {wd*S:.1f} {wd*S:.1f} 0 0 {sweep} {X(x):.1f} {Y(ey):.1f}" fill="none" stroke="{INK}" stroke-width="1.1" stroke-dasharray="5 4"/>')

def tree(x, y, r):
    o.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="{r*S:.1f}" fill="none" stroke="#999" stroke-width="1.2" stroke-dasharray="3 3"/>'
             f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="3" fill="#999"/>')

def lattice(a, b, c, d): line(a, b, c, d, 7, LAT, '4 4')

# ---------- what is below (light grey context) ----------
poly([(-3.15, -4.6), (42.5, -4.6), (42.5, 26.0), (-3.15, 26.0)], 'none', G, 2)
rect(-3.15, 26.0, 45.65, 2.6, '#f1f1f1', 'none'); txt(24, 27.7, 'ROAD', 15, 600, '#888')
line(-0.8, 26.0, 6.9, 26.0, 7, '#fff'); line(-0.8, 26.0, 6.9, 26.0, 2, G, '10 6')
txt(1.6, 20.3, 'FORECOURT', 16, 700, '#999'); sub(1.6, 21.0, 'below', 12, '#999')
for ty in (11.5, 16.5, 21.5): tree(-1.9, ty, 1.0)
rect(1.7, 11.0, 1.9, 4.9, 'none', G, 1.2, rx=16); rect(4.2, 10.9, 2.1, 5.1, 'none', G, 1.2, rx=16)
poly([(7.7, 10.5), (11.7, 10.5), (11.7, 14.6), (27.9, 14.6), (27.9, 19.35), (7.7, 19.35)], '#ececec', G, 1.5)
for cx in (14.9, 24.2):
    rect(cx - 1.5, 15.5, 3, 3, '#fff', G, 1); tree(cx, 17.0, 1.25)
txt(19.5, 17.6, 'REFLECTING POOL', 15, 700, '#999'); sub(19.5, 18.3, 'below', 12, '#999')
rect(7.7, 19.35, 22.5, 2.45, 'none', G, 1, '3 4'); rect(7.7, 21.8, 22.5, 1.2, '#f6f6f6', G, 1); rect(7.7, 23.0, 34.8, 3.0, 'none', G, 1, '3 4')
rect(27.9, 14.6, 2.3, 7.2, '#f6f6f6', G, 1)
txt(26, -2.2, 'REAR LAWN', 15, 700, '#999'); rect(37.6, -4.0, 4.3, 3.6, '#f6f6f6', G, 1.2)
tree(9, -2.6, 1.0); tree(19, -3.0, 1.0); tree(33, -2.8, 1.0); tree(39.6, 23.0, 1.1); tree(40.3, 16.5, 1.2); tree(39.8, 10.5, 1.2)
# roofs of the low blocks
o.append('<defs><pattern id="gr" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="0.9" fill="#c4c4c4"/><circle cx="5.5" cy="5.5" r="0.9" fill="#c4c4c4"/></pattern>'
         f'<marker id="ah" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="{INK}"/></marker></defs>')
rect(0, 0, 16.75, 7.0, 'url(#gr)', G, 2); rect(30.2, 7.0, 6.6, 10.9, 'url(#gr)', G, 2)
rect(13.6, 2.35, 2.7, 2.5, '#fff', G, 1.2); sub(14.95, 3.75, 'skylight', 11, '#888')
txt(5.2, 3.3, 'GARAGE BLOCK ROOF', 15, 700, '#888'); sub(5.2, 4.0, 'gravel · one storey, below', 12, '#888')
txt(33.5, 16.9, 'SPA ROOF', 13, 700, '#888')

# ---------- first floor ----------
x0, y0, x1, y1 = 8.4, 6.6, 35.8, 15.2
rect(x0, y0, x1 - x0, y1 - y0, '#fff', 'none')
# outer walls
wall(x0, y0, x1, y0); glass(16.6, y0, 21.2, y0); glass(24.6, y0, 26.2, y0); glass(28.7, y0, 30.3, y0)
wall(x1, y0, x1, y1)
wall(x0, y0, x0, 7.3); glass(x0, 7.3, x0, 12.4); wall(x0, 12.4, x0, y1)
wall(x0, y1, 10.1, y1); glass(10.1, y1, 34.3, y1); wall(34.3, y1, x1, y1)
lattice(x0 - 0.38, 7.3, x0 - 0.38, 12.4); lattice(10.1, y1 + 0.38, 34.3, y1 + 0.38)
o.append(f'<text x="{X(22.2):.1f}" y="{Y(y1 + 1.05):.1f}" font-size="13" font-weight="700" letter-spacing=".1em" fill="{LAT}" text-anchor="middle">TIMBER LATTICE SCREEN (brown line) · VIEW OVER THE POOL</text>')
# primary suite
iwall(15.75, y0, 15.75, y1)
iwall(x0, 10.3, 13.4, 10.3); iwall(13.4, y0, 13.4, 10.3)
door_v(15.75, 8.75, 0.95, 't', 'w')                 # suite entrance from the gallery
door_v(13.4, 8.4, 0.9, 'b', 'w')                    # dressing -> bathroom
gap(13.6, 10.3, 15.55, 10.3)
# stair void + landing
rect(15.9, 7.3, 6.0, 1.15, '#fff', INK, 1.5)
for i in range(1, 20): line(15.9 + 6.0 * i / 20, 7.3, 15.9 + 6.0 * i / 20, 8.45, 1)
o.append(f'<line x1="{X(21.6)}" y1="{Y(7.875)}" x2="{X(16.2)}" y2="{Y(7.875)}" stroke="{INK}" stroke-width="1.8" marker-end="url(#ah)"/>')
line(15.9, 8.6, 21.9, 8.6, 2); line(15.9, 8.68, 21.9, 8.68, 1)
sub(18.9, 9.25, 'STAIR DOWN · glass balustrade', 12, '#333')
# bedrooms 2-4
iwall(23.3, 8.45, 23.3, y1); iwall(23.3, 8.45, x1, 8.45); iwall(27.4, 8.45, 27.4, y1); iwall(31.5, 8.45, 31.5, y1)
for (a, b, da) in ((23.3, 27.4, 23.75), (27.4, 31.5, 27.85), (31.5, 35.8, 31.95)):
    iwall(b - 2.25, 8.45, b - 2.25, 10.7); iwall(b - 2.25, 10.7, b, 10.7)      # ensuite box
    door_h(da, 8.45, 0.9, 'l', 's')                                           # bedroom door from the corridor
    door_v(b - 2.25, 9.6, 0.8, 'b', 'w')                                      # ensuite door
iwall(34.2, y0, 34.2, 8.45); door_v(34.2, 7.2, 0.8, 't', 'w')                  # linen store
# fixed items
o.append(f'<ellipse cx="{X(9.75):.1f}" cy="{Y(8.5):.1f}" rx="{0.45*S:.1f}" ry="{0.95*S:.1f}" fill="#eee" stroke="{INK}" stroke-width="1.6"/>')
rect(10.9, 6.95, 2.2, 0.55, '#bbb', 'none')
# labels
txt(12.1, 12.7, 'PRIMARY', 18); txt(12.1, 13.45, 'BEDROOM', 18)
txt(11.95, 8.75, 'BATHROOM', 14); sub(11.95, 9.4, 'freestanding bath', 11)
txt(14.58, 7.75, 'DRESS-', 11); txt(14.58, 8.2, 'ING', 11)
txt(19.5, 11.9, 'LOUNGE', 20); sub(19.5, 12.6, 'open to the landing'); sub(19.5, 13.2, 'behind the lattice')
txt(22.6, 7.75, 'LAND-', 10); txt(22.6, 8.1, 'ING', 10)
sub(28.7, 7.75, 'CORRIDOR', 12, '#333'); txt(35.0, 7.9, 'LINEN', 9)
for i, (a, b) in enumerate(((23.3, 27.4), (27.4, 31.5), (31.5, 35.8))):
    txt((a + b) / 2, 12.9, f'BEDROOM {i + 2}', 15)
    txt(b - 1.12, 9.75, 'ENSUITE', 10)

# title, north, scale
o.append(f'<text x="70" y="78" font-size="38" letter-spacing=".3em" font-weight="300">CASA OMBRA</text>')
o.append(f'<text x="72" y="112" font-size="17" letter-spacing=".2em" fill="#555">FIRST FLOOR · SKETCH PLAN</text>')
o.append(f'<g transform="translate(2290,95)"><polygon points="0,-30 10,8 0,0 -10,8" fill="{INK}"/><text y="30" font-size="16" text-anchor="middle" font-weight="700">N</text></g>')
bx, by = 70, 1290
o.append(f'<line x1="{bx}" y1="{by}" x2="{bx + 10*S}" y2="{by}" stroke="{INK}" stroke-width="3"/>')
for i in (0, 5, 10): o.append(f'<line x1="{bx + i*S}" y1="{by-7}" x2="{bx + i*S}" y2="{by+7}" stroke="{INK}" stroke-width="2"/><text x="{bx + i*S}" y="{by+26}" font-size="14" text-anchor="middle">{i} m</text>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="background:#fff;font-family:Helvetica,Arial,sans-serif">'
       f'<rect width="{W}" height="{H}" fill="#fff"/>' + ''.join(o) + '</svg>')
open(sys.argv[1], 'w').write('<!doctype html><html><body style="margin:0">' + svg + '</body></html>')
