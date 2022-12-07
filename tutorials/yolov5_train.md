# YOLOV5训练教程
## 1. 打印学习率曲线
yolov5中有打印学习率曲线的功能，但是默认关闭，需要修改源码将其打开。
以V7.0为例，对 /yolov5/train.py 进行修改，修改后每次训练时会将学习率曲线同步保存在训练结果下。
``` python
    # /yolov5/train.py:33
    from torch.optim import lr_scheduler
    from tqdm import tqdm
+   from utils.plots import plot_lr_scheduler

    # /yolov5/train.py:160
    if opt.cos_lr:
            lf = one_cycle(1, hyp['lrf'], epochs)  # cosine 1->hyp['lrf']
        else:
            lf = lambda x: (1 - x / epochs) * (1.0 - hyp['lrf']) + hyp['lrf']  # linear
    scheduler = lr_scheduler.LambdaLR(optimizer, lr_lambda=lf)  # plot_lr_scheduler(optimizer, scheduler, epochs)
+   plot_lr_scheduler(optimizer, scheduler, epochs, save_dir=save_dir)
```
