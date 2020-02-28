import pygame
import random
import pygame.font
pygame.font.init()
pygame.mixer.init()

# Colors
BLACK = (0, 0, 0)
GREEN = (20, 200, 55)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
FONT_COLOR = (150, 150, 150)
clock = pygame.time.Clock()

# Screen Dimensions
screen_height = 600
screen_width = 800

# Set name of window
pygame.display.set_caption('Snake')

# Snake and Food size
object_w = 20
object_h = 20

# Create screen variable
screen = pygame.display.set_mode((screen_width, screen_height))

# List containing a list of coordinates of each segment
snake_segments = []
snake_length = 0

# Sets starting score
score = 0
font_name = pygame.font.match_font("Pixel Miners")


class Logic:
    """Creates logic for game. Movement of snake, collisions, and draws food"""
    def __init__(self):
        self.x_change = 0
        self.y_change = 0
        self.head_x = 400
        self.head_y = 300
        # Sets the random X and Y coordinates for food
        self.food_x = round(random.randrange(0, screen_width - object_w) / 10) * 10
        self.food_y = round(random.randrange(0, screen_height - object_h) / 10) * 10
        self.snake_length = 0
        self.score = 0
        self.running = True

    def movements(self):
        """How the snake responds to key-presses and logic for adding segments"""
        if self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.x_change = -10
                        self.y_change = 0
                    elif event.key == pygame.K_RIGHT:
                        self.x_change = 10
                        self.y_change = 0
                    elif event.key == pygame.K_UP:
                        self.x_change = 0
                        self.y_change = -10
                    elif event.key == pygame.K_DOWN:
                        self.x_change = 0
                        self.y_change = 10

            self.head_x += self.x_change
            self.head_y += self.y_change

            snake_head = []
            snake_head.append(self.head_x)
            snake_head.append(self.head_y)
            snake_segments.append(snake_head)
            snake()

            # If there becomes more segments in list than the desired snake length, then continue
            # to delete the oldest segments in order to keep the desired length
            if len(snake_segments) > self.snake_length:
                del (snake_segments[0])

            # Sets boundaries
            if self.head_x >= 800 or self.head_x < 0 or self.head_y >= 600 or self.head_y < 0:
                snake_segments.clear()
                self.running = False
                end_game()

    def collision(self):
        """Collision between snake and food"""
        if self.head_x == self.food_x and self.head_y == self.food_y:
            self.food_x = round(random.randrange(0, screen_width - object_w) / 10) * 10
            self.food_y = round(random.randrange(0, screen_height - object_h) / 10) * 10
            self.snake_length += 1
            self.score += 1

            # Play collision SFX
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('Music:SFX/SynthChime1.wav'))

    def draw_food(self):
        # Draws food
        pygame.draw.rect(screen, RED, (self.food_x, self.food_y, object_w, object_h))


class Button:

    def __init__(self, screen, msg):
        """Initialize button attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont("Pixel Miners", 54)

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepped only once
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw a blank button and then draw message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


def snake():
    for segment in snake_segments:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], object_w, object_h))


def draw_score(background, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, FONT_COLOR)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    background.blit(text_surface, text_rect)


def game_menu():
    # Play menu music
    pygame.mixer.music.load('Music:SFX/Dragon-Mystery_Looping.mp3')
    pygame.mixer.music.play(-1)

    menu = True
    while menu:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.fill(BLACK)

        # Change color of text when cursor hovers over
        if play_button.msg_image_rect.collidepoint(mouse_x, mouse_y):
            play_button.text_color = RED
            play_button.prep_msg("Play")
            play_button.draw_button()
        else:
            play_button.text_color = WHITE
            play_button.prep_msg("Play")
            play_button.draw_button()

        # Button responsiveness to click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
                if button_clicked:
                    menu = False
                    # Play in-game music
                    pygame.mixer.music.load('Music:SFX/bensound-scifi.mp3')
                    pygame.mixer.music.play(-1)

        pygame.display.update()


def end_game():
    # Play wall collision SFX
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('Music:SFX/PowerDown3.wav'))

    end = True
    while end:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.fill(BLACK)

        # Change color of text when cursor hovers over
        if end_button.msg_image_rect.collidepoint(mouse_x, mouse_y):
            end_button.text_color = RED
            end_button.prep_msg("Restart")
            end_button.draw_button()
        else:
            end_button.text_color = WHITE
            end_button.prep_msg("Restart")
            end_button.draw_button()

        # Button responsiveness to click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_clicked = end_button.rect.collidepoint(mouse_x, mouse_y)
                if button_clicked:
                    game_loop()
                    end = False

        pygame.display.update()


play_button = Button(screen, "Play")
end_button = Button(screen, "Restart")
game_menu()


def game_loop():
    # Set name of window
    pygame.display.set_caption('Snake Game')

    logic = Logic()
    while logic.running:
        screen.fill(BLACK)
        logic.draw_food()
        snake()
        logic.movements()
        logic.collision()
        draw_score(screen, str(logic.score), 25, screen_width / 2, 10)
        clock.tick(15)
        pygame.display.update()

game_loop()