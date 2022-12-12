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

## 2. 后台训练
使用服务器进行训练时，建议将训练任务放到后台进行训练，防止因为网络原因而导致的断开。
使用下面的命令，其中：
`nohup` 表示用户退出时进程不会被关闭
`commnd` 表示要运行的命令
`> output.txt` 表示将标准输出定向到`output.txt`中，可以通过`output.txt`查看运行程序运行状态
`&` 表示后台执行，不影响当前终端的使用
``` bash
nohup command > output.txt &
```
当想要关闭已经开始的进程时，需要先得到该进程的PID，可以通过命令`ps -ux`查看当前用户正在进行的进程，找到对应的进程PID将其kill，通过命令`kill -9 id`，其中id是刚才找到的PID号