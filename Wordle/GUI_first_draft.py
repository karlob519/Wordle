import pygame
import time
import sys
import engine as eng

# Generating the list of valid guesses
valid_guesses = eng.guesses()

# Initiating Pygame
pygame.init()
pygame.font.init()

# Display
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# End of game window
WIN_X, WIN_Y = WIDTH / 2, 50

# Setting the title
pygame.display.set_caption('WORDLE')

# Box sizes for the grid and keyboard
grid_box_width, grid_box_height = WIDTH / 15, HEIGHT / 12
kb_box_width, kb_box_height = WIDTH / 20, HEIGHT / 17

# Font sizes
grid_font_size = 55
kb_font_size = 17
middle = 18

# Fonts
grid_font = pygame.font.SysFont(None, grid_font_size)
keyboard_font = pygame.font.Font('freesansbold.ttf', kb_font_size)

# Keyboard
keyboard = 'qwertyuiopasdfghjklzxcvbnm'

# Defining colours we will use in RGB code
green = (29, 196, 57)
yellow = (227, 227, 20)
dark_grey = (100, 100, 100)
light_grey = (200, 200, 200)
red = (200, 0, 10)
black = (0, 0, 0)
white = (255, 255, 255)

kb_colour = black
gs_colour = white

# Single box class
class Box:
    def __init__(self, x: int, y: int, text: str, colour: tuple):
        self.x = x
        self.y = y
        self.text = text
        self.colour = colour


# Single button class
class Button(Box):
    def __init__(self, x: int, y: int, text: str, colour: tuple, scale: int, on_click_function=None, one_press=False):
        super().__init__(x, y, text, colour)
        
        self.scale = scale
        self.on_click_function = on_click_function
        self.one_press = one_press
        
        # Fill colour
        self.a = colour[0]
        self.b = colour[1]
        self.c = colour[2]

        self.fill_colours = {'normal': self.colour, 
                             'hover' : (max(0, self.a-20), max(0, self.b-20), max(0, self.c-20)),
                             'pressed' : (max(0, self.a-40), max(0, self.b-40), max(0, self.c-40))}
        
        # Button surface
        self.button_surface = pygame.Surface((self.scale*kb_box_width, kb_box_height))
        self.button_rect = pygame.Rect(self.x, self.y, self.scale*kb_box_width, kb_box_height)
        self.button_surf = keyboard_font.render(self.text, True, kb_colour)

        self.already_pressed = False

    def process(self):
        mouse_pos = pygame.mouse.get_pos()
        self.button_surface.fill(self.fill_colours['normal'])
        if self.button_rect.collidepoint(mouse_pos):
            self.button_surface.fill(self.fill_colours['hover'])
            if pygame.mouse.get_pressed(num_buttons=5)[0]:
                self.button_surface.fill(self.fill_colours['pressed'])
                if self.one_press:
                    self.on_click_function()
                elif not self.already_pressed:
                    self.on_click_function()
                    self.already_pressed = True
            else:
                self.already_pressed = False
        self.button_surface.blit(self.button_surf, 
                [self.button_rect.width/2 - self.button_surf.get_rect().width/2, 
                self.button_rect.height/2 - self.button_surf.get_rect().height/2
            ])
        screen.blit(self.button_surface, self.button_rect)

     
# Indicator class
class Indicator:
    def __init__(self, x: int, y: int, ind: int):
        self.x = x + 5
        self.y = y + grid_box_height - 5
        self.ind = ind

    def show(self):
        self.end_x = self.x + grid_box_width - 10
        self.end_y = self.y
        if self.ind == courser:
            pygame.draw.line(screen, light_grey, (self.x, self.y), (self.end_x, self.end_y), width=3)
        else:
            pygame.draw.line(screen, white, (self.x, self.y), (self.end_x, self.end_y), width=3)
            

# List of boxes
buttons = []
kb_boxes = []
grid_cells = []
empty_grid = []
indicators = []

# Courser, num of attempts
courser = 0
attempt_num = 0

# We will generate a solution later, now its just an empty string
wordle = ''

def text_objects(text: str, font: int, colour: tuple):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

def message_display(text: str, font_size: int, colour: tuple, x: int, y: int):
    largeText = pygame.font.Font('freesansbold.ttf', font_size)
    TextSurf, TextRect = text_objects(text, largeText, colour)
    TextRect.center = (x , y)
    screen.blit(TextSurf, TextRect)
    return
    
