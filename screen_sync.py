import os
import sys
import numpy as np
import click
import time

import cv2
import pyautogui

import colorsys

import yeelight  # noqa
from yeelight import transitions as tr

from yeelight import Bulb


def compute_average_image_color(img):
    average_color_per_row = np.average(img, axis=0)
    average_color = np.average(average_color_per_row, axis=0)

    r, g, b = average_color

    r = int(r)
    g = int(g)
    b = int(b)

    return (r, g, b)


def compute_dominant_color(img):
    pixels = np.float32(img.reshape(-1, 3))

    n_colors = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(
        pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    dominant = palette[np.argmax(counts)]

    return dominant


def compute_average_image_color_old(img):
    width, height = img.size

    r_total = 0
    g_total = 0
    b_total = 0

    count = 0
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = img.getpixel((x, y))
            r_total += r
            g_total += g
            b_total += b
            count += 1

    red = int(r_total/count)
    green = int(g_total/count)
    blue = int(b_total/count)
    return (red, green, blue)


def get_screen_colors():
    # take screenshot using pyautogui
    image = pyautogui.screenshot()
    image_np = np.array(image)

    # div = 16
    # quantized = image_np // div * div + div // 2

    average_color = compute_average_image_color(image_np)
    print('average_color', average_color)

    dominant_color = compute_dominant_color(image_np)
    print('dominant_color', dominant_color)

    # print(average_color)
    # since the pyautogui takes as a
    # PIL(pillow) and in RGB we need to
    # convert it to numpy array and BGR
    # so we can write it to the disk
    # image = cv2.cvtColor(np.array(image),
    #                     cv2.COLOR_RGB2BGR)

    return average_color


def get_random_color():
    color = list(np.random.choice(range(256), size=3))
    red = int(color[0])
    green = int(color[1])
    blue = int(color[2])

    return (red, green, blue)


def vividify_color(red, green, blue):
    h, s, v = colorsys.rgb_to_hsv(red/255, green/255, blue/255)

    if v < 0.25:
        v * 2
    elif v < 0.45:
        v = v * 1.5
    elif v < 0.65:
        v = v * 1.2

    if v > 1:
        v = 1

    red, green, blue = colorsys.hsv_to_rgb(h, s, v)

    red = int(red * 255)
    green = int(green * 255)
    blue = int(blue * 255)

    return (red, green, blue)


def vividify_color_old(red, green, blue):
    while (red < 30) or (green < 30) or (blue < 30):
        red += 1
        green += 1
        blue += 1

    if green >= 255:
        green = 255

    if blue >= 255:
        blue = 255

    if red > green and red > blue:
        red = int(red * 1.5)
    elif green > red and green > blue:
        green = int(green * 1.5)
    elif blue > red and blue > green:
        blue = int(blue * 1.5)
    # else:
    #     red = int(red *1.3)
    #     green = int(green *1.3)
    #     blue = int(blue *1.3)

    if red >= 255:
        red = 255

    if green >= 255:
        green = 255

    if blue >= 255:
        blue = 255

    return red, green, blue


bulb = Bulb("192.168.1.51", effect="smooth", duration=300)
bulb.turn_on()
bulb.set_brightness(100)


bulb.start_music()
while bulb.music_mode:
    red, green, blue = get_screen_colors()
    # red, green, blue = get_random_color()

    red, green, blue = vividify_color(red, green, blue)
    print(red, green, blue)

    # bulb.set_rgb(red, green, blue)
    print("===")
    time.sleep(1)


    # bulb.stop_music()
