import sys

from kivymd.app import MDApp
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import (
    OneLineAvatarIconListItem,
    OneLineIconListItem, MDList,
)
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.metrics import dp


class CheckboxRange(MDCheckbox):
    pass


class ContentNavigationDrawer(BoxLayout):
    pass


class IconListItem(OneLineAvatarIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))


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
    def calculate(self):
        print("Calculate")


class MainApp(MDApp):
    """Main class."""
    title = "Booklet for Epson XP-100"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_lang_items = []
        self.menu_lang = None
        self.menu_dots_items = []
        self.menu_dots = None
        # To avoid duplicates
        self.nav_drawer_item_names_dict = {
            "About": "About",
            "About author": "About author",
            "Language": "Language",
            "Exit": "Exit"
        }
        self.nav_drawer_funcs_dict = {
            self.nav_drawer_item_names_dict["About"]: self.show_about,
            self.nav_drawer_item_names_dict["About author"]: self.show_about_author,
            self.nav_drawer_item_names_dict["Language"]: self.menu_lang_callback,
            self.nav_drawer_item_names_dict["Exit"]: lambda x: sys.exit(0)
        }

    def build(self):
        self.menu_lang_items = [
            {
                "viewclass": "IconListItem",
                "icon": "data/images/us_rect.png",
                "height": dp(56),
                "text": "English",
                "on_release": lambda x=f"English": self.menu_lang_items_callback(x)
            },
            {
                "viewclass": "IconListItem",
                "icon": "data/images/ru_rect.png",
                "height": dp(56),
                "text": "Русский",
                "on_release": lambda x=f"Русский": self.menu_lang_items_callback(x)
            }
        ]
        self.menu_lang = MDDropdownMenu(
            items=self.menu_lang_items,
            position="auto",
            width_mult=4
        )
        self.menu_dots_items = [
            {
                "viewclass": "IconListItem",
                "icon": "exit-to-app",
                "height": dp(56),
                "text": self.nav_drawer_item_names_dict["Exit"],
                "on_release": lambda: sys.exit(0)
            }
        ]
        self.menu_dots = MDDropdownMenu(
            items=self.menu_dots_items,
            position="auto",
            width_mult=4
        )
        return MainScreen()

    def on_start(self):
        icons_item = {
            "web": self.nav_drawer_item_names_dict["Language"],
            "account": self.nav_drawer_item_names_dict["About author"],
            "information-outline": self.nav_drawer_item_names_dict["About"],
            "exit-to-app": self.nav_drawer_item_names_dict["Exit"]
        }
        for icon_name in icons_item.keys():
            self.root.ids["content_drawer"].ids["md_list"].add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name])
            )

    def tbar_dots_callback(self, dots_button):
        """Callback for self.menu_dots MDDropdownMenu."""
        self.menu_dots.caller = dots_button
        self.menu_dots.open()

    def menu_lang_callback(self, chosen_item):
        """Callback for language ItemDrawer."""
        self.menu_lang.caller = chosen_item
        self.menu_lang.open()

    def menu_lang_items_callback(self, chosen_item):
        """Callback for self.menu_lang_items."""
        self.menu_lang.dismiss()
        print(f"menu_lang_items {chosen_item}")

    def show_about(self, chosen_item):
        print("About")

    def show_about_author(self, chosen_item):
        print("About author")

    def change_language(self, chosen_item):
        print("Change language")


if __name__ in ("__main__", "__android__"):
    MainApp().run()
