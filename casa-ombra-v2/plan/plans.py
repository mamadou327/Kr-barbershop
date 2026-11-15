"""Casa Ombra v2 - a simple, buildable house. Writes site+ground and first-floor sketch plans as HTML/SVG.
Coordinates in metres. X = east, Y = south (road side). Origin = NW corner of the house.

House:  ground floor  0..36 x 0..12   (north band y 0..5 is single storey, front zone y 5..12 under the box)
        first floor   0..36 x 5..15   (a long concrete box, 3 m overhang to the south = covered terrace)
"""
import sys

S, OX, OY = 30, 560, 230
W, H = 2400, 1350
INK, G, LAT, RED = '#111', '#9a9a9a', '#9a6a35', '#c0392b'


class P:
    def __init__(self): self.o = []
    def X(self, v): return OX + v * S
    def Y(self, v): return OY + v * S
    def add(self, s): self.o.append(s)

    def line(self, a, b, c, d, w=2, col=INK, dash=''):
        da = f'stroke-dasharray="{dash}"' if dash else ''
        self.add(f'<line x1="{self.X(a):.1f}" y1="{self.Y(b):.1f}" x2="{self.X(c):.1f}" y2="{self.Y(d):.1f}" stroke="{col}" stroke-width="{w}" {da} stroke-linecap="square"/>')
    def wall(self, a, b, c, d): self.line(a, b, c, d, 9)
    def iwall(self, a, b, c, d): self.line(a, b, c, d, 4.5)
    def glass(self, a, b, c, d): self.line(a, b, c, d, 7); self.line(a, b, c, d, 3.5, '#fff')
    def gap(self, a, b, c, d): self.line(a, b, c, d, 12, '#fff')
    def lattice(self, a, b, c, d): self.line(a, b, c, d, 7, LAT, '4 4')

    def rect(self, x, y, w, h, fill='none', st=INK, sw=1.5, dash='', rx=0):
        da = f'stroke-dasharray="{dash}"' if dash else ''
        self.add(f'<rect x="{self.X(x):.1f}" y="{self.Y(y):.1f}" width="{w*S:.1f}" height="{h*S:.1f}" rx="{rx}" fill="{fill}" stroke="{st}" stroke-width="{sw}" {da}/>')

    def txt(self, x, y, s, size=20, weight=700, col=INK, ls='.12em', anchor='middle'):
        self.add(f'<text x="{self.X(x):.1f}" y="{self.Y(y):.1f}" font-size="{size}" font-weight="{weight}" letter-spacing="{ls}" fill="{col}" text-anchor="{anchor}">{s}</text>')
    def sub(self, x, y, s, size=13, col='#555'): self.txt(x, y, s, size, 400, col, '.05em')

    def door_h(self, x0, y, wd, swing='s'):
        self.gap(x0, y, x0 + wd, y); sy = 1 if swing == 's' else -1
        self.line(x0, y, x0, y + sy * wd, 2)
        sweep = 0 if swing == 's' else 1
        self.add(f'<path d="M{self.X(x0):.1f} {self.Y(y + sy*wd):.1f} A {wd*S:.1f} {wd*S:.1f} 0 0 {sweep} {self.X(x0+wd):.1f} {self.Y(y):.1f}" fill="none" stroke="{INK}" stroke-width="1.1" stroke-dasharray="5 4"/>')
    def door_v(self, x, y0, wd, swing='e'):
        self.gap(x, y0, x, y0 + wd); sx = 1 if swing == 'e' else -1
        self.line(x, y0, x + sx * wd, y0, 2)
        sweep = 1 if swing == 'e' else 0
        self.add(f'<path d="M{self.X(x + sx*wd):.1f} {self.Y(y0):.1f} A {wd*S:.1f} {wd*S:.1f} 0 0 {sweep} {self.X(x):.1f} {self.Y(y0+wd):.1f}" fill="none" stroke="{INK}" stroke-width="1.1" stroke-dasharray="5 4"/>')

    def tree(self, x, y, r=1.3, col='#333'):
        self.add(f'<circle cx="{self.X(x):.1f}" cy="{self.Y(y):.1f}" r="{r*S:.1f}" fill="none" stroke="{col}" stroke-width="1.3" stroke-dasharray="3 3"/><circle cx="{self.X(x):.1f}" cy="{self.Y(y):.1f}" r="3.5" fill="{col}"/>')
    def car(self, x0, y0, x1, y1, label, col=INK):
        self.rect(x0, y0, x1 - x0, y1 - y0, '#fff', col, 1.8, rx=14)
        self.add(f'<text transform="translate({self.X((x0+x1)/2):.1f},{self.Y((y0+y1)/2):.1f}) rotate(-90)" font-size="13" font-weight="700" letter-spacing=".06em" text-anchor="middle" dy="5" fill="{col}">{label}</text>')
    def stair(self, x0, y0, x1, y1, n, arrow_from, arrow_to):
        self.rect(x0, y0, x1 - x0, y1 - y0, '#fff', INK, 1.5)
        for i in range(1, n): xx = x0 + (x1 - x0) * i / n; self.line(xx, y0, xx, y1, 1)
        ym = (y0 + y1) / 2
        self.add(f'<line x1="{self.X(arrow_from):.1f}" y1="{self.Y(ym):.1f}" x2="{self.X(arrow_to):.1f}" y2="{self.Y(ym):.1f}" stroke="{INK}" stroke-width="1.8" marker-end="url(#ah)"/>')

    def site(self, grey=False):
        c = '#999' if grey else '#444'
        self.rect(-2, -6, 42, 32, 'none', G, 2)                                  # boundary wall
        self.rect(-2, 26, 42, 3, '#f1f1f1', 'none'); self.txt(19, 27.9, 'ROAD', 14, 600, '#888')
        self.line(0, 26, 10, 26, 7, '#fff'); self.line(0, 26, 10, 26, 2, INK if not grey else G, '10 6'); self.sub(5, 25.5, 'SLIDING GATE', 12, c)
        self.rect(-1, 12, 13, 14, 'none', G, 1, '4 5'); self.txt(5.5, 23.3, 'FORECOURT', 15, 700, c); self.sub(5.5, 24.0, 'travertine', 12, c)
        self.rect(12, 12, 24, 3, '#f5f5f5', G, 1); self.sub(24, 13.85, 'COVERED TERRACE (under the first floor)', 12, c)
        self.rect(14, 16, 20, 4, '#d6d6d6' if not grey else '#ececec', INK if not grey else G, 1.8)
        self.txt(24, 18.3, 'POOL', 16, 700, '#333' if not grey else '#999'); self.sub(24, 19.0, '20 x 4 m · black stone', 12, c)
        for tx in (13.0, 35.0): self.rect(tx - 1.2, 16.8, 2.4, 2.4, '#fff', G, 1); self.tree(tx, 18.0, 1.15, '#555' if not grey else '#aaa')
        self.rect(12, 20.6, 28, 5.4, 'none', G, 1, '3 4'); self.sub(23.5, 25.4, 'LAWN · three olive trees', 12, c)
        for tx in (20, 27, 34): self.tree(tx, 23.0, 1.3, '#555' if not grey else '#aaa')
        self.rect(-2, -6, 42, 6, 'none', G, 1, '3 4'); self.txt(19, -3.2, 'REAR GARDEN', 14, 700, c)
        for tx in (4, 12, 26, 34): self.tree(tx, -3.0, 1.1, '#777' if not grey else '#bbb')
        self.tree(-0.6, 15.5, 0.9, '#777' if not grey else '#bbb'); self.tree(-0.6, 20.0, 0.9, '#777' if not grey else '#bbb')

    def frame(self, title):
        self.add(f'<text x="70" y="78" font-size="38" letter-spacing=".3em" font-weight="300">CASA OMBRA</text>')
        self.add(f'<text x="72" y="112" font-size="17" letter-spacing=".2em" fill="#555">{title}</text>')
        self.add(f'<g transform="translate(2290,95)"><polygon points="0,-30 10,8 0,0 -10,8" fill="{INK}"/><text y="30" font-size="16" text-anchor="middle" font-weight="700">N</text></g>')
        bx, by = 70, 1290
        self.add(f'<line x1="{bx}" y1="{by}" x2="{bx + 10*S}" y2="{by}" stroke="{INK}" stroke-width="3"/>')
        for i in (0, 5, 10): self.add(f'<line x1="{bx + i*S}" y1="{by-7}" x2="{bx + i*S}" y2="{by+7}" stroke="{INK}" stroke-width="2"/><text x="{bx + i*S}" y="{by+26}" font-size="14" text-anchor="middle">{i} m</text>')

    def write(self, path):
        defs = f'<defs><marker id="ah" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="{INK}"/></marker>' \
               f'<pattern id="gr" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="0.9" fill="#c4c4c4"/><circle cx="5.5" cy="5.5" r="0.9" fill="#c4c4c4"/></pattern></defs>'
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="background:#fff;font-family:Helvetica,Arial,sans-serif">{defs}<rect width="{W}" height="{H}" fill="#fff"/>' + ''.join(self.o) + '</svg>'
        open(path, 'w').write('<!doctype html><html><body style="margin:0">' + svg + '</body></html>')


