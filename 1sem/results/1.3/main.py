from core.input.utils import *

if __name__ == '__main__':
    img = image_to_np_array("uzu.png")

    print('Введите целый коэффициент растяжения')
    numerator = safe_number_input(int, 1)

    print('Введите целый коэффициент сжатия')
    denominator = safe_number_input(int, 1)

    args = [numerator, denominator]
    result = Image.fromarray(two_step_resampling(img, *args).astype(np.uint8), 'RGB')
    result.save(path.join('output', "picture.png"))
