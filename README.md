# ChinguBrightnessChanger
a brightness and color temperature gui with **vim** keybindings
> **chingu** means **friend** in korean

![brightnessGui Screenshot](https://user-images.githubusercontent.com/68774237/131709040-a51d3372-d8c8-4ab0-aa95-19543ed1708d.png)

## Usage
keybindings
```
h - lower the color temperature
j - lower the brightness
k - increase the brightness
l - increase the color temperature

r - to reset
q - to quit
```

## Requirments
- linux
- [redshift](https://wiki.archlinux.org/title/Redshift)
##### **python packages**
- pygame 1.9.5+

## Installation
1. clone or download the project/python file

    `$ git clone https://github.com/Rdkang/chinguBrightnessChanger.git`

2. run the main python file called **gui.py**

    `$ python gui.py`

3. thats it! :)

i would suggest a program like [xbindkeys](https://wiki.archlinux.org/title/Xbindkeys) to assign a shortcut of your choosing to run the program

such as having this in your `.xbindkeysrc`:
```bash
"python ~/Documents/chinguBrightnessChanger/gui.py"
    alt+c
```      


## Todo
- be able to change the brightness of each display independent of each other