# Drawing a single box for the keyboard
def draw_box_kb(x: int, y: int, text: str, colour: tuple, box_width: int, box_height: int):
    write = keyboard_font.render(text.upper(), 1, kb_colour)
    box = Box(x, y, text, colour)
    pygame.draw.rect(screen, box.colour, (box.x, box.y, box_width, box_height))
    screen.blit(write, (box.x + middle, box.y + middle))
    return

# Drawing a border when there is no input
def drawStyleRect_empty(colour: tuple, x: int, y: int, width: int, height: int):
    pygame.draw.rect(screen, colour, (x,y,width,height), 0)
    for i in range(2):
        pygame.draw.rect(screen, (200,200,200), (x-i,y-i,width+2,height+2), 1)
    return

# Drawing a box when ther is input
def drawStyleRect_fill(colour: tuple, x: int, y: int, width: int, height: int):
    pygame.draw.rect(screen, colour, (x,y,width,height), 0)
    for i in range(2):
        pygame.draw.rect(screen, black, (x-i,y-i,width+2,height+2), 1)
    return

# Drawing a single box for the grid
def draw_cell_grid(x: int, y: int, text: str, colour: tuple, box_width: int, box_height: int):
    write = grid_font.render(text, 1, white)
    box = Box(x, y, text, colour)
    drawStyleRect_empty(box.colour, box.x, box.y, box_width, box_height)
    screen.blit(write, (box.x + 2*middle, box.y + 2*middle))
    
    return
 
# Filling a cell with input from the keyboard
def fill_cell(box: Box, letter: str):
    write = grid_font.render(letter.upper(), 1, black)
    box.text = letter
    drawStyleRect_fill(box.colour, box.x, box.y, grid_box_width, grid_box_height)
    screen.blit(write, (box.x + 1.2*middle, box.y + 1.5*middle))
    return 

#Updating the row with input from the score
def fill_cell_update(box: Box, colour: tuple):
    write = grid_font.render(box.text.upper(), 1, white)
    box.colour = colour
    drawStyleRect_fill(box.colour, box.x, box.y, grid_box_width, grid_box_height)
    screen.blit(write, (box.x + 1.2*middle, box.y + 1.5*middle))
    return

# Constructing the keyboard
def kb():
    boxes = []
    dx = kb_box_width + 3
    dy = kb_box_height + 2
    start_x = WIDTH / 4
    start_y = HEIGHT - 3*kb_box_height - 10
    c = 0

    # Getting the top row
    for i in range(10):
        x = start_x + i*dx
        y = start_y
        text = keyboard[i]
        colour = light_grey
        box = Box(x, y, text, colour)
        boxes.append(box)
        c += 1 

    # Getting the middle row
    start_x += kb_box_width / 2
    start_y += dy
    for i in range(c, 19):
        x = start_x + (i-10)*dx
        y = start_y
        text = keyboard[i]
        colour = light_grey
        box = Box(x, y, text, colour)
        boxes.append(box)
        c += 1
    
    # Getting the bottom row
    start_x -= kb_box_width/2
    start_y += dy
    for i in range(9):
        if i == 0:
            x = start_x
            y = start_y
            text = 'ENTER'
            colour = light_grey
            button = Button(x, y, text, colour, 1.5, enter)
            buttons.append(button)
        elif i < 8:
            start_x1 = start_x + kb_box_width / 2
            x = start_x1 + i * dx
            y = start_y
            text = keyboard[18+i]
            colour = light_grey
            box = Box(x, y, text, colour)
            boxes.append(box)
        else:
            start_x1 = start_x + kb_box_width / 2
            x = start_x1 + i * dx
            y = start_y
            text = 'BACK'
            colour = light_grey
            button = Button(x, y, text, colour, 1.5, back)
            buttons.append(button)

    return boxes
            
# Constructing the guessing grid
def grid():
    grid_boxes = []
    dx = grid_box_width + 5
    dy = grid_box_height + 7
    start_x = WIDTH / 3
    start_y = 200
    for i in range(6):
        for j in range(5):
            x = start_x + j*dx
            y = start_y + i*dy
            text = ' '
            colour = white
            box = Box(x, y, text, colour)
            grid_boxes.append(box)

    return grid_boxes

def update_cells(score: list):
    global courser
    for i in range(5):
        x = courser + i - 5
        if score[x%5] == 2:
            colour = green
        elif score[x%5] == 1:
            colour = yellow
        else:
            colour = dark_grey
        box = grid_cells[x]
        fill_cell_update(box, colour)
        grid_cells[x] = box
    return

