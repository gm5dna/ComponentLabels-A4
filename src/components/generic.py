from src.stickerrect import StickerRect
from src.components.component import BasicComponent

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import black, toColor
from reportlab.lib.units import inch

class Generic(BasicComponent):
    def __init__(self, text: str):
        self.value = text
        self.type = "generic"
        self.str1 = None
        self.str2 = None
        self.str3 = None

    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        pass
