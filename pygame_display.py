from math import tan
from time import sleep
import freenect
import pygame, sys, seaborn

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS_COUNT = 4

MAIN_WINDOW_SURFACE = None

FPS_CLOCK = pygame.time.Clock()
COLOR_MAP = seaborn.color_palette("Spectral", 1100).as_hex()


def initialize_pygame():
    
    pygame.init()

    global MAIN_WINDOW_SURFACE
    MAIN_WINDOW_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            
    window_title = 'Kinect depth preview'
    pygame.display.set_caption(window_title)


def update_depth():
    global depth
    depth, _ = freenect.sync_get_depth()


def quit_pygame():
    freenect.sync_stop()
    pygame.quit()
    sys.exit()


def get_color(depth_value):
    if depth_value == 2047:
        return 0
    if depth_value >= 1100:
        return 0x00ff00
    hex = COLOR_MAP[int(depth_value)]
    return int(hex[1:], base=16)


def main_loop():
    while True:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:           
                quit_pygame()
            
            elif event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                   quit_pygame()
                       
        update_depth()
        draw_pixels()
        # tilt_state = freenect.get_tilt_state(device)
        # print(f"tilt: {freenect.get_tilt_degs(tilt_state)}")
        pygame.display.update()
        FPS_CLOCK.tick(FPS_COUNT)

def to_cm(d):
    return 12.36 * tan(d / 2842.5 + 1.1863)


def draw_pixels():
    # MAIN_WINDOW_SURFACE.fill(pygame.Color('black'))
    
    try:
        # start_time = pygame.time.get_ticks()
        pixel_array_obj = pygame.PixelArray(MAIN_WINDOW_SURFACE)

        for y in range(WINDOW_HEIGHT):
            for x in range(WINDOW_WIDTH):
                d = int(depth[y][x])
                color = get_color(d)

                if x == 320 and y == 240:

                    print(f"depth: {to_cm(d)}cm")
                    color = 0xd40b95

                pixel_array_obj[x, y] = color

        # end_time = pygame.time.get_ticks()   
        # delta_time = end_time - start_time
        # print('Draw time:', delta_time)
    
    except IndexError as e:
        print(f"Error drawing pixel: {x}, {y}")
        print(f"IndexError: {e}")
    
    finally:
        # unlock the surface object to draw other images.
        # del pixel_array_obj
        pass
    
def get_first_frame():
    d, _ = freenect.sync_get_depth()
    return d

if __name__ == '__main__':
    ctx = freenect.init()

    global depth
    while True:
        try:
            depth = get_first_frame()
            break
        except TypeError as e:
            sleep(.7)
    
    # global device
    # device = freenect.open_device(ctx, 0)
    # print(ctx, device)
    
    initialize_pygame()
    draw_pixels()

    main_loop()
