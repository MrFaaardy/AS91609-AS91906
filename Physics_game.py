#By Hanz Santos
#14/4/2025

import arcade
import arcade.gui
from arcade.gui import *

import numpy
import scipy 
import pymunk


# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
SCREEN_TITLE = "Window"
SIDEBAR_WIDTH = 200
SIDEBAR_HIDE_DELAY = 2.0 
SIDEBAR_ANIMATION_SPEED = 5.0 


class MainView(arcade.View):
    #Main View
    
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        
        self.ui = UIManager()
        self.ui.enable()
        
        # Create main layout
        self.grid_layout = UIGridLayout(
            column_count=4, 
            row_count=3,
            vertical_spacing=20, 
            horizontal_spacing=20,  
            )
        
        # Title
        self.title = UITextArea(text="Main Menu", width=300, height=60, font_size=24,text_color=arcade.color.WHITE)
        
        # Buttons
        self.Button1 = UIFlatButton(text="Pendulum", width=200, height=200)
        self.Button1.on_click = self.on_environment_click
        
        self.Button2 = UIFlatButton(text="Button2", width=200, height=200)
        
        self.Button3 = UIFlatButton(text="Exit", width=200, height=200)
        self.Button3.on_click = self.on_exit_click
        
        # Add elements to layout
        self.grid_layout.add(self.Button1, column=0, row=0)
        self.grid_layout.add(self.Button2, column=1, row=0)
        self.grid_layout.add(self.Button3, column=2, row=0)
        
        # Center the layout
        self.ui.add(UIAnchorLayout().add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.grid_layout,
        ))

        self.ui.add(UIAnchorLayout().add(
            anchor_x="center_x",
            anchor_y="top",
            child=self.title,
        ))
    
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
    """Second view with auto-hiding sidebar"""
    
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_GRAY)
        
        self.ui = UIManager()
        self.ui.enable()
        
        # Sidebar properties
        self.sidebar_x = -SIDEBAR_WIDTH + 10  # Start mostly hidden
        self.sidebar_target_x = -SIDEBAR_WIDTH + 10
        self.sidebar_visible = False
        self.mouse_in_sidebar = False
        self.hide_timer = 0.0
        
        # Create sidebar UI
        self.setup_sidebar()
        
        # Main content area
        self.setup_main_content()
    
    def setup_sidebar(self):
        """Create sidebar UI elements"""
        self.sidebar_layout = UIBoxLayout(vertical=True, space_between=10)
        
        # Sidebar title
        sidebar_title = UITextArea(text="Sidebar", width=180, font_size=16,text_color=arcade.color.WHITE)
        
        # Sidebar buttons
        button1 = UIFlatButton(text="Option 1", width=180, height=40)
        button2 = UIFlatButton(text="Option 2", width=180, height=40)
        button3 = UIFlatButton(text="Option 3", width=180, height=40)
        button4 = UIFlatButton(text="Back to Menu", width=180, height=40)
        button4.on_click = self.on_back_click
        
        # Add elements to sidebar
        self.sidebar_layout.add(sidebar_title)
        self.sidebar_layout.add(button1)
        self.sidebar_layout.add(button2)
        self.sidebar_layout.add(button3)
        self.sidebar_layout.add(button4)
        
        # Create sidebar container with background
        self.sidebar_container = UIAnchorLayout(
            anchor_x="left",
            anchor_y="center_y",
            child=UISpace(
                width=SIDEBAR_WIDTH,
                height=SCREEN_HEIGHT,
                color=arcade.color.DARK_GRAY,
                child=UIAnchorLayout(
                    anchor_x="center",
                    anchor_y="center",
                    child=self.sidebar_layout
                )
            )
        )
        
        # Position sidebar (will be animated)
        self.sidebar_widget = self.ui.add(self.sidebar_container)
    
    def setup_main_content(self):
        """Create main content area"""
        main_content = UIBoxLayout(vertical=True, space_between=20)
        
        title = UITextArea(text="Environment View", width=400, height=60,font_size=20,text_color=arcade.color.BLACK)
        
        info_text = UITextArea(
            text="This is the main content area.\nHover over the left edge to show the sidebar.\nThe sidebar will auto-hide after 2 seconds.",
            width=500,
            height=100,
            font_size=14,
            text_color=arcade.color.DARK_GRAY
        )
        
        main_content.add(title)
        main_content.add(info_text)
        
        # Center main content
        self.ui.add(UIAnchorLayout(
            anchor_x="center",
            anchor_y="center",
            child=main_content
        ))
    
    def on_back_click(self, event):
        """Return to main menu"""
        main_view = MainView()
        self.window.show_view(main_view)
    
    def on_update(self, delta_time):
        """Update sidebar animation and auto-hide logic"""
        # Check if mouse is in sidebar area
        mouse_x, mouse_y = arcade.get_mouse_position(self.window)
        
        # Consider sidebar area including when it's hidden
        sidebar_hover_zone = 50  # pixels from left edge
        self.mouse_in_sidebar = (mouse_x < max(self.sidebar_x + SIDEBAR_WIDTH, sidebar_hover_zone))
        
        # Determine target position
        if self.mouse_in_sidebar:
            self.sidebar_target_x = 0  # Fully visible
            self.hide_timer = 0.0
            self.sidebar_visible = True
        else:
            if self.sidebar_visible:
                self.hide_timer += delta_time
                if self.hide_timer >= SIDEBAR_HIDE_DELAY:
                    self.sidebar_target_x = -SIDEBAR_WIDTH + 10  # Mostly hidden, show small edge
                    self.sidebar_visible = False
        
        # Animate sidebar position
        if abs(self.sidebar_x - self.sidebar_target_x) > 1:
            diff = self.sidebar_target_x - self.sidebar_x
            self.sidebar_x += diff * SIDEBAR_ANIMATION_SPEED * delta_time
        else:
            self.sidebar_x = self.sidebar_target_x
        
        # Update sidebar position
        if hasattr(self, 'sidebar_widget') and self.sidebar_widget:
            # Remove and re-add sidebar at new position
            self.ui.remove(self.sidebar_widget)
            
            # Create new positioned sidebar
            positioned_sidebar = UISpace(
                x=self.sidebar_x,
                y=0,
                width=SIDEBAR_WIDTH,
                height=SCREEN_HEIGHT,
                color=arcade.color.DARK_GRAY,
                child=UIAnchorLayout(
                    anchor_x="center",
                    anchor_y="center",
                    child=self.sidebar_layout
                )
            )
            
            self.sidebar_widget = self.ui.add(positioned_sidebar)
    
    def on_draw(self):
        self.clear()
        
        # Draw a visual indicator for the sidebar hover zone when sidebar is hidden
        if not self.sidebar_visible and not self.mouse_in_sidebar:
            arcade.draw_rectangle_filled(
                5, SCREEN_HEIGHT // 2, 10, SCREEN_HEIGHT,
                arcade.color.GRAY
            )
        
        self.ui.draw()
        
        # Draw some sample content
        arcade.draw_text("Main Content Area", 
                        SCREEN_WIDTH // 2, 
                        SCREEN_HEIGHT - 100,
                        arcade.color.BLACK, 
                        font_size=24, 
                        anchor_x="center")
    
    def on_hide_view(self):
        # Disable UI when hiding view
        self.ui.disable()


class Sidebar:
    """Standalone sidebar class (alternative implementation)"""
    
    def __init__(self, x=0, y=0, width=200, height=600):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = False
        self.target_x = x
        self.animation_speed = 5.0
        
        # UI elements
        self.ui_manager = None
        self.buttons = []
    
    def toggle(self):
        """Toggle sidebar visibility"""
        self.visible = not self.visible
        self.target_x = 0 if self.visible else -self.width + 10
    
    def update(self, delta_time):
        """Update sidebar position animation"""
        if abs(self.x - self.target_x) > 1:
            diff = self.target_x - self.x
            self.x += diff * self.animation_speed * delta_time
        else:
            self.x = self.target_x
    
    def on_draw(self):
        """Draw the sidebar"""
        if self.x > -self.width:  # Only draw if at least partially visible
            arcade.draw_rectangle_filled(
                self.x + self.width // 2, 
                self.y + self.height // 2,
                self.width, 
                self.height,
                arcade.color.DARK_GRAY
            )


def main():
    """Main function to run the application"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    main_view = MainView()
    window.show_view(main_view)
    arcade.run()


if __name__ == "__main__":
    main()

