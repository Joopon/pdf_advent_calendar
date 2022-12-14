IMAGE_SIZE = (3508, 2480) # a4 300 ppi

BORDER_PERCENT = (0.06, 0.09)
DOOR_PERCENT =  (0.85, 0.8)
GAP_PERCENT =  (1-BORDER_PERCENT[0]-DOOR_PERCENT[0], 1-BORDER_PERCENT[1]-DOOR_PERCENT[1])

DOOR_IMAGE_OVERLAP = 3 # pixel
DOOR_LINE_WIDTH = 1
LINE_COLOR = "black"
FONT = "arial.ttf"
FONT_SIZE = 55

NUM_DOORS = (6, 4) # number of doors in x and y direction
DOOR_NUMBERS = [
     1,  2,  3,  4,  5,  6,
     7,  8,  9, 10, 11, 12,
    13, 14, 15, 16, 17, 18,
    19, 20, 21, 22, 23, 24 ]