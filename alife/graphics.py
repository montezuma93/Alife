import pygame
from random import choice as choice
from numpy import *

# PyGame colours
COLOR_TRANSPARENT = (1,2,3)
COLOR_WHITE  = (255, 255, 255)
COLOR_RED  = (255, 0, 0)
COLOR_BLACK  = (0, 0, 0)

# RGB intensities given a sprite ID
id2rgb = array([
    [0.,0.,0.], # VOID     = 0  = BLACK
    [1.,1.,1.], # ROCK     = 1  = WHITE
    [0.,0.,0.], # MISC     = 2  = BLACK
    [0.,1.,0.], # PLANT    = 3  = GREEN
    [0.,0.,1.], # ANIMAL   = 4  = BLUE
    [1.,0.,0.], # ENEMY    = 5  = RED
    ])

def rgb2color(a, default=COLOR_BLACK):
    ''' 
        Convert RGB intensity to a colour
        (and return the default colour if there is no intensity)
    '''
    if sum(a) <= .0:
        return default
    return a * 255

def build_image_wireframe(pos,rad,ID):
    '''
        Build a wireframe image at pos, with radius rad, and ID.
    '''
    color = id2rgb[ID]*255
    image = pygame.Surface((rad*2, rad*2))
    image.fill(COLOR_TRANSPARENT)
    image.set_colorkey(COLOR_TRANSPARENT)
    pygame.draw.circle(image, color, (rad,rad), rad )
    rect=image.get_rect(center=pos)
    return rect, image

def rotate(image, angle):
    ''' Rotate an image (keeping center and size) '''
    rec = image.get_rect()
    img_rotated = pygame.transform.rotate(image, angle)
    rec_rotated = rec.copy()
    rec_rotated.center = img_rotated.get_rect().center
    return img_rotated.subsurface(rec_rotated).copy()

def build_image_bank(image):
    ''' Build images for every single angle 0...359 (applicable to moving sprites) '''
    return [rotate(image, deg-180) for deg in range(360)]

trees = [
    # Location of tree tiles
   (280,183,62,66), (125,3,40,38), (451,115,66,64), (383,115,64,64), (217,55,54,52), (3,55,46,48),
   (443,55,52,56), (163,55,50,50), (39,3,38,38), (3,183,64,64), (365,3,47,48), (416,3,46,48), (3,3,32,32),
   (215,3,46,44), (71,183,64,64), (169,3,42,42), (385,55,54,54), (139,183,68,64), (67,115,56,58), (275,55,48,52), (3,115,60,56),
   (327,55,54,54), (346,183,62,66), (81,3,40,38), (255,115,58,6), (466,3,48,48), (127,115,56,60), (3,257,66,70), (111,55,48,50),
   (317,115,62,62), (407,341,110,114), (301,341,102,114), (211,183,65,65), (151,257,74,72), (73,257,74,70), (385,257,78,78),
   (195,341,102,108), (467,257,70,80), (53,55,54,50), (265,3,46,46), (315,3,46,46), (412,183,68,70), (229,257,74,74),
   (187,115,64,62), (3,341,94,82), (101,341,90,90), (307,257,74,78),
    ]

land = {
        # Denotes the location of each tile given its character code
        ' ' : [(0,0)],                                   # land
        'v' : [(4,7),(5,7),(4,5),(5,5),(6,4)],           # top ridge
        '^' : [(2,0),(4,0)],                             # bottom ridge
        '[' : [(3,3),(3,5),(6,2),(4,2)],                 # left ridge
        ']' : [(5,1),(1,1),(2,1),(1,5),(1,7)],           # right ridge
       '\\' : [(7,5)],                                   # bottom left ridge
        '/' : [(7,3)],                                   # bottom right ridge
        '+' : [(5,3)],                                   # top left ridge
        'L' : [(2,5)],                                   # top right ridge
        '&' : [(3,7)],                                   # bottom left concave (after rotation 90 deg)
        'D' : [(3,7)],                                   # top left concave 
        'C' : [(2,3)],                                   # top right concave
        '-' : [(2,7)],                                   # bottom right concave
        '~' : [(7,7)],                                   # water
    }

