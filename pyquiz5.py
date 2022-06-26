from turtle import color, right
import pygame
import pygame.gfxdraw
import sys
import time
import random
# the Label class is this module below
from label import *


pygame.init()
pygame.mixer.init()
hit = pygame.mixer.Sound("sounds/hit.wav")
grey = [255,250,240]
colorbutton = "white on cornflowerblue"
hovercolor = "blue on orange"
screen = pygame.display.set_mode((1300, 780))
clock = pygame.time.Clock()

buttons = pygame.sprite.Group()

class Button(pygame.sprite.Sprite):
    ''' A button treated like a Sprite... and killed too '''
    
    def __init__(self, position, text, size,
        colors=colorbutton,
        hover_colors="red on green",
        style="button1",
        borderc=(255,255,255),
        command=lambda: print("No command activated for this button")):

        # the hover_colors attribute needs to be fixed
        super().__init__()
        global num

        self.text = text
        self.command = command
        # --- colors ---
        self.colors = colors
        self.original_colors = colors
        self.fg, self.bg = self.colors.split(" on ")
        # hover_colors
        if hover_colors == "red on green":
            self.hover_colors = f"{self.bg} on {self.fg}"
        else:
            self.hover_colors = hover_colors
        # styles can be button1 or button2 (more simple this one)
        self.style = style
        self.borderc = borderc # for the style2
        # font
        self.font = pygame.font.SysFont("Arial", size)
        self.render(self.text)
        self.x, self.y, self.w , self.h = self.text_render.get_rect()
        self.x, self.y = position
        self.rect = pygame.Rect(self.x, self.y, 500, self.h)
        self.position = position
        self.pressed = 1
        # the groups with all the buttons
        buttons.add(self)

    def render(self, text):
        # we have a surface
        self.text_render = self.font.render(text, 1, self.fg)
        # memorize the surface in the image attributes
        self.image = self.text_render

    def update(self):
        self.fg, self.bg = self.colors.split(" on ")
        if self.style == "button1":
            self.draw_button1()
        elif self.style == "button2":
            self.draw_button2()
        if self.command != None:
            self.hover()
            self.click()

    def draw_button1(self):
        ''' draws 4 lines around the button and the background '''
        # horizontal up
        lcolor = (150, 150, 150)
        lcolor2 = (50, 50, 50)
        pygame.draw.line(screen, lcolor, self.position,
            (self.x + self.w , self.y), 5)
        pygame.draw.line(screen, lcolor, (self.x, self.y - 2),
            (self.x, self.y + self.h), 5)
        # horizontal down
        pygame.draw.line(screen, lcolor2, (self.x, self.y + self.h),
            (self.x + self.w , self.y + self.h), 5)
        pygame.draw.line(screen, lcolor2, (self.x + self.w , self.y + self.h),
            [self.x + self.w , self.y], 5)
        # background of the button
        pygame.draw.rect(screen, self.bg, self.rect)  

    def draw_button2(self):
        ''' a linear border '''
        # the width is set to 500 to have the same size not depending on the text size
        pygame.draw.rect(screen, self.bg, (self.x - 50, self.y, 1300 , self.h))
        pygame.gfxdraw.rectangle(screen, (self.x - 50, self.y, 1300 , self.h), self.borderc)

    def check_collision(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # you can change the colors when the pointer is on the button if you want
            self.colors = self.hover_colors
            # pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            self.colors = self.original_colors
            # pygame.mouse.set_cursor(*pygame.cursors.arrow)


    def hover(self):
        ''' checks if the mouse is over the button and changes the color if it is true '''

        self.check_collision()

    def click(self):
        ''' checks if you click on the button and makes the call to the action just one time'''
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and self.pressed == 1 and self.command == on_right:
                print("The answer is:'" + self.text + "'")
                self.command()
                rightorwrong.change_text("RIGHT ANSWER", "green")
                self.pressed = 0
            if pygame.mouse.get_pressed()[0] and self.pressed == 1 and self.command == on_false:
                print("The answer is:'" + self.text + "'")
                self.command()
                rightorwrong.change_text("FALSE ANSWER", "red")
                self.pressed = 0
                

            if pygame.mouse.get_pressed() == (0,0,0):
                self.pressed = 1



# ACTION FOR BUTTON CLICK ================

def on_click():
    
    print("Click on one answer")

def on_right():
    check_score("right")

def on_false():
    ''' if there is no 'right' as arg it means it's false '''
    check_score()

def check_score(answered="wrong"):
    ''' here we check if the answer is right '''
    global qnum, points, rightorwrong
    
    # until there are questions (before last)
    hit.play() # click sound
    if qnum < len(questions):
        print(qnum, len(questions))
        if answered == "right":
            time.sleep(.1) # to avoid adding more point when pressing too much
            points += 1
            # Show the score text
     
        # time.sleep(2)
        
        qnum += 1 # counter for next question in the list
        score.change_text("SCORE: " + str(points), "green")
        # Change the text of the question
        title.change_text(str(qnum) + ". " + questions[qnum-1][0], color="black")
        # change the question number
        # num_question.change_text(str(qnum), "blue")
        show_question(qnum) # delete old buttons and show new
        

    # for the last question...
    elif qnum == len(questions):
        print(qnum, len(questions))
        if answered == "right":
            kill()
            score.change_text("You reached a score of " + str(points), "green")
            title.change_text("", color="black")
            rightorwrong.change_text("", color="red")
            time.sleep(.1)
            points +=1
   
        kill()
        score.change_text("You reached a score of " + str(points), "green")
        title.change_text("", color="black")
        rightorwrong.change_text("", color="red")

    time.sleep(.5)

questions = [
    ["What is meant by the term 'data quality'?", ["The quality of the data, which is characterized by accuracy, precision, level of error, and bias.",
    "The generality present in the source data",  
    "The resolution of the data.", 
    "The lineage of the data"]],
    ["What is meant by the term 'accuracy' in data quality?", ["The level of detail at which data is stored.", 
    "The overall quality of the data.", 
    "Lack of bias in the data.", 
    "The correctness of the output of the dataset."]],
    ["At what point does data quality always start?", ["At the source, with correct input which good data requirements are followed by testing from source to end of chain", 
    "When transferring the data from application databases to the BI (Business Intelligence) application",
    "When testing, after the user enters the wrong input.",
    "When converting data to new requirements."]],
    ["Preserving the quality of data becomes increasingly important over time, which trend(s) are currently taking place that contribute to this?", 
    ["All answers apply.",
    "Big data, data is collected and linked from more angles.",
    "The increasing regulation in various industries.",
    "Testing a BI solution is gaining more and more attention in many organizations and 'BI testers' are in high demand.",]],
    ["Tools to use to clean up data include these tasks except:", ["Prune", 
    "Extract",
    "Transform", 
    "Load"]],
    ["Data must be ... to have high quality:", [ "Unambiguous", "Incoherent",
    "Complex", "Inaccessible"]],
    ["When data is of high quality, then..:", ["It leads to insights that help the organization make better decisions.",
    "It creates discord.",
    "It limits opportunities.",
    "It is complicated/impractical."]],
    ["Which of the following could be the approaches to Artificial Intelligence?", ["All of the mentioned.", "Strong Artificial Intelligence",
    "Weak Artificial Intelligence", "Applied Artificial Intelligence"]],
    ["Which of the following task/tasks Artificial Intelligence could not do yet?", ["All of the mentioned", "Understand natural language robustly",
    "Web mining", "Construction of plans in real time dynamic systems"]],
    ["What is the field of Natural Language Processing (NLP)?", ["All of the mentioned", "Computer Science",
    "Artificial Intelligence", "Linguistics"]],
    ["What is the main challenge/s of NLP?", ["Handling Ambiguity of Sentences",
    "Handling Tokenization", "Handling POS-Tagging", "All of the mentioned"]],
    ["What is a finite set of rules that specifies a language?", [ "Grammar", "Signs",
    "Communication", "Phrase"]]

]




def show_question(qnum):
    ''' put your buttons here '''
    
    # Kills the previous buttons/sprites
    kill()

    
    # The 4 position of the buttons
    pos = [200, 250, 300, 350]
    # randomized, so that the right one is not on top
    random.shuffle(pos)

    Button((10, 200), "1. ", 36, colorbutton,
        hover_colors=hovercolor, style="button2", borderc=(255,255,0),
        command=None)
    Button((10, 250), "2. ", 36, colorbutton,
        hover_colors=hovercolor, style="button2", borderc=(255,255,0),
        command=None)
    Button((10, 300), "3. ", 36,colorbutton,
        hover_colors=hovercolor, style="button2", borderc=(255,255,0),
        command=None)
    Button((10, 350), "4. ", 36, colorbutton,
        hover_colors=hovercolor, style="button2", borderc=(255,255,0),
        command=None)


    # ============== TEXT: question and answers ====================
    Button((50, pos[0]), questions[qnum-1][1][0], 36, colorbutton,
        hover_colors=hovercolor, style="button2", borderc=(255,255,0),
        command=on_right)
    Button((50, pos[1]), questions[qnum-1][1][1], 36, colorbutton,
        hover_colors=hovercolor, style="button2", borderc=(255,255,0),
        command=on_false)
    Button((50, pos[2]), questions[qnum-1][1][2], 36, colorbutton,
        hover_colors=hovercolor, style="button2", borderc=(255,255,0),
        command=on_false)
    Button((50, pos[3]), questions[qnum-1][1][3], 36, colorbutton,
        hover_colors=hovercolor, style="button2", borderc=(255,255,0),
        command=on_false)

def kill():
    for _ in buttons:
        _.kill()    

qnum = 1
points = 0
# ================= SOME LABELS ==========================
gametitle = Label(screen, 'Data Engineering & NLP quiz', 0, 0, size=20, color="cornflowerblue")
# num_question = Label(screen, str(qnum) + ".", 100, 105, size=50, color="black")
score = Label(screen, "SCORE: 0", 50, 400, size=50, color="green")
title = Label(screen, str(qnum) + ". " + questions[qnum-1][0], 0, 100, 30, color="black")
rightorwrong = Label(screen, "", 300, 500, size=100, color="green")

def start_again():
    pass

def loop():
    global game_on, points, grey

    show_question(qnum)
 
    while True:
        screen.fill(grey)
        for event in pygame.event.get(): # ====== quit / exit
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        buttons.update() #                     update buttons
        buttons.draw(screen)
        show_labels()        #                 update labels
        clock.tick(60)
        pygame.display.update()
        
   

if __name__ == '__main__':
    pygame.init()
    game_on = 1
    loop()