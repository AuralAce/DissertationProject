from colorama import Fore, Back, Style
import random

bar_array = ['█', '█', '█', '█', '█', '█', '█']

sort = ["Cartridge Colour","Room Name, Alphabetically","Size of Memory(GB)"]

def choose_sort():
    rand = random.choice(sort)
    return rand

sorter = choose_sort()

print(sorter)

for i in range(7):
    print(bar_array[i], end=" ")
