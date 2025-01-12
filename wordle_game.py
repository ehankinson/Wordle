import pygame
import sys
import random
from wordle import Wordle

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
BG_COLOR = (18, 18, 19)
TEXT_COLOR = (255, 255, 255)
GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)
GRAY = (58, 58, 60)
DARKER_GRAY = (30, 30, 31)  # For wrong letters
FONT = pygame.font.Font(None, 45)
SMALL_FONT = pygame.font.Font(None, 40)
POPUP_BG = (40, 40, 40)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER = (130, 130, 130)
POPUP_WIDTH = 300
POPUP_HEIGHT = 200

# Additional Constants for Confetti
CONFETTI_COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 0, 255), (0, 255, 255),
    (255, 128, 0), (255, 0, 128), (128, 0, 255)
]

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle Game")

# Keyboard layout
KEYBOARD = [
    "QWERTYUIOP",
    "ASDFGHJKL",
    "ZXCVBNM"
]

def draw_text(text, color, x, y, font=FONT, offset_x=0, offset_y=0):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x + offset_x, y + offset_y))
    screen.blit(text_surface, text_rect)

def draw_grid(guesses, current_guess, all_feedback):
    grid_width = 5 * 75
    x_offset = (WIDTH - grid_width) // 2
    for row in range(6):
        for col in range(5):
            x = x_offset + col * 75 + 37.5
            y = 50 + row * 75 + 37.5
            
            # Draw the box
            if row < len(guesses):
                # Get the feedback color for completed guesses
                feedback_color = GRAY
                if row < len(all_feedback):
                    if all_feedback[row][col] == 'g':
                        feedback_color = GREEN
                    elif all_feedback[row][col] == 'y':
                        feedback_color = YELLOW
                    else:  # 'b'
                        feedback_color = DARKER_GRAY
                pygame.draw.rect(screen, feedback_color, (x - 37.5, y - 37.5, 70, 70), 0)  # Filled rectangle
                pygame.draw.rect(screen, GRAY, (x - 37.5, y - 37.5, 70, 70), 2)  # Border
                draw_text(guesses[row][col].upper(), TEXT_COLOR, x, y, FONT, offset_x=-2, offset_y=-2)
            else:
                pygame.draw.rect(screen, GRAY, (x - 37.5, y - 37.5, 70, 70), 2)
                if row == len(guesses) and col < len(current_guess):
                    draw_text(current_guess[col].upper(), TEXT_COLOR, x, y, FONT, offset_x=-2, offset_y=-2)

def draw_keyboard():
    buffer = 50
    y_offset = 6 * 75 + 50 + buffer
    key_size = 55
    key_spacing = 5
    for row, keys in enumerate(KEYBOARD):
        x_offset = (WIDTH - len(keys) * (key_size + key_spacing)) // 2
        for col, key in enumerate(keys):
            x = x_offset + col * (key_size + key_spacing) + key_size / 2
            y = y_offset + row * (key_size + key_spacing) + key_size / 2
            pygame.draw.rect(screen, GRAY, (x - key_size / 2, y - key_size / 2, key_size, key_size), 0)
            draw_text(key, TEXT_COLOR, x, y, SMALL_FONT)

class Confetti:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = random.choice(CONFETTI_COLORS)
        self.size = random.randint(5, 10)
        self.speed = random.randint(2, 8)
        self.angle = random.uniform(-0.5, 0.5)

    def update(self):
        self.y += self.speed
        self.x += self.angle
        return self.y < HEIGHT

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

def create_confetti():
    confetti = []
    for _ in range(100):  # Number of confetti pieces
        x = random.randint(0, WIDTH)
        y = random.randint(-HEIGHT, 0)
        confetti.append(Confetti(x, y))
    return confetti

def reset_game(wordle):
    final_word = wordle.get_random_word()
    print(f"Final word is: {final_word}")
    f_letters = wordle.final_guess_letters(final_word)
    return final_word, f_letters, [], "", []

