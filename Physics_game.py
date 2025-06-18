#By Hanz Santos
#14/4/2025

import arcade
import arcade.gui
from arcade.gui import *
from arcade.pymunk_physics_engine import PymunkPhysicsEngine

import numpy
import scipy 
import pymunk


# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
SCREEN_TITLE = "Window"


class MainView(arcade.View):
    #Main View
    
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)
        
        self.ui = UIManager()
        self.ui.enable()
        
        # Create main layout
        self.grid_layout = UIGridLayout(
            column_count=4, 
            row_count=3,
            vertical_spacing=20, 
            horizontal_spacing=20,  
            align_horizontal="center",
            align_vertical="center",
            )
        
        # Title
        self.title = UITextArea(
            text="Main Menu",  
            height=60, 
            font_size=24,
            multiline=False,
            text_color=arcade.color.WHITE,
            )
        
        # Buttons
        self.Button1 = UIFlatButton(text="Gravity", width=200, height=200)
        self.Button1.on_click = self.on_environment_click
        
        self.Button2 = UIFlatButton(width=200, height=200)
        
        self.Button3 = UIFlatButton(width=200, height=200)
        self.Button3.on_click = self.on_exit_click
        
        # Add elements to layout
        self.grid_layout.add(self.Button1, column=0, row=0)
        self.grid_layout.add(self.Button2, column=1, row=0)
        self.grid_layout.add(self.Button3, column=2, row=0)
        
        self.anchor = self.ui.add(UIAnchorLayout())

        # Center the layout
        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.grid_layout,
        )

        self.anchor.add(
            anchor_x="center_x",
            anchor_y="top",
            child=self.title
        )
    
    def on_environment_click(self, event):
        """Switch to environment view"""
        env_view = EnvironmentView()
        self.window.show_view(env_view)
    
    def on_exit_click(self, event):
        """Exit the application"""
        arcade.exit()
    
    def on_draw(self):
        self.clear()
        self.ui.draw()
    
    def on_hide_view(self):
        # Disable UI when hiding view
        self.ui.disable()


class EnvironmentView(arcade.View):
    def __init__(self):
        pass
        
class BallObject(arcade.SpriteCircle):
    """Ball object for the physics simulation"""
    
    def __init__(self, radius, color):
        super().__init__(radius, color)
        self.radius = radius
        self.color = color
        self.mass = 1.0
        self.friction = 0.6
        self.elasticity = 0.8

    def setup_physics(self, physics_engine):
        """Physics properties for the ball object"""
        physics_engine.add_sprite(
            self,
            mass=self.mass,
            friction=self.friction,
            elasticity=self.elasticity,
            moment=pymunk.moment_for_circle(self.mass, 0, self.radius)
        )

def main():
    """Run Program"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    main_view = MainView()
    window.show_view(main_view)
    arcade.run()


if __name__ == "__main__":
    main()

