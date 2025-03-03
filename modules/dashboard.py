import os
import random
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.label import Label
from fabric.widgets.button import Button
from fabric.widgets.stack import Stack
from fabric.widgets.image import Image
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GLib, Gtk, Vte, Pango, GdkPixbuf
import modules.icons  as icons
from modules.widgets import Widgets
from modules.buttons import Buttons
from modules.pins import Pins
from modules.wallpapers import WallpaperSelector
from modules.kanban import Kanban
import modules.data as data

class Dashboard(Box):
    def __init__(self, **kwargs):
        super().__init__(
            name="dashboard",
            orientation="v",
            spacing=8,
            h_align="fill",
            v_align="fill",
            h_expand=True,
            visible=True,
            all_visible=True,
        )

        self.notch = kwargs["notch"]

        self.widgets = Widgets(notch=self.notch)
        self.pins = Pins()
        self.kanban = Kanban()
        self.wallpapers = WallpaperSelector()

        self.stack = Stack(
            name="stack",
            transition_type="slide-left-right",
            transition_duration=500,
        )

        self.switcher = Gtk.StackSwitcher(
            name="switcher",
            spacing=8,
        )

        self.label_1 = Label(
            name="label-1",
            label="Widgets",
        )

        self.label_2 = Label(
            name="label-2",
            label="Pins",
        )

        self.label_3 = Label(
            name="label-3",
            label="Kanban",
        )

        self.label_4 = Label(
            name="label-4",
            label="Wallpapers",
        )

        # Create the coming_soon labels as attributes for later update
        self.coming_soon_start_label = Label(
            name="coming-soon-label",
            label="I need...",
            justification="center",
        )
        self.coming_soon_end_label = Label(
            name="coming-soon-label",
            label="To sleep...",
            justification="center",
        )

        self.soon = Image(
            name="coming-soon",
            pixbuf=GdkPixbuf.Pixbuf.new_from_file_at_scale(
                f"{data.HOME_DIR}/.config/hyprfabricated/assets/soon.png", 366, 300, True
            ),
        )

        self.coming_soon = Box(
            name="coming-soon",
            orientation="v",
            h_align="fill",
            v_align="fill",
            h_expand=True,
            v_expand=True,
            spacing=8,
            children=[
            Box(
                h_align="center",
                v_align="fill",
                h_expand=True,
                v_expand=True,
                children=[self.coming_soon_start_label],
            ),
            self.soon,
            Box(
                h_align="center",
                v_align="fill",
                h_expand=True,
                v_expand=True,
                children=[self.coming_soon_end_label],
            ),
            ],
        )

        self.stack.add_titled(self.widgets, "widgets", "Widgets")
        self.stack.add_titled(self.pins, "pins", "Pins")
        self.stack.add_titled(self.kanban, "kanban", "Kanban")
        self.stack.add_titled(self.wallpapers, "wallpapers", "Wallpapers")
        self.stack.add_titled(self.coming_soon, "coming-soon", "Coming soon...")

        self.switcher.set_stack(self.stack)
        self.switcher.set_hexpand(True)
        self.switcher.set_homogeneous(True)
        self.switcher.set_can_focus(True)

        # Add signal to detect when the visible child changes
        self.stack.connect("notify::visible-child", self.on_visible_child_changed)

        self.add(self.switcher)
        self.add(self.stack)

        self.show_all()

    def go_to_next_child(self):
        children = self.stack.get_children()
        current_index = self.get_current_index(children)
        next_index = (current_index + 1) % len(children)
        self.stack.set_visible_child(children[next_index])

    def go_to_previous_child(self):
        children = self.stack.get_children()
        current_index = self.get_current_index(children)
        previous_index = (current_index - 1 + len(children)) % len(children)
        self.stack.set_visible_child(children[previous_index])

    def get_current_index(self, children):
        current_child = self.stack.get_visible_child()
        return children.index(current_child) if current_child in children else -1

    def on_visible_child_changed(self, stack, param):
        visible = stack.get_visible_child()
        if visible == self.wallpapers:
            self.wallpapers.search_entry.set_text("")
            self.wallpapers.search_entry.grab_focus()
        if visible == self.coming_soon:
            # Define paired messages for the coming_soon widget using tuples
            text_pairs = (
                ("I need...", "To sleep..."),
                ("Another day...", " Another bug..."),
                ("I really need...", "An energy drink..."),
                ("7 minutes without ricing...", "TIME TO CODE!"),
                ("git commit... git p-", "tf is a merge?"),
                ("This should work...", "Why doesn't it work?"),
                ("Just one more line...", "8 hours later..."),
                ("Hello world...", "Segfault."),
                ("I'll fix that later...", "Technical debt intensifies."),
                ("sudo rm -rf /", "Wait, NO—"),
                ("Almost done...", "SyntaxError: unexpected EOF"),
                ("AI will take our jobs...", "Meanwhile: writing regex."),
                ("Arch is unstable!", "3 years, no reinstall."),
                ("printf(\"Hello world\");", "Where is my semicolon?"),
                ("I'll sleep early today...", "3AM: still debugging."),
                ("Oh, a tiny bug...", "Refactoring the whole codebase."),
                ("rm -rf node_modules", "Project reborn."),
                ("Pipenv, poetry, venv...", "Which one was I using?"),
            )

            new_start_text, new_end_text = random.choice(text_pairs)
            self.coming_soon_start_label.set_text(new_start_text)
            self.coming_soon_end_label.set_text(new_end_text)
