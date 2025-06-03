from typing import Optional

import flet as ft


class _SnackBar(ft.SnackBar):
    def __init__(
        self,
        page: ft.Page,
        message: str,
        color: Optional[ft.ColorValue] = None,
        bgcolor: Optional[ft.ColorValue] = None,
    ) -> None:
        super().__init__(
            content=ft.Text(message, text_align=ft.TextAlign.CENTER, color=color),
            bgcolor=bgcolor,
            show_close_icon=True,
        )
        self.page: ft.Page = page

    def show(self) -> None:
        self.page.open(self)


def success_snackbar(page: ft.Page, message: str) -> None:
    _SnackBar(page, message, color="on_primary", bgcolor="primary").show()


def error_snackbar(page: ft.Page, message: str) -> None:
    _SnackBar(page, message, color="on_error", bgcolor="error").show()


def info_snackbar(page: ft.Page, message: str) -> None:
    _SnackBar(page, message, color="on_secondary", bgcolor="secondary").show()
