"""Create a ten-page, print-ready Solar System name-card PDF."""

from math import cos, pi, sin
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas


OUTPUT = Path("output/pdf/solar-system-name-cards.pdf")
PAGE_WIDTH, PAGE_HEIGHT = landscape(A4)

CARDS = [
    ("SUN", "#F9B233", "#FFF2B3"),
    ("MERCURY", "#A7A7A7", "#E6E6E6"),
    ("VENUS", "#D99A54", "#F4D7A3"),
    ("EARTH", "#2878B8", "#BFE5F5"),
    ("MARS", "#C85D3C", "#F0C1B3"),
    ("JUPITER", "#C98B59", "#F0D2B5"),
    ("SATURN", "#D8B96C", "#F4E8BA"),
    ("URANUS", "#6ECAE0", "#CBEFF5"),
    ("NEPTUNE", "#365CB4", "#C5D2F0"),
    ("PLUTO", "#A78A78", "#E0C9B5"),
]


def draw_planet(c, name, color, accent):
    cx, cy = PAGE_WIDTH / 2, PAGE_HEIGHT / 2 + 35
    r = 135 if name in {"SUN", "JUPITER", "SATURN"} else 118

    if name == "SATURN":
        c.saveState()
        c.translate(cx, cy)
        c.rotate(-16)
        c.setStrokeColor(HexColor("#B4944D"))
        c.setLineWidth(18)
        c.ellipse(-r * 1.52, -r * 0.48, r * 1.52, r * 0.48, stroke=1, fill=0)
        c.restoreState()

    c.setFillColor(HexColor(color))
    c.setStrokeColor(HexColor("#1F2A44"))
    c.setLineWidth(4)
    c.circle(cx, cy, r, fill=1, stroke=1)
    c.saveState()
    clip = c.beginPath()
    clip.circle(cx, cy, r)
    c.clipPath(clip, stroke=0, fill=0)

    c.setFillColor(HexColor(accent))
    if name == "SUN":
        for angle in range(0, 360, 30):
            rad = angle * pi / 180
            c.setStrokeColor(HexColor("#E88819"))
            c.setLineWidth(7)
            c.line(cx + cos(rad) * r * 1.13, cy + sin(rad) * r * 1.13,
                   cx + cos(rad) * r * 1.34, cy + sin(rad) * r * 1.34)
        for dx, dy, rr in [(-45, 35, 19), (46, -38, 26), (12, 58, 13), (-4, -62, 16)]:
            c.circle(cx + dx, cy + dy, rr, fill=1, stroke=0)
    elif name == "EARTH":
        c.setFillColor(HexColor("#4DAA57"))
        c.ellipse(cx - 92, cy + 9, cx - 14, cy + 75, fill=1, stroke=0)
        c.ellipse(cx + 5, cy - 80, cx + 92, cy + 11, fill=1, stroke=0)
        c.ellipse(cx - 17, cy - 14, cx + 34, cy + 40, fill=1, stroke=0)
    elif name == "JUPITER":
        c.setFillColor(HexColor("#F1D2B7"))
        for offset in [-80, -35, 12, 62]:
            c.rect(cx - r, cy + offset, 2 * r, 18, fill=1, stroke=0)
        c.setFillColor(HexColor("#C95C45"))
        c.ellipse(cx + 35, cy - 40, cx + 92, cy - 9, fill=1, stroke=0)
    elif name == "NEPTUNE":
        c.setFillColor(HexColor("#7299DB"))
        c.rect(cx - r, cy - 25, 2 * r, 18, fill=1, stroke=0)
        c.rect(cx - r, cy + 50, 2 * r, 12, fill=1, stroke=0)
    else:
        c.setFillColor(HexColor(accent))
        for dx, dy, rr in [(-42, 30, 17), (48, 42, 12), (30, -52, 20), (-58, -34, 10)]:
            c.circle(cx + dx, cy + dy, rr, fill=1, stroke=0)
    c.restoreState()


def draw_card(c, name, color, accent):
    c.setFillColor(HexColor("#0B1736"))
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#FFFFFF"))
    c.setLineWidth(2)
    c.roundRect(24, 24, PAGE_WIDTH - 48, PAGE_HEIGHT - 48, 18, fill=0, stroke=1)
    draw_planet(c, name, color, accent)

    c.setFillColor(white)
    font_size = 42 if len(name) <= 7 else 36
    c.setFont("Helvetica-Bold", font_size)
    c.drawCentredString(PAGE_WIDTH / 2, 47, name.title())


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=landscape(A4), pageCompression=1)
    c.setTitle("Solar System Name Cards")
    for card in CARDS:
        draw_card(c, *card)
        c.showPage()
    c.save()


if __name__ == "__main__":
    main()
