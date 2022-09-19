import pygame.mixer as mx

# Defining sound effects 
# Mute is off by default, toggled by TAB
mute_val = True

def mute():
    global mute_val
    if not mute_val:
        mute_val = True
    else:
        mute_val = False

    return

def intro():
    sound = mx.Sound('SFX/intro.wav')
    if not mute_val:
        mx.Sound.play(sound)

    return

def loss():
    sound = mx.Sound('SFX/Fail sound effect.wav')
    if not mute_val:
        mx.Sound.play(sound)

    return

def win():
    sound = mx.Sound('SFX/WIN sound effect.wav')
    if not mute_val:
        mx.Sound.play(sound)

    return

def click():
    sound = mx.Sound('SFX/click.wav')
    if not mute_val:
        mx.Sound.play(sound)

    return

def back():
    sound = mx.Sound('SFX/back.wav')
    if not mute_val:
        mx.Sound.play(sound)

    return

def animation():
    sound = mx.Sound('SFX/karate_animation.wav')
    if not mute_val:
        mx.Sound.play(sound)

    return

def invalid():
    sound = mx.Sound('SFX/invalid_guess.wav')
    if not mute_val:
        mx.Sound.play(sound)

    return

def quit():
    sound = mx.Sound('SFX/game_over.wav')
    if not mute_val:
        mx.Sound.play(sound)

    return 

def clown():
    sound = mx.Sound('SFX/clown.wav')
    if not mute_val:
        mx.Sound.play(sound)

    return