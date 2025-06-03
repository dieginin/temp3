import os
import platform
import subprocess
import tempfile
import time
from random import uniform
from typing import Callable, Optional

import flet as ft
import requests

from components import Subtitle as Text
from components import accept_dialog, error_snackbar, info_snackbar, success_snackbar
from version import VERSION


def get_latest_version() -> tuple[str, str]:
    GITHUB_REPO = "dieginin/temp2"
    API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

    response = requests.get(API_URL)

    if response.status_code == 200:
        data = response.json()
        version = data["tag_name"].replace("v", "")
        assets = data.get("assets", [])
        download_url = ""

        current_os = platform.system()
        if current_os == "Windows":
            for asset in assets:
                if asset["name"].endswith(".msi"):
                    download_url = asset["browser_download_url"]
                    break
        elif current_os == "Darwin":
            for asset in assets:
                if asset["name"].endswith(".dmg"):
                    download_url = asset["browser_download_url"]
                    break

        return version, download_url
    raise Exception("Could not fetch latest version")


class Updater:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.check_for_updates()

    def check_for_updates(self) -> None:
        parse_version = lambda v: tuple(map(int, v.split(".")))

        info_snackbar(self.page, "Checking for updates...")
        time.sleep(uniform(0, 1))

        try:
            latest_version, download_url = get_latest_version()
            if parse_version(latest_version) > parse_version(VERSION):
                accept_dialog(
                    self.page,
                    "Update Available",
                    ft.Text(f"A new version {latest_version} is available"),
                    on_accept=lambda: self.start_update(latest_version, download_url),
                    accept_txt="Update",
                )
            else:
                success_snackbar(self.page, "You are already on the latest version")
        except Exception as e:
            error_snackbar(self.page, f"Error: {e}")

    def start_update(self, latest_version: str, download_url: str) -> None:
        def update_progress(value: Optional[float]) -> None:
            progress.value = value
            if value is not None:
                status.value = f"Downloading update\nv{latest_version}... {float(value * 100):.1f}%"
            else:
                status.value = "Download complete\nRunning installer..."
            self.page.update()

        time.sleep(0.05)
        self.page.clean()
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.title = "Updating..."
        progress = ft.ProgressBar(width=500)
        status = Text("Preparing to download update...")
        self.page.add(status, progress)
        time.sleep(uniform(0, 1))

        status.value = f"Downloading update\nv{latest_version}... 0%"
        self.page.update()

        try:
            filepath = download_update(download_url, update_progress)
            update_progress(None)
            time.sleep(uniform(0, 3))
            self.run_installer(filepath)
        except:
            error_snackbar(self.page, "Failed to download update")

    def run_installer(self, filepath: str) -> None:
        try:
            current_os = platform.system()
            if current_os == "Windows":
                subprocess.Popen([filepath])
            elif current_os == "Darwin":
                os.system(f"open '{filepath}'")

            try:
                time.sleep(uniform(0, 1))
                os.remove(filepath)
                self.page.window.close()
            except:
                error_snackbar(self.page, "Error deleting installer")
        except:
            error_snackbar(self.page, "Failed to run installer")


def download_update(url: str, progress_callback: Callable) -> str:
    local_filename = os.path.basename(url)
    filepath = os.path.join(tempfile.gettempdir(), local_filename)

    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress_callback(downloaded / total_size)
    return filepath
