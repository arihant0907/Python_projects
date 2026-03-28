import flet as ft

def main(page: ft.Page):
    page.title = "Glass Task Manager"
    page.theme_mode = ft.ThemeMode.DARK 
    page.window_width = 450
    page.window_height = 750
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # Task input field
    task_input = ft.TextField(
        hint_text="What's on your mind?",
        border=ft.InputBorder.NONE,
        filled=False,
        expand=True,
        on_submit=lambda e: add_task(e)
    )

    tasks_column = ft.Column(spacing=15, scroll=ft.ScrollMode.ADAPTIVE)

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

    theme_icon = ft.IconButton(ft.Icons.LIGHT_MODE, on_click=toggle_theme)

    def delete_task(container):
        tasks_column.controls.remove(container)
        page.update()

    def add_task(e):
        if task_input.value.strip():
            task_card = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Checkbox(label=task_input.value, fill_color=ft.Colors.BLUE_400),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE_ROUNDED,
                            icon_size=18,
                            on_click=lambda _: delete_task(task_card)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                padding=10,
                border_radius=15,
                border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.ON_SURFACE)),
                bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.ON_SURFACE),
                blur=ft.Blur(10, 10, ft.BlurStyle.INNER),
            )
            
            tasks_column.controls.append(task_card)
            task_input.value = ""
            page.update()

    # The Input Bar (Header) - Fixed padding syntax
    input_bar = ft.Container(
        content=ft.Row([task_input]),
        padding=ft.Padding(left=20, top=0, right=10, bottom=0), 
        border_radius=30,
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_GREY_500),
        height=60,
    )

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD_TASK_ROUNDED,
        bgcolor=ft.Colors.BLUE_400,
        on_click=add_task,
        shape=ft.RoundedRectangleBorder(radius=15)
    )

    footer_name = ft.Text(
        "Created by @rihant", 
        size=10, 
        weight=ft.FontWeight.W_300,
        color=ft.Colors.with_opacity(0.3, ft.Colors.ON_SURFACE), # This makes it faint
        italic=True
    )

    page.add(
        ft.Row(
            [
                ft.Text("Focus", size=40, weight=ft.FontWeight.BOLD),
                theme_icon
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        ft.Text("Stay productive, stay organized.", size=14, color=ft.Colors.GREY_500),
        # Replaced VerticalDivider with a simple Container for spacing
        ft.Container(height=20), 
        input_bar,
        ft.Divider(height=40, thickness=0.5, color=ft.Colors.with_opacity(0.1, ft.Colors.ON_SURFACE)),
        tasks_column,
        # This pushes the name to the very bottom
        ft.Container(
            content=footer_name,
            alignment=ft.Alignment.CENTER,
            padding=ft.Padding(0, 10, 0, 0)
        )
    )

# Use run() instead of app() to clear the deprecation warning
ft.run(main)