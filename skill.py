from mycroft import MycroftSkill, intent_file_handler
import random
import math
from PIL import Image
from mycroft.skills.core import resting_screen_handler
import tempfile
import time
from os.path import join

class AlgorithmicArtSkill(MycroftSkill):
    def update_picture(self):
        image, formula = psy_art()
        path = join(tempfile.gettempdir(), "algorithmic_art{n}.png".
                    format(n=time.time()))
        image.save(path, "PNG")
        self.gui['imgLink'] = path
        self.gui['formula'] = formula
        self.gui.show_image(path)

    @resting_screen_handler("AlgorithmicArt")
    def idle(self, message):
        self.update_picture()

    @intent_file_handler('ShowImage.intent')
    def handle_intent(self, message):
        self.update_picture()


def create_skill():
    return AlgorithmicArtSkill()



class X:
    def eval(self, x, y):
        return x

    def __str__(self):
        return "x"


class Y:
    def eval(self, x, y):
        return y

    def __str__(self):
        return "y"


class SinPi:
    def __init__(self, prob):
        self.arg = generate_formula(prob * prob)

    def __str__(self):
        return "sin(pi*" + str(self.arg) + ")"

    def eval(self, x, y):
        return math.sin(math.pi * self.arg.eval(x, y))


class CosPi:
    def __init__(self, prob):
        self.arg = generate_formula(prob * prob)

    def __str__(self):
        return "cos(pi*" + str(self.arg) + ")"

    def eval(self, x, y):
        return math.cos(math.pi * self.arg.eval(x, y))


class Times:
    def __init__(self, prob):
        self.lhs = generate_formula(prob * prob)
        self.rhs = generate_formula(prob * prob)

    def __str__(self):
        return str(self.lhs) + "*" + str(self.rhs)

    def eval(self, x, y):
        return self.lhs.eval(x, y) * self.rhs.eval(x, y)


class Sum:
    def __init__(self, prob):
        self.lhs = generate_formula(prob * prob)
        self.rhs = generate_formula(prob * prob)

    def __str__(self):
        return str(self.lhs) + "+" + str(self.rhs)

    def eval(self, x, y):
        return self.lhs.eval(x, y) + self.rhs.eval(x, y)


class Subtract:
    def __init__(self, prob):
        self.lhs = generate_formula(prob * prob)
        self.rhs = generate_formula(prob * prob)

    def __str__(self):
        return str(self.lhs) + "-" + str(self.rhs)

    def eval(self, x, y):
        return self.lhs.eval(x, y) - self.rhs.eval(x, y)


class Division:
    def __init__(self, prob):
        self.lhs = generate_formula(prob * prob)
        self.rhs = generate_formula(prob * prob)

    def __str__(self):
        return str(self.lhs) + "/" + str(self.rhs)

    def eval(self, x, y):
        val = self.rhs.eval(x, y)
        if val == 0:
            return 1
        return self.lhs.eval(x, y) / val


class Remainder:
    def __init__(self, prob):
        self.lhs = generate_formula(prob * prob)
        self.rhs = generate_formula(prob * prob)

    def __str__(self):
        return str(self.lhs) + "%" + str(self.rhs)

    def eval(self, x, y):
        val = self.rhs.eval(x, y)
        if val == 0:
            return self.lhs.eval(x, y)
        return self.lhs.eval(x, y) % val


class SquareRoot:
    def __init__(self, prob):
        self.arg = generate_formula(prob * prob)

    def __str__(self):
        return "sqrt(" + str(self.arg) + ")"

    def eval(self, x, y):
        return math.sqrt(abs(self.arg.eval(x, y)))


class Ln:
    def __init__(self, prob):
        self.arg = generate_formula(prob * prob)

    def __str__(self):
        return "ln(" + str(self.arg) + ")"

    def eval(self, x, y):
        val = self.arg.eval(x, y)
        # force domain, val > 0
        # no right or wrong here
        val = abs(val)
        if val == 0:
            val = 0.000000000001

        return math.log(val)


class Log:
    def __init__(self, prob, base=None):
        self.arg = generate_formula(prob * prob)
        self.base = base or random.randint(2, 100)

    def __str__(self):
        return "log"+str(self.base)+"(" + str(self.arg) + ")"

    def eval(self, x, y):
        val = self.arg.eval(x, y)
        # force domain, val > 0
        # no right or wrong here
        val = abs(val)
        if val == 0:
            val = 0.000000000001
        return math.log(val, self.base)


def generate_formula(prob=0.99):
    if random.random() < prob:
        return random.choice([SinPi, CosPi,
                              Times, Sum, Subtract, Division, Remainder,
                              SquareRoot,
                              Ln, Log
                              ])(prob)
    else:
        return random.choice([X, Y])()


def plot_intensity(exp, pixelsPerUnit=150):
    canvasWidth = 2 * pixelsPerUnit + 1
    canvas = Image.new("L", (canvasWidth, canvasWidth))

    for py in range(canvasWidth):
        for px in range(canvasWidth):
            # Convert pixel location to [-1,1] coordinates
            x = float(px - pixelsPerUnit) / pixelsPerUnit
            y = -float(py - pixelsPerUnit) / pixelsPerUnit
            z = exp.eval(x, y)
            # Scale [-1,1] result to [0,255].
            intensity = int(z * 127.5 + 127.5)
            canvas.putpixel((px, py), intensity)

    return canvas


def plot_color(redExp, greenExp, blueExp, pixelsPerUnit=150):
    redPlane = plot_intensity(redExp, pixelsPerUnit)
    greenPlane = plot_intensity(greenExp, pixelsPerUnit)
    bluePlane = plot_intensity(blueExp, pixelsPerUnit)
    return Image.merge("RGB", (redPlane, greenPlane, bluePlane))


def psy_art():
    # TODO find error
    while True:
        try:
            redExp = generate_formula()
            greenExp = generate_formula()
            blueExp = generate_formula()

            formula = "red = " + str(redExp) + \
                      "\ngreen = " + str(greenExp) +\
                      "\nblue = " + str(blueExp)

            image = plot_color(redExp, greenExp, blueExp)
            return image, formula
        except:
            continue
