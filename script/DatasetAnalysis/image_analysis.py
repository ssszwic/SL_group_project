import cv2
import argparse
import os
import glob
import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt

ROOT = os.getcwd()

def analysis_image(img_dirs, save_dir, step=10, print_info=True):
    png_list = []
    jpg_list = []
    for img_dir in img_dirs:
        print(img_dir)
        png_list += glob.glob(img_dir + '*.png')
        jpg_list += glob.glob(img_dir + '*.jpeg') + glob.glob(img_dir + '*.jpg') + glob.glob(img_dir + '*.jpe')
        print(len(jpg_list))
    
    img_list = png_list + jpg_list
    img_num = len(img_list)

    if img_num == 0:
        raise Exception('no image or image trpe is unsupport!')

    if print_info:
        print('----------------------------------')
        print('png num: ', len(png_list))
        print('jpg (jpeg, jpe) num: ', len(jpg_list))
        print('total num: ', img_num)

    width_np = np.zeros(img_num, dtype=np.int32)
    height_np = np.zeros(img_num, dtype=np.int32)

    # read height and width of every image
    for i in tqdm(range(len(img_list)), desc='Processing'):
        img = cv2.imread(img_list[i])
        height_np[i] = img.shape[0]
        width_np[i] = img.shape[1]

    area_np = height_np * width_np

    # plot histogram
    min_width = min(width_np)
    max_width = max(width_np)
    min_height = min(height_np)
    max_height = max(height_np)
    min_area = min(area_np)
    max_area = max(area_np)

    if print_info:
        print('----------------------------------')
        print('min_width: ', min_width)
        print('max_width: ', max_width)
        print('min_height: ', min_height)
        print('max_height: ', max_height)
        print('min_area: ', min_area)
        print('max_area: ', max_area)

    plt.figure(1)
    plt.hist(height_np, bins=int((max_height - min_height) / step))
    plt.xlabel("pixel")
    plt.ylabel("number")
    plt.title("height")
    plt.savefig(save_dir + 'height_hist.svg')

    plt.figure(2)
    plt.hist(width_np, bins=int((max_width - min_width) / step))
    plt.xlabel("pixel")
    plt.ylabel("number")
    plt.title("width")
    plt.savefig(save_dir + 'width_hist.svg')

    plt.figure(3)
    plt.hist(area_np, bins=int((max_area - min_area) / pow(step, 4)))
    plt.xlabel("pixel^2")
    plt.ylabel("number")
    plt.title("area")
    plt.savefig(save_dir + 'area_hist.svg')

    print('save image at ' + save_dir)
    return min_width, max_width, min_height, max_height

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--images_dir', type=str, nargs='+', required=True, help='images directory')
    parser.add_argument('--save_dir', type=str, default=ROOT, required=False, help='images directory')
    parser.add_argument('--step', type=int, default=10, required=False, help='images directory')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_opt()
    dirs = []
    image_dirs = args.images_dir
    for image_dir in image_dirs:
        if not os.path.exists(image_dir):
            raise Exception('images directory ', image_dir, ' is not exists!')
        if image_dir[-1] != '/':
            dirs.append(image_dir + '/')
        else:
            dirs.append(image_dir)

    save_dir = args.save_dir
    if save_dir[-1] != '/':
        save_dir = save_dir + '/'

    assert args.step > 0
    analysis_image(dirs, save_dir, step=args.step)

    
    
    
