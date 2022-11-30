from PIL import Image, ImageDraw, ImageFont
import os
import math

IMAGE_SIZE = (3508, 2480) # a4 300 ppi

BORDER_PERCENT = (0.06, 0.09)
DOOR_PERCENT =  (0.85, 0.8)
GAP_PERCENT =  (1-BORDER_PERCENT[0]-DOOR_PERCENT[0], 1-BORDER_PERCENT[1]-DOOR_PERCENT[1])

DOOR_IMAGE_OVERLAP = 3 # pixel
DOOR_LINE_WIDTH = 1
LINE_COLOR = "black"
FONT = "fonts/arial.ttf"
FONT_SIZE = 55

IMAGES_DIR = "images"
OUTPUT_DIR = "output"

DOOR_NUMBERS = [
     1,  2,  3,  4,  5,  6, 
     7,  8,  9, 10, 11, 12,
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
    resized = image.resize((math.ceil(ratio*image.size[0]), math.ceil(ratio*image.size[1]))) # ceil size: if size ends up longer than new_size, it gets croped afterwards
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
    door_image = Image.open(door_image_name)
    door_size = (sizes['door'][0] + 2*DOOR_IMAGE_OVERLAP, sizes['door'][1] + 2*DOOR_IMAGE_OVERLAP)
    door_image = resize_image(door_image, door_size)
    door_pos = get_door_pos(door_pos_num, sizes)
    door_pos = (door_pos[0] - DOOR_IMAGE_OVERLAP, door_pos[1] - DOOR_IMAGE_OVERLAP)
    back_image.paste(door_image, door_pos)

def make_front_image_doors(front_image, door_numbers, sizes):
    front_draw = ImageDraw.Draw(front_image)
    font = ImageFont.truetype(FONT, FONT_SIZE)
    for pos in range(24):
        door_pos = get_door_pos(pos, sizes)
        door_rect = [door_pos, (door_pos[0]+sizes['door'][0], door_pos[1]+sizes['door'][1])]
        front_draw.rectangle(door_rect, outline=LINE_COLOR, width=DOOR_LINE_WIDTH)
        num_pos = (door_pos[0] + int(sizes['door'][0]/2), door_pos[1] + int(sizes['door'][1]/2))
        front_draw.text(num_pos, str(door_numbers[pos]), fill=LINE_COLOR, font=font, anchor="mm")

def make_front_image(front_image_name):
    front_image = Image.new(mode="RGB", size=IMAGE_SIZE, color="white")
    image = Image.open(front_image_name)
    image = resize_image(image, IMAGE_SIZE)
    front_image.paste(image)
    return front_image

def load_image_names():
    files = os.listdir(IMAGES_DIR)
    door_images = [None]*24
    front_image = None
    for file in files:
        file_no_ext = os.path.splitext(file)[0]
        if file_no_ext.isnumeric():
            if int(file_no_ext) in range(1,25):
                door_images[int(file_no_ext)-1] = os.path.join(IMAGES_DIR, file)

        if file_no_ext == "front-image":
            front_image = os.path.join(IMAGES_DIR, file)

    for i in range(24):
        if door_images[i] == None:
            print("Door image " + str(i+1) + " is missing in directory '" + str(IMAGES_DIR) + "'")
            exit(-1)

    if front_image == None:
        print("No front image in directory '" + str(IMAGES_DIR) + "'")
        exit(-1)

    return front_image, door_images

sizes = calculate_sizes()
front_image_name, door_image_names = load_image_names()

front_image = make_front_image(front_image_name)
make_front_image_doors(front_image, DOOR_NUMBERS, sizes)

back_image = Image.new(mode="RGB", size=IMAGE_SIZE, color="white")
for pos in range(24):
    add_door_image(back_image, door_image_names[DOOR_NUMBERS[pos]-1], pos, sizes)

#front_image.show()
#back_image.show()

if not os.path.exists(OUTPUT_DIR):
    print("Output directory '" + OUTPUT_DIR + "' doesn't exist. No pdfs were created")
    exit()

front_image.save(os.path.join(OUTPUT_DIR, "front-image.pdf"), "PDF")
back_image.save(os.path.join(OUTPUT_DIR, "back-image.pdf"), "PDF")

#front_image.save(os.path.join(OUTPUT_DIR, "front-image.png"), "PNG", dpi=(300,300))
#back_image.save(os.path.join(OUTPUT_DIR, "back-image.png"), "PNG", dpi=(300,300))