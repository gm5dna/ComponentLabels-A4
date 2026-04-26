from src.components.component import BasicComponent, Label

from reportlab.pdfgen.canvas import Canvas


class Crystal(BasicComponent):
    def __init__(self, name: str | Label, frequency: str, cl: str):
        self.value = name
        self.type = "crystal"
        self.str1 = "{}".format(frequency)
        self.str2 = "CL = {}".format(cl)
        self.str3 = None

    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        c.setLineWidth(0.9)
        c.line(x - size, y, x - size / 3, y)
        c.line(x + size / 3, y, x + size, y)

        c.line(x - size / 3, y - size / 2, x - size / 3, y + size / 2)
        c.line(x + size / 3, y - size / 2, x + size / 3, y + size / 2)

        c.rect(x - size / 6, y - 2 * size / 3, size / 3, 4 * size / 3, fill=0, stroke=1)
