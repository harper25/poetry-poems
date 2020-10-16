# -*- coding: utf-8 -*-
from ..utils import collapse_path
from .colors import colors


class Line:

    RIGHT_MARGIN = 2

    def __init__(self, text=None, color=None, pad=0):
        self._text = text
        self.color_name = color
        self.pad = pad

    @property
    def text(self):
        return " " * self.pad + self._text

    def render(self, screen, x, y):
        max_y, max_x = screen.getmaxyx()
        max_width = max_x - Line.RIGHT_MARGIN
        color_name = self.color_name
        color_pair = 0 if not color_name else colors[color_name].as_pair
        screen.addnstr(y, x, self.text, max_width, color_pair)


class EnvLine(Line):

    SELECTED_STR = "●"
    UNSELECTED_STR = " " * len(SELECTED_STR)
    UNSET_DIR_STR = "-- Not Set --"

    def __init__(self, env=None, **kwargs):
        self.env = env
        self.selected = kwargs.pop("selected")
        self.expanded = kwargs.pop("expanded")
        super().__init__(env.envname, **kwargs)

    @property
    def text(self):
        prefix = self.SELECTED_STR if self.selected else self.UNSELECTED_STR
        text = self.env.envname

        try:
            if self.expanded == 0:
                pass
            if self.expanded == 1:
                text = f"{text} ({collapse_path(self.env.envpath)})"
            if self.expanded == 2:
                text = f"{text} ({collapse_path(self.env.binpath)})"
        except EnvironmentError as e:
            text = f"{text} ({str(e)})"

        return f"{prefix} {text}"
