import logging
import time

from PIL import Image
import numpy as np


def get_pixel_amount(hidden_data_len: int, bits_amount: int):
    return np.ceil((8*hidden_data_len)/float(bits_amount)).astype(int)


def insert(bits_amount: int, base_img, img_to_hide):
    if not 1 < bits_amount < 8:
        raise ValueError("bits_amount must be between 0 and 8")

    base_data = [format(x, '08b') for x in list(base_img.getdata())]
    hidden_data = [format(x, '08b') for x in list(img_to_hide.getdata())]
    print(''.join(hidden_data[:100]))

    pixels_amount = get_pixel_amount(len(hidden_data), bits_amount)
    if pixels_amount > len(base_data):
        logging.error("Cannot encode (not enough pixels). Increase amount of bits to use")
        return None

    hidden_joint = ''.join(hidden_data)

    for x in range(pixels_amount):
        base_data[x] = base_data[x][:8-bits_amount] + hidden_joint[x*bits_amount:x*bits_amount+bits_amount]
    
    encoded_data = [int(pix, 2) for pix in base_data]
    encoded_img = Image.fromarray(np.array(encoded_data).reshape(*base_img.size))
    return encoded_img


def extract(bits_amount: int, size: tuple, img):
    # TODO: extract from custom position
    length = size[0]*size[1]
    data_cut = [format(x, '08b') for x in list(img.getdata())]
    data_cut = [x[len(x)-bits_amount:] for x in data_cut]
    print(''.join(data_cut[:100]))

    data_joint = ''.join(data_cut)
    extr_data = [data_joint[i:i + 8] for i in range(0, len(data_joint), 8)]
    extr_data = [int(pix, 2) for pix in extr_data]
    extr_img = Image.fromarray(np.array(extr_data[:length]).reshape(size[1], size[0]))
    return extr_img


if __name__ == "__main__":
    bits_amount = 3
    base_img = Image.open("assets/lena.jpg").convert("L")
    hidden_img = Image.open('assets/arrival_circle.jpg').convert("L")
    hidden_img = Image.open('assets/nature.jpg').convert("L")

    inserted = insert(bits_amount, base_img, hidden_img)
    extracted = extract(bits_amount, hidden_img.size, inserted)
    extracted.show()