def ground(path):
    p = P(); p.site()
    p.rect(0, 0, 36, 12, '#fff', 'none')
    # outer walls
    p.wall(0, 0, 36, 0); p.wall(0, 0, 0, 12); p.wall(36, 0, 36, 12)
    p.wall(0, 12, 0.4, 12); p.glass(0.4, 12, 8.6, 12); p.wall(8.6, 12, 9, 12)       # garage glass front
    p.glass(9, 12, 36, 12)                                                            # hall + living/dining/kitchen glass
    p.glass(36, 5.6, 36, 11.4)                                                        # east glass end
    # garage | hall glass wall
    p.iwall(9, 0, 9, 5); p.glass(9, 5, 9, 12); p.door_v(9, 9.6, 1.0, 'e')
    # north band y 0..5
    p.iwall(9, 5, 15, 5); p.iwall(15, 0, 15, 5)
    p.iwall(11.0, 0, 11.0, 5)
    p.iwall(15, 5, 36, 5)
    p.iwall(24, 0, 24, 5); p.iwall(28, 0, 28, 5); p.iwall(31, 0, 31, 5)
    p.door_h(9.8, 5, 0.8, 'n'); p.door_h(11.15, 5, 0.75, 'n')                         # WC, coats (under the high end of the stair)
    p.door_h(19, 5, 1.0, 'n'); p.door_h(24.6, 5, 0.9, 'n'); p.door_h(28.6, 5, 0.9, 'n')
    p.door_v(31, 1.6, 0.9, 'e')                                                       # utility -> gym
    p.gap(33.8, 0, 35.4, 0); p.line(33.8, 0, 35.4, 0, 3, INK)                         # gym door to rear garden
    # front door (south glass, faces the forecourt side)
    p.gap(10.3, 12, 12.1, 12)
    p.add(f'<line x1="{p.X(10.55):.1f}" y1="{p.Y(12.55):.1f}" x2="{p.X(11.85):.1f}" y2="{p.Y(11.45):.1f}" stroke="{INK}" stroke-width="5"/>')
    p.add(f'<line x1="{p.X(11.2):.1f}" y1="{p.Y(14.6):.1f}" x2="{p.X(11.2):.1f}" y2="{p.Y(12.9):.1f}" stroke="{INK}" stroke-width="2.2" marker-end="url(#ah)"/>')
    p.txt(11.2, 15.4, 'FRONT DOOR', 13, 700)
    # stair along the back of the hall, rising east
    p.stair(9.6, 5.25, 15.0, 6.45, 18, 14.7, 10.0); p.sub(12.3, 7.1, 'FLOATING STAIR · UP', 12, '#333')
    # fixed items
    p.rect(0.5, 0.4, 8.0, 0.35, '#bbb', 'none')
    p.rect(20.6, 5.2, 3.0, 0.45, '#333', 'none')                                     # fireplace on back wall
    p.rect(30.0, 5.2, 5.6, 0.75, '#bbb', 'none'); p.rect(30.6, 7.6, 4.2, 1.2, '#eee')  # kitchen run + island
    p.rect(24.4, 8.4, 4.2, 1.1, 'none', '#999', 1)                                    # dining table hint
    p.rect(16.2, 0.5, 6.6, 0.25, '#333', 'none')                                      # cinema screen
    # cars
    p.car(1.4, 4.8, 3.6, 9.8, 'SVJ'); p.car(5.2, 4.6, 7.3, 9.6, 'SF90')
    p.car(1.6, 16.0, 3.5, 20.9, 'M3 CS'); p.car(5.0, 15.9, 7.1, 21.0, 'URUS')
    # labels
    p.txt(4.5, 2.6, 'GARAGE', 18); p.sub(4.5, 3.3, 'glass front + glass wall to hall', 11)
    p.txt(10.0, 2.3, 'WC', 13); p.txt(13.0, 2.3, 'COATS', 12)
    p.txt(12.2, 9.4, 'ENTRANCE', 15); p.txt(12.2, 10.1, 'HALL', 15)
    p.txt(19.5, 2.4, 'CINEMA', 17); p.sub(19.5, 3.1, '8 seats', 12)
    p.txt(26, 2.4, 'PANTRY', 12); p.txt(29.5, 2.4, 'UTILITY', 12); p.txt(33.5, 2.4, 'GYM', 15); p.sub(33.5, 3.1, 'door to garden', 11)
    p.txt(19.5, 9.4, 'LIVING', 18); p.sub(22.1, 6.25, 'fire', 11)
    p.txt(26.5, 11.4, 'DINING', 15); p.txt(32.7, 10.6, 'KITCHEN', 15)
    p.rect(0, 5, 36, 10, 'none', RED, 2, '14 9'); p.add(f'<text x="{p.X(35.8):.1f}" y="{p.Y(15) + 18:.1f}" font-size="12" font-weight="700" letter-spacing=".06em" fill="{RED}" text-anchor="end">FIRST FLOOR ABOVE (red dashed)</text>')
    p.frame('SITE + GROUND FLOOR · SKETCH PLAN'); p.write(path)


