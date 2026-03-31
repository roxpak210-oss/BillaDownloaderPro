import flet as ft
import yt_dlp
import os
import threading

def main(page: ft.Page):
    # --- Page Config ---
    page.title = "Billa Downloader 🐱"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- UI Elements ---
    url_input = ft.TextField(
        label="Paste Video Link",
        hint_text="YouTube, Facebook, or Instagram...",
        border_color="#FF9500",
        expand=True,
        prefix_icon="link"
    )

    video_list = ft.Column(spacing=10)

    def start_download(e):
        url = url_input.value.strip()
        if not url: return

        # UI Progress Card
        status_text = ft.Text("Hunting...", size=12, color="#AAAAAA")
        new_card = ft.Card(
            content=ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon("pets", color="#FF9500"),
                    title=ft.Text("Downloading Video..."),
                    subtitle=status_text,
                ), padding=10
            )
        )
        video_list.controls.insert(0, new_card)
        url_input.value = ""
        page.update()

        def dl_worker():
            # For Android, we save to the public Downloads folder
            # On Windows, this also saves to your user Downloads
            download_path = os.path.join(os.path.expanduser("~"), "Downloads", "%(title)s.%(ext)s")
            
            ydl_opts = {
                'format': 'best',
                'nocheckcertificate': True,
                'outtmpl': download_path,
                'noplaylist': True,
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                status_text.value = "✅ Finished! Check Downloads"
                new_card.content.content.leading.color = "green"
                new_card.content.content.leading.name = "check_circle"
            except Exception as ex:
                status_text.value = "❌ Download Failed"
            page.update()

        threading.Thread(target=dl_worker, daemon=True).start()

    # --- Build Layout ---
    page.add(
        ft.Column([
            ft.Row([
                ft.Text("Billa Pro", size=32, weight="bold", color="#FF9500"),
                ft.Icon("pets", color="#FF9500")
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                url_input,
                ft.IconButton(
                    icon="download",
                    on_click=start_download,
                    icon_color="#FF9500",
                    bgcolor="#222222"
                )
            ]),
            ft.Divider(height=30, color="#444444"),
            ft.Text("Recent History", size=16, weight="bold", color="#777777"),
            video_list
        ])
    )

if __name__ == "__main__":
    # Use run() for modern Flet compatibility
    ft.run(main)