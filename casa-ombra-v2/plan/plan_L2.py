"""Casa Ombra L2 - single-storey L-shaped house following the user's AutoDraw sketch.
Metres. X = east, Y = south. Origin = NW corner of the house. Road along the SOUTH.

Main arm x 0..45,  y 0..11   (garage at the west end, living spaces facing the pool)
East arm x 33..45, y 11..28  (bedrooms facing west onto the pool, corridor on the outside)
Pool in the corner between the two arms; forecourt in front of the garage.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import plans as base

base.S, base.OX, base.OY = 26, 578, 326
INK, G, LAT, RED = base.INK, base.G, base.LAT, base.RED


def draw(path):
    p = base.P(); S = base.S
    # ---------------- site ----------------
    p.rect(-3, 31, 51, 3, '#f1f1f1', 'none'); p.txt(22.5, 32.9, 'ROAD', 14, 600, '#888')
    p.rect(-3, -6, 51, 37, 'none', G, 2)
    p.line(-1.5, 31, 9, 31, 7, '#fff'); p.line(-1.5, 31, 9, 31, 2, INK, '10 6'); p.sub(3.75, 30.4, 'SLIDING GATE', 11)
    # forecourt
    p.rect(-2.5, 13, 13, 17.5, 'none', G, 1, '4 5'); p.txt(4, 27.6, 'FORECOURT', 15); p.sub(4, 28.3, 'travertine', 11)
    p.car(-0.6, 15.6, 1.6, 20.6, 'M3 CS'); p.car(2.6, 15.5, 4.9, 20.7, 'URUS')
    p.line(10.5, 13.6, 10.5, 30.5, 6, '#bbb'); p.sub(10.0, 24, '', 10)
    p.add(f'<text transform="translate({p.X(11.1):.1f},{p.Y(24.5):.1f}) rotate(-90)" font-size="10" letter-spacing=".05em" fill="#666" text-anchor="middle">LOW TRAVERTINE WALL + OLIVES</text>')
    for ty in (16, 21.5, 27): p.tree(9.2, ty, 0.9, '#666')
    # covered walkway / terraces under the roof overhang
    p.rect(-0.5, 11, 33.5, 2.4, '#f4f4f4', G, 1); p.sub(22, 12.5, 'COVERED TERRACE (roof overhang)', 11)
    p.rect(30.6, 13.4, 2.4, 14.6, '#f4f4f4', G, 1)
    p.add(f'<text transform="translate({p.X(31.85):.1f},{p.Y(21):.1f}) rotate(-90)" font-size="10" letter-spacing=".05em" fill="#555" text-anchor="middle">COVERED TERRACE</text>')
    # pool + olives + lawn
    p.rect(12.5, 15.5, 16.5, 7, '#d6d6d6', INK, 1.8); p.txt(20.75, 19.2, 'POOL', 17, 700, '#333'); p.sub(20.75, 20.0, '16.5 x 7 m · black stone', 11)
    for (tx, ty) in ((14.2, 24.6), (27.2, 24.6)): p.rect(tx - 1.2, ty - 1.2, 2.4, 2.4, '#fff', G, 1); p.tree(tx, ty, 1.1, '#555')
    p.rect(11.3, 26.4, 19.1, 4.1, 'none', G, 1, '3 4'); p.rect(30.4, 28.4, 17.1, 2.1, 'none', G, 1, '3 4'); p.sub(22, 28.9, 'LAWN · olive trees', 11)
    p.tree(18.5, 28.4, 1.2, '#555'); p.tree(26.5, 28.6, 1.1, '#555')
    # rear garden
    p.rect(-2.5, -5.5, 50, 5.5, 'none', G, 1, '3 4'); p.txt(22.5, -2.4, 'REAR GARDEN', 13, 700, '#444')
    for tx in (4, 12, 31, 39): p.tree(tx, -3, 1.0, '#777')

    # ---------------- house ----------------
    p.rect(0, 0, 45, 11, '#fff', 'none'); p.rect(33, 11, 12, 17, '#fff', 'none')
    p.wall(0, 0, 45, 0); p.wall(45, 0, 45, 28); p.wall(33, 28, 45, 28); p.wall(0, 0, 0, 11)
    # south face of the main arm
    p.wall(0, 11, 0.4, 11); p.glass(0.4, 11, 10.6, 11); p.wall(10.6, 11, 11, 11)       # garage glass
    p.wall(11, 11, 12.0, 11); p.wall(13.8, 11, 16, 11)                                    # hall: solid + front door gap
    p.glass(16, 11, 33, 11)                                                               # kitchen / dining / living glass to the pool
    # west face of the east arm
    p.glass(33, 11, 33, 27.6); p.wall(33, 27.6, 33, 28)
    p.lattice(32.55, 11.6, 32.55, 27.4)
    # rear windows
    p.glass(26, 0, 32.5, 0)                                                                # living to the rear garden
    p.glass(45, 13, 45, 15); p.glass(45, 19, 45, 21); p.glass(45, 24.5, 45, 26.5)          # corridor windows (east)
    p.glass(36, 28, 42, 28)                                                                # primary suite to the south lawn
    # front door
    p.gap(12.0, 11, 13.8, 11)
    p.add(f'<line x1="{p.X(12.2):.1f}" y1="{p.Y(11.55):.1f}" x2="{p.X(13.6):.1f}" y2="{p.Y(10.45):.1f}" stroke="{INK}" stroke-width="5"/>')
    p.add(f'<line x1="{p.X(7.5):.1f}" y1="{p.Y(12.3):.1f}" x2="{p.X(11.6):.1f}" y2="{p.Y(12.3):.1f}" stroke="{INK}" stroke-width="2.2" marker-end="url(#ah)"/>')
    p.txt(12.9, 14.3, 'FRONT DOOR', 11)
    # garage | hall: glass wall + door
    p.glass(11, 0, 11, 11); p.door_v(11, 7.6, 1.0, 'w')
    # hall | services/kitchen
    p.iwall(16, 0, 16, 4.2)
    # services strip y 0..4.2 : WC | pantry | utility, then cinema
    p.iwall(16, 4.2, 25.5, 4.2); p.iwall(18.6, 0, 18.6, 4.2); p.iwall(22, 0, 22, 4.2); p.iwall(25.5, 0, 25.5, 4.2)
    p.door_h(16.6, 4.2, 0.8, 'n'); p.door_h(19.2, 4.2, 0.9, 'n'); p.door_h(22.8, 4.2, 0.9, 'n')
    # corner block: cinema | gym, gallery to the bedroom wing
    p.iwall(33, 0, 33, 7); p.iwall(33, 7, 45, 7); p.iwall(40, 0, 40, 7)
    p.door_h(34, 7, 1.0, 'n'); p.door_h(41, 7, 0.9, 'n')
    p.gap(33, 7.6, 33, 10.6)                                                               # living -> gallery opening
    # east arm: corridor x 43..45, rooms x 33..43
    p.iwall(43, 11, 43, 28); p.iwall(33, 11, 43, 11)
    p.gap(43.2, 11, 44.8, 11)
    for (y0, y1, name) in ((11, 16.5, 'BEDROOM 2'), (16.5, 22, 'BEDROOM 3')):
        p.iwall(33, y1, 43, y1)
        p.iwall(40.2, y0, 40.2, y0 + 3.0); p.iwall(40.2, y0 + 3.0, 43, y0 + 3.0)       # ensuite box against the corridor
        p.door_v(43, y0 + 3.5, 0.9, 'w'); p.door_v(40.2, y0 + 0.6, 0.8, 'w')
        p.txt(36.4, (y0 + y1) / 2 + 0.9, name, 12); p.txt(41.6, y0 + 1.8, 'ENSUITE', 8)
    # primary suite y 22..28: bath + dressing against the corridor
    p.iwall(39.5, 22, 39.5, 28); p.iwall(39.5, 25, 43, 25)
    p.door_v(43, 22.6, 0.9, 'w'); p.door_v(39.5, 25.6, 0.9, 'w'); p.door_v(39.5, 22.5, 0.9, 'w')
    p.add(f'<ellipse cx="{p.X(41.3):.1f}" cy="{p.Y(26.6):.1f}" rx="{0.95*S:.1f}" ry="{0.45*S:.1f}" fill="#eee" stroke="{INK}" stroke-width="1.4"/>')
    p.rect(34.4, 24.0, 2.4, 2.3, 'none', '#999', 1)
    # fixed items
    p.rect(0.5, 0.35, 10, 0.35, '#bbb', 'none')
    p.rect(26.6, 0.3, 4.6, 0.35, '#333', 'none'); p.sub(28.9, 1.3, 'fireplace', 10)
    p.rect(16.4, 4.45, 6.0, 0.7, '#bbb', 'none'); p.rect(17.5, 7.0, 3.8, 1.2, '#eee')       # kitchen run + island
    p.rect(22.7, 7.0, 4.0, 1.2, 'none', '#999', 1)                                         # dining table
    p.rect(33.3, 0.4, 0.25, 6.2, '#333', 'none')                                           # cinema screen
    p.car(1.4, 2.6, 3.6, 7.6, 'SVJ'); p.car(5.6, 2.8, 7.8, 7.8, 'SF90')
    # labels
    p.txt(5.5, 9.4, 'GARAGE', 16); p.sub(5.5, 10.15, 'glass door to the forecourt', 10)
    p.txt(13.5, 5.2, 'ENTRANCE', 13); p.txt(13.5, 5.9, 'HALL', 13); p.sub(13.5, 6.6, 'glass wall', 10); p.sub(13.5, 7.2, 'onto the cars', 10)
    p.txt(17.3, 2.4, 'WC', 11); p.txt(20.3, 2.4, 'PANTRY', 10); p.txt(23.75, 2.4, 'UTILITY', 10)
    p.txt(19.4, 10.0, 'KITCHEN', 13); p.txt(24.7, 10.0, 'DINING', 13)
    p.txt(29.4, 6.2, 'LIVING', 17); p.sub(29.4, 7.0, 'glass to garden + pool', 10)
    p.txt(36.6, 3.6, 'CINEMA', 13); p.sub(36.6, 4.3, '8 seats', 10)
    p.txt(42.5, 3.6, 'GYM', 12)
    p.sub(39, 9.2, 'GALLERY · skylight', 11, '#333')
    p.add(f'<text transform="translate({p.X(44.15):.1f},{p.Y(19.5):.1f}) rotate(90)" font-size="10" letter-spacing=".06em" fill="#333" text-anchor="middle">CORRIDOR · windows to the side garden</text>')
    p.txt(36.3, 26.9, 'PRIMARY', 12); p.txt(36.3, 27.5, 'SUITE', 12)
    p.txt(41.3, 24.0, 'DRESSING', 8); p.txt(41.3, 25.85, 'BATH', 9)
    p.add(f'<text transform="translate({p.X(32.0):.1f},{p.Y(13.9):.1f})" font-size="10" font-weight="700" letter-spacing=".05em" fill="{LAT}" text-anchor="end">TIMBER LATTICE (brown)</text>')
    p.frame('SINGLE-STOREY L-SHAPED HOUSE · SKETCH PLAN')
    p.write(path)


if __name__ == '__main__':
    draw(sys.argv[1])
