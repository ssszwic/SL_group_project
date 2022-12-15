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
- `nohup` 表示用户退出时进程不会被关闭
- `command` 表示要运行的命令
- `> output.txt` 表示将标准输出定向到`output.txt`中，可以通过`output.txt`查看运行程序运行状态
- `&` 表示后台执行，不影响当前终端的使用
``` bash
nohup command > output.txt &
```
当想要关闭已经开始的进程时，需要先得到该进程的PID，可以通过命令`ps -ux`查看当前用户正在进行的进程，找到对应的进程PID将其kill，通过命令`kill -9 id`，其中id是刚才找到的PID号

## 3. 打印每一类目标的ap
在每一个epoch结束时，默认只输出所有目标的平均ap，以V7.0为例，若想要输出每一类目标的ap，只需要改变函数`validate.run`的`verbose`参数，将原来的`False`改为`True`
``` python
# /yolov5/train.py:350
    results, maps, _ = validate.run(data_dict,
                                    batch_size=batch_size // WORLD_SIZE * 2,
                                    imgsz=imgsz,
                                    half=amp,
                                    model=ema.ema,
                                    single_cls=single_cls,
                                    dataloader=val_loader,
                                    save_dir=save_dir,
-                                   verbose=False,
+                                   verbose=True,
                                    plots=False,
                                    callbacks=callbacks,
                                    compute_loss=compute_loss)
```

## 4. 绘制每一类目标的ap曲线
yolov5默认只绘制所有目标的整体map，可以添加相应的代码绘制每一类的ap曲线，以V7.0为例
在每一个epoch训练结束后验证时，将所有的ap输出
``` python
# /yolov5/val.py:273
    stats = [torch.cat(x, 0).cpu().numpy() for x in zip(*stats)]  # to numpy
    if len(stats) and stats[0].any():
        tp, fp, p, r, f1, ap, ap_class = ap_per_class(*stats, plot=plots, save_dir=save_dir, names=names)
+       ap50_90 = ap
        ap50, ap = ap[:, 0], ap.mean(1)  # AP@0.5, AP@0.5:0.95
        mp, mr, map50, map = p.mean(), r.mean(), ap50.mean(), ap.mean()
    nt = np.bincount(stats[3].astype(int), minlength=nc)  # number of targets per class

# /yolov5/val.py:334
    for i, c in enumerate(ap_class):
        maps[c] = ap[i]
-   return (mp, mr, map50, map, *(loss.cpu() / len(dataloader)).tolist()), maps, t
+   return (mp, mr, map50, map, *(loss.cpu() / len(dataloader)).tolist()), maps, t, ap50_90
```
训练过程中保存所有epoch的ap
``` python
# /yolov5/train.py:256
    LOGGER.info(f'Image sizes {imgsz} train, {imgsz} val\n'
                f'Using {train_loader.num_workers * WORLD_SIZE} dataloader workers\n'
                f"Logging results to {colorstr('bold', save_dir)}\n"
                f'Starting training for {epochs} epochs...')
+   aps = []
    for epoch in range(start_epoch, epochs):

# /yolov5/train.py:348
    final_epoch = (epoch + 1 == epochs) or stopper.possible_stop
    if not noval or final_epoch:  # Calculate mAP
-      results, maps, _ = validate.run(data_dict,
+      results, maps, _, ap = validate.run(data_dict,
                                        batch_size=batch_size // WORLD_SIZE * 2,
                                        imgsz=imgsz,
                                        half=amp,
                                        model=ema.ema,
                                        single_cls=single_cls,
                                        dataloader=val_loader,
                                        save_dir=save_dir,
                                        verbose=True,
                                        plots=False,
                                        callbacks=callbacks,
                                        compute_loss=compute_loss)
+       aps.append(ap)

# /yolov5/train.py:410
-   results, _, _ = validate.run(
+   results, _, _, _ = validate.run(
        data_dict,
        batch_size=batch_size // WORLD_SIZE * 2,
        imgsz=imgsz,
        model=attempt_load(f, device).half(),
        iou_thres=0.65 if is_coco else 0.60,  # best pycocotools at iou 0.65
        single_cls=single_cls,
        dataloader=val_loader,
        save_dir=save_dir,
        save_json=is_coco,
        verbose=True,
        plots=plots,
        callbacks=callbacks,
        compute_loss=compute_loss)  # val best model with plots
```
训练结束后调用相关函数绘制ap
``` python
# /yolov5/train.py:32
    import yaml
    from torch.optim import lr_scheduler
    from tqdm import tqdm
+   from utils.metrics import plot_ap_curve

# /yolov5/train.py:402
    # end training -----------------------------------------------------------------------------------------------------
+   plot_ap_curve(aps, save_dir=Path(save_dir) / 'ap_curve.png', names=names)
    if RANK in {-1, 0}:
        LOGGER.info(f'\n{epoch - start_epoch + 1} epochs completed in {(time.time() - t0) / 3600:.3f} hours.')
```
绘制的函数定义如下
``` python
# /yolov5/utils/metrics.py:358
        ax.set_title(f'{ylabel}-Confidence Curve')
        fig.savefig(save_dir, dpi=250)
        plt.close(fig)

+   def plot_ap_curve(aps, save_dir=Path('ap_curve.png'), names=(), xlabel='epoch', ylabel='ap'):
+       fig, ax = plt.subplots(4, 3, figsize=(27, 24), tight_layout=True)
+       axes = ax.flatten()
+       for i in range(10):
+           iou = 0.5 + i * 0.05
+           ap = np.empty(shape=(len(aps), aps[0].shape[0]))
+           for j in range(len(aps)):
+               ap[j] = aps[j][:, i].T
+           ap = ap.T+
+           px = np.array(list(range(len(aps))))
+           for j, y in enumerate(ap):
+               axes[i].plot(px, y, linewidth=1, label=f'{names[j]}')  # plot(confidence, metric)+
+           y = smooth(ap.mean(0), 0.05)
+           axes[i].plot(px, y, linewidth=3, color='blue', label='all classes')
+           axes[i].set_xlabel(xlabel)
+           axes[i].set_ylabel(ylabel)
+           axes[i].legend(bbox_to_anchor=(1.04, 1), loc="upper left")
+           axes[i].set_title('mAP_' + '{:.2f}'.format(iou) + ' Curve')
+       fig.savefig(save_dir, dpi=250)
+       plt.close(fig)
```
修改之后，在每次训练结束时会将ap曲线以图片形式`ap_curve.png`保存在输出目录下
> 注意在以上过程中修改了`validate.run`函数的输出，运行其他脚本调用该函数时需要对返回值的接收部分修改，否则可能会报错