try:
    print("Elementary imports: ")
    import os
    import json
    import glob
    import argparse
    print("numpy/scipy imports:")
    import numpy as np
    from scipy import signal as sg
    import scipy.ndimage as ndimage
    from scipy.ndimage.filters import maximum_filter
    from scipy.signal import convolve
    print("PIL imports:")
    from PIL import Image
    print("matplotlib imports:")
    import matplotlib.pyplot as plt
except ImportError:
    print("Need to fix the installation")
    raise
print("All imports okay. Yay!")
def convolve_green_and_red(image):
    kernel = np.array([
        [0.33333334, 0.20784314, 0.12941177, 0.10196079, 0.11764706, 0.10980392, 0.10980392, 0.10980392, 0.10980392],
        [0.23921569, 0.20784314, 0.17254902, 0.28235295, 0.28627452, 0.41960785, 0.3882353, 0.34509805, 0.22352941],
        [0.20392157, 0.18431373, 0.25882354, 0.53333336, 0.8117647, 0.8392157, 0.73333335, 0.45882353, 0.44313726],
        [0.21960784, 0.21176471, 0.5176471, 0.7921569, 0.90588236, 0.91764706, 0.8627451, 0.61960787, 0.46666667],
        [0.29803923, 0.41568628, 0.74509805, 0.85490197, 0.8392157, 0.80784315, 0.80784315, 0.7647059, 0.57254905],
        [0.3647059, 0.5921569, 0.8392157, 0.83137256, 0.8235294, 0.8901961, 0.89411765, 0.8235294, 0.6627451],
        [0.37254903, 0.6509804, 0.8509804, 0.8352941, 0.85490197, 0.92941177, 0.90588236, 0.8392157, 0.69411767],
        [0.34901962, 0.6313726, 0.8666667, 0.87058824, 0.88235295, 0.92941177, 0.9137255, 0.87058824, 0.72156864],
        [0.24705882, 0.4392157, 0.76862746, 0.8745098, 0.92156863, 0.99607843, 0.9490196, 0.9607843, 0.6509804]])
    kernel = kernel - kernel.mean()
    # kernel = np.flipud(kernel)
    # kernel = np.fliplr(kernel)
    converted_img_by_green = convolve(image[:, :, 1], kernel, 'same')
    converted_img_by_red = convolve(image[:, :, 0], kernel, 'same')
    return converted_img_by_green, converted_img_by_red
def find_tfl_lights(c_image: np.ndarray, **kwargs):
    """
    Detect candidates for TFL lights. Use c_image, kwargs and you imagination to implement
    :param c_image: The image itself as np.uint8, shape of (H, W, 3)
    :param kwargs: Whatever config you want to pass in here
    :return: 4-tuple of x_red, y_red, x_green, y_green
    """
    conv_by_green_res, conv_by_red_res = convolve_green_and_red(c_image)
    x_red = list()
    y_red = list()
    x_green = list()
    y_green = list()
    filtered_green_res = ndimage.maximum_filter(conv_by_green_res, (20, 20))
    filtered_red_res = ndimage.maximum_filter(conv_by_red_res, (35, 35))
    red_counter = 0
    geen_counter = 0
    counter = 0
    for i in range(len(filtered_green_res)):
        for j in range(len(filtered_green_res[0])):
            counter += 1
            if filtered_green_res[i][j] == conv_by_green_res[i][j] and conv_by_green_res[i][j] > 2.6 and counter >= 10:
                x_green.append(j-2)
                y_green.append(i-2)
                geen_counter += 1
                counter = 0
            elif filtered_red_res[i][j] == conv_by_red_res[i][j] and conv_by_red_res[i][j] > 3 and counter >= 10:
                x_red.append(j-2)
                y_red.append(i-2)
                red_counter += 1
                counter = 0
    print(geen_counter+red_counter)

    return x_red, y_red, x_green, y_green

def show_image_and_gt(image, objs, fig_num=None):
    plt.figure(fig_num).clf()
    plt.imshow(image)
    labels = set()
    if objs is not None:
        for o in objs:
            poly = np.array(o['polygon'])[list(np.arange(len(o['polygon']))) + [0]]
            plt.plot(poly[:, 0], poly[:, 1], 'r', label=o['label'])
            labels.add(o['label'])
        if len(labels) > 1:
            plt.legend()
def test_find_tfl_lights(image_path, json_path=None, fig_num=None):
    """
    Run the attention code
    """
    image = np.array(Image.open(image_path)).astype(np.float32) / 255
    if json_path is None:
        objects = None
    else:
        gt_data = json.load(open(json_path))
        what = ['traffic light']
        objects = [o for o in gt_data['objects'] if o['label'] in what]
    show_image_and_gt(image, objects, fig_num)
    red_x, red_y, green_x, green_y = find_tfl_lights(image, some_threshold=42)
    plt.plot(red_x, red_y, 'ro', color='r', markersize=4)
    plt.plot(green_x, green_y, 'ro', color='g', markersize=4)
def main(argv=None):
    """It's nice to have a standalone tester for the algorithm.
    Consider looping over some images from here, so you can manually exmine the results
    Keep this functionality even after you have all system running, because you sometime want to debug/improve a module
    :param argv: In case you want to programmatically run this"""
    parser = argparse.ArgumentParser("Test TFL attention mechanism")
    parser.add_argument('-i', '--image', type=str, help='Path to an image')
    parser.add_argument("-j", "--json", type=str, help="Path to json GT for comparison")
    parser.add_argument('-d', '--dir', type=str, help='Directory to scan images in')
    args = parser.parse_args(argv)
    default_base = 't/'
    if args.dir is None:
        args.dir = default_base
    flist = glob.glob(os.path.join(args.dir, '*_leftImg8bit.png'))
    for image in flist:
        json_fn = image.replace('_leftImg8bit.png', '_gtFine_polygons.json')
        if not os.path.exists(json_fn):
            json_fn = None
        test_find_tfl_lights(image, json_fn)
    if len(flist):
        print("You should now see some images, with the ground truth marked on them. Close all to quit.")
    else:
        print("Bad configuration?? Didn't find any picture to show")
    plt.show(block=True)
if __name__ == '__main__':
    main()