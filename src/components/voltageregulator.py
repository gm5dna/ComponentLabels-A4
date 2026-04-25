from src.components.component import BasicComponent, Label

from reportlab.pdfgen.canvas import Canvas


class VoltageRegulator(BasicComponent):
    def __init__(self, name: str | Label, vin_max: str, vout: str, iload_max: str):
        self.value = name
        self.type = "regulator"
        self.str1 = "Vin <= {}".format(vin_max)
        self.str2 = "Vout = {}".format(vout)
        self.str3 = "Iload <= {}".format(iload_max)

    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        c.setLineWidth(0.9)

        left = x - size * 2 / 3
        bottom = y - size / 2
        width = size * 4 / 3
        height = size

        c.rect(left, bottom, width, height, fill=0, stroke=1)
        c.line(x - size, y, left, y)
        c.line(left + width, y, x + size, y)
        c.line(x, bottom, x, bottom - size / 2)
