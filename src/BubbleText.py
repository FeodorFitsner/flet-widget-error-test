from dataclasses import field
from typing import List, Union
from flet import *
import asyncio

class AnimatedTextBubble(Container):
    def __init__(
        self, 
        texts: Union[str, List[str]] = field(default_factory=Union),
        speed: Union[int, float] = 10,
        pause: Union[int, float] = 0.0,
        bgcolor: ColorValue = Colors.GREY_900,
        border_radius: Union[int, BorderRadius] = 20,
        markdown_code_theme: MarkdownCodeTheme = MarkdownCodeTheme.ATOM_ONE_DARK,
        markdown_extension_set: MarkdownExtensionSet = MarkdownExtensionSet.GITHUB_WEB,
        border: Border | None = None
    ):
        super().__init__()
        self._running = False
        self.adaptive = True
        self.expand = True
        self.expand_loose = True
        self.padding = 10
        self.ink = True
        self.clipboard = Clipboard()
        self.border = border
        self.markdown_code_theme = markdown_code_theme
        self.markdown_extension_set = markdown_extension_set
        self.border_radius = border_radius
        self.bgcolor = bgcolor
        self.pause = pause
        self.speed = speed
        self.texts = texts

        self.on_long_press = self._copy_to_clipboard

        self.message_column = Column(spacing=2, tight=False)
        self.content = self.message_column

    def is_isolated(self):
        return True

    async def _copy_to_clipboard(self, e):
        full_text = "\n".join(self.texts)

        clean_text = (
            full_text.replace("#", "")
            .replace("*", "")
            .replace("`", "")
            .strip()
        )

        await self.clipboard.set(clean_text)

        sb = SnackBar(
            content=Text("✅ Copied to clipboard", color=Colors.WHITE),
            bgcolor=self.bgcolor,
        )

        self.page.show_dialog(sb)
        self.page.update()

    def did_mount(self):
        self._running = True
        self.page.run_task(self._type_loop)
        return super().did_mount()

    def will_unmount(self):
        self._running = False
        return super().will_unmount()

    async def _type_text(self, full_text: str):
        partial_text = ""
        md = Markdown(
            value="",
            selectable=True,
            extension_set=self.markdown_extension_set,
            code_theme=self.markdown_code_theme,
            on_tap_link=lambda e: self.page.launch_url(e.data),
        )
        self.message_column.controls.append(md)

        for ch in full_text:
            partial_text += ch
            md.value = partial_text
            self.update()
            await asyncio.sleep(1 / self.speed)
        self.update()

        if self.pause > 0:
            await asyncio.sleep(self.pause)

    async def _type_loop(self):
        for text in self.texts:
            if not self._running:
                break
            await self._type_text(text)

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