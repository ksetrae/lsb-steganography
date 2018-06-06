import logging
from io import StringIO

from PIL import Image
import numpy as np

bits_amount = 2

base_img = Image.open("assets/lena.jpg").convert("L")
base_data = list(base_img.getdata())
base_data = [format(x, '08b') for x in base_data]


hidden_img = Image.open('assets/arrival_circle.jpg').convert("L")
hidden_data = list(hidden_img.getdata())
hidden_data = [format(x, '08b') for x in hidden_data]


pixels_amount = (8*len(hidden_data)/float(bits_amount))
if pixels_amount > len(base_data):
    logging.error("Cannot encode (not enough pixels). Increase amount of bits to use")

hidden_joint = ''.join(hidden_data)

for x in range(np.ceil(pixels_amount).astype(int)):
    to_insert = hidden_joint[:bits_amount]
    hidden_joint = hidden_joint[bits_amount:]
    base_data[x] = base_data[x][:6] + to_insert

encoded_data = [int(pix, 2) for pix in base_data]
encoded_img = Image.fromarray(np.array(encoded_data).reshape(*base_img.size))
encoded_img.show()
