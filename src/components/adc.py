from src.components.component import BasicComponent, Label

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import black
from reportlab.lib.units import inch
from src.stickerrect import StickerRect


class AnalogDigitalConverter(BasicComponent):
    def __init__(self, name: str | Label, channels: str, vdd: str, resolution: str):
        self.value = name
        self.type = "ADC"
        self.channels = channels
        self.str1 = "Vdd = {}".format(vdd)
        self.str2 = "{}".format(resolution)
        self.str3 = None

    def draw(self, c: Canvas, rect: StickerRect, draw_center_line: bool) -> None:
        print("Generating sticker '{}' ({})".format(self.value, self.type))

        value_font_size = 0.20 * inch
        small_font_size = 0.108 * inch
        channel_font_size = 0.08 * inch

        text_x = rect.left + rect.width / 2
        text_bottom = rect.bottom + rect.height / 4
        channel_bottom = rect.bottom + rect.height / 13
        small_text_x = rect.left + 5 * rect.width / 6
        small_text_bottom = rect.bottom + rect.height / 8 + rect.height / 4

        if self.str1 is None:
            small_text_bottom -= rect.height / 16

        if self.str2 is None:
            small_text_bottom -= rect.height / 16

        if self.str3 is None:
            small_text_bottom -= rect.height / 16

        def draw(pos: float) -> None:
            Label.to_label(self.value).draw_centered(c, text_x, text_bottom + pos, value_font_size)

            c.setFont("main", channel_font_size)
            c.drawCentredString(text_x, channel_bottom + pos, "{} channel".format(self.channels))

            c.setFont("main", small_font_size)
            bottom = small_text_bottom

            if self.str1 is not None:
                Label.to_label(self.str1).draw_centered(c, small_text_x, bottom + pos, small_font_size)
                bottom -= rect.height / 8

            if self.str2 is not None:
                Label.to_label(self.str2).draw_centered(c, small_text_x, bottom + pos, small_font_size)
                bottom -= rect.height / 8

            if self.str3 is not None:
                Label.to_label(self.str3).draw_centered(c, small_text_x, bottom + pos, small_font_size)

            self.draw_icon(c, rect.left + rect.width / 6, rect.bottom + rect.height / 4 + pos, rect.height / 6)

        if draw_center_line:
            c.setStrokeColor(black, 0.25)
            c.setLineWidth(0.7)
            c.line(rect.left, rect.bottom + rect.height / 2, rect.left + rect.width, rect.bottom + rect.height / 2)

        c.setStrokeColor(black, 1)
        c.setLineWidth(2)
        c.setLineCap(1)

        for pos in (0, rect.height / 2):
            draw(pos)

        c.setLineCap(0)

    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        c.roundRect(x - size * 2 / 3, y - size * 2 / 3, size * 4 / 3, size * 4 / 3, size / 8)

        c.line(x - size, y, x - size * 2 / 3, y)
        c.line(x + size * 2 / 3, y + size / 3, x + size, y + size / 3)
        c.line(x + size * 2 / 3, y, x + size, y)
        c.line(x + size * 2 / 3, y - size / 3, x + size, y - size / 3)

        c.setFont("main", size / 1.9)
        c.drawCentredString(x - size / 5, y - size / 6, "A")
        c.drawCentredString(x + size / 5, y - size / 6, "D")
