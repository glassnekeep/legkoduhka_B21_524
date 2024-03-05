# 1 + (6 - 1)%10 == 6 --> Rank filtration.
import numpy as np


def apply_aperture(img, new_image, x, y, size, threshold):
    size //= 2

    left = max(y - size, 0)
    right = min(y + size + 1, img.shape[1])
    low = max(x - size, 0)
    above = min(x + size + 1, img.shape[0])
    
    aperture = img[low : above, left : right]
    
    ones = (aperture == 255).sum()

    if ones >= threshold:
        new_image[x, y] = 255


def rank_filter(img, size, threshold):
    if size % 2 == 0:
        raise Exception("Only even size of aperture is supported")

    new_img = np.zeros(shape=img.shape)

    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            apply_aperture(img, new_img, x, y, size, threshold)
            
    return new_img.astype(np.uint8)


if __name__ == '__main__':
    pass