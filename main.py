import flet as ft
import yt_dlp

def main(page: ft.Page):
    page.title = "Billa Downloader"
    page.theme_mode = ft.ThemeMode.DARK
    page.add(ft.Text("Billa Downloader Pro is Ready!"))

ft.app(target=main)
