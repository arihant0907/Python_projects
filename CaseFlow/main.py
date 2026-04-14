import flet as ft
import re

def main(page: ft.Page):
    page.title = "CaseFlow - Selective Converter"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 450
    page.window_height = 600
    #page.bgcolor = "#1A1C1E" # Dark surface color hex
    page.padding = 30

    # --- Transformation Logic ---
    def transform_text(text, case_type):
        if not text: return ""
        if case_type == "UPPERCASE": return text.upper()
        if case_type == "lowercase": return text.lower()
        if case_type == "Title Case": return text.title()
        if case_type == "snake_case":
            return re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower().replace(" ", "_").replace("-", "_")
        if case_type == "camelCase":
            s = re.sub(r"(_|-)+", " ", text).title().replace(" ", "")
            return s[0].lower() + s[1:]
        if case_type == "kebab-case":
            s = re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower().replace(" ", "_")
            return s.replace("_", "-")
        return text

    # --- Event Handlers ---
    def update_result(e):
        result_text.value = transform_text(text_input.value, case_dropdown.value)
        page.update()

    def copy_result(e):
        if result_text.value:
            page.set_clipboard(result_text.value)
            page.show_snack_bar(ft.SnackBar(ft.Text("Copied to clipboard!"), open=True))

    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        theme_icon.icon = ft.Icons.DARK_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.LIGHT_MODE
        page.update()

    # --- UI Components ---
    theme_icon = ft.IconButton(ft.Icons.LIGHT_MODE, on_click=toggle_theme)
    
    text_input = ft.TextField(
        label="Input Text",
        hint_text="Enter text to convert...",
        on_change=update_result,
        border_radius=15,
        adaptive=True
    )

    case_dropdown = ft.Dropdown(
        label="Select Target Case",
        value="UPPERCASE", # Default selection
        on_text_change=update_result,
        options=[
            ft.dropdown.Option("UPPERCASE"),
            ft.dropdown.Option("lowercase"),
            ft.dropdown.Option("Title Case"),
            ft.dropdown.Option("snake_case"),
            ft.dropdown.Option("camelCase"),
            ft.dropdown.Option("kebab-case"),
        ],
        border_radius=15,
    )

    result_text = ft.Text(
        value="",
        size=24,
        weight=ft.FontWeight.W_500,
        #color=ft.Colors.BLUE_400,
        selectable=True,
    )

    # --- Layout ---
    page.add(
        ft.Row([
            ft.Text("CaseFlow", size=28, weight=ft.FontWeight.BOLD),
            theme_icon
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        
        ft.Divider(height=20, thickness=0),
        ft.ResponsiveRow([
            case_dropdown,
            text_input
        ]),
        
        ft.Divider(height=40, color=ft.Colors.OUTLINE_VARIANT),
        
        # Result Display Area
        ft.Column([
            ft.Text("Resultant Text:",
             size=14,
             #color=ft.Colors.GREY_500
             ),
            ft.Container(
                content=result_text,
                padding=20,
                #bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.ON_SURFACE),
                border_radius=15,
                alignment=ft.Alignment.CENTER,
                on_click=copy_result # Click the box to copy
            ),
            ft.Text("(Click the box above to copy)", size=12, italic=True,
             #color=ft.Colors.GREY_500
             )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),

        ft.Container(expand=True),
        ft.Container(
            content=ft.Text("Created by [Your Name]", size=10, italic=True, 
            #color=ft.Colors.with_opacity(0.3, ft.Colors.ON_SURFACE)
            ),
            alignment=ft.Alignment.BOTTOM_CENTER
        )
    )

ft.run(main)