import re
import subprocess
import pathlib
import sys
import os
import pygame
from pygame import font

BACKGROUND = '#282a36'
FONT = 'JetBrainsMono Nerd Font'
REFRESH_RATE = 60
WINDOW_W = 450
WINDOW_H = 200

pygame.init()
clock = pygame.time.Clock()

path = pathlib.Path(__file__).parent.absolute()
temperaturePath = "/tmp/temperature.txt"

FPS = 60
temperature = 6500
COUNT = 0

white = '#f8f8f2'

Screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption('Brightness Gui')


def counter():
    global COUNT
    COUNT += 1
    return COUNT


def message_screen(message: str, colour: str, font_size: int, x_pos: int, y_pos: int):
    font = pygame.font.SysFont(FONT, font_size)
    screen_text = font.render(message, True, colour)
    Screen.blit(screen_text, [int(WINDOW_W * x_pos), int(WINDOW_H * y_pos)])


def exiting():
    message_screen('game is saving', white, 30, 0.4, 0.5)
    pygame.quit()
    sys.exit()


def connectedScreens():
    # returns the text of connected screens
    screens = subprocess.run(r"xrandr -q | grep connected | awk '/ connected/ {print $1}'", shell=True, capture_output=True)

    # pattern to match everything in apostrophes as the new line is also returned from the terminal command
    pattern = re.compile("'([^']*)'")

    screens = re.findall(pattern, str(screens.stdout.split()))
    if len(screens) > 1:
        # reverse the list so that hdmi is first
        screens.reverse()
        screens.insert(0, 'All')
        return screens
    else:
        screens.insert(0, 'All')
        return screens


def getBrightness():
    # if 'all' will return the brightness of the first display otherwise what is chosen
    if chosenDisplay == 'All':
        brightnesss = subprocess.run(f"xrandr --verbose --current | grep ^{display[1]} -A5 | tail -n1", shell=True, capture_output=True)
    else:
        brightnesss = subprocess.run(f"xrandr --verbose --current | grep ^{chosenDisplay} -A5 | tail -n1", shell=True, capture_output=True)
    return float(str(brightnesss.stdout).split(' ')[1][:-3])


def getTemp():
    global temperature

    # creates 'temperature.txt' if doesn't exist
    if not os.path.exists(temperaturePath):
        with open(temperaturePath, 'w'):
            pass

    # reads temperature.txt for the temperature to use if not then puts the number '6500' in the file and uses that
    with open(temperaturePath, 'r+') as file:
        lines = file.readlines()
        # if there are no lines in the file
        if not lines:
            pass
        else:
            temperature = lines[0]


def makeNextTemp(height):
    # deletes all lines in the file
    open(temperaturePath, 'w').close()

    with open(temperaturePath, 'r+') as file:
        # if temperature is below 1900 will make the newTemp 6000, if true then increase the temperature and viceVersa
        if int(temperature) - 1000 <= 1900:
            newTemp = 6000
            file.write(str(newTemp))
            return newTemp
        else:
            if height == True:
                newTemp = int(temperature) + 1000
                file.write(str(newTemp))
            elif height == False:
                newTemp = int(temperature) - 1000
                file.write(str(newTemp))
                return newTemp


display = connectedScreens()
chosenDisplay = display[0]


# where it all comes together
def maingameloop():
    global display, chosenDisplay

    running = True
    while running:
        brightness = getBrightness()

        pyevents = pygame.event.get()
        for event in pyevents:
            # press 'x' or 'q' to quit
            if event.type == pygame.QUIT:
                exiting()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    exiting()

                if chosenDisplay == 'All':
                    # changes the **brightness** using redshift
                    if event.key == pygame.K_j:
                        getTemp()
                        changed = subprocess.run(f"redshift -b {brightness-0.1} -PO {temperature}", shell=True, capture_output=True)
                    if event.key == pygame.K_k:
                        getTemp()
                        changed = subprocess.run(f"redshift -b {brightness+0.1} -PO {temperature}", shell=True, capture_output=True)
                else:
                    if event.key == pygame.K_j:
                        getTemp()
                        indieChange = subprocess.run(
                            f"xrandr --output {chosenDisplay} --mode 1920x1080 --rate {REFRESH_RATE} --brightness {brightness - 0.1}", shell=True, capture_output=True)
                    if event.key == pygame.K_k:
                        getTemp()
                        indieChange = subprocess.run(
                            f"xrandr --output {chosenDisplay} --mode 1920x1080 --rate {REFRESH_RATE} --brightness {brightness + 0.1}", shell=True, capture_output=True)

                # changes the **temperature** using redshift
                if event.key == pygame.K_h:
                    getTemp()
                    newTemp = makeNextTemp(False)
                    changed = subprocess.run(f"redshift -b {brightness} -PO {newTemp}", shell=True, capture_output=True)
                if event.key == pygame.K_l:
                    getTemp()
                    newTemp = makeNextTemp(True)
                    changed = subprocess.run(f"redshift -b {brightness} -PO {newTemp}", shell=True, capture_output=True)

                # resets the brightness and temperature
                if event.key == pygame.K_r:
                    changed = subprocess.run(f"redshift -x", shell=True, capture_output=True)
                    open(temperaturePath, 'w').close()

                    with open(temperaturePath, 'r+') as file:
                        file.write('6500')

                # work in progress
                if event.key == pygame.K_d:
                    for index, indiDisplay in enumerate(display):
                        if chosenDisplay == indiDisplay:
                            rightIndex = index

                    if rightIndex == len(display) - 1:
                        chosenDisplay = display[0]
                    elif rightIndex == 0:
                        chosenDisplay = display[1]
                    elif rightIndex == 1:
                        chosenDisplay = display[2]
                    elif rightIndex == 2:
                        chosenDisplay = display[3]

        # graphical user interface is here
        Screen.fill(BACKGROUND)
        message_screen('Brightness Gui', white, 20, 0.1, 0.1)
        message_screen(f"{chosenDisplay}", white, 30, 0.1, 0.4)
        message_screen(f"{brightness}", white, 20, 0.6, 0.42)

        pygame.display.update()
        clock.tick(FPS)


maingameloop()
