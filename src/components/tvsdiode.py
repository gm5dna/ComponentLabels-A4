from src.components.component import BasicComponent, Label

from reportlab.pdfgen.canvas import Canvas


class TVSDiode(BasicComponent):
    def __init__(self, name: str | Label):
        self.value = name
        self.type = "TVS diode"
        self.str1 = None
        self.str2 = None
        self.str3 = None

    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        c.line(x - size, y, x - size / 3, y)
        c.line(x + size, y, x + size / 3, y)

        c.line(x - size / 3, y - size / 2, x - size / 3, y + size / 2)
        c.line(x + size / 3, y - size / 2, x + size / 3, y + size / 2)

        c.line(x - size / 3, y - size / 2, x, y)
        c.line(x - size / 3, y + size / 2, x, y)
        c.line(x + size / 3, y - size / 2, x, y)
        c.line(x + size / 3, y + size / 2, x, y)

        c.line(x - size / 3, y + size / 2, x - size / 2, y + 2 * size / 3)
        c.line(x + size / 3, y - size / 2, x + size / 2, y - 2 * size / 3)
