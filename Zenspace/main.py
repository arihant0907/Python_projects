import flet as ft
import time

def main(page: ft.Page):
    page.title = "ZenSpace - Focus & Breathe"
    page.window_width = 380
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0

    # 1. Background Gradient Container
    bg_container = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=[ft.Colors.BLUE_900, ft.Colors.PURPLE_900],
        ),
        padding=30,
    )

    # 2. The Breathing Circle (Animation)
    breathing_circle = ft.Container(
        width=150,
        height=150,
        border_radius=75,
        border=ft.border.all(2, ft.Colors.WHITE24),
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        animate=ft.Animation(4000, ft.AnimationCurve.EASE_IN_OUT),
        content=ft.Text("Inhale", size=16, weight=ft.FontWeight.W_300),
        alignment=ft.Alignment.CENTER,
    )

    def start_breathing(e):
        # A simple loop to simulate breathing expansion
        if breathing_circle.width == 150:
            breathing_circle.width = 250
            breathing_circle.height = 250
            breathing_circle.border_radius = 125
            breathing_circle.content.value = "Exhale"
            breathing_circle.bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.CYAN_200)
        else:
            breathing_circle.width = 150
            breathing_circle.height = 150
            breathing_circle.border_radius = 75
            breathing_circle.content.value = "Inhale"
            breathing_circle.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
        page.update()

    # 3. Ambient Sound Toggles (Unique UI)
    def create_sound_chip(label, icon):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, color=ft.Colors.WHITE70),
                ft.Text(label, size=10, color=ft.Colors.WHITE70)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=80,
            height=80,
            border_radius=15,
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE10),
            on_click=lambda _: print(f"Playing {label}...")
        )

    # 4. Final Layout Construction
    bg_container.content = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row([ft.IconButton(ft.Icons.MENU_ROUNDED, icon_color=ft.Colors.WHITE)], alignment=ft.MainAxisAlignment.START),
            ft.Container(height=40),
            ft.Text("Peace of Mind", size=32, weight=ft.FontWeight.BOLD),
            ft.Text("Select your focus frequency", color=ft.Colors.WHITE70),
            ft.Container(height=60),
            
            # Interactive Animation Center
            ft.GestureDetector(
                on_tap=start_breathing,
                content=breathing_circle
            ),
            
            ft.Container(height=80),
            
            # Soundscape Grid
            ft.Text("Ambient Sounds", size=16, weight=ft.FontWeight.W_600),
            ft.Row([
                create_sound_chip("Rain", ft.Icons.UMBRELLA_ROUNDED),
                create_sound_chip("Forest", ft.Icons.FOREST_ROUNDED),
                create_sound_chip("Waves", ft.Icons.WATER_ROUNDED),
            ], alignment=ft.MainAxisAlignment.CENTER),
            
            # Signature Footer
            ft.Container(
                expand=True,
                content=ft.Column([
                    ft.Text("Created by Your Name", size=10, color=ft.Colors.WHITE24, italic=True)
                ], alignment=ft.MainAxisAlignment.END, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
        ]
    )

    page.add(bg_container)

ft.run(main)