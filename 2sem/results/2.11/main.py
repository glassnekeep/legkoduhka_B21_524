import os

from core.input.utils import *
from PIL import ImageFilter


def semitone(img):
    return (0.3 * img[:, :, 0] + 0.59 * img[:, :, 1] + 0.11 * img[:, :, 2]).astype(np.uint8)


def to_semitone(img_name):
    img = image_to_np_array(img_name)
    return Image.fromarray(semitone(img), 'L')


def tan(image, window_size=15, k1=0.2, k2 = 0.01, a1=0.1, R=128, gamma = 2):
    image = to_semitone(image)
    img_array = np.array(image)

    mean = Image.fromarray(img_array).filter(ImageFilter.BoxBlur(window_size)).convert('L')
    mean_array = np.array(mean)
    mean_sq = Image.fromarray(img_array).filter(ImageFilter.BoxBlur(window_size)).convert('L').point(lambda x: x ** 2)
    mean_sq_array = np.array(mean_sq)
    variance = mean_sq_array - mean_array ** 2
    M = np.min(img_array)
    a2 = k1 * ((variance / R) ** gamma)
    a3 = k2 * ((variance / R) ** gamma)
    threshold = (1 - a1) * mean_array + a2 * variance / R * (mean_array - M) + a3 * M
    binary_array = np.where(img_array > threshold, 255, 0).astype(np.uint8)
    binary_image = Image.fromarray(binary_array)

    return binary_image


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input = os.path.join(current_dir, 'input')
    output_path = os.path.join(current_dir, 'output')
    relative_path = "2sem/results/input/*"
    glob = os.listdir(input)
    for input_path in glob:
        curr_opath = os.path.join(output_path, os.path.basename(input_path))
        result = tan(input_path)
        result.save(path.join('output', input_path))
