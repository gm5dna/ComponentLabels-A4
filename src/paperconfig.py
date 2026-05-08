from reportlab.lib.pagesizes import A4, LETTER
from reportlab.lib.units import inch, mm
from typing import Dict, List, Set, Tuple

class PaperConfig:
    def __init__(
        self,
        paper_name: str,
        pagesize: Tuple[float, float],
        sticker_width: float,
        sticker_height: float,
        sticker_corner_radius: float,
        left_margin: float,
        top_margin: float,
        horizontal_stride: float,
        vertical_stride: float,
        num_stickers_horizontal: int,
        num_stickers_vertical: int,
    ) -> None:
        self.paper_name = paper_name
        self.pagesize = pagesize
        self.sticker_width = sticker_width
        self.sticker_height = sticker_height
        self.sticker_corner_radius = sticker_corner_radius
        self.left_margin = left_margin
        self.top_margin = top_margin
        self.horizontal_stride = horizontal_stride
        self.vertical_stride = vertical_stride
        self.num_stickers_horizontal = num_stickers_horizontal
        self.num_stickers_vertical = num_stickers_vertical


AVERY_5260 = PaperConfig(
    paper_name="Avery 5260",
    pagesize=LETTER,
    sticker_width=(2 + 5/8) * inch,
    sticker_height=1 * inch,
    sticker_corner_radius=0.1 * inch,
    left_margin=3/16 * inch,
    top_margin=0.5 * inch,
    horizontal_stride=(2 + 6/8) * inch,
    vertical_stride=1 * inch,
    num_stickers_horizontal=3,
    num_stickers_vertical=10,
)


AVERY_L7157 = PaperConfig(
    paper_name="Avery L7157",
    pagesize=A4,
    sticker_width=64 * mm,
    sticker_height=24.3 * mm,
    sticker_corner_radius=3 * mm,
    left_margin=6.4 * mm,
    top_margin=14.1 * mm,
    horizontal_stride=66.552 * mm,
    vertical_stride=24.3 * mm,
    num_stickers_horizontal=3,
    num_stickers_vertical=11,
)


AVERY_J8157 = PaperConfig(
    paper_name="Avery J8157",
    pagesize=A4,
    sticker_width=64.1 * mm,
    sticker_height=24.3 * mm,
    sticker_corner_radius=3 * mm,
    left_margin=5.4 * mm,
    top_margin=14 * mm,
    horizontal_stride=66.5 * mm,
    vertical_stride=24.3 * mm,
    num_stickers_horizontal=3,
    num_stickers_vertical=11,
)


EJ_RANGE_24 = PaperConfig(
    paper_name="EJRange 24",
    pagesize=A4,
    sticker_width=63.5 * mm,
    sticker_height=33.9 * mm,
    sticker_corner_radius=2 * mm,
    left_margin=6.5 * mm,
    top_margin=13.2 * mm,
    horizontal_stride=66.45 * mm,
    vertical_stride=33.9 * mm,
    num_stickers_horizontal=3,
    num_stickers_vertical=8,
)


VYSOCINA = PaperConfig( # Available from: https://www.obalyvysocina.cz/produkty/samolepici-etikety#70x254-mm3300-ks
    paper_name="Samolepky z Vysočiny",
    pagesize=A4,
    sticker_width=62 * mm,
    sticker_height=24 * mm,
    sticker_corner_radius=0,
    left_margin=4 * mm,
    top_margin=8.8 * mm,
    horizontal_stride=70 * mm,
    vertical_stride=25.4 * mm,
    num_stickers_horizontal=3,
    num_stickers_vertical=11
)


