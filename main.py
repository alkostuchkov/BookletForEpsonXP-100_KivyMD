from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import (
    OneLineAvatarIconListItem,
    OneLineIconListItem, MDList,
)
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import Screen
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.metrics import dp


class IconListItem(OneLineAvatarIconListItem):
    icon = StringProperty()


class CheckboxRange(MDCheckbox):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()


class ContentNavigationDrawer(BoxLayout):
    pass


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""
        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class MainScreen(MDScreen):
    """App Root."""
    pass


class MainContainer(BoxLayout):
    """MainContainer in App Root screen."""
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
        return MainScreen()

    def on_start(self):
        self.menu_lang = MDDropdownMenu(
            # caller=self.root.ids["tf_lang"],
            items=self.menu_lang_items,
            position="bottom",
            width_mult=4
        )

        icons_item = {
            "web": "Language",
            "account": "About author",
            "information-outline": "About",
            "exit-to-app": "Exit"
        }
        for icon_name in icons_item.keys():
            self.root.ids["content_drawer"].ids["md_list"].add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name])
            )


if __name__ in ("__main__", "__android__"):
    MainApp().run()
