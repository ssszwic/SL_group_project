import cv2
import argparse
import os
import glob
import numpy as np
import prettytable as pt
from tqdm import tqdm
from matplotlib import pyplot as plt
from collections import Counter

ROOT = os.getcwd()

def show_dict_excel(src_dict):
    keys = sorted(src_dict.keys())
    tb = pt.PrettyTable()
    tb.field_names = ["Label", "width", "height", "area", "Number"]
    sum = 0
    for key in keys:
        tb.add_row([key, key[1], key[0], key[0] * key[1], src_dict[key]])
        sum += src_dict[key]
    tb.add_row(['Sum', '-', '-', '-', sum])
    print(tb)


def analysis_image(img_dirs, save_dir, hist=True):
    png_list = []
    jpg_list = []
    for img_dir in img_dirs:
        png_list += glob.glob(img_dir + '*.png')
        jpg_list += glob.glob(img_dir + '*.jpeg') + glob.glob(img_dir + '*.jpg') + glob.glob(img_dir + '*.jpe')
    
    img_list = png_list + jpg_list
    img_num = len(img_list)

    if img_num == 0:
        raise Exception('no image or image trpe is unsupport!')

    print('------------------------------image------------------------------')
    print('png num: ', len(png_list))
    print('jpg (jpeg, jpe) num: ', len(jpg_list))
    print('total num: ', img_num)

    width_np = np.zeros(img_num, dtype=np.int32)
    height_np = np.zeros(img_num, dtype=np.int32)
    shape_list = []
    shape_str = []
    
    # read height and width of every image
    for i in tqdm(range(len(img_list)), desc='Processing'):
        img = cv2.imread(img_list[i])
        # ignore channel
        shape_list.append(img.shape)
        shape_str.append(str(img.shape))
        height_np[i] = img.shape[0]
        width_np[i] = img.shape[1]

    area_np = height_np * width_np

    print('------------------------------tabel------------------------------')
    show_dict_excel(Counter(shape_list))

    # plot histogram
    min_width = min(width_np)
    max_width = max(width_np)
    min_height = min(height_np)
    max_height = max(height_np)
    min_area = min(area_np)
    max_area = max(area_np)

    print('------------------------------info------------------------------')
    print('min_width: ', min_width)
    print('max_width: ', max_width)
    print('min_height: ', min_height)
    print('max_height: ', max_height)
    print('min_area: ', min_area)
    print('max_area: ', max_area)

    if hist:
        print('---------------------------histogram---------------------------')
        plt.figure(1)
        plt.xticks(fontsize=4)
        plt.hist(shape_str, bins=len(set(shape_str)) * 3)
        plt.xlabel("shape")
        plt.ylabel("frequency")
        plt.title("shape")
        plt.savefig(save_dir + 'shape_hist.svg')

        plt.figure(2)
        plt.hist(height_np, bins=len(set(height_np)) * 3)
        plt.xlabel("height/pixel")
        plt.ylabel("frequency")
        plt.title("height")
        plt.savefig(save_dir + 'height_hist.svg')

        plt.figure(3)
        plt.hist(width_np, bins=len(set(width_np)) * 3)
        plt.xlabel("width/pixel")
        plt.ylabel("frequency")
        plt.title("width")
        plt.savefig(save_dir + 'width_hist.svg')
        
        plt.figure(4)
        plt.hist(area_np, bins=len(set(area_np)) * 3)
        plt.xlabel("area/pixel^2")
        plt.ylabel("frequency")
        plt.title("area")
        plt.savefig(save_dir + 'area_hist.svg')

        print('save image at ' + save_dir)
    return min_width, max_width, min_height, max_height

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--images_dir', type=str, nargs='+', required=True, help='images directory')
    parser.add_argument('--save_dir', type=str, default=ROOT, required=False, help='save directory, default save at current directory')
    parser.add_argument('--hist', action='store_true', required=False, help="gengrate histogram")
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
    
    if args.hist:
        hist = True
    else:
        hist = False
    analysis_image(dirs, save_dir, hist=hist)