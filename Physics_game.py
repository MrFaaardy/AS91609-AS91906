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
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
SCREEN_TITLE = "Physics test"


class MainView(arcade.View):
    #Main View
    
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
        """Switch to environment view"""
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
    
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        
        # Get the actual window size
        width, height = self.window.get_size()
        
        # Create physics engine with stronger gravity
        self.physics_engine = PymunkPhysicsEngine(gravity=(0, -900))
        
        # Create box walls as static sprites
        self.wall_list = arcade.SpriteList()

        # Floor
        floor = arcade.SpriteSolidColor(width=width, height=20, color=arcade.color.WHITE)
        floor.position = width // 2, 10
        self.wall_list.append(floor)
        self.physics_engine.add_sprite(
            floor,
            body_type=PymunkPhysicsEngine.STATIC,
            friction=0.5,
            elasticity=0.99,
        )

        # Ceiling
        ceiling = arcade.SpriteSolidColor(width=width, height=20, color=arcade.color.WHITE)
        ceiling.position = width // 2, height - 10
        self.wall_list.append(ceiling)
        self.physics_engine.add_sprite(
            ceiling,
            body_type=PymunkPhysicsEngine.STATIC,
            friction=0.5,
            elasticity=0.99,
        )

        # Left wall
        left_wall = arcade.SpriteSolidColor(width=20, height=height, color=arcade.color.WHITE)
        left_wall.position = 10, height // 2
        self.wall_list.append(left_wall)
        self.physics_engine.add_sprite(
            left_wall,
            body_type=PymunkPhysicsEngine.STATIC,
            friction=0.5,
            elasticity=0.99,
        )

        # Right wall
        right_wall = arcade.SpriteSolidColor(width=20, height=height, color=arcade.color.WHITE)
        right_wall.position = width - 10, height // 2
        self.wall_list.append(right_wall)
        self.physics_engine.add_sprite(
            right_wall,
            body_type=PymunkPhysicsEngine.STATIC,
            friction=0.5,
            elasticity=0.99,
        )
        
        # List to keep track of balls
        self.ball_list = arcade.SpriteList()
        
        # UI for back button
        self.ui = UIManager()
        self.ui.enable()
        
        # Back button
        back_button = UIFlatButton(text="Back to Menu", width=200)
        back_button.on_click = self.on_back_click
        
        self.anchor = self.ui.add(UIAnchorLayout())
        self.anchor.add(
            anchor_x="left",
            anchor_y="bottom",
            child=back_button
        )
        
        # Schedule ball spawning
        arcade.schedule(self.spawn_ball, 1.0)  # Spawn a ball every second

    
    def spawn_ball(self, delta_time):

        MAX_BALLS = 10
        if len(self.ball_list) >= MAX_BALLS:
            return
        
        """Spawn a new ball at a random position at the top of the screen"""
        radius = random.randint(15, 40)
        color = random.choice([
            arcade.color.RED, 
            arcade.color.BLUE, 
            arcade.color.YELLOW, 
            arcade.color.GREEN,
            arcade.color.PURPLE
        ])
        
        ball = BallObject(radius, color)
        
        # Position at random x at top of screen
        x = random.randint(radius, SCREEN_WIDTH - radius)
        y = 600 - radius
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
