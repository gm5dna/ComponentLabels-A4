from src.components.component import BasicComponent, Label

from reportlab.pdfgen.canvas import Canvas

class Generic(BasicComponent):
    def __init__(self, text: str | Label):
        self.value = text
        self.type = "generic"
        self.str1 = None
        self.str2 = None
        self.str3 = None

    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        pass
