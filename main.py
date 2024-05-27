from turtle import Turtle, Screen
from math import acos, sin, tau, sqrt, cos
from colorsys import hsv_to_rgb
from PIL import Image

import os

# utility functions
# - colorspace transformations
def hex_to_rgb(colors: list[str]) -> list[tuple[float, float, float]]:
    return [(int(s[0:2], 16) / 255, int(s[2:4], 16) / 255, int(s[4:6], 16) / 255) for s in colors]

def rgb_to_hex(rgb: list[tuple[float, float, float]]) -> list[str]:
    return [f"{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}" for (r, g, b) in rgb]

# - palette manipulations
def rainbow(n: int) -> list[str]:
    rgb = [hsv_to_rgb(i / n, 1.0, 1.0) for i in range(n)]
    return rgb_to_hex(rgb)

def smooth(times: int, colors: list[str]) -> list[str]:
    rgb = hex_to_rgb(colors)

    for _ in range(times):
        new_rgb = []

        for i in range(len(rgb)):
            next_i = (i + 1) % len(rgb)

            r = (rgb[i][0] + rgb[next_i][0]) / 2
            g = (rgb[i][1] + rgb[next_i][1]) / 2
            b = (rgb[i][2] + rgb[next_i][2]) / 2

            new_rgb.append(rgb[i])
            new_rgb.append((r, g, b))

        rgb = new_rgb

    return rgb_to_hex(rgb)

# ms between
CALLBACK_FREQUENCY = 10
FRACTION_ADJUSTMENT = 0.95

palette = []

with open("palette.txt", "r") as f:
    for line in f:
        stripped = line.replace("\n", "")

        if len(stripped) == 6:
            palette.append(stripped)

sides = 6
fraction_i = 79
smoothness_i = 5

# initial value irrelevant - set later based on fraction_i
fraction = 0
colors = palette

held = {}
callbacks = []

t = Turtle()
t.speed(0)
t.penup()
t.hideturtle()

def render(w: int, h: int):
    global fraction

    radius = min(w, h) / 2
    length = 2 * radius * sin(tau / 2 / sides)

    center_x = cos(tau / sides / 2) * radius
    center_y = sin(tau / sides / 2) * radius

    t.clear()
    t.goto(-center_x, -center_y)

    t.setheading(90)

    i = 0
    while length > 2:
        t.fillcolor(colors[i % len(colors)])
        t.begin_fill()

        for _ in range(sides):
            t.forward(length)
            t.right(360 / sides)

        t.end_fill()
        t.forward(fraction * length)

        a = (1 - fraction) * length
        b = fraction * length
        gamma = (tau / 2) - tau / sides

        length = sqrt(a * a + b * b - 2 * a * b * cos(gamma))

        c = b
        b = a
        a = length

        angle = acos((a * a + b * b - c * c) / (2 * a * b))

        t.right(angle / tau * 360)
        i += 1

# general functions
def rerender():
    s.tracer(False)
    t.clear()

    render(s.window_width(), s.window_height())

    s.tracer(True)

def adjust_callback(key, change, smooth=False):
    if not smooth:
        def press():
            change()
            rerender()

        s.onkeypress(press, key)
        return

    def down():
        held[key] = True

    def up():
        held[key] = False

    def f():
        if held.get(key, False):
            change()
            rerender()

    s.onkeypress(down, key)
    s.onkeyrelease(up, key)

    callbacks.append(f)

def run_callbacks():
    for c in callbacks:
        c()

    root.after(CALLBACK_FREQUENCY, run_callbacks)

# key functions
def change_fraction(by: int):
    global fraction, fraction_i

    fraction_i += by

    if fraction_i < 0:
        fraction = 0.5 * (pow(FRACTION_ADJUSTMENT, -fraction_i) - 1) + 0.5
    else:
        fraction = 0.5 * (1 - pow(FRACTION_ADJUSTMENT, fraction_i)) + 0.5

def change_smoothness(by: int):
    global colors, smoothness_i

    if len(colors) == len(palette) and by < 0:
        return

    smoothness_i += by

    colors = [f"#{c}" for c in smooth(smoothness_i, palette)]

def save_canvas():
    global sides, fraction, fraction_i, smoothness_i

    s.getcanvas().postscript(file="temp.eps")

    filename = input("filename: ")

    image = Image.open("temp.eps")
    image.save(filename)

    os.remove("temp.eps")

    print(f"saved to {filename}!")

    print(f"""variables at time of screenshot:
sides: {sides}
fraction: {fraction}
fraction index: {fraction_i}
smoothness index: {smoothness_i}""")

# calculate initial value
change_fraction(0)
change_smoothness(0)

s = Screen()
s.setup(800, 800)

adjust_callback("q", lambda: globals().update(sides=sides - 1))
adjust_callback("w", lambda: globals().update(sides=sides + 1))

adjust_callback("a", lambda: change_fraction(-1), smooth=True)
adjust_callback("s", lambda: change_fraction(1), smooth=True)

adjust_callback("z", lambda: change_smoothness(-1))
adjust_callback("x", lambda: change_smoothness(1))

s.onkeypress(save_canvas, "e")

s.listen()

s.tracer(False)

render(s.window_width(), s.window_height())

s.tracer(True)

root = s.getcanvas().winfo_toplevel()
root.after(CALLBACK_FREQUENCY, run_callbacks)

s.mainloop()
