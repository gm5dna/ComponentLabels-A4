from src.components.component import BasicComponent, Label

from reportlab.pdfgen.canvas import Canvas


class DCDCConverter(BasicComponent):
    def __init__(
        self,
        name: str | Label,
        power: str,
        Vin: str,
        Vout: str,
    ):
        self.value = name
        self.type = "DC/DC"
        self.str1 = "P = {}".format(power)
        self.str2 = "Vin = {}".format(Vin)
        self.str3 = "Vout = {}".format(Vout)

    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        c.setLineWidth(0.9)
        left = x - size * 2 / 3
        bottom = y - size * 2 / 3
        width = size * 4 / 3
        height = size * 4 / 3

        c.rect(left, bottom, width, height, fill=0, stroke=1)
        c.line(left, bottom, left + width, bottom + height)

        c.line(x - size, y, left, y)
        c.line(left + width, y, x + size, y)

        dash = size / 3.2
        gap = size / 8
        split_gap = size / 8

        top_dash_y = y + size / 4
        top_dash_x = x - size / 5
        c.line(top_dash_x - dash / 2, top_dash_y + gap / 2, top_dash_x + dash / 2, top_dash_y + gap / 2)
        c.line(top_dash_x - dash / 2, top_dash_y - gap / 2, top_dash_x - split_gap / 2, top_dash_y - gap / 2)
        c.line(top_dash_x + split_gap / 2, top_dash_y - gap / 2, top_dash_x + dash / 2, top_dash_y - gap / 2)

        bottom_dash_y = y - size / 4
        bottom_dash_x = x + size / 5
        c.line(bottom_dash_x - dash / 2, bottom_dash_y + gap / 2, bottom_dash_x + dash / 2, bottom_dash_y + gap / 2)
        c.line(bottom_dash_x - dash / 2, bottom_dash_y - gap / 2, bottom_dash_x - split_gap / 2, bottom_dash_y - gap / 2)
        c.line(bottom_dash_x + split_gap / 2, bottom_dash_y - gap / 2, bottom_dash_x + dash / 2, bottom_dash_y - gap / 2)
