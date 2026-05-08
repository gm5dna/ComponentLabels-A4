import argparse
import sys

from reportlab.lib.colors import HexColor, black
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from src.components.component import Component, Label
from src.components.resistor import Resistor
from src.components.capacitor import Capacitor
from src.components.transistor import NPNBJT, PNPBJT, NMOSFET, PMOSFET
from src.components.diode import Diode, SchottkyDiode, ZenerDiode, LED
from src.components.nut import SquareNut, HexNut, Washer
from src.components.screw import RecessedHeadScrew, RoundHeadScrew, FlatHeadScrew
from src.components.threadedinsert import ThreadedInsert
from src.components.spring import CompressionSpring, ExtensionSpring
from src.components.generic import Generic
from src.components.polyfuse import Polyfuse
from src.components.inductor import Inductor
from src.components.opamp import OperationalAmplifier
from src.components.adc import AnalogDigitalConverter
from src.components.optocoupler import Optocoupler
from src.components.tvsdiode import TVSDiode
from src.components.crystal import Crystal
from src.components.dcdcconverter import DCDCConverter
from src.components.voltageregulator import VoltageRegulator
from src.paperconfig import (
    PaperConfig,
    AVERY_5260,
    AVERY_L7157,
    AVERY_L7160,
    VYSOCINA,
    list_layout_names,
    resolve_layout,
)
from src.stickerrect import StickerRect

from typing import List

def begin_page(c: Canvas, layout: PaperConfig, draw_outlines: bool) -> None:
    # Draw the outlines of the stickers. Not recommended for the actual print.
    if draw_outlines:
        render_outlines(c, layout)

def end_page(c: Canvas) -> None:
    c.showPage()

