"""Casa Ombra ground-floor sketch -> SVG. Geometry measured from the bird's-eye photo (see model2.py)."""
import sys

S, OX, OY = 36, 483, 300
W, H = 2400, 1350
INK = '#111'
o = []

def X(v): return OX + v * S
def Y(v): return OY + v * S

def line(a, b, c, d, w=2, col=INK, dash=''):
    o.append(f'<line x1="{X(a):.1f}" y1="{Y(b):.1f}" x2="{X(c):.1f}" y2="{Y(d):.1f}" stroke="{col}" stroke-width="{w}" '
             f'{"stroke-dasharray=" + chr(34) + dash + chr(34) if dash else ""} stroke-linecap="square"/>')

def wall(a, b, c, d): line(a, b, c, d, 10)
def iwall(a, b, c, d): line(a, b, c, d, 5)

def glass(a, b, c, d):
    line(a, b, c, d, 8, INK)
    line(a, b, c, d, 4, '#fff')

def rect(x, y, w, h, fill='none', st=INK, sw=1.5, dash='', rx=0):
    o.append(f'<rect x="{X(x):.1f}" y="{Y(y):.1f}" width="{w*S:.1f}" height="{h*S:.1f}" rx="{rx}" fill="{fill}" stroke="{st}" stroke-width="{sw}" '
             f'{"stroke-dasharray=" + chr(34) + dash + chr(34) if dash else ""}/>')

def poly(pts, fill='none', st=INK, sw=1.5, dash=''):
    p = ' '.join(f'{X(x):.1f},{Y(y):.1f}' for x, y in pts)
    o.append(f'<polygon points="{p}" fill="{fill}" stroke="{st}" stroke-width="{sw}" {"stroke-dasharray=" + chr(34) + dash + chr(34) if dash else ""}/>')

def txt(x, y, s, size=22, weight=700, col=INK, ls='.12em', anchor='middle'):
    o.append(f'<text x="{X(x):.1f}" y="{Y(y):.1f}" font-size="{size}" font-weight="{weight}" letter-spacing="{ls}" fill="{col}" text-anchor="{anchor}">{s}</text>')

def sub(x, y, s, size=14, col='#555'): txt(x, y, s, size, 400, col, '.06em')

def gap(a, b, c, d):
    """white-out a door opening in a wall"""
    line(a, b, c, d, 13, '#fff')

def door_h(x0, y, wd, hinge='l', swing='s'):
    """door in a horizontal wall at y, opening from x0 to x0+wd; hinge left/right; swings south (+y) or north (-y)"""
    gap(x0, y, x0 + wd, y)
    hx = x0 if hinge == 'l' else x0 + wd
    ex = x0 + wd if hinge == 'l' else x0
    sy = 1 if swing == 's' else -1
    line(hx, y, hx, y + sy * wd, 2)
    sweep = 1 if (hinge == 'l') == (swing == 'n') else 0
    o.append(f'<path d="M{X(hx):.1f} {Y(y + sy*wd):.1f} A {wd*S:.1f} {wd*S:.1f} 0 0 {1 - sweep} {X(ex):.1f} {Y(y):.1f}" fill="none" stroke="{INK}" stroke-width="1.1" stroke-dasharray="5 4"/>')

def door_v(x, y0, wd, hinge='t', swing='e'):
    """door in a vertical wall at x, opening from y0 to y0+wd; hinge top/bottom; swings east (+x) or west (-x)"""
    gap(x, y0, x, y0 + wd)
    hy = y0 if hinge == 't' else y0 + wd
    ey = y0 + wd if hinge == 't' else y0
    sx = 1 if swing == 'e' else -1
    line(x, hy, x + sx * wd, hy, 2)
    sweep = 1 if (hinge == 't') == (swing == 'e') else 0
    o.append(f'<path d="M{X(x + sx*wd):.1f} {Y(hy):.1f} A {wd*S:.1f} {wd*S:.1f} 0 0 {sweep} {X(x):.1f} {Y(ey):.1f}" fill="none" stroke="{INK}" stroke-width="1.1" stroke-dasharray="5 4"/>')

def tree(x, y, r):
    o.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="{r*S:.1f}" fill="none" stroke="#333" stroke-width="1.3" stroke-dasharray="3 3"/>'
             f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="4" fill="#333"/>')

