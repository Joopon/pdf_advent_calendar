import PIL
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageColor
import random

IMAGE_SIZE = (3508, 2480) # a4 300 ppi

BORDER_PERCENT = (0.06, 0.09)
DOOR_PERCENT =  (0.85, 0.82)
GAP_PERCENT =  (1-BORDER_PERCENT[0]-DOOR_PERCENT[0], 1-BORDER_PERCENT[1]-DOOR_PERCENT[1])

DOOR_IMAGE_OVERLAP = 3 # pixel
DOOR_LINE_WIDTH = 2
FONT_SIZE = 50

FRONT_IMAGE_NAME = "front-image.png"

DOOR_NUMBERS = [
    2, 1, 3, 4, 5, 6, 
    7, 8, 9, 10, 11, 12,
    13, 14, 15, 16, 17, 18, 
    19, 20, 21, 22, 23, 24 ]

def calculate_sizes():
    border_size = (int((IMAGE_SIZE[0]*BORDER_PERCENT[0])/2), int((IMAGE_SIZE[1]*BORDER_PERCENT[1])/2))
    door_size = (int((IMAGE_SIZE[0]*DOOR_PERCENT[0])/6), int((IMAGE_SIZE[1]*DOOR_PERCENT[1])/4))
    gap_size = (int((IMAGE_SIZE[0]*GAP_PERCENT[0])/5), int((IMAGE_SIZE[1]*GAP_PERCENT[1])/3))
    return {'border': border_size, 'door': door_size, 'gap': gap_size}

# fixed aspect ratio scale, then crop to new size
def resize_image(image, new_size):
    ratio_x = new_size[0] / image.size[0]
    ratio_y = new_size[1] / image.size[1]
    ratio = max(ratio_x, ratio_y)
    resized = image.resize((int(ratio*image.size[0]), int(ratio*image.size[1])))
    assert(resized.size[0] >= new_size[0] and resized.size[1] >= new_size[1])
    
    diff = (resized.size[0] - new_size[0], resized.size[1] - new_size[1])
    resized = resized.crop((diff[0]/2, diff[1]/2, diff[0]/2 + new_size[0], diff[1]/2 + new_size[1]))
    assert(resized.size[0] == new_size[0] and resized.size[1] == new_size[1])
    return resized

def get_door_pos(pos_num, sizes):
    assert(pos_num < 24)
    x = int(pos_num%6)
    y = int(pos_num/6)
    x_pos = sizes['border'][0] + x*(sizes['door'][0]+sizes['gap'][0])
    y_pos = sizes['border'][1] + y*(sizes['door'][1]+sizes['gap'][1])
    return (x_pos, y_pos)

def add_door_image(back_image, door_image_name, door_pos_num, sizes):
    door_image = PIL.Image.open(door_image_name)
    door_size = (sizes['door'][0] + 2*DOOR_IMAGE_OVERLAP, sizes['door'][1] + 2*DOOR_IMAGE_OVERLAP)
    door_image = resize_image(door_image, door_size)
    door_pos = get_door_pos(door_pos_num, sizes)
    door_pos = (door_pos[0] - DOOR_IMAGE_OVERLAP, door_pos[1] - DOOR_IMAGE_OVERLAP)
    back_image.paste(door_image, door_pos)

def make_front_image_doors(front_image, door_numbers, sizes):
    front_draw = ImageDraw.Draw(front_image)
    font = ImageFont.truetype("fonts/arial.ttf", FONT_SIZE)
    idx = 0
    for i in door_numbers:
        door_pos = get_door_pos(idx, sizes)
        door_rect = [door_pos, (door_pos[0]+sizes['door'][0], door_pos[1]+sizes['door'][1])]
        front_draw.rectangle(door_rect, outline="black", width=DOOR_LINE_WIDTH)
        num_pos = (door_pos[0] + int(sizes['door'][0]/2), door_pos[1] + int(sizes['door'][1]/2))
        front_draw.text(num_pos, str(i), fill="black", font=font, anchor="mm")
        idx+=1

sizes = calculate_sizes()

#image = PIL.Image.new(mode="RGB", size=IMAGE_SIZE, color="#ff00ff")
front_image = PIL.Image.open(FRONT_IMAGE_NAME)
back_image = PIL.Image.new(mode="RGB", size=IMAGE_SIZE, color=ImageColor.getrgb("white"))

front_image = resize_image(front_image, IMAGE_SIZE)
make_front_image_doors(front_image, DOOR_NUMBERS, sizes)
front_image.show()

for i in range(24):
    add_door_image(back_image, "test-door.jpg", i, sizes)

back_image.show()


#back_image.save("/tmp/output.pdf", "PDF")
#back_image.close()

    