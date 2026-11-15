"""Build the hero's exact Fibonacci tiling and finite recursive copies.

The square sides obey F[n] = F[n-1] + F[n-2]. Quarter-circles meet
at shared tile corners. A repeated family of similarity maps fits the
same seven-square construction inside larger squares (a finite IFS view).
Randomness in the browser affects drawing times, never these proportions.
"""
from pathlib import Path
from math import isclose

ROOT = Path(__file__).resolve().parents[1]

def fibonacci_tiles(count):
    sequence = [1, 1]
    while len(sequence) < count:
        sequence.append(sum(sequence[-2:]))
    tiles = [(0, 0, 1, 0)]
    left, top, right, bottom = 0, 0, 1, 1
    for n in range(1, count):
        side = sequence[n]
        direction = n % 4
        if direction == 1:
            x, y = right, top
            assert bottom - top == side
            right += side
        elif direction == 2:
            x, y = left, bottom
            assert right - left == side
            bottom += side
        elif direction == 3:
            x, y = left - side, top
            assert bottom - top == side
            left -= side
        else:
            x, y = left, top - side
            assert right - left == side
            top -= side
        tiles.append((x, y, side, direction))
    return tiles

def arc(tile):
    x, y, s, direction = tile
    return [((x, y+s), (x+s, y), (x+s, y+s)),
            ((x, y), (x+s, y+s), (x, y+s)),
            ((x+s, y), (x, y+s), (x, y)),
            ((x+s, y+s), (x, y), (x+s, y))][direction]

def validate(tiles):
    for n, tile in enumerate(tiles):
        x, y, side, _ = tile
        if n > 1:
            assert side == tiles[n-1][2] + tiles[n-2][2]
        if n:
            previous = arc(tiles[n-1])
            current = arc(tile)
            assert previous[1] == current[0]
            u = (previous[1][0]-previous[2][0], previous[1][1]-previous[2][1])
            v = (current[0][0]-current[2][0], current[0][1]-current[2][1])
            assert u[0]*v[1] == u[1]*v[0]  # Matching tangent at each joint.
            assert u[0]*v[0] + u[1]*v[1] > 0
        start, end, center = arc(tile)
        for px, py in (start, end):
            assert isclose((px-center[0])**2 + (py-center[1])**2, side**2)
        for ox, oy, os, _ in tiles[:n]:
            assert min(x+side, ox+os) <= max(x, ox) or min(y+side, oy+os) <= max(y, oy)

def pair(point):
    return f'{point[0]:.3f},{point[1]:.3f}'

def tile_paths(tile, mapping):
    x, y, s, _ = tile
    corners = [mapping((x,y)), mapping((x+s,y)), mapping((x+s,y+s)), mapping((x,y+s))]
    border = 'M' + ' L'.join(map(pair, corners)) + ' Z'
    a, b, _ = arc(tile)
    # Keep each quarter-circle consistent with the mapping's vertical orientation.
    radius = abs(mapping((x+s,y))[0] - mapping((x,y))[0])
    sweep = int(mapping((x,y+s))[1] > mapping((x,y))[1])
    curve = f'M{pair(mapping(a))} A{radius:.3f},{radius:.3f} 0 0 {sweep} {pair(mapping(b))}'
    return border, curve

TILES = fibonacci_tiles(16)
SMALL = fibonacci_tiles(7)
validate(TILES)
validate(SMALL)
LEFT = min(t[0] for t in SMALL)
TOP = min(t[1] for t in SMALL)
WIDTH = max(t[0]+t[2] for t in SMALL) - LEFT
HEIGHT = max(t[1]+t[2] for t in SMALL) - TOP

parts = []
def stroke(kind, d, depth=0):
    return f'<path class="pi-genesis__{kind}" data-depth="{depth}" d="{d}" pathLength="1"/>'

def recursive_patch(px, py, side, depth):
    # Fit the same 21:13 Fibonacci rectangle into each square, with a clear margin.
    scale = side * .86 / WIDTH
    offset_x = px + side*.07
    offset_y = py + (side - HEIGHT*scale)*.5
    mapping = lambda point: (offset_x+(point[0]-LEFT)*scale, offset_y+(TOP+HEIGHT-point[1])*scale)
    borders, curves = [], []
    for tile in SMALL:
        border, curve = tile_paths(tile, mapping)
        borders.append(border)
        curves.append(curve)
    parts.append(stroke('subdivision', ' '.join(borders), depth))
    parts.append(stroke('echo', ' '.join(curves), depth))
    if depth < 3 and side > 120:
        for tile in SMALL[-2:]:
            x,y,s,_ = tile
            tx,ty = mapping((x,y+s))
            recursive_patch(tx,ty,s*scale,depth+1)

mapping = lambda point: (500+(point[0]-.6)*3.5, 500+(point[1]-.8)*3.5)
parts.append('''{# Exact Fibonacci squares, joined quarter-circles and recursive similarity copies. #}
<div class="pi-genesis" aria-hidden="true">
  <div class="pi-genesis__atmosphere"></div>
  <svg class="pi-genesis__drawing" viewBox="0 0 1000 1000" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>''')
for n,tile in enumerate(TILES):
    x,y,s,direction = tile
    px,py = mapping((x,y))
    size=s*3.5
    border,curve=tile_paths(tile,mapping)
    parts.append(f'<g id="pi-growth-{n}" data-fibonacci="{s}">')
    # Draw square sides individually, beginning near the construction's origin.
    corners = [mapping((x,y)),mapping((x+s,y)),mapping((x+s,y+s)),mapping((x,y+s))]
    edges = [(corners[i],corners[(i+1)%4]) for i in range(4)]
    distance = lambda p: (p[0]-500)**2 + (p[1]-500)**2
    edges.sort(key=lambda edge: min(map(distance,edge)))
    for order,(start,end) in enumerate(edges):
        if distance(start) > distance(end):
            start,end = end,start
        parts.append(stroke('tile',f'M{pair(start)} L{pair(end)}').replace('data-depth="0"',f'data-depth="0" data-edge="{order}"'))
    parts.append(stroke('arc',curve))
    if n>=5:
        parts.append(f'<g transform="rotate({n*90} {px+size/2:.3f} {py+size/2:.3f})">')
        recursive_patch(px,py,size,1)
        parts.append('</g>')
    if n>=4:
        # A measured side documents the actual integer square size.
        inset=size*.055
        length=size*.22
        parts.append(stroke('measure', f'M{px+inset:.3f},{py+inset:.3f} h{length:.3f} m{-length:.3f},{-inset*.35:.3f} v{inset*.7:.3f} m{length:.3f},0 v{-inset*.7:.3f}'))
    a,b,_=arc(tile)
    if n>=4:
        node=mapping(b)
        parts.append(f'<circle class="pi-genesis__node" cx="{node[0]:.3f}" cy="{node[1]:.3f}" r="1.6"/>')
    parts.append('</g>')
parts.append('</defs>')
for phase in (-24,12):
    parts.append(f'<g class="pi-genesis__generation" style="--phase:{phase}s">')
    for n in range(len(TILES)):
        parts.append(f'<use href="#pi-growth-{n}"/>')
    parts.append('</g>')
parts.append('''</svg>
  <span class="pi-genesis__origin"></span>
</div>''')
output=ROOT/'pi_development/web/templates/web/components/fibonacci_field.html'
output.write_text('\n'.join(parts)+'\n',encoding='utf-8')
print(f'Built {len(TILES)} non-overlapping Fibonacci squares; all arcs connect; recursive geometry valid.')