def first(path):
    p = P(); p.site(grey=True)
    # ground floor below
    p.rect(0, 0, 36, 5, 'url(#gr)', G, 2); p.sub(7, 2.6, 'flat roof (garage + services below)', 12, '#888'); p.sub(26, 2.6, 'flat roof (cinema · pantry · utility · gym below)', 12, '#888')
    p.car(1.6, 16.0, 3.5, 20.9, 'M3 CS', G); p.car(5.0, 15.9, 7.1, 21.0, 'URUS', G)
    # box
    p.rect(0, 5, 36, 10, '#fff', 'none')
    p.wall(0, 5, 36, 5); p.wall(36, 5, 36, 15); p.wall(0, 5, 0, 15)
    for a, b in ((3, 7), (14, 16), (20, 22), (26.5, 28.5), (32.5, 34.5)): p.glass(a, 5, b, 5)   # corridor windows north
    p.wall(0, 15, 0.4, 15); p.glass(0.4, 15, 35.6, 15); p.wall(35.6, 15, 36, 15)
    p.glass(0, 7.5, 0, 14.4)
    p.lattice(0.6, 15.42, 35.4, 15.42); p.lattice(-0.42, 7.5, -0.42, 14.4)
    p.add(f'<text x="{p.X(18):.1f}" y="{p.Y(16.25):.1f}" font-size="13" font-weight="700" letter-spacing=".08em" fill="{LAT}" text-anchor="middle">TIMBER LATTICE SCREEN (brown) · ALL ROOMS FACE THE POOL</text>')
    # corridor y 5..7.4 (stair void sits in it, glass balustrade on its south side)
    CY = 7.4
    p.iwall(0, CY, 9.0, CY); p.iwall(10.1, CY, 13, CY); p.iwall(17, CY, 36, CY)
    p.door_h(9.05, CY, 1.0, 's')                                     # into the primary suite
    # primary suite 0..13
    p.iwall(13, CY, 13, 15)
    p.iwall(0, 10.9, 5.5, 10.9); p.iwall(5.5, CY, 5.5, 10.9)        # bathroom
    p.iwall(8.5, CY, 8.5, 10.9)                                     # dressing 5.5..8.5
    p.door_v(5.5, 9.7, 0.9, 'w'); p.gap(5.7, 10.9, 8.3, 10.9)
    # stair void (top at the west end) + balustrade
    p.stair(9.6, 5.25, 15.0, 6.45, 18, 10.0, 14.7); p.sub(12.3, 7.15, 'STAIR DOWN · glass balustrade', 11, '#333')
    p.line(9.6, 6.6, 15.0, 6.6, 2); p.line(15.0, 5.25, 15.0, 6.6, 2)
    # lounge 13..17, open to the corridor
    p.iwall(17, CY, 17, 15)
    # bedrooms 17..36, three of 6.33 m
    xs = [17, 23.33, 29.67, 36]
    for i in range(3):
        a, b = xs[i], xs[i + 1]
        if i > 0: p.iwall(a, CY, a, 15)
        p.iwall(b - 2.6, CY, b - 2.6, 10.0); p.iwall(b - 2.6, 10.0, b, 10.0)
        p.door_h(a + 0.4, CY, 0.9, 's'); p.door_v(b - 2.6, 8.7, 0.8, 'e')
        p.txt((a + b) / 2 - 0.4, 12.8, f'BEDROOM {i + 2}', 14); p.txt(b - 1.3, 8.9, 'ENSUITE', 9)
    # fixed items
    p.add(f'<ellipse cx="{p.X(2.6):.1f}" cy="{p.Y(9.0):.1f}" rx="{1.0*S:.1f}" ry="{0.5*S:.1f}" fill="#eee" stroke="{INK}" stroke-width="1.5"/>')
    p.rect(9.9, 11.6, 2.3, 2.4, 'none', '#999', 1)
    # labels
    p.txt(5.6, 13.4, 'PRIMARY SUITE', 16); p.txt(2.8, 10.3, 'BATH', 12); p.txt(7.0, 9.2, 'DRESSING', 10)
    p.txt(15.0, 11.2, 'LOUNGE', 14); p.sub(15.0, 11.9, 'open to the corridor', 11)
    p.sub(26, 6.4, 'CORRIDOR · windows to the rear garden', 12, '#333')
    p.frame('FIRST FLOOR · SKETCH PLAN'); p.write(path)


if __name__ == '__main__':
    out = sys.argv[1]
    ground(out + '/ground.html'); first(out + '/first.html')
