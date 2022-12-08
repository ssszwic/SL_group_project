# DatasetProcess
数据集处理脚本

## label_replace
对YOLOV5格式的数据集的标签进行替换、删除等处理

- Requirements
    |package|version|
    |:-:|:-:|
    |tqdm|4.64.1|

    只在该版本下测试通过，其它版本应该也没问题

- Parameter
    |parameter|resolve|
    |:-:|:-:|
    |label_dict|标签字典，指定要替换或删除的标签|
    |images_dir|标签所在文件夹路径|
    |save_dir|生成的新的标签所在文件夹的路径|

- label_dict
    通过label_dict指定所要替换的标签，YOLOV5的标签用数字0, 1, 2, 3... nc-1表示，其中nc为类别的数量，label_dict的类型为字典，其中字典的key表示原label中的标签，对应的alue表示替换后label中的标签，若value为-1，则表示删除该标签，key中没有提到的标签维持原样。
    假如现在要对VisDrone的标签进行替换删除，VisDrone的标签为:
    ``` yaml
    0: pedestrian
    1: people
    2: bicycle
    3: car
    4: van
    5: truck
    6: tricycle
    7: awning-tricycle
    8: bus
    9: motor
    ```
    想要删除其中的bicycle、truck、tricycle、awning-tricycle、bus，对应的label_dict为
    ``` python
    {2:-1, 3:2, 4:3, 5:-1, 6:-1, 7:-1, 8:-1, 9:4}
    ```
    表示删去原label中的2、5、6、7、8，将3、4、9分别替换成2、3、4，替换后的标签为：
    ``` yaml
    0: pedestrian
    1: people
    2: car
    3: van
    4: motor
    ```
    
- Start
    注意要将label_dict包含在双引号内
    ``` python
    # 将/home/user/Work/Dataset/VisDrone/VisDrone2019-DET-train/labels_src中的label根据label_dict进行替换，将替换后的label放在/home/user/Work/Dataset/VisDrone/VisDrone2019-DET-train/labels下
    python label_replace.py \
        --label_dict "{2:-1, 3:2, 4:3, 5:-1, 6:-1, 7:-1, 8:-1, 9:4}" \
        --label_dir /home/user/Work/Dataset/VisDrone/VisDrone2019-DET-train/labels_src \
        --save_dir /home/user/Work/Dataset/VisDrone/VisDrone2019-DET-train/labels
    ```

- Other
  目前只支持YOLOV5的标签格式