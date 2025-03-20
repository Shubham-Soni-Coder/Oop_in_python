import pygame
import tkinter as tk
from tkinter import messagebox
import threading

class MsgBoxHandler:
    def __init__(self):
        self.root = None  # Placeholder for Tkinter root window
        self.is_thread_running = False  # Flag to track if the thread is already running

    def show_msg(self):
        try:
            # If a message box/root already exists, destroy it
            if self.root is not None:
                self.root.destroy()
                self.root = None

            # Create a new Tkinter root window
            self.root = tk.Tk()
            self.root.withdraw()

            # Show the message box
            messagebox.showinfo("Info", "New message box created!")
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            # Destroy the root window after the message box is closed
            if self.root is not None:
                self.root.destroy()
                self.root = None
            self.is_thread_running = False

    def run_in_thread(self):
        # Start the thread to show the message box
        threading.Thread(target=self.show_msg).start()

# Function to check if the button is clicked
def is_button_clicked(mouse_pos, button_rect):
    return button_rect.collidepoint(mouse_pos)

# Pygame integration
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Pygame Window")

msg_handler = MsgBoxHandler()

# Button properties
button_color = (0, 200, 0)  # Green
button_hover_color = (0, 255, 0)  # Lighter green
button_rect = pygame.Rect(150, 120, 100, 50)  # x, y, width, height
font = pygame.font.Font(None, 36)  # Default font

# Main Pygame loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if is_button_clicked(event.pos, button_rect):
                msg_handler.run_in_thread()

    # Draw the button
    mouse_pos = pygame.mouse.get_pos()
    if is_button_clicked(mouse_pos, button_rect):
        pygame.draw.rect(screen, button_hover_color, button_rect)
    else:
        pygame.draw.rect(screen, button_color, button_rect)
    
    # Draw the button text
    button_text = font.render("Click Me", True, (255, 255, 255))  # White text
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.fill((50, 150, 255))  # Background color
    screen.blit(button_text, text_rect)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
