from PIL import Image as pim
from glob import glob
from core.input.utils import *
import os
import math


def grac(img):
    inpt = np.array(img, dtype=np.int64)
    h, w = inpt.shape
    gximg = np.zeros((h, w), dtype=np.uint64)
    gyimg = np.zeros((h, w), dtype=np.uint64)
    gimg = np.zeros((h, w), dtype=np.uint64)

    maxgx, maxgy, maxg = 0, 0, 0

    for y in range(1, h - 1):
        for x in range(1, w - 1):
            gximg[y, x] = np.abs(np.sum(inpt[y - 1, x - 1:x + 2]) - np.sum(inpt[y + 1, x - 1:x + 2]))
            gyimg[y, x] = np.abs(np.sum(inpt[y - 1:y + 2, x + 1]) - np.sum(inpt[y - 1:y + 2, x - 1]))
            gimg[y, x] = gximg[y, x] + gyimg[y, x]

            maxgx = max(maxgx, gximg[y, x])
            maxgy = max(maxgy, gyimg[y, x])
            maxg = max(maxg, gimg[y, x])

    for y in range(1, h - 1):
        for x in range(1, w - 1):
            gximg[y, x] = math.floor((gximg[y, x] / maxgx) * 255)
            gyimg[y, x] = math.floor((gyimg[y, x] / maxgy) * 255)
            gimg[y, x] = math.floor((gimg[y, x] / maxg) * 255)

    gximg = gximg.astype(np.uint8)
    gyimg = gyimg.astype(np.uint8)
    gimg = gimg.astype(np.uint8)

    T = 25
    res = np.zeros((h, w), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            if gimg[y, x] >= T:
                res[y, x] = 255
            else:
                res[y, x] = 0

    return pim.fromarray(gximg, mode='L'), pim.fromarray(gyimg, mode='L'), pim.fromarray(gimg, mode='L'), pim.fromarray(res, mode='L')


def main():
    input = os.path.join(os.path.dirname(__file__), 'input/*')
    output = os.path.join(os.path.dirname(__file__), 'output/')

    for file in glob(input):
        name = os.path.splitext(os.path.basename(file))[0]
        polyTon = toPolutoneSRGB(file)
        polyTon.save(output + 'Polutone' + name + '.bmp')
        gx, gy, g, binar = grac(polyTon)
        gx.save(output + 'GX' + name + '.bmp')
        gy.save(output + 'GY' + name + '.bmp')
        g.save(output + 'G' + name + '.bmp')
        binar.save(output + 'BIN' + name + '.bmp')


if __name__ == "__main__":
    main()