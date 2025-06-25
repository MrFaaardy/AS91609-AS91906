#By Hanz Santos
#14/4/2025

import arcade
import arcade.gui
from arcade.gui import *
from arcade.pymunk_physics_engine import PymunkPhysicsEngine

import numpy
import scipy 
import pymunk
import random

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 720
SCREEN_TITLE = "Physics Simulation"


class MainView(arcade.View):
    # Creates the main view 
    
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        
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
            text="Physics Simulation",  
            height=60, 
            font_size=24,
            multiline=False,
            text_color=arcade.color.WHITE,
            )
        
        # Buttons
        self.Button1 = UIFlatButton(text="Gravity", width=200, height=200)
        self.Button1.on_click = self.on_environment_click
        
        self.Button2 = UIFlatButton(text="Place Holder", width=200, height=200)
        
        self.Button3 = UIFlatButton(text="Place Holder", width=200, height=200)

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
        # Switch to environment view
        env_view = EnvironmentView()
        self.window.show_view(env_view)
    
    def on_draw(self):
        self.clear()
        self.ui.draw()
    
    def on_hide_view(self):
        # Disable UI when hiding view
        self.ui.disable()

class EnvironmentView(arcade.View):
    """Environment View for the physics simulation"""
    
    sidebar_width = 300
    w = arcade.View.width
    h = arcade.View.height

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        
        # Create physics engine with gravity
        self.physics_engine = PymunkPhysicsEngine(gravity=(0, -900))
        
        widget_area = self.w - self.sidebar_width

        # Creates the walls for the balls to spawn in
        self.wall_list = arcade.SpriteList()

        floor = arcade.SpriteSolidColor(width=widget_area, height=20, color=arcade.color.WHITE)
        floor.position = widget_area // 2, 10
        self.wall_list.append(floor)
        self.physics_engine.add_sprite(
            floor,
            body_type=PymunkPhysicsEngine.STATIC,
            friction=0.5,
            elasticity=0.99,
        )

        ceiling = arcade.SpriteSolidColor(width=widget_area, height=20, color=arcade.color.WHITE)
        ceiling.position = widget_area // 2, self.h - 10
        self.wall_list.append(ceiling)
        self.physics_engine.add_sprite(
            ceiling,
            body_type=PymunkPhysicsEngine.STATIC,
            friction=0.5,
            elasticity=0.99,
        )

        left_wall = arcade.SpriteSolidColor(width=20, height=self.h, color=arcade.color.WHITE)
        left_wall.position = 10, self.h // 2
        self.wall_list.append(left_wall)
        self.physics_engine.add_sprite(
            left_wall,
            body_type=PymunkPhysicsEngine.STATIC,
            friction=0.5,
            elasticity=0.99,
        )

        right_wall = arcade.SpriteSolidColor(width=20, height=self.h, color=arcade.color.WHITE)
        right_wall.position = widget_area, self.h // 2
        self.wall_list.append(right_wall)
        self.physics_engine.add_sprite(
            right_wall,
            body_type=PymunkPhysicsEngine.STATIC,
            friction=0.5,
            elasticity=0.99,
        )
        
        # List for the ball objects
        self.ball_list = arcade.SpriteList()
        
        # Enable the UI manager
        self.ui = UIManager()
        self.ui.enable()
        
        self.sidebar_layout = UIBoxLayout(vertical=True, width=self.sidebar_width, height=self.h, space_between=20)

        self.sidebar = UITextArea(
            text="Change Object's properties", width=self.sidebar_width - 20, height=100, font_size=18,
            text_color=arcade.color.WHITE, x= self.w - self.sidebar_width + 10, y=self.h // 2
        )

        self.radius_slider = UISlider(value=30, min_value=15, max_value=60, width=self.sidebar_width - 40)
        self.elasticity_slider = UISlider(value=0.99, min_value=0.5, max_value=1.0, width=self.sidebar_width - 40)

        self.radius_label = UILabel(text=f"Ball Radius: {self.radius_slider.value:.0f}", width=self.sidebar_width - 40)
        self.elasticity_label = UILabel(text=f"Elasticity: {self.elasticity_slider.value:.2f}", width=self.sidebar_width - 40)

        def on_radius_change(event):
            self.radius_label.text = f"Ball Radius: {self.radius_slider.value:.0f}"

        def on_elasticity_change(event):
            self.elasticity_label.text = f"Elasticity: {self.elasticity_slider.value:.2f}"

        self.radius_slider.on_change = on_radius_change
        self.elasticity_slider.on_change = on_elasticity_change

        # Back button
        back_button = UIFlatButton(text="Back to Menu", width=200)
        back_button.on_click = self.on_back_click

        # Button to spawn balls
        spawn_button = UIFlatButton(text="Spawn Ball", width=200)
        spawn_button.on_click = self.on_spawn_ball_click

        self.sidebar_layout.add(self.sidebar)
        self.sidebar_layout.add(back_button)
        self.sidebar_layout.add(spawn_button)
        self.sidebar_layout.add(self.radius_label)
        self.sidebar_layout.add(self.radius_slider)
        self.sidebar_layout.add(self.elasticity_label)
        self.sidebar_layout.add(self.elasticity_slider)
        

        # Anchor layout for sidebar
        self.anchor = UIAnchorLayout()
        
        self.anchor.add(
            anchor_x="right", anchor_y="top", child=self.sidebar_layout
        )

        self.ui.add(self.anchor)

    def on_spawn_ball_click(self, event):
        """Spawn a ball immediately when the button is pressed."""
        self.spawn_ball(0)
    
    def spawn_ball(self, delta_time):

        MAX_BALLS = 20
        if len(self.ball_list) >= MAX_BALLS:
            oldest_ball = self.ball_list.pop(0)
            self.physics_engine.remove_sprite(oldest_ball)
        
        radius = int(self.radius_slider.value)
        elasticity = float(self.elasticity_slider.value)
        color = random.choice([
            arcade.color.RED, 
            arcade.color.BLUE, 
            arcade.color.YELLOW, 
            arcade.color.GREEN,
            arcade.color.PURPLE
        ])
        
        ball = BallObject(radius, color)
        ball.elasticity = elasticity
        
        # Position at random x at top of screen
        x = random.randint(radius, (self.w - self.sidebar_width) - radius)
        y = self.h - 100
        ball.position = (x, y)
        
        # Add to physics engine
        ball.setup_physics(self.physics_engine)
        
        # Add to ball list
        self.ball_list.append(ball)
    
    def on_back_click(self, event):
        """Return to main menu"""
        arcade.unschedule(self.spawn_ball) 
        main_view = MainView()
        self.window.show_view(main_view)
    
    def on_draw(self):
        """Draw the environment"""
        self.clear()
        
        # Step physics
        self.physics_engine.step(1/60.0)
        
        # Draw all objects
        self.wall_list.draw()
        self.ball_list.draw()
        self.ui.draw()
    
    def on_hide_view(self):
        """Disable UI when hiding view"""
        arcade.unschedule(self.spawn_ball)
        self.ui.disable()
    
        
class BallObject(arcade.SpriteCircle):
    """Ball object for the physics simulation"""
    
    def __init__(self, radius, color):
        super().__init__(radius, color)
        self.radius = radius
        self.color = color
        self.mass = radius / 10  # Larger balls have more mass
        self.friction = 0.4
        self.elasticity = 0.99  # Slightly bouncy

    def setup_physics(self, physics_engine):
        """Add this ball to the physics engine with its physical properties."""
        physics_engine.add_sprite(
            self,
            mass=self.mass,
            friction=self.friction,
            elasticity=self.elasticity,
            collision_type="ball"
        )

def main():
    """Run Program"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)
    main_view = MainView()
    window.show_view(main_view)
    arcade.run()


if __name__ == "__main__":
    main()
