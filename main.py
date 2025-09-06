import svgwrite

# 🎨 Colors
COLOR_A = "#a9a9d4"
COLOR_B = "#ffffff"
COLOR_C = "#C4B5FD"
COLOR_D = "#1a1a2e"

# 🖼️ Canvas
MIRROR_CENTER = (299, 229)  # symmetry axis
WIDTH, HEIGHT = MIRROR_CENTER[0] * 2, MIRROR_CENTER[1] * 2
BAR_WIDTH = 50

dwg = svgwrite.Drawing("logo.svg", size=(f"{WIDTH}px", f"{HEIGHT}px"), profile="tiny")


def add_shape(shape):
    """Helper to add a shape to the drawing."""
    dwg.add(shape)


def mirror_transform(base_transform: str, mirror: bool, mirror_center=MIRROR_CENTER):
    """Return a combined transform if mirroring is enabled."""
    if not mirror:
        return base_transform
    mx, my = mirror_center
    return f"translate({2 * mx},{2 * my}) scale(-1,-1) {base_transform}".strip()


def draw_right_triangle(dwg, insert, size, fill, stroke=None,
                        mirror=False, mirror_center=MIRROR_CENTER):
    """Draw a right isosceles triangle (90° angle)."""
    x, y = insert
    w, h = size

    points = [
        (x, y),  # bottom-left
        (x + w, y),  # bottom-right
        (x, y - h)  # top-left
    ]

    transform = mirror_transform("", mirror, mirror_center)
    tri = dwg.polygon(
        points=points,
        fill=fill,
        stroke=stroke,
        stroke_width=2,
        **({"transform": transform} if transform else {})
    )
    add_shape(tri)


def draw_rotated_rect(dwg, insert, size, fill, stroke=None,
                      angle=0, mirror=False, mirror_center=MIRROR_CENTER):
    """Draw a rotated rectangle, optionally mirrored."""
    x, y = insert
    w, h = size
    cx, cy = x + w / 2, y + h / 2  # center of rectangle

    base_transform = f"rotate({angle},{cx},{cy})" if angle else ""
    transform = mirror_transform(base_transform, mirror, mirror_center)

    rect = dwg.rect(
        insert=insert,
        size=size,
        fill=fill,
        stroke=stroke,
        stroke_width=2,
        **({"transform": transform} if transform else {})
    )
    add_shape(rect)


def draw_symmetric(func, *args, **kwargs):
    """Helper to draw a shape on both sides (mirrored)."""
    func(dwg, *args, **kwargs, mirror=False)
    func(dwg, *args, **kwargs, mirror=True)


# =========================
# 🎨 Drawing instructions
# =========================


# Symmetric shapes


draw_symmetric(draw_rotated_rect, insert=(0, 111), size=(BAR_WIDTH, 200), fill=COLOR_B, stroke=COLOR_B, angle=0)
draw_symmetric(draw_right_triangle, insert=(0, 316), size=(70, 70), fill=COLOR_C, stroke=COLOR_C)
draw_symmetric(draw_rotated_rect, insert=(4, 67), size=(100, BAR_WIDTH), fill=COLOR_B, stroke=COLOR_B, angle=-45)
draw_symmetric(draw_rotated_rect, insert=(146, 344), size=(100, BAR_WIDTH), fill=COLOR_B, stroke=COLOR_B, angle=-45)
draw_symmetric(draw_rotated_rect, insert=(-11, 345), size=(200, BAR_WIDTH), fill=COLOR_C, stroke=COLOR_C, angle=45)

# Long central bar
draw_rotated_rect(dwg, insert=(4, 204), size=(590, BAR_WIDTH), fill=COLOR_A, stroke=COLOR_A, angle=45)

# Save SVG
dwg.save()
