# Originally posted by pilover100 here: https://discord.com/channels/251118043411775489/769121688503582730/980789669711212585

import pygame
from pygame.locals import *
import pathlib
import sys

def render_text(text, x, y, foreground, background, top_surf):
    """
    Renders text onto the display
    """
    font_obj = pygame.font.Font("freesansbold.ttf", 16)
    text_surf = font_obj.render(text, True, foreground, background)
    text_rect = text_surf.get_rect()
    text_rect.center=(x,y)
    top_surf.blit(text_surf, text_rect)
    return (text_surf, text_rect)  # For caching

def swizzle_image(image_surf, swizzle, x, y, top_surf):
    """
    Takes an image from a surface and swaps the colours to
    produce a swizzled image.
    """
    image_pixels = pygame.PixelArray(image_surf)
    
    # Colour key:     R    G    B     "r/g/b" = red/green/blue value, " " = 0
    colour_swaps = [["r", "g", "b"],  # 0 red + yellow (Republic)
                    ["r", "b", "g"],  # 1 red + magenta
                    ["g", "r", "b"],  # 2 green and yellow (Free Worlds)
                    ["b", "r", "g"],  # 3 Green and cyan (sheragi, test dummy)
                    ["g", "b", "r"],  # 4 blue + magenta (syndicate)
                    ["b", "g", "r"],  # 5 blue + cyan (merchant)
                    ["g", "b", "b"],  # 6 red and black (pirate)
                    ["r", "b", "b"],  # 7 pure red
                    ["r", "g", "g"],  # 8 faded red
                    ["g", "b", "b"],  # 9 pure black
                    ["g", "g", "g"],  # 10 faded black
                    ["r", "r", "r"],  # 11 pure white
                    ["g", "g", "b"],  # 12 darkened blue
                    ["g", "b", "r"],  # 13 pure blue
                    ["g", "g", "r"],  # 14 faded blue
                    ["b", "g", "g"],  # 15 darkened cyan
                    ["b", "r", "r"],  # 16 pure cyan
                    ["g", "r", "r"],  # 17 faded cyan
                    ["b", "g", "b"],  # 18 darkened green
                    ["b", "r", "b"],  # 19 pure green
                    ["g", "r", "g"],  # 20 faded green
                    ["g", "g", "b"],  # 21 darkened yellow
                    ["r", "r", "b"],  # 22 pure yellow
                    ["r", "r", "g"],  # 23 faded yellow
                    ["g", "b", "g"],  # 24 darkened magenta
                    ["r", "b", "r"],  # 25 pure magenta
                    ["r", "g", "r"],  # 26 faded magenta
                    ["b", " ", " "],  # 27 red only (cloaked)
                    [" ", " ", " "]]  # 28 black only (outline)
    x_pixels = image_pixels.shape[0]
    y_pixels = image_pixels.shape[1]

    for i in range(x_pixels):
        # Work down each column
        for j in range(y_pixels):  # For each pixel in the column
            px_colour = image_surf.unmap_rgb(image_pixels[i, j])  # Extract components
            red = px_colour.r
            green = px_colour.g
            blue = px_colour.b
            alpha = px_colour.a  # Doesn't change so not bothering to dump it in new colour.

            profile = colour_swaps[swizzle]
            new_colour = []
            for channel in profile:
                if channel == "r":
                    new_colour.append(red)
                elif channel == "g":
                    new_colour.append(green)
                elif channel == "b":
                    new_colour.append(blue)
                else:
                    new_colour.append(0)
            image_pixels[i,j] = (new_colour[0], new_colour[1], new_colour[2], alpha)  # Set the pixel to its new colour
    image_pixels.close()
    image_rect = image_surf.get_rect()
    image_rect.center = (x,y)
    top_surf.blit(image_surf, image_rect)
    pygame.display.update()
    return (image_surf, image_rect)  # For caching

def close():
    pygame.quit()
    sys.exit()

