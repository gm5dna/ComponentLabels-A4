from src.components.component import BasicComponent

from reportlab.pdfgen.canvas import Canvas

class Polyfuse(BasicComponent):
    def __init__(self, voltage: str, current: str, package: str):
        self.value = "{} {}".format(voltage, current)
        self.type = "polyfuse"
        self.str1 = "{}".format(package)
        self.str2 = "V = {}".format(voltage)
        self.str3 = "I = {}".format(current)

    def draw_polyfuse(self, c: Canvas, x: float, y: float, size: float) -> None:
        c.line(x - size * 1.5, y, x + size * 1.5, y)

        c.line(x - size, y - size / 2, x + size, y - size / 2)
        c.line(x - size, y + size / 2, x + size, y + size / 2)

        c.line(x - size, y - size / 2, x - size, y + size / 2)
        c.line(x + size, y - size / 2, x + size, y + size / 2)
        
        c.line(x - size, y - size, x + size, y + size)
        c.line(x - size, y - size, x - size * 1.5, y - size)
        c.line(x + size, y + size, x + size * 1.5, y + size)

    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        self.draw_polyfuse(c, x, y, size)