def update_kb(score: list, guess: str):
    chars = dict.fromkeys(list(guess))
    for i in range(5):
        char = list(guess)[i]
        x = courser + i - 5
        if score[x%5] == 2 and chars[char] != yellow:
            chars[char] = green
        elif score[x%5] == 1:
            chars[char] = yellow
        else:
            if chars[char] is None:
                chars[char] = dark_grey
    for key in chars.keys():
        for box in kb_boxes:
            if box.text == key:
                box.colour = chars[key]
                draw_box_kb(box.x, box.y, box.text, box.colour, kb_box_width, kb_box_height)
            else:
                None
    return 

# Function of the button play_again, restarting the game
def f_yes():
    screen.fill(white)
    generate()
    return

# Function of button quit, quitting the program
def f_no():
    pygame.quit()
    sys.exit()
    
#Defining what happens when the solution is guessed within 6 attempts
def win():
    win_text = 'YOU WIN!'
    message_display(win_text, 40, green, WIN_X, WIN_Y)
    return

# Defining what happens when the solution is not guessed within 6 attempts
def loss():
    win_text = f'YOU LOSE!   ANSWER  :  {wordle.upper()}'
    message_display(win_text, 40, red, WIN_X, WIN_Y)
    return

# Play again and quit buttons
scale = 3
play_again = Button(WIN_X - 150, WIN_Y + 50, 'PLAY AGAIN', green, scale, f_yes)
quit = Button(WIN_X - 125 + scale*kb_box_width, WIN_Y + 50, 'QUIT', red, scale, f_no)
buttons.append(play_again)
buttons.append(quit)

# Defining a function for the case when the guess in invalid
def invalid_guess():
    text = 'Invalid guess, please try again'
    message_display(text, 40, dark_grey, WIN_X, WIN_Y)
    #time.sleep(1)
    return

# Defining a function that fills the canvas blank(white)
def blank():
    tup = (0, 0, 1000, 100)
    screen.fill(white, tup)

# Defining functions of back and enter
def enter():
    global courser, attempt_num

    blank()
    guess = ''.join([grid_cells[t].text for t in range(((courser-1)//5) * 5, courser)])
    if guess in valid_guesses:
        score = eng.score(guess, wordle)
        update_cells(score)
        update_kb(score, guess)
        pygame.display.update()
        attempt_num += 1
        if attempt_num == 6 and sum(eng.score(guess, wordle)) != 10:
            time.sleep(0.5)
            loss()
        else:  
            score = eng.score(guess, wordle)
            if sum(score) == 10:
                time.sleep(0.5)
                win()
            else:
                None
    else:
        invalid_guess()
    return 
    
def back():
    global courser, grid_cells
    courser -= 1
    box = empty_grid[courser]
    draw_cell_grid(box.x, box.y, box.text, box.colour, grid_box_width, grid_box_height)
    grid_cells[courser] = box
    return 

screen.fill(white)

# Setting up the user interface
def generate():
    global kb_boxes, grid_cells, wordle, courser, attempt_num, empty_grid, indicators
    
    # Generating a wordle
    wordle = eng.wordle()

    #Generating all the boxes we will need
    kb_boxes = kb()
    grid_cells = grid()
    empty_grid = grid()

    # Indicator list
    indicators = [Indicator(grid_cells[t].x, grid_cells[t].y, t) for t in range(len(grid_cells))]

    # Resetting the courser and the number of attempt_num 
    courser = 0
    attempt_num = 0

    for box in kb_boxes:
        draw_box_kb(box.x, box.y, box.text, box.colour, kb_box_width, kb_box_height)

    for cell in grid_cells:
        draw_cell_grid(cell.x, cell.y, cell.text, cell.colour, grid_box_width, grid_box_height)
    
    return

# Main game loop
def game_loop():   
    global courser, attempt_num
    
    run = True
    while run:
        # Indicator
        if courser < 30:
            try:
                indicator = indicators[courser]
                indicator.show()
            except IndexError:
                pygame.quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_BACKSPACE:
                    back()
                elif event.key == pygame.K_RETURN and (courser) % 5 == 0:
                    enter()
                elif event.key == pygame.K_RETURN and (courser) % 5 != 0:
                    None
                elif event.key == pygame.K_RIGHT:
                    courser += 1
                elif event.key == pygame.K_LEFT:
                    courser -= 1
                elif event.key == pygame.K_1:
                    print(wordle)
                else:
                    letter = event.unicode
                    box = grid_cells[courser]
                    fill_cell(box, letter)
                    grid_cells[courser] = box
                    courser += 1
                if courser < 30:
                    try:
                        indicator.show()
                    except IndexError:
                        pygame.quit()

        for button in buttons[:4]:
            button.process()
            indicator.show()

        pygame.display.update()

    return

def game():
    generate()
    game_loop()
    pygame.quit()
    sys.exit()

game()