import sys
import os
import gettext
import locale

from kivy.config import Config, ConfigParser
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.metrics import dp
from kivy.lang import Observable
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.toast import toast
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import (
    OneLineAvatarIconListItem,
    OneLineIconListItem, MDList,
)
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.selectioncontrol import MDCheckbox


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
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     print(self.ids["main_container"].ids["btn_calculate"].text)
    pass


class MainContainer(BoxLayout):
    """MainContainer in App Root screen."""
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

    def clear_inputoutput_fields(self):
        """Clear input and output fields."""
        self.ids["tf_last_page"].text = ""
        self.ids["tf_face_pages"].text = ""
        self.ids["tf_verso_pages"].text = ""
        self.ids["lbl_total_pages_for_printing"].opacity = 0
        self.ids["lbl_necessary_sheets"].opacity = 0
        self.ids["lbl_middle_of_booklet"].opacity = 0

    def calculate(self, first_page, last_page):
        """Calculate result."""
        # root = MDApp.get_running_app().root
        # print(root.ids)

        if not first_page:
            toast(MDApp.get_running_app().tr._("The first page can't be empty"))
            self.ids["tf_first_page"].focus = True
            return
        else:
            first_page = int(first_page)
            if not last_page:
                toast(MDApp.get_running_app().tr._("The last page can't be empty"))
                self.ids["tf_last_page"].focus = True
                return
            else:
                last_page = int(last_page)

        if first_page <= 0:
            toast(MDApp.get_running_app().tr._("Amount of pages must be more than 0"))
            self.ids["tf_first_page"].focus = True
            return
        if (last_page - first_page) < 0:
            toast(MDApp.get_running_app().tr._("The last page cannot be less than the first one"))
            self.ids["tf_last_page"].focus = True
            return

        # Рассчитываем сколько страниц нужно напечатать
        # Calculate how many sheets need to print
        amount_pages = (last_page - first_page) + 1

        # Проверка количества страниц кратности 4 (4 страницы на 1 листе!)
        # Если не кратно 4, то добавляем по 1, пока не будет кратно 4
        while (amount_pages % 4) != 0:
            amount_pages += 1  # теперь последняя страница = amount_pages

        # Вывод итогового количества страниц и листов
        # self.ids["lbl_total_pages_for_printing"].text = MDApp.get_running_app().tr._(f"Total pages for printing: {amount_pages}")
        self.ids["lbl_total_pages_for_printing"].text = MDApp.get_running_app().tr._("Total pages for printing: {}").format(amount_pages)
        self.ids["lbl_total_pages_for_printing"].opacity = 1

        # Необходимое количество листов для печати
        amount_sheets = amount_pages // 4
        # self.ids["lbl_necessary_sheets"].text = MDApp.get_running_app().tr._(f"Necessary sheets for printing: {amount_sheets}")
        self.ids["lbl_necessary_sheets"].text = MDApp.get_running_app().tr._("Necessary sheets for printing: {}").format(amount_sheets)
        self.ids["lbl_necessary_sheets"].opacity = 1

        # Находим левую страницу середины брошюры left_face_page
        left_face_page = first_page + (amount_pages // 2 - 1)
        # Находим правую страницу середины брошюры right_face_page
        right_face_page = left_face_page + 1
        # Вывод страниц середины брошюры
        # self.ids["lbl_middle_of_booklet"].text = MDApp.get_running_app().tr._(f"The middle of the booklet: {left_face_page}, {right_face_page}")
        self.ids["lbl_middle_of_booklet"].text = MDApp.get_running_app().tr._("The middle of the booklet: {}, {}").format(left_face_page, right_face_page)
        self.ids["lbl_middle_of_booklet"].opacity = 1

        # Находим левую оборотную страницу left_verso_page
        left_verso_page = left_face_page - 1
        # //Находим правую оборотную страницу right_verso_page
        right_verso_page = right_face_page + 1

        # Вычисляем и печатаем левые и правые лицевые страницы
        tmp_string = ""
        while (left_face_page >= (first_page + 1)) or (right_face_page <= (amount_pages - 1)):
            if right_face_page != (first_page + (amount_pages - 2)):
                tmp_string += f"{left_face_page},{right_face_page},"
            else:  # после последней правой страницы не ставим запятую
                tmp_string += f"{left_face_page},{right_face_page}"

            left_face_page -= 2
            right_face_page += 2

        self.ids["tf_face_pages"].text = tmp_string
        tmp_string = ""  # обнуляем временную строку

        # Вычисляем и печатаем левые и правые оборотные страницы
        while (left_verso_page >= first_page) or (right_verso_page <= amount_pages):
            if right_verso_page != (first_page + (amount_pages - 1)):
                tmp_string += f"{right_verso_page},{left_verso_page},"
            else:  # после последней правой страницы не ставим запятую
                tmp_string += f"{right_verso_page},{left_verso_page}"

            left_verso_page -= 2
            right_verso_page += 2

        self.ids["tf_verso_pages"].text = tmp_string


class Lang(Observable):
    observers = []
    lang = None

    def __init__(self, defaultlang):
        super(Lang, self).__init__()
        self.ugettext = None
        self.lang = defaultlang
        self.switch_lang(self.lang)

    def _(self, text):
        try:
            return self.ugettext(text)
        except UnicodeDecodeError:
            return self.ugettext(text.decode("utf-8"))

    def fbind(self, name, func, *args, **kwargs):
        if name == "_":
            self.observers.append((func, args, kwargs))
        else:
            return super(Lang, self).fbind(name, func, *args, **kwargs)

    def funbind(self, name, func, *args, **kwargs):
        if name == "_":
            key = (func, args, kwargs)
            if key in self.observers:
                self.observers.remove(key)
        else:
            return super(Lang, self).funbind(name, func, *args, **kwargs)

    def switch_lang(self, lang):
        # get the right locales directory and instantiate a gettext
        try:
            locale_dir = os.path.join(os.path.dirname(__file__), "data", "locales")
            locales = gettext.translation("bookletapp", locale_dir, languages=[lang])
            self.ugettext = locales.gettext

            # update all the kv rules attached to this text
            for func, args, kwargs in self.observers:
                func(*args, None, None)
        except:
            toast(MDApp.get_running_app().tr._("Can't translate the App"))


class MainApp(MDApp):
    """Main class."""
    is_first_started = BooleanProperty(True)
    dialog_switch_language = None
    # Language: get system locale.
    lang = StringProperty(locale.getdefaultlocale()[0][:2])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tr = None
        self.menu_lang_items = []
        self.menu_lang = None
        self.menu_dots_items = []
        self.menu_dots = None
        # To avoid duplicates
        self.nav_drawer_item_names_dict = {}
        self.nav_drawer_funcs_dict = {}
        # My config.
        self.config = ConfigParser()
        # The current target TextInput widget requesting the keyboard
        # is presented just above the soft keyboard.
        Window.softinput_mode = "below_target"

    def build_config(self, config):
        """Default config."""
        self.config.setdefaults("applanguage",
                {
                    "language": self.lang
                })

    def save_config(self):
        """Save the App config."""
        self.config.set("applanguage", "language", self.lang)
        self.config.write()

    def my_load_config(self):
        """Load the App config."""
        self.lang = self.config.get("applanguage", "language")

    def build(self):
        self.my_load_config()
        # Instantiate an instance of Lang.
        self.tr = Lang(self.lang)
        self.title = self.tr._("Booklet for Epson XP-100")
        # To avoid duplicates
        self.nav_drawer_item_names_dict = {
            "About": self.tr._("About"),
            "About author": self.tr._("About author"),
            "Language": self.tr._("Language"),
            "Exit": self.tr._("Exit")
        }
        self.nav_drawer_funcs_dict = {
            self.nav_drawer_item_names_dict["About"]: self.show_about,
            self.nav_drawer_item_names_dict["About author"]: self.show_about_author,
            self.nav_drawer_item_names_dict["Language"]: self.menu_lang_callback,
            self.nav_drawer_item_names_dict["Exit"]: lambda x: sys.exit(0)
        }
        self.menu_lang_items = [
            {
                "viewclass": "IconListItem",
                "icon": "data/images/us_rect.png",
                "height": dp(56),
                "text": self.tr._("English"),
                "on_release": lambda x=f"en": self.menu_lang_items_callback(x)
            },
            {
                "viewclass": "IconListItem",
                "icon": "data/images/ru_rect.png",
                "height": dp(56),
                "text": self.tr._("Русский"),
                "on_release": lambda x=f"ru": self.menu_lang_items_callback(x)
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
        self.is_first_started = False

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
        self.lang = chosen_item
        MDApp.get_running_app().root.ids["main_container"].clear_inputoutput_fields()
        MDApp.get_running_app().root.ids["nav_drawer"].set_state("close")

    def on_stop(self):
        """Save config."""
        self.save_config()

    def on_pause(self):
        # Save data if needed
        return True

    def on_resume(self):
        # Check if any data needs replacing
        pass

    def on_lang(self, instance, lang):
        """User changed language."""
        # Skip the first tr.switch_lang
        # because self.tr is not defined yet.
        # The first switch will be in the build method: self.tr = Lang(self.lang)
        # after self.my_load_config().
        if not self.is_first_started:
            self.tr.switch_lang(lang)

            if not self.dialog_switch_language:
                self.dialog_switch_language = MDDialog(
                    title=self.tr._("Change language"),
                    text=self.tr._("You have to restart the app"
                                   "\nto change the language completely."),
                    auto_dismiss=False,
                    buttons=[
                        MDRaisedButton(
                            text=self.tr._("OK"),
                            on_release=self.stop
                        )
                    ]
                )
                self.dialog_switch_language.open()

    def show_about(self, chosen_item):
        print("About")

    def show_about_author(self, chosen_item):
        print("About author")


if __name__ in ("__main__", "__android__"):
    MainApp().run()
