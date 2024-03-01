from core.input.utils import *


def execute(img, f1, f2, number_type=int):
    data_type = np.uint8
    color_model = 'RGB'
    factor = safe_number_input(number_type, 0.5)
    result = Image.fromarray(one_step_resampling(img, factor, f1, f2).astype(data_type), color_model)

    return result


if __name__ == '__main__':
    img = image_to_np_array("uzu.png")
    result = execute(img, lambda a, b: int(round(a / b)), lambda a, b: a * b)
    result.save(path.join('output', "picture.png"))