def main():
    pygame.init()
    window = pygame.display.set_mode(flags = pygame.FULLSCREEN)  # Made the screen as large as possible and turn on HW accel,
    pygame.display.set_caption("ES Image Swizzler")  # ....................................... pygame will chose sensible defaults for the rest so no point messing with it.

    FPS = 10  # We're not looking for ultra high performane here are we? (if you are, then don't look at python)
    DELAY = 10  # how long until values of swizzle are accepted, once delay_count reaches 0 a value is accepted
    delay_count = -1
    clock = pygame.time.Clock()
    pygame.key.set_repeat(0,0)  # No key repeat

    window.fill((0,0,0))  # Fill window with black
    x_size, y_size = window.get_size()

    image_x = x_size // 2  # Images are lumped into the centre of the screen
    image_y = y_size // 2

    prompt_x = x_size // 2  # Where the text goes for prompts (near the top)
    prompt_y = y_size // 8

    status_y = y_size - (y_size // 8)
    path_x = x_size // 3
    swizzle_x = (x_size // 3) * 2

    path = str(pathlib.Path.home())  # Set the path to this as a default
    swizzle = 0  # Default swizzle

    pygame.key.start_text_input()  # Makes life a little easier (handles capitilisation for us
    mode = 0  # 0 = default, type numbers to change swizzle, press enter to type an image path. 1 = type path
    messages = ["Type numbers or press +/- to change swizzle. Press return/enter to type image path. Press escape to quit.","Type image path relative to your home directory and press enter to confirm"]
    text_input = ""

    new_image = 0
    new_swizzle = 0

    image = pygame.Surface((1,1))  # Skimp for the initial surfaces
    swizzled_image = image.copy()
    swizzled_rect = swizzled_image.get_rect()
    swizzled_rect.center = (image_x, image_y)

    while True:  # Main loop
        for event in pygame.event.get():
            if event.type == QUIT:
                close()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    close()
                elif event.key == K_RETURN:
                    if mode:
                        path = (str(pathlib.Path.home()) + text_input).replace(r"\\", "/")
                        text_input = ""
                        mode = 0
                        new_image = 1
                    else:
                        mode = 1
                        text_input = ""
                elif event.key == K_PLUS or event.key == K_KP_PLUS:
                    swizzle += 1
                elif event.key == K_MINUS or event.key == K_KP_MINUS:
                    swizzle -= 1
                elif event.key == K_BACKSPACE:
                    text_input = text_input[:-1]
            if event.type == TEXTINPUT:
                if mode:
                    text_input += event.text
                else:
                    text_input += event.text
                    delay_count = DELAY  # Set delay

        delay_count -= 1  # clocks and sanity checks
        if delay_count == 0:
            new_swizzle = 1
            try:
                swizzle = int(text_input)
            except:
                pass
            text_input = ""

        if swizzle < 0:
            swizzle = 0
        elif swizzle > 28:
            swizzle = 28

        window.fill((0,0,0))

        render_text(f"Swizzle: {str(swizzle)}", swizzle_x, status_y, (255,255,255), (0,0,0), window)  # Draw status text, swizzle and path
        if mode:
            path_text = (str(pathlib.Path.home()) + text_input).replace(r"\\", "/")
            render_text(f"Path: {path_text}", path_x, status_y, (255,255,255), (0,0,0), window)
        else:
            render_text(f"Path: {path}", path_x, status_y, (255,255,255), (0,0,0), window)

        render_text(messages[mode], prompt_x, prompt_y, (255,255,255), (0,0,0), window)  # Prompt text

        if new_image:  # loads a new image
            new_swizzle = 1
            new_image = 0
            try:
                image = pygame.image.load(path)
            except:
                render_text("Could not load image!", image_x, image_y, (255,255,255), (0,0,0), window)

        if new_swizzle:  # Swizzles and displays images
            new_swizzle = 0
            swizzled_image = image.copy()  # So we don't overwrite the original
            try:
                swizzled_image, swizzled_rect = swizzle_image(swizzled_image, swizzle, image_x, image_y, window)  # Draw the image
            except:
                swizzled_image, swizzled_rect = render_text("Could not swizzle image!", image_x, image_y, (255,255,255), (0,0,0), window)
        else:  # No new image, so just do the last one again to save time
            window.blit(swizzled_image, swizzled_rect)
        pygame.display.update()
        clock.tick(FPS)  # Finally, tick the clock



if __name__ == "__main__":
    main()
