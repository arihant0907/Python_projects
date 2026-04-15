import flet as ft
from ascii_magic import AsciiArt
import os
from ascii_magic import AsciiArt, Front, Back

def main(page: ft.Page):
    page.title = "Image to ASCII Art"
    page.theme_mode = ft.ThemeMode.DARK

    selected_file_path = {"path": None}

    # --- ASCII SETTINGS UI ---
    columns_input = ft.TextField(label="Columns", value="80")
    columns_input.tooltip = "More columns = more detailed but wider output"

    width_ratio_input = ft.TextField(label="Width Ratio", value="2.0")
    char_input = ft.TextField(label="Characters", value=" .:-=+*#%@", expand=True)

    enhance_checkbox = ft.Checkbox(label="Enhance Image", value=False)
    mono_checkbox = ft.Checkbox(label="Monochrome", value=False)


    front_dropdown = ft.Dropdown(
        label="Front Color",
        options=[
            ft.dropdown.Option("BLACK"),
            ft.dropdown.Option("RED"),
            ft.dropdown.Option("GREEN"),
            ft.dropdown.Option("YELLOW"),
            ft.dropdown.Option("BLUE"),
            ft.dropdown.Option("MAGENTA"),
            ft.dropdown.Option("CYAN"),
            ft.dropdown.Option("WHITE"),
        ],
    )

    back_dropdown = ft.Dropdown(
        label="Background Color",
        options=[
            ft.dropdown.Option("BLACK"),
            ft.dropdown.Option("RED"),
            ft.dropdown.Option("GREEN"),
            ft.dropdown.Option("YELLOW"),
            ft.dropdown.Option("BLUE"),
            ft.dropdown.Option("MAGENTA"),
            ft.dropdown.Option("CYAN"),
            ft.dropdown.Option("WHITE"),
        ],
    )

    # --- UI Elements ---

    ascii_output = ft.TextField(
        label="ASCII Output",
        multiline=True,
        min_lines=20,
        max_lines=30,
        read_only=False,
        expand=True,
        text_size=12,
    )

    sheet = ft.BottomSheet(
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("⚙️ ASCII Settings", size=16, weight="bold"),
                ft.Card(
                    content=ft.Container(
                        padding=15,
                        content=ft.Row(
                            [
                                ft.Container(columns_input),
                                ft.Container(width_ratio_input),
                                ft.Container(char_input),
                                ft.Container(front_dropdown),
                                ft.Container(back_dropdown),
                                ft.Container(enhance_checkbox),
                                ft.Container(mono_checkbox),
                            ],
                            wrap=True,
                            spacing=10,
                            run_spacing=10,
                            width=page.window.width
                        ),
                    )
                ),
            ],
        )
    )

    file_name_text = ft.Text("No file selected", size=14)

    # --- Functions ---
    async def handle_pick_files(e: ft.Event[ft.Button]):
        files = await ft.FilePicker().pick_files(allow_multiple=False)
        if files:
            file = files[0]
            selected_files.value = f"Selected: {file.name}"
            file_path = file.path
            selected_file_path["path"] = file_path

        else:
            selected_files.value = "Not Selected"
            
        page.update()


    def convert_to_ascii(e):
        if not selected_file_path["path"]:
            ascii_output.value = "⚠️ Select an image first."
            page.update()
            return

        try:
            # --- Read values safely ---
            columns = int(columns_input.value or 120)
            width_ratio = float(width_ratio_input.value or 2.0)
            chars = char_input.value or None

            enhance = enhance_checkbox.value or False 
            monochrome = mono_checkbox.value or False 

            # --- Handle colors ---
            front = getattr(Front, front_dropdown.value) if front_dropdown.value else None
            back = getattr(Back, back_dropdown.value) if back_dropdown.value else None

            # --- Generate ASCII ---
            art = AsciiArt.from_image(
                selected_file_path["path"]
            )

            ascii_output.value = art.to_ascii(
                columns=columns,
                width_ratio=width_ratio,
                char=chars,
                enhance_image=enhance,
                monochrome=monochrome,
                front=front,
                back=back,
            )

        except Exception as ex:
            ascii_output.value = f"Error: {ex}"

        page.update()


    async def copy_to_clipboard(e):
        if ascii_output.value:
            await ft.Clipboard().set(ascii_output.value)
            page.snack_bar = ft.SnackBar(ft.Text("Copied to clipboard!"))
            page.snack_bar.open = True
            page.update()


    def export_to_file(e):
        if not ascii_output.value:
            return

        save_path = "ascii_art.txt"
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(ascii_output.value)

        page.snack_bar = ft.SnackBar(ft.Text(f"Saved to {save_path}"))
        page.snack_bar.open = True
        page.update()

    def clear_ascii_output(e):
        ascii_output.value=""

    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_icon.icon = ft.Icons.DARK_MODE
        else:
            page.theme_mode = ft.ThemeMode.DARK
            theme_icon.icon = ft.Icons.LIGHT_MODE

        page.update()

    # these button 
    theme_icon = ft.IconButton(
        icon=ft.Icons.LIGHT_MODE,
        tooltip="Toggle Theme",
        on_click=toggle_theme,
    )

    # --- AppBar ---
    page.appbar = ft.AppBar(
        title=ft.Text("AsciiSnap",font_family="Roboto",size=30,),
        center_title=False,  
        title_spacing=30,  
        actions=[
            ft.Container(
                content=theme_icon,
                margin=ft.margin.only(right=20), 
            )
        ],
    )

    # --- Layout ---
    page.add(
        ft.Container(
            padding=20,
            expand=True,   
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Choose Image",
                                icon=ft.Icons.UPLOAD_FILE,
                                on_click=handle_pick_files
                            ),
                            selected_files := ft.Text(),
                        ]
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Convert to ASCII",
                                icon=ft.Icons.AUTO_FIX_HIGH,
                                on_click=convert_to_ascii,
                            ),
                            ft.ElevatedButton(
                                "Copy to Clipboard",
                                icon=ft.Icons.COPY,
                                on_click=copy_to_clipboard,
                            ),
                            ft.ElevatedButton(
                                "Export as .txt",
                                icon=ft.Icons.SAVE,
                                on_click=export_to_file,
                            ),
                        ],
                        wrap=True,
                        spacing=10,
                        run_spacing=10,
                        width=page.window.width
                    ),
                    ft.Divider(),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.BACKSPACE,
                                on_click=clear_ascii_output,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.SETTINGS_ROUNDED,
                                on_click=lambda x: page.show_dialog(sheet),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),

                    ascii_output

                ],
                expand=True,
                scroll=ft.ScrollMode.HIDDEN,
            ),
        )
    )

ft.run(main)