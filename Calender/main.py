import flet as ft
import calendar
from datetime import datetime


def main(page: ft.Page):
    page.title = "Calendar"
    #page.bgcolor = ft.Colors.WHITE
    page.theme_mode = ft.ThemeMode.DARK

    today = datetime.today()
    current_year = today.year
    current_month = today.month

    calendar_grid = ft.GridView(
        expand=True,
        runs_count=7,
        max_extent=70,
        spacing=5,
        run_spacing=5,
    )

    header_text = ft.Text(
        size=22,
        weight=ft.FontWeight.BOLD
    )

    # ---------------- Calendar Builder ----------------
    def build_calendar():
        calendar_grid.controls.clear()

        header_text.value = f"{calendar.month_name[current_month]} {current_year}"

        # Weekday headers
        for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            calendar_grid.controls.append(
                ft.Container(
                    content=ft.Text(day, weight=ft.FontWeight.BOLD),
                    alignment=ft.Alignment.CENTER,
                )
            )

        month_calendar = calendar.monthcalendar(current_year, current_month)

        for week in month_calendar:
            for day in week:
                if day == 0:
                    calendar_grid.controls.append(ft.Container())
                else:
                    is_today = (
                        day == today.day
                        and current_month == today.month
                        and current_year == today.year
                    )

                    calendar_grid.controls.append(
                        ft.Container(
                            content=ft.Text(
                                str(day),
                                color=ft.Colors.WHITE if is_today else ft.Colors.BLACK,
                            ),
                            alignment=ft.Alignment.CENTER,
                            bgcolor=ft.Colors.BLUE_400 if is_today else ft.Colors.GREY_200,
                            border_radius=10,
                        )
                    )

        page.update()

    # ---------------- Navigation ----------------
    def prev_month(e):
        nonlocal current_month, current_year
        current_month -= 1
        if current_month == 0:
            current_month = 12
            current_year -= 1
        build_calendar()

    def next_month(e):
        nonlocal current_month, current_year
        current_month += 1
        if current_month == 13:
            current_month = 1
            current_year += 1
        build_calendar()

    def prev_year(e):
        nonlocal current_year
        current_year -= 1
        build_calendar()

    def next_year(e):
        nonlocal current_year
        current_year += 1
        build_calendar()

    def toggle_theme(e):
        page.theme_mode = (
            ft.ThemeMode.LIGHT 
            if page.theme_mode == ft.ThemeMode.DARK 
            else ft.ThemeMode.DARK
        )
        theme_icon.icon = (
            ft.Icons.LIGHT_MODE 
            if page.theme_mode == ft.ThemeMode.DARK 
            else ft.Icons.DARK_MODE
        )
        page.update()

    # ------------- App Bar ------------------
    theme_icon = ft.IconButton(ft.Icons.LIGHT_MODE, on_click=toggle_theme)

    app_bar=ft.Row(
        [
            ft.Text("Calender", size=40, weight=ft.FontWeight.BOLD),
            theme_icon
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # ---------------- App Navigations ----------------
    navigation = ft.Row(
        controls=[
            ft.IconButton(ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT, on_click=prev_year),
            ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT, on_click=prev_month),
            header_text,
            ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT, on_click=next_month),
            ft.IconButton(ft.Icons.KEYBOARD_DOUBLE_ARROW_RIGHT, on_click=next_year),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )
    footer_name = ft.Text(
        "Created by @rihant", 
        size=10, 
        weight=ft.FontWeight.W_300,
        color=ft.Colors.with_opacity(0.3, ft.Colors.ON_SURFACE), # This makes it faint
        italic=True
    )

    page.add(
        ft.Column(
            controls=[app_bar,navigation, calendar_grid,footer_name],
            expand=True,
            spacing=20,
        )
    )

    build_calendar()


ft.app(target=main)
