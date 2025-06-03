from typing import Optional

import flet as ft


class _Text(ft.Text):
    def __init__(
        self,
        value: Optional[str] = None,
        text_align: Optional[ft.TextAlign] = None,
    ) -> None:
        super().__init__()
        self.value = value
        self.text_align = text_align
        self.weight = ft.FontWeight.W_100


class Title(_Text):
    def __init__(
        self,
        value: Optional[str] = None,
        text_align: Optional[ft.TextAlign] = ft.TextAlign.CENTER,
    ) -> None:
        super().__init__(value, text_align)
        self.color = "primary"
        self.size = 76


class Subtitle(_Text):
    def __init__(
        self,
        value: Optional[str] = None,
        text_align: Optional[ft.TextAlign] = ft.TextAlign.CENTER,
    ) -> None:
        super().__init__(value, text_align)
        self.color = "outline"
        self.size = 60


class RegularText(_Text):
    def __init__(
        self,
        value: Optional[str] = None,
        text_align: Optional[ft.TextAlign] = ft.TextAlign.CENTER,
        size: int = 48,
    ) -> None:
        super().__init__(value, text_align)
        self.color = "outline"
        self.size = size
