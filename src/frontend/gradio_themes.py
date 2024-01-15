from __future__ import annotations

from typing import Iterable

from gradio.themes.soft import Soft
from gradio.themes import Size
from gradio.themes.utils import colors, sizes, fonts

text_xsm = Size(
    name="text_xsm",
    xxs="4px",
    xs="5px",
    sm="6px",
    md="7px",
    lg="8px",
    xl="10px",
    xxl="12px",
)

spacing_xsm = Size(
    name="spacing_xsm",
    xxs="1px",
    xs="1px",
    sm="1px",
    md="2px",
    lg="3px",
    xl="5px",
    xxl="7px",
)

radius_xsm = Size(
    name="radius_xsm",
    xxs="1px",
    xs="1px",
    sm="1px",
    md="2px",
    lg="3px",
    xl="5px",
    xxl="7px",
)


class SoftTheme(Soft):
    def __init__(
            self,
            *,
            primary_hue: colors.Color | str = colors.indigo,
            secondary_hue: colors.Color | str = colors.indigo,
            neutral_hue: colors.Color | str = colors.gray,
            spacing_size: sizes.Size | str = sizes.spacing_md,
            radius_size: sizes.Size | str = sizes.radius_md,
            text_size: sizes.Size | str = sizes.text_md,
            font: fonts.Font
                  | str
                  | Iterable[fonts.Font | str] = (
                    fonts.GoogleFont("Montserrat"),
                    "ui-sans-serif",
                    "system-ui",
                    "sans-serif",
            ),
            font_mono: fonts.Font
                       | str
                       | Iterable[fonts.Font | str] = (
                    fonts.GoogleFont("IBM Plex Mono"),
                    "ui-monospace",
                    "Consolas",
                    "monospace",
            ),
    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,
        )
        super().set(
            checkbox_label_text_size="*text_sm",
        )


def get_simple_title(title, description):
    return f"""{description}<h1 align="center"> {title}</h1>"""


def get_dark_js() -> str:
    return """
        if (document.querySelectorAll('.dark').length) {
            document.querySelectorAll('.dark').forEach(el => el.classList.remove('dark'));
        } else {
            document.querySelector('body').classList.add('dark');
        }
    """


def wrap_js_to_lambda(num_params: int, *args: str) -> str:
    """
    Generates a JS code representing JS lambda that wraps all given '*args' code strings.
    The lambda function has number of parameters based on 'num_params' and returns them
    without modification in an array. Lambda with zero parameters returns an empty array.
    """
    params = ", ".join([f"p{i}" for i in range(num_params)])
    newline = "\n"
    return f"""
        ({params}) => {{
            {newline.join([a for a in args if a is not None])}
            return [{params}];
        }}
    """
