import numpy as np
from PIL import Image
from tensorflow import keras


my_model = keras.models.load_model(r"utils/rel_97_bt50_ep20_.h5")

def crop_img(cord, img):
    height, width, _ = img.shape
    left = cord[0] - 40
    top = cord[1] - 40
    right = cord[0] + 41
    bottom = cord[1] + 41
    return np.array(Image.fromarray(img).crop((left, top, right, bottom)))


def get_candidate_imgs(x_y_red, x_y_green, image):
    red_cropped_imgs = list()
    green_cropped_imgs = list()

    for position in x_y_red:
        cropped_img = crop_img(position, image)
        red_cropped_imgs.append(cropped_img)

    for position in x_y_green:
        cropped_img = crop_img(position, image)
        green_cropped_imgs.append(cropped_img)

    return red_cropped_imgs, green_cropped_imgs


def is_tfl(model, image):
    model_res = model.predict(image.reshape([-1] + [81, 81] + [3]))
    return model_res[0][1] > model_res[0][0] and model_res[0][1] >= 0.98


def run_neural_net(x_y_red, x_y_green, img):
    red_tfl_imgs, green_tfl_imgs = get_candidate_imgs(x_y_red, x_y_green, img)
    global my_model
    is_red_tfl = []
    is_green_tfl =[]

    for red_tfl in red_tfl_imgs:
        is_red_tfl.append(is_tfl(my_model, np.array(red_tfl)))

    for green_tfl in green_tfl_imgs:
        is_green_tfl.append(is_tfl(my_model, np.array(green_tfl)))

    red_tfls = []
    for index, val in enumerate(is_red_tfl):
        if val:
            red_tfls.append(x_y_red[index])

    green_tfls = []
    for index, val in enumerate(is_green_tfl):
        if val:
            green_tfls.append(x_y_green[index])

    return red_tfls, green_tfls
