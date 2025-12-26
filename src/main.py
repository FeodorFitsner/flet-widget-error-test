from BubbleText import AnimatedTextBubble
from flet import *

@component
def App(page: Page):
    text = [
        "### 🌟 What is Flet?\n\n"
        "**Flet** is a framework in Python for building web, desktop, and mobile apps.\n\n"
        "### Features\n"
        "- Cross-platform\n"
        "- Easy to use\n"
        "- Based on Flutter\n\n"
        "```python\n"
        "import flet as ft\n"
        "def main(page: ft.Page):\n"
        "    page.bgcolor = ft.colors.BLACK\n"
        "    page.add(ft.Text('Hello Flet'))\n"
        "ft.app(target=main)\n"
        "```\n\n"
        "Official link: [flet.dev](https://flet.dev)\n"
        "Github Repo: [flet-dev](https://github.com/flet-dev/flet)"
    ]

    bubble = AnimatedTextBubble(texts=text)
    
    return SafeArea(content=Column(controls=[bubble]))

# App Entry Point
def main(page: Page):
    
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.render(lambda: App(page))

run(main)