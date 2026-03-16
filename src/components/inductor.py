from src.components.component import BasicComponent, Label

from reportlab.pdfgen.canvas import Canvas

class Inductor(BasicComponent):
    def __init__(self, inductance: str, i_max: str, package: str, label_scale: float = 1.0):
        self.value = Label("{} {}".format(inductance, i_max), label_scale)
        self.type = "inductor"
        self.str1 = "{}".format(package)
        self.str2 = "L = {}".format(inductance)
        self.str3 = "I = {}".format(i_max)

    def draw_polyfuse(self, c: Canvas, x: float, y: float, size: float) -> None:
        arc_size = size / 2

        for i in range(4):
            c.arc(
                x - size + arc_size * i,
                y - arc_size / 2,
                x - size + arc_size * (i + 1),
                y + arc_size / 2,
                0, 180
            )

        c.line(x - size * 1.5, y, x - size, y)
        c.line(x + size * 1.5, y, x + size, y)

    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        self.draw_polyfuse(c, x, y, size)


