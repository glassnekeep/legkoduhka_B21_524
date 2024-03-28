import numpy as np
from PIL import Image as pim
from glob import glob
import os
from statistics import mean


def small_square(x, y, arr):
    mat = np.sum(arr[y - 1:y + 1, x:x + 2]) // 4
    disp = (arr[y][x] - mat) ** 2 + (arr[y][x + 1] - mat) ** 2 + (arr[y - 1][x] - mat) ** 2 + (
                arr[y - 1][x + 1] - mat) ** 2
    return mat, disp


def big_square(x, y, arr):
    mat, disp = small_square(x - 1, y + 1, arr)

    tmat, tdisp = small_square(x, y + 1, arr)
    if tdisp < disp:
        disp = tdisp
        mat = tmat

    tmat, tdisp = small_square(x - 1, y, arr)
    if tdisp < disp:
        disp = tdisp
        mat = tmat

    tmat, tdisp = small_square(x, y, arr)
    if tdisp < disp:
        disp = tdisp
        mat = tmat

    return mat


def filter(img):
    inptArr = np.array(img)
    h, w = inptArr.shape
    newArr = np.zeros((h, w), dtype=np.uint8)
    for y in range(1, h - 2):
        for x in range(1, w - 2):
            newArr[y][x] = big_square(x, y, inptArr)

    return pim.fromarray(newArr, mode='L')


def difference(polyTon, res):
    result = pim.new(polyTon.mode, (polyTon.width, polyTon.height))

    for x in range(result.width):
        for y in range(result.height):
            result.putpixel((x, y), abs(polyTon.getpixel((x, y)) - res.getpixel((x, y))))

    return result


def toSRGB(imgname):
    input_image = pim.open(imgname).convert('RGB')
    origPicArr = np.array(input_image)
    newPicArr = np.zeros((origPicArr.shape[0], origPicArr.shape[1]), dtype=origPicArr.dtype)

    for y in range(origPicArr.shape[0]):
        for x in range(origPicArr.shape[1]):
            newPicArr[y][x] = np.mean(origPicArr[y][x])

    return pim.fromarray(newPicArr, mode='L')


def main():
    inptdir = os.path.join(os.path.dirname(__file__), 'input/*')
    for filename in glob(inptdir):
        polyTon = pim.open(filename).convert('L')
        res = filter(polyTon)
        res.save(
            os.path.join(os.path.dirname(__file__), 'output', os.path.splitext(os.path.basename(filename))[0] + '.bmp'))
        diff = difference(polyTon, res)
        diff.save(
            os.path.join(os.path.dirname(__file__), 'diff', os.path.splitext(os.path.basename(filename))[0] + '.bmp'))


if __name__ == "__main__":
    main()