def car(x0, y0, x1, y1, label):
    rect(x0, y0, x1 - x0, y1 - y0, '#fff', INK, 1.8, rx=16)
    o.append(f'<text transform="translate({X((x0+x1)/2):.1f},{Y((y0+y1)/2):.1f}) rotate(-90)" font-size="14" font-weight="700" letter-spacing=".08em" text-anchor="middle" dy="5">{label}</text>')

# ---------- site (light) ----------
G = '#9a9a9a'
poly([(-3.15, -4.6), (42.5, -4.6), (42.5, 26.0), (-3.15, 26.0)], 'none', G, 2)                 # plot boundary walls
rect(-3.15, 26.0, 45.65, 2.6, '#f1f1f1', 'none')                                              # road
txt(24, 27.7, 'ROAD', 15, 600, '#888')
line(-0.8, 26.0, 6.9, 26.0, 7, '#fff'); line(-0.8, 26.0, 6.9, 26.0, 2, INK, '10 6'); sub(3.05, 25.5, 'SLIDING GATE')
# forecourt
txt(1.6, 20.3, 'FORECOURT', 18, 700, '#444'); sub(1.6, 21.1, 'travertine')
for ty in (11.5, 16.5, 21.5): tree(-1.9, ty, 1.0)
# pool + terrace
poly([(7.7, 10.5), (11.7, 10.5), (11.7, 14.6), (27.9, 14.6), (27.9, 19.35), (7.7, 19.35)], '#dcdcdc', INK, 2)
for cx in (14.9, 24.2):
    rect(cx - 1.5, 15.5, 3, 3, '#fff'); tree(cx, 17.0, 1.25)
txt(19.5, 17.0, 'REFLECTING POOL', 17, 700, '#333'); sub(19.5, 17.8, 'black stone · two olive islands')
poly([(11.3, 7.0), (13.5, 7.0), (13.5, 12.7), (30.2, 12.7), (30.2, 14.6), (11.7, 14.6), (11.7, 10.5), (11.3, 10.5)], '#f6f6f6', G, 1.2)
sub(21.5, 13.85, 'COVERED TERRACE (under the first floor)')
# steps up from the forecourt
rect(9.6, 7.2, 1.7, 3.2, '#fff', INK, 1.5)
for i in range(1, 4): line(9.6 + 1.7 * i / 4, 7.2, 9.6 + 1.7 * i / 4, 10.4, 1.2)
sub(7.5, 8.55, 'LIT'); sub(7.5, 9.1, 'STEPS'); sub(7.5, 9.65, 'up'); o.append(f'<line x1="{X(9.75)}" y1="{Y(8.8)}" x2="{X(11.1)}" y2="{Y(8.8)}" stroke="{INK}" stroke-width="1.6" marker-end="url(#ah)"/>')
# garden south of the pool
rect(7.7, 19.35, 22.5, 2.45, 'none', G, 1, '3 4'); rect(7.7, 21.8, 22.5, 1.2, '#f6f6f6', G, 1); rect(7.7, 23.0, 34.8, 3.0, 'none', G, 1, '3 4')
sub(19, 20.75, 'planted terrace · boulders'); sub(19, 22.6, 'GARDEN WALK'); sub(24, 24.7, 'planting · olive trees')
rect(27.9, 14.6, 2.3, 7.2, '#f6f6f6', G, 1)
for (sx, sy) in ((31.5, 19.6), (33.4, 20.6), (35.2, 19.9), (37.0, 21.2), (38.6, 20.2), (33.0, 22.2), (36.0, 22.9)): rect(sx, sy, 1.2, 0.8, '#fff', G, 1, rx=6)
sub(36.2, 24.3, 'STEPPING-STONE LAWN'); tree(39.6, 23.0, 1.1); tree(40.3, 16.5, 1.2); tree(39.8, 10.5, 1.2)
# rear garden
txt(26, -2.2, 'REAR LAWN', 17, 700, '#444'); rect(37.6, -4.0, 4.3, 3.6, '#f6f6f6', G, 1.2); sub(39.75, -2.4, 'SUNKEN'); sub(39.75, -1.7, 'LOUNGE')
for sy in (-3.0, -1.2, 0.6, 2.4, 4.2): rect(-2.2, sy, 1.1, 0.8, '#fff', G, 1, rx=6)
tree(9, -2.6, 1.0); tree(19, -3.0, 1.0); tree(33, -2.8, 1.0)
# first-floor box above
rect(8.4, 6.6, 27.4, 8.6, 'none', '#c0392b', 2, '14 9')
txt(22.1, 16.0 - 0.35, '', 13)
FF_LABEL = f'<text x="{X(29.9):.1f}" y="{Y(6.25):.1f}" font-size="13" font-weight="700" letter-spacing=".08em" fill="#c0392b" text-anchor="end">FIRST FLOOR ABOVE (red dashed line)</text>'