# Avery L7159 (and physically-equivalent variants: inkjet J8159, EU LR7159).
# A4, 24 labels per sheet (3 columns x 8 rows), 63.5 x 33.9 mm each.
# Margins are LabelPlanet's measured values for this Avery template
# (top 12.9 mm, left 7.25 mm). Corner radius is estimated (Avery only
# states "rounded corners"). Verify against an actual sheet using
# scripts/check_alignment.py before committing to a box of labels.
# Note: same physical label size as EJ_RANGE_24 but Avery's margins
# differ, so this is a separate preset.
AVERY_L7159 = PaperConfig(
    paper_name="Avery L7159",
    pagesize=A4,
    sticker_width=63.5 * mm,
    sticker_height=33.9 * mm,
    sticker_corner_radius=2 * mm,
    left_margin=7.25 * mm,
    top_margin=12.9 * mm,
    horizontal_stride=66 * mm,
    vertical_stride=33.9 * mm,
    num_stickers_horizontal=3,
    num_stickers_vertical=8,
)


# Avery L7160 (and physically-equivalent inkjet variant J8160).
# A4, 21 labels per sheet (3 columns x 7 rows), 63.5 x 38.1 mm each.
# This is one of the most widely-stocked label sheets in the UK.
# Margins/stride taken from Avery's published L7160 dimensions; verify
# against an actual sheet using scripts/check_alignment.py before
# committing to a box of labels.
AVERY_L7160 = PaperConfig(
    paper_name="Avery L7160",
    pagesize=A4,
    sticker_width=63.5 * mm,
    sticker_height=38.1 * mm,
    sticker_corner_radius=2 * mm,
    left_margin=7.21 * mm,
    top_margin=15.1 * mm,
    horizontal_stride=66 * mm,
    vertical_stride=38.1 * mm,
    num_stickers_horizontal=3,
    num_stickers_vertical=7,
)


# Lookup table for the --layout CLI flag. Keys are normalised to upper-case
# at lookup time, so users may pass "L7160", "l7160", or "AVERY_L7160".
# J8160 is an alias for L7160 (same physical layout, different Avery SKU).
LAYOUTS: Dict[str, PaperConfig] = {
    "5260": AVERY_5260,
    "AVERY_5260": AVERY_5260,
    "L7157": AVERY_L7157,
    "AVERY_L7157": AVERY_L7157,
    "J8157": AVERY_J8157,
    "AVERY_J8157": AVERY_J8157,
    "L7159": AVERY_L7159,
    "AVERY_L7159": AVERY_L7159,
    "J8159": AVERY_L7159,
    "LR7159": AVERY_L7159,
    "LL24": AVERY_L7159,
    "L7160": AVERY_L7160,
    "AVERY_L7160": AVERY_L7160,
    "J8160": AVERY_L7160,
    "LL21": AVERY_L7160,
    "EJ24": EJ_RANGE_24,
    "EJ_RANGE_24": EJ_RANGE_24,
    "VYSOCINA": VYSOCINA,
}


def resolve_layout(name: str) -> PaperConfig:
    """Look up a layout by case-insensitive name. Raises KeyError if unknown."""
    return LAYOUTS[name.upper()]


def list_layout_names() -> str:
    """Return a human-readable list of available layouts for --list-layouts and error messages."""
    aliases_by_id: Dict[int, List[str]] = {}
    for key, cfg in LAYOUTS.items():
        aliases_by_id.setdefault(id(cfg), []).append(key)

    lines: List[str] = []
    seen_ids: Set[int] = set()
    for cfg in LAYOUTS.values():
        if id(cfg) in seen_ids:
            continue
        seen_ids.add(id(cfg))
        names = ", ".join(aliases_by_id[id(cfg)])
        page = "A4" if cfg.pagesize == A4 else ("Letter" if cfg.pagesize == LETTER else "?")
        grid = f"{cfg.num_stickers_horizontal}x{cfg.num_stickers_vertical}"
        size = f"{cfg.sticker_width / mm:.1f} x {cfg.sticker_height / mm:.1f} mm"
        lines.append(f"  {names:<32} {cfg.paper_name:<24} {page}  {grid:<5}  {size}")
    return "\n".join(lines)
