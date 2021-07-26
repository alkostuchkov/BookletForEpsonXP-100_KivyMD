from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import (
    OneLineAvatarIconListItem,
    ILeftBodyTouch,
)
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.metrics import dp


class Container(BoxLayout):
    """Root."""
    pass


class IconListItem(OneLineAvatarIconListItem):
    icon = StringProperty()


class CheckboxRange(MDCheckbox):
    pass


class MainApp(MDApp):
    """Main class."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_lang_items = []
        self.menu_lang = None

    def build(self):
        self.menu_lang_items = [
            {
                "viewclass": "IconListItem",
                "icon": "data/images/us_rect.png",
                "height": dp(56),
                "text": "English",
                # "on_release":
            },
            {
                "viewclass": "IconListItem",
                "icon": "data/images/ru_rect.png",
                "height": dp(56),
                "text": "Русский",
                # "on_release":
            }
        ]
        return Container()

    def on_start(self):
        self.menu_lang = MDDropdownMenu(
            caller=self.root.ids["tf_lang"],
            items=self.menu_lang_items,
            position="bottom",
            width_mult=4
        )


if __name__ in ("__main__", "__android__"):
    MainApp().run()