# ---------- building ----------
# room fills
rect(0, 0, 16.75, 7.0, '#fff', 'none'); rect(13.5, 7.0, 16.7, 5.7, '#fff', 'none'); rect(30.2, 7.0, 6.6, 10.9, '#fff', 'none')
# exterior walls
wall(0, 0, 16.75, 0); wall(0, 0, 0, 7.0); wall(16.75, 0, 16.75, 7.0)
wall(0, 7.0, 0.3, 7.0); glass(0.3, 7.0, 6.7, 7.0); wall(6.7, 7.0, 13.5, 7.0)
wall(16.75, 7.0, 30.2, 7.0); glass(23.9, 7.0, 26.4, 7.0); glass(27.5, 7.0, 29.6, 7.0)
glass(13.5, 7.0, 13.5, 12.7); glass(13.5, 12.7, 30.2, 12.7)
wall(30.2, 12.7, 30.2, 17.9); wall(30.2, 17.9, 36.8, 17.9); glass(32.6, 17.9, 35.0, 17.9); wall(36.8, 17.9, 36.8, 7.0); wall(36.8, 7.0, 30.2, 7.0)
# garage | cinema | gallery
iwall(7.3, 0, 7.3, 4.1); glass(7.3, 4.1, 7.3, 7.0)
iwall(7.3, 4.1, 13.15, 4.1); iwall(13.15, 0, 13.15, 4.1)
iwall(13.15, 2.0, 16.75, 2.0); iwall(14.95, 0, 14.95, 2.0)
# shared wall low block / pavilion with the opening
iwall(13.5, 7.0, 13.8, 7.0); iwall(15.5, 7.0, 16.75, 7.0); gap(13.85, 7.0, 15.45, 7.0)
# pavilion | leisure wing
iwall(30.2, 7.0, 30.2, 12.7)
iwall(30.2, 9.4, 36.8, 9.4); iwall(33.6, 7.0, 33.6, 9.4); iwall(32.6, 9.4, 32.6, 12.4); iwall(34.7, 9.4, 34.7, 12.4); iwall(32.6, 12.4, 36.8, 12.4)
# doors
door_v(7.3, 5.5, 1.0, 't', 'e')                 # garage <-> gallery (glass door)
door_h(11.4, 4.1, 0.95, 'l', 'n')               # cinema
door_h(13.55, 2.0, 0.85, 'l', 'n'); door_h(15.4, 2.0, 0.85, 'l', 'n')   # WC, coats
door_v(30.2, 7.5, 0.9, 't', 'e'); door_v(30.2, 11.45, 0.9, 'b', 'e')    # pantry, spa
door_v(33.6, 7.8, 0.85, 't', 'e')               # plant
door_h(33.2, 12.4, 0.8, 'l', 'n'); door_h(35.3, 12.4, 0.8, 'l', 'n')    # sauna, steam
door_v(30.2, 13.3, 1.0, 't', 'e')               # spa -> terrace
# front door: glass pivot in the west glass face
gap(13.5, 8.0, 13.5, 9.6)
o.append(f'<line x1="{X(13.5 - 0.55):.1f}" y1="{Y(8.25):.1f}" x2="{X(13.5 + 0.9):.1f}" y2="{Y(9.45):.1f}" stroke="{INK}" stroke-width="5"/>')
o.append(f'<line x1="{X(11.55)}" y1="{Y(8.8)}" x2="{X(12.75)}" y2="{Y(8.8)}" stroke="{INK}" stroke-width="2.2" marker-end="url(#ah)"/>')
o.append(f'<text x="{X(12.4):.1f}" y="{Y(7.75):.1f}" font-size="13" font-weight="700" letter-spacing=".06em" text-anchor="middle">FRONT</text>')
o.append(f'<text x="{X(12.4):.1f}" y="{Y(8.2):.1f}" font-size="13" font-weight="700" letter-spacing=".06em" text-anchor="middle">DOOR</text>')
# stair
rect(15.9, 7.3, 6.0, 1.15, '#fff', INK, 1.5)
for i in range(1, 20): line(15.9 + 6.0 * i / 20, 7.3, 15.9 + 6.0 * i / 20, 8.45, 1)
o.append(f'<line x1="{X(16.2)}" y1="{Y(7.875)}" x2="{X(21.6)}" y2="{Y(7.875)}" stroke="{INK}" stroke-width="1.8" marker-end="url(#ah)"/>')
sub(18.9, 9.0, 'FLOATING STAIR · UP', 13, '#333')
# fixed items
rect(0.6, 0.35, 6.3, 0.35, '#bbb', 'none')
rect(14.05, 2.7, 1.8, 1.8, '#f0f0f0'); tree(14.95, 3.6, 0.75); rect(13.6, 2.35, 2.7, 2.5, 'none', INK, 1.1, '8 5')
rect(23.45, 8.9, 0.4, 2.4, '#333', 'none')
rect(27.9, 8.7, 1.1, 2.9, '#eee'); rect(29.5, 8.75, 0.55, 2.5, '#bbb', 'none'); rect(27.25, 7.2, 2.3, 0.6, '#bbb', 'none')
rect(31.0, 13.2, 2.2, 4.0, '#dcdcdc', INK, 1.8)
for i in range(1, 4): line(31.0, 13.2 + 0.3 * i, 33.2, 13.2 + 0.3 * i, 1)
# cars
car(0.9, 1.65, 3.0, 6.55, 'SVJ'); car(4.0, 1.8, 6.0, 6.5, 'SF90')
car(1.7, 11.0, 3.6, 15.9, 'M3 CS'); car(4.2, 10.9, 6.3, 16.0, 'URUS')
# labels
txt(3.65, 3.9 - 4.6 + 4.2, '', 1)
o.append(f'<text x="{X(3.65):.1f}" y="{Y(6.75):.1f}" font-size="0"></text>')
txt(3.65, 1.4, 'GARAGE', 19); sub(3.5, 7.65, 'glass front', 12); o.append(FF_LABEL)
txt(10.2, 2.0, 'CINEMA'); sub(10.2, 2.75, '6 seats')
txt(10.25, 5.5, 'GALLERY', 18); sub(10.25, 6.2, 'glass wall onto the cars', 12)
txt(14.05, 0.9, 'WC', 13); txt(15.85, 0.9, 'COATS', 11)
sub(14.95, 5.35, 'OLIVE · SKYLIGHT', 12, '#333'); txt(14.95, 6.2, 'LOBBY', 15)
txt(15.2, 10.6, 'ENTRANCE', 17); txt(15.2, 11.35, 'HALL', 17)
txt(20.4, 10.9, 'LIVING'); txt(25.65, 10.9, 'DINING'); txt(28.45, 12.3, 'KITCHEN', 15)
sub(22.55, 10.2, 'fire', 12)
txt(31.9, 8.4, 'PANTRY', 13); txt(35.2, 8.4, 'PLANT', 13)
txt(31.4, 10.8, 'SHOWER', 12); txt(33.65, 11.1, 'SAUNA', 12); txt(35.75, 11.1, 'STEAM', 12)
txt(34.95, 14.6, 'SPA', 20); sub(34.95, 15.35, 'plunge pool'); sub(34.95, 15.95, 'loungers')
sub(33.8, 18.75, 'door to garden', 12)

