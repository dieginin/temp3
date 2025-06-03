import flet as ft

from controllers import Updater
from version import VERSION


def main(page: ft.Page) -> None:
    page.title = f"MiApp v{VERSION}"
    page.add(ft.Text(f"App version {VERSION}"))

    Updater(page)


ft.app(main)
