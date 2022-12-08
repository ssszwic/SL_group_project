import argparse
import os
import ast
from tqdm import tqdm

def label_replace(label_dir, save_dir, label_dict):
    # label_list = glob.glob(label_dir + '*.txt')
    label_list = os.listdir(label_dir)
    for i in tqdm(range(len(label_list)), desc='Processing'):
        assert os.path.splitext(label_list[i])[-1] == '.txt'
        old_name = label_dir + label_list[i]
        new_name = save_dir + label_list[i]
        with open(old_name, 'r') as fr:
            # overlap old file
            with open(new_name, 'w') as fw:
                for line in fr.readlines():
                    line_list = line.split(' ')
                    # matching
                    if int(line_list[0]) in label_dict:
                        if(label_dict[int(line_list[0])] == -1):
                            # delate label
                            continue
                        line_list[0] = str(label_dict[int(line_list[0])])
                    new_line = ' '.join(line_list)
                    fw.write(new_line)

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label_dict', type=ast.literal_eval, required=True, help='label dictionary')
    parser.add_argument('--label_dir', type=str, required=True, help='images directory')
    parser.add_argument('--save_dir', type=str, required=True, help='save directory')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_opt()
    if not os.path.exists(args.label_dir):
        raise Exception('images directory ', args.label_dir, ' is not exists!')
    if not os.path.exists(args.save_dir):
        print("save directory is not exits, create", args.save_dir)
        os.makedirs(args.save_dir) 

    label_dir = args.label_dir
    save_dir = args.save_dir
    if label_dir[-1] != '/':
        label_dir += '/'
    if save_dir[-1] != '/':
        save_dir += '/'

    label_dict = args.label_dict

    label_replace(label_dir, save_dir, label_dict)
    

    
    