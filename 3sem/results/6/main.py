from filter import rank_filter
from my_io import prompt, image_to_np_array, safe_number_input, path, Image


def difference_image(img1: np.array, img2: np.array) -> np.array:
    return img1 - img2


images = {
    'Text': 'text_bin_light.bmp',
    'Face': 'face.bmp',
    'House': 'house_bin.bmp',
    'Chess': 'chess_bin.bmp'
}

if __name__ == '__main__':
    print('Выберите изображение:')
    selected_image = prompt(images)
    img = image_to_np_array(selected_image)

    print('Выберите размер окна (обязательно нечетный)')
    size = safe_number_input(1, 29)

    print('Введите ранг:')
    rank = safe_number_input(1, size**2)

    res_img = rank_filter(img, size, rank)
    difference = difference_image(img, res_img)
    res_img = Image.fromarray(res_img, 'L')
    difference = Image.fromarray(difference, 'L')

    difference.save(path.join('differential_pictures', selected_image))
    print('Введите название сохраненного изображения (оставьте пустым, чтобы \
не сохранять)')
    selected_path = input()
    if selected_path:
        res_img.save(path.join('pictures_results', selected_path))