terr = {
        # Denotes the collision quaters of each tile given its character code (since one picture tile covers 4 game tiles)
        ' ' : array([[0,0],
                     [0,0]]),
        'v' : array([[0,0],
                     [1,1]]), 
        '[' : array([[1,0],
                     [1,0]]),                       
        ']' : array([[0,1],
                     [0,1]]),                       
       '\\' : array([[1,0],
                     [1,1]]),                       
        '/' : array([[0,1],
                     [1,1]]),                       
        '+' : array([[1,1],
                     [1,0]]),                       
        '^' : array([[1,1],
                     [0,0]]),                       
        'L' : array([[1,1],
                     [0,1]]),                       
        'C' : array([[0,0],     # <-- top right is soft
                     [0,0]]),                       
        'D' : array([[0,0],     # <-- top left is soft
                     [0,0]]),                       
        '&' : array([[0,0],     # <-- bottom left is soft
                     [0,0]]),                       
        '-' : array([[0,0],     # <-- bottom right is soft
                     [0,0]]),    
        '~' : array([[1,1],
                     [1,1]]),                       
    }

def get_tree(n):
    ''' Load a plant '''
    sheet = pygame.image.load('./img/trees_packed.png').convert_alpha()
    image = sheet.subsurface(trees[n])
    return image

def get_rock(n):
    ''' Load a rock '''
    return pygame.image.load('./img/rock_'+str(n)+'.png').convert_alpha()

def build_image_png(pos,rad,ID):
    '''
        Load the appropriate image given an object ID (see object codes in objects.py), as follows:
    '''
    if ID == 1:
        image = get_rock(random.choice(10))
    elif ID == 2:
        print("No such object type")
    elif ID == 3:
        image = get_tree(random.choice(len(trees)))
    elif ID >= 4 and ID <= 11:
        image = pygame.image.load('./img/green_bug_m%d.png' % (ID-3)).convert_alpha()
    else:
        return build_image_wireframe(pos,rad,4)

    # Scale the image to fit the size of the sprite
    image = pygame.transform.scale(image, (rad*2, rad*2))

    rect=image.get_rect(center=pos)
    return rect, image

def build_map_png(size,N_COLS,N_ROWS,GRID_SIZE,tile_codes):
    '''
        Build the map.

        Build the map of N_COLS * N_ROWS squares of size GRID_SIZE.
        Images are based on the tile_codes array. 

        Return 
            - the image, and 
            - the terrain map (where 1 = gridsquare unpassable).

        Note: A tile image covers 4 game tiles, therefore we only need to draw 
        for every other row and column. However, this does mean that maps need 
        to be an even number of columns and rows!
    '''
    # Init.
    background = pygame.Surface(size)
    terrain = zeros((N_ROWS,N_COLS),dtype=int)
    # Load.
    sheet = pygame.image.load('./img/ground.png').convert_alpha()
    # Draw
    for j in range(0,N_COLS,2):
        for k in range(0,N_ROWS,2):
            bgimg = pygame.image.load('./img/water.png').convert()
            background.blit(bgimg, (j*GRID_SIZE, k*GRID_SIZE))
            c = tile_codes[k,j]
            if c != '.':
                (x,y) = choice(land[c])
                image = sheet.subsurface((x*128,y*128,128,128))
                if c == '&':
                    image = rotate(image,90)
                #img = pygame.transform.scale(img, (GRID_SIZE, GRID_SIZE))
                background.blit(image, (j*GRID_SIZE, k*GRID_SIZE))
                terrain[k:k+2,j:j+2] = terr[c]
    background = background.convert()           # can speed up when we have an 'intense' background
    return background, terrain

def rebuild_map(background, tile_codes):
    '''
        Rebuild the dirty parts of the map, as indicated in tile_codes. 
        (This should be faster than repainting the whole thing). 
    '''
    #TODO
    return

def get_banner(s):
    image = pygame.Surface((300, 20))
    image.fill(COLOR_TRANSPARENT)
    image.set_colorkey(COLOR_TRANSPARENT)

    myfont = pygame.font.SysFont("monospace", 17)
    label = myfont.render(s, 1, COLOR_WHITE)
    image.blit(label, [0,0])
    return image

def draw_banner(surface, s):
    lines = s.split("\n")
    #print(lines)
    myfont = pygame.font.SysFont("monospace", 17)
    l,h = myfont.size('--------------------')
    pygame.draw.rect(surface, COLOR_BLACK, (1,1,1+l,1+h*len(lines)))
    j = 0
    color = COLOR_RED
    for line in lines:
        #print(j,line)
        label = myfont.render(line, 1, color)
        surface.blit(label, [1,h*j])
        j = j + 1
        color = COLOR_WHITE

#from agents.evolution import SimpleEvolver 
#a = SimpleEvolver(random.randn(2,1), random.randn(2,1), 3)
#print(draw_banner(None,"%s \n (%s: G%d)" % ("5","5", 2)))
#print(draw_banner(None,str(a)))
