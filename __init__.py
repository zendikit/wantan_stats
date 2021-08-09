from aqt import gui_hooks

from .hooks import on_deck_browser_will_render_content

gui_hooks.deck_browser_will_render_content.append(
        on_deck_browser_will_render_content)
