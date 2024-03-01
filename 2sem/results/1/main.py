from core.input.utils import *


def semitone(img):
    return (0.3 * img[:, :, 0] + 0.59 * img[:, :, 1] + 0.11 * img[:, :, 2]).astype(np.uint8)


def to_semitone(img_name):
    img = image_to_np_array(img_name)
    return Image.fromarray(semitone(img), 'L')


if __name__ == '__main__':
    result = to_semitone('picture.png')
    result.save(path.join('output', "picture.png"))

