import flet as ft

from config import VERSION
from controllers import Updater


def main(page: ft.Page) -> None:
    page.title = f"MiApp v{VERSION}"
    page.add(ft.Text(f"App version {VERSION}"))

    Updater(page)


ft.app(main)
