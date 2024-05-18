from PIL import Image
import numpy as np
from os import path

def image_to_np_array(image_name: str) -> np.array:
    img_src = Image.open(path.join('input', image_name)).convert('RGB')
    return np.array(img_src)


def two_step_resampling(img: np.array, numerator: int,
                        denominator: int) -> np.array:
    tmp = one_step_resampling(img, numerator, lambda a, b: a * b,
                              lambda a, b: int(round(a / b)))
    return one_step_resampling(tmp, denominator,
                               lambda a, b: int(round(a / b)),
                               lambda a, b: a * b)


def one_step_resampling(img: np.array, factor: float, f1, f2):
    dimensions = img.shape[0:2]
    new_dimensions = tuple(f1(dimension, factor) for dimension in
                           dimensions)
    new_shape = (*new_dimensions, img.shape[2])
    new_img = np.empty(new_shape)

    for x in range(new_dimensions[0]):
        for y in range(new_dimensions[1]):
            new_img[x, y] = img[
                min(f2(x, factor), dimensions[0] - 1),
                min(f2(y, factor), dimensions[1] - 1)
            ]
    return new_img


def safe_number_input(number_type: type, lower_bound=None, upper_bound=None):
    input_correct = False
    user_input = 0

    while not input_correct:
        try:
            user_input = number_type(input('> '))
            if lower_bound is not None and user_input < lower_bound:
                raise ValueError
            if upper_bound is not None and user_input > upper_bound:
                raise ValueError
            input_correct = True
        except ValueError:
            print("Введите корректное значение")
    return user_input


def toPolutoneSRGB(imgname):
    input_image = Image.open(imgname).convert('RGB')
    origPicArr = np.array(input_image)
    newPicArr = np.zeros((origPicArr.shape[0], origPicArr.shape[1]), dtype=origPicArr.dtype)

    for y in range(origPicArr.shape[0]):
        for x in range(origPicArr.shape[1]):
            newPicArr[y][x] = np.mean(origPicArr[y][x])

    return Image.fromarray(newPicArr, mode='L')