def draw_button(screen, text, rect, color):
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, TEXT_COLOR, rect, 2)
    text_surface = SMALL_FONT.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def show_result_popup(screen, background, won=True):
    popup_rect = pygame.Rect((WIDTH - POPUP_WIDTH) // 2, (HEIGHT - POPUP_HEIGHT) // 2,
                           POPUP_WIDTH, POPUP_HEIGHT)
    
    # Adjust button dimensions and positioning
    button_width = 180
    button_height = 50
    button_spacing = 20
    bottom_padding = 30
    title_height = 40
    
    # Calculate vertical positioning to account for title and all spaces
    total_content_height = title_height + button_height * 2 + button_spacing + bottom_padding
    start_y = popup_rect.centery - total_content_height/2 + title_height + button_spacing
    
    # Center the buttons horizontally and position them vertically
    continue_button = pygame.Rect(popup_rect.centerx - button_width//2,
                                start_y,
                                button_width, button_height)
    
    quit_button = pygame.Rect(popup_rect.centerx - button_width//2,
                            continue_button.bottom + button_spacing,
                            button_width, button_height)

    while True:
        # Draw the background and popup
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, POPUP_BG, popup_rect)
        pygame.draw.rect(screen, TEXT_COLOR, popup_rect, 2)

        # Draw title
        title_text = "You Won!" if won else "You Lost!"
        title = FONT.render(title_text, True, TEXT_COLOR)
        title_rect = title.get_rect(centerx=popup_rect.centerx, top=popup_rect.top + 20)
        screen.blit(title, title_rect)

        # Get mouse position and check for hover
        mouse_pos = pygame.mouse.get_pos()
        continue_color = BUTTON_HOVER if continue_button.collidepoint(mouse_pos) else BUTTON_COLOR
        quit_color = BUTTON_HOVER if quit_button.collidepoint(mouse_pos) else BUTTON_COLOR

        # Draw buttons
        draw_button(screen, "Continue", continue_button, continue_color)
        draw_button(screen, "Quit", quit_button, quit_color)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    return True
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def celebrate_win(screen):
    confetti = create_confetti()
    celebration_time = 0
    start_time = pygame.time.get_ticks()
    
    background = screen.copy()
    
    while celebration_time < 3000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    return show_result_popup(screen, background, won=True)
        
        screen.blit(background, (0, 0))
        
        confetti = [c for c in confetti if c.update()]
        for c in confetti:
            c.draw(screen)
            
        if len(confetti) < 100:
            confetti.extend([Confetti(random.randint(0, WIDTH), -10) for _ in range(5)])
            
        pygame.display.flip()
        celebration_time = pygame.time.get_ticks() - start_time
    
    return show_result_popup(screen, background, won=True)

def main():
    wordle = Wordle()
    final_word, f_letters, guesses, current_guess, all_feedback = reset_game(wordle)

    while True:
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(current_guess) == 5:
                        feedback = wordle.compare(f_letters, current_guess)
                        guesses.append(current_guess)
                        all_feedback.append(feedback)
                        if feedback == ['g', 'g', 'g', 'g', 'g']:
                            print("You guessed the word!")
                            current_guess = ""
                            draw_grid(guesses, current_guess, all_feedback)
                            draw_keyboard()  # Draw keyboard before taking screenshot
                            pygame.display.flip()
                            if celebrate_win(screen):
                                final_word, f_letters, guesses, current_guess, all_feedback = reset_game(wordle)
                            continue
                        current_guess = ""
                        # Check if player has used all 6 guesses
                        if len(guesses) >= 6:
                            print(f"Game Over! The word was: {final_word}")
                            draw_grid(guesses, current_guess, all_feedback)
                            draw_keyboard()  # Draw keyboard before taking screenshot
                            pygame.display.flip()
                            if show_result_popup(screen, screen.copy(), won=False):
                                final_word, f_letters, guesses, current_guess, all_feedback = reset_game(wordle)
                            continue
                elif event.key == pygame.K_BACKSPACE:
                    current_guess = current_guess[:-1]
                elif len(current_guess) < 5 and event.unicode.isalpha():
                    current_guess += event.unicode.lower()

        draw_grid(guesses, current_guess, all_feedback)
        draw_keyboard()

        pygame.display.flip()

if __name__ == "__main__":
    main()