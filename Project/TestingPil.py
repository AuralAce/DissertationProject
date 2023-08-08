from PIL import Image
import random

main_img = Image.open("Images/Sort The Memory Cards.png")

sort_img = ""

bar_img = ""

sort = ["By Colour","Alphabetically","By Size"]

def choose_sort():

    global sort_img

    rand = random.choice(sort)
    sort_img = Image.open(f"Images/{rand}.png")
    return rand

sorter= choose_sort()

main_img = Image.alpha_composite(main_img, sort_img)

main_img.show()

read = input()

if read == "1":

    bar_img = Image.open(f"Images/Green 1.png")

    main_img = Image.alpha_composite(main_img, bar_img)

    main_img.show()

