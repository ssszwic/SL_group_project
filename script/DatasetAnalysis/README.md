# DatasetAnalysis
数据集分析脚本

## image_analysis
分析数据集图片的尺寸、宽度、高度、面积分布，生成直方图，同时打印最大值和最小值。

- Requirements
    |package|version|
    |:-:|:-:|
    |opencv-python|4.5.2|
    |numpy|1.23.4|
    |tqdm|4.64.1|
    |matplotlib|3.5.3|
    |prettytable|3.5.0|
    只在该版本下测试通过，其它版本应该也没问题

- Parameter
    |parameter|resolve|
    |:-:|:-:|
    |images_dir|图片所在文件夹路径，支持多个文件夹，同时输入多个文件夹时用空格隔开|
    |save_dir|生成的直方图的保存路径，默认为当前目录|
    |hist|保存直方图结果|

- Start
    ``` python
    # 分析 /home/data0/images 中的图片，结果保存在 /home/out 下
    python image_analysis.py --images_dir /home/data0/images \
                            --save_dir /home/out \
                            --hist

    # 分析 /home/data0/images 和 /home/data1/images 中的图片，结果保存在 /home/out 下
    python image_analysis.py --images_dir /home/data0/images /home/data1/images \
                            --save_dir /home/out
                            --hist
    ```

- Other
  目前支持的图片格式有 png、jpg、jpeg、jpe，可以自行补充