def render_stickers(
    c: Canvas,
    layout: PaperConfig,
    values: List[Component | None],
    draw_outlines: bool,
    draw_center_line: bool,
) -> None:
    # Set the title
    c.setTitle(f"Resistor Labels - {layout.paper_name}")

    # Begin the first page
    begin_page(c, layout, draw_outlines)

    for (position, value) in enumerate(values):
        rowId = (position // layout.num_stickers_horizontal) % layout.num_stickers_vertical
        columnId = position % layout.num_stickers_horizontal

        # If we are at the first sticker of a new page, change the page
        if rowId == 0 and columnId == 0 and position != 0:
            end_page(c)
            begin_page(c, layout, draw_outlines)

        if value is not None:
            with StickerRect(c, layout, rowId, columnId, False) as rect:
                value.draw(c, rect, draw_center_line)

    # End the page one final time
    end_page(c)

def render_outlines(c: Canvas, layout: PaperConfig) -> None:
    for row in range(layout.num_stickers_vertical):
        for column in range(layout.num_stickers_horizontal):
            with StickerRect(c, layout, row, column, False) as rect:
                c.setStrokeColor(black, 0.5)
                c.setLineWidth(0)
                c.roundRect(rect.left, rect.bottom, rect.width, rect.height, rect.corner)

DEFAULT_LAYOUT = "VYSOCINA"
DEFAULT_OUTPUT = "ComponentLabels.pdf"


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="LabelGenerator",
        description="Generate a PDF of component labels for printing on Avery / similar label sheets.",
    )
    parser.add_argument(
        "--layout",
        default=DEFAULT_LAYOUT,
        help=(
            "Label sheet preset to render onto. Case-insensitive; accepts the short form "
            "(e.g. L7160) or the full constant name (AVERY_L7160). "
            "Use --list-layouts to see all available presets. "
            "Default: %(default)s."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_OUTPUT,
        help="Output PDF path. Default: %(default)s.",
    )
    parser.add_argument(
        "--list-layouts",
        action="store_true",
        help="Print available layout presets and exit.",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = parse_args()

    if args.list_layouts:
        print("Available layouts:\n")
        print(list_layout_names())
        return

    try:
        layout = resolve_layout(args.layout)
    except KeyError:
        print(f"Error: unknown layout '{args.layout}'.\n", file=sys.stderr)
        print("Available layouts:", file=sys.stderr)
        print(list_layout_names(), file=sys.stderr)
        sys.exit(2)

    pdfmetrics.registerFont(TTFont('main', 'Roboto-Bold.ttf'))

    # ############################################################################
    # Put your own component values in here!
    #
    # Add "None" if no label should get generated at a specific position.
    # ############################################################################

    components: List[Component | None] = []

    # Resistors

    components.append(Resistor(0))

    common_resistor_values: List[float] = [
        # E6
        # 1, 1.5, 2.2, 3.3, 4.7, 6.8

        # E12
        # 1, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2

        # Mostly complete E24. The bundle of resistors I bought did not come with some.
        1, 1.2, 1.5, 1.8, 2, 2.2, 2.4, 2.7, 3, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1

        # E24
        # 1, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2, 2.2, 2.4, 2.7, 3, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1
    ]

    for exponent in range(6): # Ohms to 100kOhms (exclusive)
        for value in common_resistor_values:
            components.append(Resistor(value * (10 ** exponent)))

    resistor_values: List[float] = [
        3300000, 4700000, 5600000, 10000000
    ]

    for value in resistor_values:
        components.append(Resistor(value))

    # Precise resistor

    components.append(Resistor(560000, True))
    components.append(Resistor(8060, True))

    # Resistor array

    components.append(Resistor(2200, False, True))

    # Capacitors

    capacitor_values: List[float] = [ # in pF
        2, 2.2, 3, 5, 10, 15, 22, 30, 33, 47, 68, 75, 82, 100, 150, 220, 330, 470, 680,
        1000, 1500, 2200, 3300, 4700, 6800, 10000, 15000, 33000, 47000, 68000, 100000
    ]

    for value in capacitor_values:
        components.append(Capacitor(value * .000000000001))

    # Padding (if necessary)

    # components.append(None)
    # components.append(None)

    # Inductors

    components.append(Inductor("2.2 μH", "1.85 A", "1210", 0.75))
    components.append(Inductor("2.2 μH", "4.2 A", "1210", 0.75))
    components.append(Inductor("1 μH", "0.6 A", "0603"))
    components.append(Inductor("2.2 μH", "1 A", "0805"))
    components.append(Inductor("1 μH", "0.6 A", "0603"))
    components.append(Inductor("4.7 μH", "1.1 A", "1008", 0.75))
    components.append(Inductor("3.3 μH", "2.4 A", "0806", 0.75))
    components.append(Inductor("1 μH", "1.6 A", "0603"))
    components.append(Inductor("4.7 μH", "0.62 A", "0603", 0.75))
    components.append(Inductor("4.7 μH", "4.5 A", "5.4x5.2", 0.75))
    components.append(Inductor("1 μH", "1.3 A", "0805"))
    components.append(Inductor("1 μH", "4.1 A", "1008"))
    components.append(Inductor("68 μH", "1.33 A", "8.7 dia", 0.75))

    # Op Amps

    components.append(OperationalAmplifier("MCP6002", "2", "1.8-6V"))

    # Analog-digital converters

    components.append(AnalogDigitalConverter("MCP3002", "2", "5 V", "10 bit"))

    # Optocouplers

    components.append(Optocoupler("HCPL-2601", "1", "5 kVrms", "10 MBd"))
    components.append(Optocoupler("HCPL-2630", "2", "5 kVrms", "10 MBd"))

    # DC/DC converters

    components.append(DCDCConverter("NMF0505SC", "1 W", "5 V", "5 V"))

    # Voltage regulators

    components.append(VoltageRegulator("LM2596T", "40 V", "5 V", "3 A"))

    # Crystals

    components.append(Crystal("AB26T", "32.768kHz", "6 pF"))

    # BJTs

    components.append(NPNBJT("2N2222", "3", "2", "1", "0.6 (6) V", "600 mA", "40 V"))
    components.append(NPNBJT("2N3904", "3", "2", "1", "0.65 (6) V", "200 mA", "40 V"))
    components.append(PNPBJT("2N3906", "3", "2", "1", "-0.65 (-5) V", "-200 mA", "-40 V"))
    components.append(PNPBJT("2N5401", "3", "2", "1", "-1 (-5) V", "-600 mA", "-150 V"))
    components.append(NPNBJT("2N5551", "3", "2", "1", "1 (6) V", "600 mA", "160 V"))
    components.append(PNPBJT("A1015",  "2", "3", "1", "-1.1 (-5) V", "-150 mA", "-50 V"))
    components.append(NPNBJT("C1815",  "2", "3", "1", "1 (5) V", "150 mA", "50 V"))
    components.append(NPNBJT("C945",   "2", "3", "1", "1 (5) V", "150 mA", "50 V"))
    components.append(NPNBJT(Label("PMBT2222A", .75), "3", "1", "2", "0.6 (6) V", "600 mA", "40 V"))
    components.append(NPNBJT(Label("SMMBT3904", .7), "3", "1", "2", "0.65 (6) V", "200 mA", "40 V"))

    components.append(NPNBJT("S8050", "3", "2", "1", "1 (6) V", "1.5 A", "25 V"))
    components.append(PNPBJT("S8550", "3", "2", "1", "-0.66 (-6) V", "-1.5 A", "-25 V"))
    components.append(PNPBJT("S9012", "3", "2", "1", "-0.66 (-5) V", "-500 mA", "-20 V"))
    components.append(NPNBJT("S9013", "3", "2", "1", "1.2 (5) V", "500 mA", "25 V"))
    components.append(NPNBJT("S9014", "3", "2", "1", "0.85 (5) V", "500 mA", "45 V"))
    components.append(PNPBJT("S9015", "3", "2", "1", "-1 (-5) V", "-100 mA", "-45 V"))
    components.append(PNPBJT("BC327", "1", "2", "3", "-1.2 (-5) V", "-800 mA", "-45 V"))
    components.append(NPNBJT("BC337", "1", "2", "3", "1.2 (5) V", "800 mA", "45 V"))

    components.append(NPNBJT("BC517", "1", "2", "3", "1.4 (10) V", "1.2 A", "30 V"))
    components.append(NPNBJT("BC547", "1", "2", "3", "0.9 (6) V", "100 mA", "45 V"))
    components.append(NPNBJT("BC548", "1", "2", "3", "0.9 (5) V", "100 mA", "30 V"))
    components.append(NPNBJT("BC549", "1", "2", "3", "0.9 (5) V", "100 mA", "30 V"))
    components.append(NPNBJT("BC550", "1", "2", "3", "0.9 (5) V", "100 mA", "45 V"))
    components.append(PNPBJT("BC556", "1", "2", "3", "-1 (-5) V", "-100 mA", "-65 V"))
    components.append(PNPBJT("BC557", "1", "2", "3", "-1 (-5) V", "-100 mA", "-45 V"))
    components.append(PNPBJT("BC588", "1", "2", "3", "-1 (-5) V", "-100 mA", "-30 V"))

    # MOSFETs

    components.append(NMOSFET("IRF520", "1", "2", "3", "2..4 V", "6.5 A", "100 V"))
    components.append(PMOSFET("IRF9520", "1", "2", "3", "-2..4 V", "-4.8 A", "-100 V"))
    components.append(NMOSFET(Label("DMN2040U", .75), "1", "3", "2", "0.5..1.2 V", "6 A", "20 V"))
    components.append(PMOSFET(Label("DMP2123L", .75), "1", "3", "2", "-0.6..1.3 V", "-3 A", "-20 V"))
    components.append(NMOSFET(Label("AO3400A", .8), "1", "3", "2", "0.7..1.4 V", "5 A", "30 V"))
    components.append(PMOSFET(Label("AO3401A", .8), "1", "3", "2", "-0.4..1.3 V", "-4 A", "-30 V"))

    # Diodes

    components.append(Diode("1N4001", "1.1 V", "1 A", "50 V"))
    components.append(Diode("1N4148W", "1 V", "300 mA", "75 V"))
    components.append(Diode("1N4148", "1 V", "300 mA", "75 V"))
    components.append(Diode("1N4007", "1.1 V", "1 A", "1 kV"))

    # Schottky Diodes

    components.append(SchottkyDiode(Label("PMEG3050", .8), "360 mV", "5 A", "40 V"))
    components.append(SchottkyDiode("BAT41", "400 mV", "100 mA", "100 V"))
    components.append(SchottkyDiode("1N5819", "600 mV", "1 A", "40 V"))
    components.append(SchottkyDiode("BAT85", "400 mV", "200 mA", "30 V"))
    components.append(SchottkyDiode("BAT54S", "800 mV", "0.2 A", "30 V"))

    # Zener Diodes

    components.append(ZenerDiode("ZPD3V6", "3.4-3.8 V", "5 mA", "1 V"))

    # LEDs

    components.append(LED("5 mm", "1.2 V", "20 mA", "940 nm", HexColor("#800000")))
    components.append(LED("5 mm", "3.0-3.2 V", "20 mA", "* nm", HexColor("#FFFFFF")))
    components.append(LED("5 mm", "1.9-2.1 V", "20 mA", "620-625 nm", HexColor("#FF0000")))
    components.append(LED("5 mm", "1.9-2.1 V", "20 mA", "610-615 nm", HexColor("#FFAA00")))
    components.append(LED("5 mm", "1.9-2.1 V", "20 mA", "588-590 nm", HexColor("#FFFF00")))
    components.append(LED("5 mm", "2.1-3.0 V", "20 mA", "567-570 nm", HexColor("#00FF00")))
    components.append(LED("5 mm", "3.0-3.2 V", "20 mA", "455-465 nm", HexColor("#0000FF")))

    components.append(LED("3 mm", "3.0-3.2 V", "20 mA", "* nm", HexColor("#FFFFFF")))
    components.append(LED("3 mm", "1.9-2.1 V", "20 mA", "620-625 nm", HexColor("#FF0000")))
    components.append(LED("3 mm", "1.9-2.1 V", "20 mA", "588-590 nm", HexColor("#FFFF00")))
    components.append(LED("3 mm", "2.1-3.0 V", "20 mA", "567-570 nm", HexColor("#00FF00")))
    components.append(LED("3 mm", "3.0-3.2 V", "20 mA", "455-465 nm", HexColor("#0000FF")))

    # Diodes that emit light of the SMD variety

    components.append(LED("0603", "2.3 V", "20 mA", "625 nm", HexColor("#FF0000")))
    components.append(LED("0603", "3.3 V", "20 mA", "626 nm", HexColor("#00FF00")))
    components.append(LED("0603", "3.3 V", "20 mA", "470 nm", HexColor("#0000FF")))
    components.append(LED("2020", "2/2.7/2.8 V", "8/5/3 mA", "622/525/468 nm", HexColor("#FFFFFF")))
    components.append(LED("3528", "5 V", "12 mA", "625/525/470 nm", HexColor("#FFFFFF")))

    # Springs

    components.append(ExtensionSpring("5 mm", "20.5 mm"))
    components.append(ExtensionSpring("5.5 mm", "25.5 mm"))
    components.append(ExtensionSpring("6.5 mm", "22 mm"))
    components.append(ExtensionSpring("8.5 mm", "47 mm"))
    components.append(ExtensionSpring("7 mm", "51 mm"))
    components.append(ExtensionSpring("7 mm", "38 mm"))
    components.append(ExtensionSpring("8.5 mm", "36.5 mm"))
    components.append(ExtensionSpring("8 mm", "28.5 mm"))
    components.append(ExtensionSpring("8 mm", "31.5 mm"))
    components.append(ExtensionSpring("8 mm", "44.5 mm"))
    components.append(ExtensionSpring("4 mm", "79.5 mm"))
    components.append(ExtensionSpring("4.5 mm", "44.5 mm"))

    components.append(CompressionSpring("7 mm", "12.5 mm"))
    components.append(CompressionSpring("6.5 mm", "10 mm"))
    components.append(CompressionSpring("7 mm", "19 mm"))
    components.append(CompressionSpring("5.5 mm", "38 mm"))
    components.append(CompressionSpring("9.5 mm", "16 mm"))
    components.append(CompressionSpring("9.5 mm", "19 mm"))
    components.append(CompressionSpring("9 mm", "35 mm"))
    components.append(CompressionSpring("5.5 mm", "17 mm"))

    # Threaded inserts

    components.append(ThreadedInsert("M2", "3.2 mm", "3 mm"))
    components.append(ThreadedInsert("M2", "3.5 mm", "3 mm"))
    components.append(ThreadedInsert("M2", "3.5 mm", "4 mm"))
    components.append(ThreadedInsert("M2", "3.5 mm", "5 mm"))
    components.append(ThreadedInsert("M2.5", "3.5 mm", "3 mm"))
    components.append(ThreadedInsert("M2.5", "3.5 mm", "4 mm"))
    components.append(ThreadedInsert("M2.5", "3.5 mm", "5 mm"))
    components.append(ThreadedInsert("M3", "4.5 mm", "3 mm"))
    components.append(ThreadedInsert("M3", "4.5 mm", "4 mm"))
    components.append(ThreadedInsert("M3", "5 mm", "4 mm"))
    components.append(ThreadedInsert("M3", "5 mm", "5 mm"))

    # Round head screws

    components.append(RoundHeadScrew("M2", "4 mm", "1.7 mm", "5 mm")) # Length is a separate parameter
    components.append(RoundHeadScrew("M2", "4 mm", "1.7 mm", "6 mm"))
    components.append(RoundHeadScrew("M2", "4 mm", "1.7 mm", "8 mm"))


    components.append(RoundHeadScrew("M2x5", "4 mm", "1.7 mm")) # Length is part of the name for easier searching
    components.append(RoundHeadScrew("M2x6", "4 mm", "1.7 mm"))
    components.append(RoundHeadScrew("M2x8", "4 mm", "1.7 mm"))

    components.append(RoundHeadScrew("M2.5", "5 mm", "2.4 mm", "6 mm"))
    components.append(RoundHeadScrew("M2.5", "5 mm", "2.4 mm", "8 mm"))
    components.append(RoundHeadScrew("M2.5", "5 mm", "2.4 mm", "12 mm"))
    components.append(RoundHeadScrew("M2.5", "5 mm", "2.4 mm", "16 mm"))
    components.append(RoundHeadScrew("M2.5", "5 mm", "2.4 mm", "20 mm"))

    components.append(RoundHeadScrew("M2.5x6", "5 mm", "2.4 mm"))
    components.append(RoundHeadScrew("M2.5x8", "5 mm", "2.4 mm"))
    components.append(RoundHeadScrew("M2.5x12", "5 mm", "2.4 mm"))
    components.append(RoundHeadScrew("M2.5x16", "5 mm", "2.4 mm"))
    components.append(RoundHeadScrew("M2.5x20", "5 mm", "2.4 mm"))

    components.append(RoundHeadScrew("M3", "6 mm", "2.6 mm", "6 mm"))
    components.append(RoundHeadScrew("M3", "6 mm", "2.6 mm", "12 mm"))
    components.append(RoundHeadScrew("M3", "6 mm", "2.6 mm", "16 mm"))
    components.append(RoundHeadScrew("M3", "6 mm", "2.6 mm", "20 mm"))

    components.append(RoundHeadScrew("M3x6", "6 mm", "2.6 mm"))
    components.append(RoundHeadScrew("M3x6", "6 mm", "2.6 mm"))
    components.append(RoundHeadScrew("M3x8", "6 mm", "2.6 mm"))
    components.append(RoundHeadScrew("M3x10", "6 mm", "2.6 mm"))
    components.append(RoundHeadScrew("M3x12", "6 mm", "2.6 mm"))
    components.append(RoundHeadScrew("M3x12", "6 mm", "2.6 mm"))
    components.append(RoundHeadScrew("M3x16", "6 mm", "2.6 mm"))
    components.append(RoundHeadScrew("M3x20", "6 mm", "2.6 mm"))
    components.append(RoundHeadScrew("M3x30", "6 mm", "2.6 mm"))

    components.append(RoundHeadScrew("M5", "10 mm", "4.2 mm", "6 mm"))
    components.append(RoundHeadScrew("M5", "10 mm", "4.2 mm", "30 mm"))

    components.append(RoundHeadScrew("M5x6", "10 mm", "4.2 mm"))
    components.append(RoundHeadScrew("M5x12", "10 mm", "4.2 mm"))
    components.append(RoundHeadScrew("M5x20", "10 mm", "4.2 mm"))
    components.append(RoundHeadScrew("M5x25", "10 mm", "4.2 mm"))
    components.append(RoundHeadScrew("M5x30", "10 mm", "4.2 mm"))

    # Flat head9  screws

    components.append(FlatHeadScrew("M2.5", "4.4 mm", "1.8 mm", "12 mm"))
    components.append(FlatHeadScrew("M2.5", "4.4 mm", "1.8 mm", "14 mm"))
    components.append(FlatHeadScrew("M2.5", "4.4 mm", "1.8 mm", "16 mm"))
    components.append(FlatHeadScrew("M2.5x12", "4.4 mm", "1.8 mm"))
    components.append(FlatHeadScrew("M2.5x14", "4.4 mm", "1.8 mm"))
    components.append(FlatHeadScrew("M2.5x16", "4.4 mm", "1.8 mm"))

    components.append(FlatHeadScrew("M2.5x4", "4.6 mm", "2 mm"))
    components.append(FlatHeadScrew("M2x4", "3.8 mm", "1.6 mm"))

    # Recessed head screws

    components.append(RecessedHeadScrew("M2x1.5", "3.5 mm", "1.5 mm"))
    components.append(RecessedHeadScrew("M2x2.5", "3.5 mm", "1.5 mm"))
    components.append(RecessedHeadScrew("M2x3.5", "3.5 mm", "1.5 mm"))
    components.append(RecessedHeadScrew("M2x5.5", "3.5 mm", "1.5 mm"))
    components.append(RecessedHeadScrew("M2.5x2", "4.5 mm", "1.5 mm"))
    components.append(RecessedHeadScrew("M2.5x2.5", "4.5 mm", "1.5 mm"))
    components.append(RecessedHeadScrew("M2.5x3.5", "4.5 mm", "1.5 mm"))
    components.append(RecessedHeadScrew("M2.5x5", "4.5 mm", "1.5 mm"))
    components.append(RecessedHeadScrew("M2.5x7", "4.5 mm", "1.5 mm"))
    components.append(RecessedHeadScrew("M3", "5.6 mm", "2 mm", "7 mm"))
    components.append(RecessedHeadScrew("M3x3", "5 mm", "2 mm"))
    components.append(RecessedHeadScrew("M3x7", "5.6 mm", "2 mm"))

    # Hex nuts

    components.append(HexNut("M2", "1.8 mm", "4 mm", "4.5 mm"))
    components.append(HexNut("M2.5", "2 mm", "5 mm", "5.7 mm"))
    components.append(HexNut("M3", "2.2 mm", "5.5 mm", "6.3 mm"))
    components.append(HexNut("M5", "4 mm", "8 mm", "9 mm"))

    # Square nuts

    components.append(SquareNut("M3", "1.8 mm", "5.4 mm", "7.2 mm"))
    components.append(SquareNut("M4", "2.2 mm", "6.8 mm", "9.4 mm"))
    components.append(SquareNut("M5", "3 mm", "8 mm", "11.3 mm"))

    # Washers

    components.append(Washer("M2.5", "0.6 mm", "6 mm"))
    components.append(Washer("M3", "0.6 mm", "7 mm"))
    components.append(Washer("M5", "1.1 mm", "10 mm"))

    # These labels are useful for "random garbage" bags

    components.append(LED("???", "??? V", "??? mA", "??? nm", HexColor("#FFC0C0")))
    components.append(Diode("???", "? V", "??? mA", "??? V"))
    components.append(NPNBJT("???", "?", "?", "?", "??? V", "??? A", "??? V"))

    # Polyfuses

    components.append(Polyfuse("6 V", "1 A", "1206"))
    components.append(Polyfuse("6 V", "1.5 A", "1206"))
    components.append(Polyfuse("12 V", "2 A", "1206"))
    components.append(Polyfuse("9 V", "0.2 A", "0603"))

    # TVS Diodes

    components.append(TVSDiode("PSM712"))
    components.append(TVSDiode("1.5KE27A"))

    # Generic single-sided text labels

    components.append(Generic("16x2 char LCD\nHD44780-compatible\n5 V, no backlight").single_side())

    components.append(Generic(Label("40x4 char LCD\nWH4004A-YGH-ET#\nHD44780-compatible\n5 V, green backlight", 0.9)).single_side())

    components.append(Generic(Label("40x2 char LCD\nDMC2079\nHD44780-compatible\n5 V, green backlight", 0.9)).single_side())

    components.append(Generic("16x2 char LCD\nHD44780-compatible\n5 V, green backlight").single_side())

    components.append(Generic("12x2 char LCD\nHD44780-compatible\n3.3 V, green backlight").single_side())

    components.append(Generic("20x4 char LCD\nHD44780-compatible\n5 V, blue backlight").single_side())

    components.append(Generic(Label("6.2\" 360x960 IPS\nER-TFT062-1-3723\nGC9503V\n2.8 V, 12 V backlight", 0.9)).single_side())

    components.append(Generic(Label("4.58\" 360x960 IPS\nER-TFT4.58-1-3723\nST7701S\n2.8 V, 12 V backlight", 0.9)).single_side())

    components.append(Generic(Label("2.2\" 132x32 OLED\nRET013232A\nSSD1305\n3.3 V, yellow dots", 0.9)).single_side())

    components.append(Generic(Label("84x48 LCD\nYeeted from Nokia 5110\nPCD8544\n3.3 V, white backlight", 0.9)).single_side())

    components.append(Generic(Label("3.95\" 720x720 IPS\nER-TFT3.95-1\nNV3052C\n2.8 V, 15 V backlight", 0.9)).single_side())

    components.append(Generic(Label("2.9\" 128x64 LCD\nERMC12864FS-2\nAIP31108\n3.3 V, white backlight", 0.9)).single_side())

    components.append(Generic(Label("1.7\" 128x64 LCD\nERM12864FSF-9\nST7567\n3.3 V, white backlight", 0.9)).single_side())

    components.append(Generic(Label("2\" 192x64 LCD\nERM19264FS-4\nUC1609C\n3.3 V, white backlight", 0.9)).single_side())

    components.append(Generic(Label("2.2\" 128x32 OLED\nER-OLED022-1W\nSSD1305\n3.3 V, white dots", 0.9)).single_side())

    components.append(Generic(Label("16x2 char LCD\nERC1602FS-4\nST7032i\n3.3-5 V, 3 V 15 mA white bl.", 0.9)).single_side())

    components.append(Generic("96x68 LCD\nHX1230\n3.3-5 V, white backlight").single_side())

    components.append(Generic("0.66\" 64x48 OLED\nSSD1306\n3.3 V, white dots").single_side())

    components.append(Generic(Label("1.54\" 152x152 Eink\nGDEW0154T8D\nUC8151D\n3.3 V, no backlight", 0.9)).single_side())

    components.append(Generic("1.28\" 128x128 memory LCD\nLS013B7DH03\n3 V, no backlight").single_side())

    # ############################################################################
    # Further configuration options
    #
    # Change the following options as you desire.
    # ############################################################################

    # Draws the line where the stickers should be folded.
    # Disable this if you don't like the line.
    draw_center_line = True

    # Draw the outlines of the stickers.
    # This is primarily a debugging option and should most likely not be enabled
    # for the actual printing.
    draw_outlines = False

    # ############################################################################
    # PDF generation
    #
    # The following is the actual functionality of this script - to generate
    # the ComponentLabels PDF file.
    # ############################################################################

    # Create the render canvas
    c = Canvas(args.output, pagesize=layout.pagesize)

    # Render the stickers
    render_stickers(c, layout, components, draw_outlines, draw_center_line)

    # Store canvas to PDF file
    c.save()
