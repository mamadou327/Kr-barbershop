"""Casa Ombra L - single-storey L-shaped house. One sketch plan (site + house).
Metres. X = east, Y = south. Origin = NW corner of the house. Road along the WEST.

West arm  x 0..11,  y 0..36  : street side (west) solid, courtyard side (east) glass
North arm x 11..48, y 0..11  : garden side (north) corridor, courtyard side (south) glass + timber lattice
Great room wraps the corner. Pool sits in the courtyard, parallel to the north arm.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import plans as base

base.S, base.OX, base.OY = 24, 848, 304
INK, G, LAT, RED = base.INK, base.G, base.LAT, base.RED


def draw(path):
    p = base.P()
    # ---------------- site ----------------
    p.rect(-17, -6, 3, 46, '#f1f1f1', 'none')
    p.add(f'<text transform="translate({p.X(-15.5):.1f},{p.Y(17):.1f}) rotate(-90)" font-size="14" font-weight="600" letter-spacing=".12em" fill="#888" text-anchor="middle">ROAD</text>')
    p.rect(-14, -6, 64, 46, 'none', G, 2)                                    # boundary walls
    p.line(-14, 22, -14, 33, 7, '#fff'); p.line(-14, 22, -14, 33, 2, INK, '10 6')
    p.add(f'<text transform="translate({p.X(-13.2):.1f},{p.Y(27.5):.1f}) rotate(-90)" font-size="11" letter-spacing=".06em" fill="#555" text-anchor="middle">SLIDING GATE</text>')
    p.rect(-13.5, 18, 13.5, 18, 'none', G, 1, '4 5'); p.txt(-6.8, 35.0, 'FORECOURT', 15); p.sub(-6.8, 35.7, 'travertine', 11)
    p.car(-8.6, 21.6, -3.7, 23.6, '', INK); p.txt(-6.15, 23.0, 'M3 CS', 12)
    p.car(-8.6, 24.8, -3.6, 26.9, '', INK); p.txt(-6.1, 26.3, 'URUS', 12)
    for ty in (19.5, 30.5): p.tree(-12.2, ty, 1.0, '#666')
    p.rect(-13.5, -5.5, 13.5, 23, 'none', G, 1, '3 4'); p.sub(-6.8, 8, 'planting · olive trees', 11)
    for ty in (0, 6, 12): p.tree(-9, ty, 1.1, '#777')
    p.rect(0, -5.5, 49.5, 5.5, 'none', G, 1, '3 4'); p.txt(30, -2.4, 'REAR GARDEN', 13, 700, '#444')
    for tx in (8, 18, 40, 46): p.tree(tx, -3, 1.0, '#777')
    # courtyard: covered terraces (roof overhang), pool, lawn
    p.rect(11, 11, 37, 2.5, '#f4f4f4', G, 1); p.sub(32, 12.55, 'COVERED TERRACE (roof overhang)', 11)
    p.rect(11, 13.5, 2.5, 22.5, '#f4f4f4', G, 1)
    p.add(f'<text transform="translate({p.X(12.35):.1f},{p.Y(26):.1f}) rotate(-90)" font-size="11" letter-spacing=".05em" fill="#555" text-anchor="middle">COVERED TERRACE</text>')
    p.rect(17, 15.5, 24, 4.5, '#d6d6d6', INK, 1.8); p.txt(29, 18.1, 'POOL', 16, 700, '#333'); p.sub(29, 18.9, '24 x 4.5 m · black stone', 11)
    for tx in (15.3, 42.7): p.rect(tx - 1.2, 16.55, 2.4, 2.4, '#fff', G, 1); p.tree(tx, 17.75, 1.1, '#555')
    p.rect(13.5, 21.5, 36, 18, 'none', G, 1, '3 4'); p.txt(31, 31.5, 'LAWN', 14, 700, '#444'); p.sub(31, 32.2, 'olive trees', 11)
    for (tx, ty) in ((19, 26), (27, 29), (36, 25.5), (44, 30), (22, 35.5), (40, 36)): p.tree(tx, ty, 1.3, '#555')

    # ---------------- house ----------------
    p.rect(0, 0, 11, 36, '#fff', 'none'); p.rect(11, 0, 37, 11, '#fff', 'none')
    # outline: west arm
    p.wall(0, 0, 0, 22.2); p.wall(0, 23.8, 0, 26.5); p.glass(0, 26.5, 0, 35.5); p.wall(0, 35.5, 0, 36)  # west face: front door gap, garage glass
    p.wall(0, 36, 11, 36)
    p.wall(11, 36, 11, 26); p.glass(11, 26, 11, 11)                                                     # east face: garage solid, hall + great room glass
    # north arm
    p.wall(0, 0, 48, 0); p.wall(48, 0, 48, 11)
    p.glass(11, 11, 48, 11)                                                                              # courtyard face
    for a, b in ((22, 24), (29, 31), (35, 37), (41.5, 43.5)): p.glass(a, 0, b, 0)                       # corridor windows
    p.glass(9.5, 0, 19.5, 0)                                                                             # living: window to the rear garden
    p.lattice(22.2, 11.45, 47.8, 11.45)                                                                  # lattice in front of the private rooms
    # garage | hall
    p.glass(0, 26, 11, 26); p.door_h(8.6, 26, 1.0, 'n')
    # front door (pivot) in the west face, from the forecourt
    p.gap(0, 22.2, 0, 23.8)
    p.add(f'<line x1="{p.X(-0.55):.1f}" y1="{p.Y(22.45):.1f}" x2="{p.X(0.55):.1f}" y2="{p.Y(23.55):.1f}" stroke="{INK}" stroke-width="5"/>')
    p.add(f'<line x1="{p.X(-3.0):.1f}" y1="{p.Y(23.0):.1f}" x2="{p.X(-0.9):.1f}" y2="{p.Y(23.0):.1f}" stroke="{INK}" stroke-width="2.2" marker-end="url(#ah)"/>')
    p.txt(-1.9, 21.6, 'FRONT DOOR', 11)
    # hall | great room: open, marked by a low stone bench line
    # service strip x 0..3, y 4..20
    p.iwall(3, 4, 3, 20); p.iwall(0, 4, 3, 4); p.iwall(0, 9.5, 3, 9.5); p.iwall(0, 15, 3, 15); p.iwall(0, 20, 3, 20)
    p.door_v(3, 5.6, 0.9, 'e'); p.door_v(3, 11.2, 0.9, 'e'); p.door_v(3, 16.6, 0.9, 'e')
    # private wing: cinema | bedrooms | primary, corridor y 0..2.2
    CY = 2.2
    p.iwall(20, 0, 20, 11)
    p.door_v(20, 0.6, 1.0, 'w')                                                                          # corridor door from the great room
    p.iwall(20, CY, 48, CY)
    p.iwall(26, CY, 26, 11); p.iwall(32, CY, 32, 11); p.iwall(38, CY, 38, 11)
    p.door_h(21, CY, 1.0, 's')                                                                           # cinema
    for a, b in ((26, 32), (32, 38)):
        p.iwall(b - 2.6, CY, b - 2.6, 5.0); p.iwall(b - 2.6, 5.0, b, 5.0)
        p.door_h(a + 0.4, CY, 0.9, 's'); p.door_v(b - 2.6, 3.4, 0.8, 'e')
    # primary 38..48: bath + dressing at the back
    p.iwall(38, 5.6, 48, 5.6); p.iwall(43.5, CY, 43.5, 5.6)
    p.door_h(38.5, CY, 0.9, 's'); p.gap(39.5, 5.6, 41.5, 5.6); p.door_v(43.5, 3.4, 0.9, 'e')
    p.glass(48, 6.2, 48, 10.6)
    # fixed items
    p.rect(3.6, 0.35, 5.0, 0.4, '#333', 'none'); p.sub(6.1, 1.45, 'fireplace', 10)
    p.rect(4.2, 16.2, 0.9, 3.4, '#bbb', 'none'); p.rect(6.6, 16.6, 1.4, 2.8, '#eee')                    # kitchen run + island
    p.rect(6.0, 11.6, 1.2, 3.0, 'none', '#999', 1)                                                       # dining table
    p.rect(20.6, 0.5 + CY - 0.2, 0.25, 7.2, '#333', 'none')                                              # cinema screen
    p.add(f'<ellipse cx="{p.X(46):.1f}" cy="{p.Y(3.9):.1f}" rx="{0.9*S if False else 0.9*base.S:.1f}" ry="{0.45*base.S:.1f}" fill="#eee" stroke="{INK}" stroke-width="1.4"/>')
    p.rect(41.5, 7.2, 2.3, 2.4, 'none', '#999', 1)
    p.rect(0.5, 35.25, 10, 0.3, '#bbb', 'none')
    # cars in the garage, noses to the glass (west)
    p.car(0.9, 27.8, 5.8, 29.9, '', INK); p.txt(3.35, 29.2, 'SVJ', 12)
    p.car(0.9, 31.4, 5.8, 33.4, '', INK); p.txt(3.35, 32.75, 'SF90', 12)
    # labels
    p.txt(7.9, 31.0, 'GARAGE', 16); p.sub(7.9, 31.7, 'glass to forecourt + hall', 10)
    p.txt(5.5, 23.3, 'ENTRANCE HALL', 14); p.sub(5.5, 24.0, 'glass wall onto the cars', 10)
    p.txt(1.5, 7.0, 'WC', 11); p.txt(1.5, 12.5, 'UTILITY', 9); p.txt(1.5, 17.7, 'PANTRY', 9)
    p.txt(8.6, 19.2, 'KITCHEN', 13); p.txt(8.8, 13.3, 'DINING', 13)
    p.txt(12.5, 5.3, 'LIVING', 18); p.sub(12.5, 6.1, 'corner room · glass to garden and pool', 11)
    p.txt(23.3, 7.6, 'CINEMA', 14); p.sub(23.3, 8.3, 'blackout lattice', 10)
    p.txt(29, 8.6, 'BEDROOM 2', 12); p.txt(35, 8.6, 'BEDROOM 3', 12)
    p.txt(30.7, 3.95, 'ENSUITE', 8); p.txt(36.7, 3.95, 'ENSUITE', 8)
    p.txt(41.3, 4.1, 'BATH', 10); p.txt(45.75, 4.9, 'DRESSING', 8)
    p.txt(43, 10.2, 'PRIMARY SUITE', 12)
    p.sub(33, 1.5, 'CORRIDOR · windows to the rear garden', 10, '#333')
    p.add(f'<text x="{p.X(35):.1f}" y="{p.Y(14.6):.1f}" font-size="11" font-weight="700" letter-spacing=".06em" fill="{LAT}" text-anchor="middle">TIMBER LATTICE IN FRONT OF THE PRIVATE ROOMS (brown)</text>')
    p.frame('SINGLE-STOREY L-SHAPED HOUSE · SKETCH PLAN')
    p.write(path)


if __name__ == '__main__':
    draw(sys.argv[1])