# title, north, scale
o.append(f'<text x="70" y="78" font-size="38" letter-spacing=".3em" font-weight="300">CASA OMBRA</text>')
o.append(f'<text x="72" y="112" font-size="17" letter-spacing=".2em" fill="#555">GROUND FLOOR · SKETCH PLAN</text>')
o.append(f'<g transform="translate(2290,95)"><polygon points="0,-30 10,8 0,0 -10,8" fill="{INK}"/><text y="30" font-size="16" text-anchor="middle" font-weight="700">N</text></g>')
bx, by = 70, 1290
o.append(f'<line x1="{bx}" y1="{by}" x2="{bx + 10*S}" y2="{by}" stroke="{INK}" stroke-width="3"/>')
for i in (0, 5, 10): o.append(f'<line x1="{bx + i*S}" y1="{by-7}" x2="{bx + i*S}" y2="{by+7}" stroke="{INK}" stroke-width="2"/><text x="{bx + i*S}" y="{by+26}" font-size="14" text-anchor="middle">{i} m</text>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="background:#fff;font-family:Helvetica,Arial,sans-serif">'
       f'<defs><marker id="ah" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="{INK}"/></marker></defs>'
       f'<rect width="{W}" height="{H}" fill="#fff"/>' + ''.join(o) + '</svg>')
open(sys.argv[1], 'w').write('<!doctype html><html><body style="margin:0">' + svg + '</body></html>')
