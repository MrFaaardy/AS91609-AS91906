#By Hanz Santos
#14/4/2025

import arcade
import arcade.gui
import numpy
import scipy 
import pymunk

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()
SCREEN_TITLE = "Making a Menu"


class MainView(arcade.View):
    """ Main application class."""

    def __init__(self):
        super().__init__()

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_HEIGHT, resizable=True)
    main_view = MainView()
    window.show_view(main_view)
    arcade.run()


if __name__ == "__main__":
    main()
