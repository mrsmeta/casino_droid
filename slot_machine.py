import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1000
screen_height = 600

# Colors
WHITE = (255, 255, 255)

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Slot Machine Game")

# Load images
icon_images = [pygame.image.load("lemon_resized.png"), pygame.image.load("flower_resized.png"), pygame.image.load("fire_resized.png")]
play_button = pygame.image.load("play_resized.png")

# Function to draw the slot machine icons
def draw_icons(icons, positions):
    for i in range(3):
        screen.blit(icons[i], positions[i])

# Function to simulate spinning
def spin():
    screen.fill(WHITE) 
    spin_durations = [1, 2, 3]  # Different durations for each icon
    icons = [random.choice(icon_images) for _ in range(3)]  # Start with a random icon for each slot
    final_icons = [None, None, None]  # Final icons to be displayed

    # Each icon will stop at a different time
    start_time = time.time()

    # While loop control
    keep_spinning = True

    while keep_spinning:
        current_time = time.time()
        keep_spinning = False  # Assume we're done unless a slot is still spinning
        for i in range(3):
            if final_icons[i] is None:  # Only spin if the final icon hasn't been set
                if current_time - start_time >= spin_durations[i]:
                    final_icons[i] = icons[i]  # Lock in the final icon for this slot
                else:
                    icons[i] = random.choice(icon_images)  # Continue spinning
                    keep_spinning = True  # At least one slot is still spinning

        draw_icons(icons, [(screen_width / 2 - 400, screen_height / 2),
                           (screen_width / 2 - 75, screen_height / 2), 
                           (screen_width / 2 + 250, screen_height / 2)])
        pygame.display.flip()
        time.sleep(0.03)  # Adjust this for speed of spin

    # Spin has finished, check results with final_icons
    if final_icons[0] == final_icons[1] == final_icons[2]:
        message = "You win!"
        winner = True
    elif final_icons[0] == final_icons[1] or final_icons[1] == final_icons[2] or final_icons[0] == final_icons[2]:
        message = "You win!"
        winner = True
    else:
        message = "Play again!"
        winner = False

    # Display the message
    font = pygame.font.Font(None, 96)
    text = font.render(message, True, (0, 0, 0))  # Black color
    text_rect = text.get_rect(center=(screen_width / 2, 100))  # Positioned at the top of the screen
    screen.blit(text, text_rect)
    pygame.display.flip()

    # If the player lost, wait for them to click to play again
    if not winner:
        waiting_for_play_again = True
        while waiting_for_play_again:
            for inner_event in pygame.event.get():
                if inner_event.type == pygame.QUIT:
                    return False  # End the game
                if inner_event.type == pygame.MOUSEBUTTONDOWN:
                    waiting_for_play_again = False  # User clicked to play again

    return winner  

# Main game loop
running = True
ready_to_play = True

while running:
    if ready_to_play:
        screen.fill(WHITE)  # Clear the screen before drawing the play button
        screen.blit(play_button, play_button.get_rect(center=(screen_width / 2, screen_height / 2)))
        pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and ready_to_play:
            # Check if the user clicked the play button
            if play_button.get_rect(center=(screen_width / 2, screen_height / 2)).collidepoint(event.pos):
                ready_to_play = False  # The game is now in "playing" state
                winner = spin()
                if not winner:
                    # If the player loses, set the game as ready to play again
                    ready_to_play = True

pygame.quit()
