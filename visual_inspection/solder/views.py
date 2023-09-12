from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpRequest
import glob
import os
import shutil
import cv2
import argparse
import pandas as pd
from .applications.yolov5.detect import run, main
from .applications.preprosess.mask_edge_image import crop_image
# from .yolov5.detect import run, main

# Create your views here.

#image pathのリストを作っておく
# image_file_path = glob.glob('.../images/*.jpeg')
image_path = sorted(glob.glob('./solder/static/raw_images/*.jpeg'))

class Image_path(TemplateView):
    template_name = 'index.html'
    def get_image_list(self, **kywargs):
        context = super().get_context_data(**kywargs)
        context['num_file'] = len(image_path)
        return context


def get_image_path(request, type_name):
    # index = int(type_name)
    # print(type_name)
    global raw_images
    raw_images = {}
    file_name_list = []
    path_list = []
    # pathはmanage.pyからの相対ぱすで良さそう
    for path in image_path:
        basename = os.path.basename(path).split('.')[0]
        raw_images[basename] = path
    # print(raw_images)
    return JsonResponse(raw_images)


import time

# 推論条件を作っておく
# }

# yoloで推論する関数
def inspction_image(request, type_name):
    basename = type_name.replace('.jpeg', '.png')
    inspected_dir = './solder/static/inspected_image/'
    masked_edge_image = 'solder/static/masked_image/' + basename
    masked_edge = crop_image(raw_images[type_name.split('.')[0]])
    cv2.imwrite(masked_edge_image, masked_edge)
    # print(masked_edge_image)
    # ここまでOK
    # # 最もスコアの良かったモデルを使って予測する
    # python3 detect.py --weights ./runs/masked_edge/weights/best.pt  --source ../../static/masked_edge/ --save-txt
    run(
        weights='./solder/applications/yolov5/runs/masked_color_96e/weights/best.pt', # masked_edge
        # weights='solder/applications/yolov5/runs/masked_color/weights/best.pt', # masked_color
        source=masked_edge_image, # 中身は => 'solder/static/masked_edge/' + basename
        # data='solder/applications/yolov5/data/pbl02.yaml',
        # imgsz=(640, 640),  # inference size (height, width)
        # conf_thres=0.038,
        # conf_thres=0.589,
        conf_thres=0.338, # masked_color
        iou_thres=0.25,  # NMS IOU threshold 初期値0.45
        # max_det=1000,  # maximum detections per image
        # device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        # view_img=False,  # show results
        save_txt=True,
        save_conf=True,
        # save_crop=False,  # save cropped prediction boxes
        # nosave=False,  # do not save images/videos
        # classes=None,  # filter by class: --class 0, or --class 0 2 3
        # agnostic_nms=False,  # class-agnostic NMS
        # augment=False,  # augmented inference
        # visualize=False,  # visualize features
        # update=False,  # update all models
        project='solder/static',
        name='inspected_image',
        exist_ok=True,
        # line_thickness=3,  # bounding box thickness (pixels)
        # hide_labels=False,  # hide labels
        # hide_conf=False,  # hide confidences
        # half=False,  # use FP16 half-precision inference
        # dnn=False,  # use OpenCV DNN for ONNX inference
        # vid_stride=1,  # video frame-rate stride
    )
    inspected_path = inspected_dir + basename
    inspected_row = {'src': inspected_path}
    # 探すファイル名を作る
    basename_txt = basename.replace('.png', '.txt')
    txt_path = inspected_dir + 'labels/' + basename_txt
    if os.path.isfile(txt_path):
        result_df = pd.read_csv(txt_path, sep=' ', header=None, names=['label', 'cx', 'cy', 'bx', 'by', 'conf'])
        label_list = result_df.loc[:, 'label'].tolist()
        label_unique = set(label_list)
        for element in label_unique:
            label_list.count(element)
            inspected_row[element] = str(label_list.count(element))

    # ファイル名が存在したら読み込んで、不良をinpected_rowに入れる
    # print(inspected_row)
    return JsonResponse(inspected_row)

"""
def run(
        weights=ROOT / 'yolov5s.pt',  # model path or triton URL
        source=ROOT / 'data/images',  # file/dir/URL/glob/screen/0(webcam)
        data=ROOT / 'data/coco128.yaml',  # dataset.yaml path
        imgsz=(640, 640),  # inference size (height, width)
        conf_thres=0.25,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img=False,  # show results
        save_txt=False,  # save results to *.txt
        save_conf=False,  # save confidences in --save-txt labels
        save_crop=False,  # save cropped prediction boxes
        nosave=False,  # do not save images/videos
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        update=False,  # update all models
        project=ROOT / 'runs/detect',  # save results to project/name
        name='exp',  # save results to project/name
        exist_ok=False,  # existing project/name ok, do not increment
        line_thickness=3,  # bounding box thickness (pixels)
        hide_labels=False,  # hide labels
        hide_conf=False,  # hide confidences
        half=False,  # use FP16 half-precision inference
        dnn=False,  # use OpenCV DNN for ONNX inference
        vid_stride=1,  # video frame-rate stride
):


"""

def clear_result(request, type_name):
    print(type_name)
    # if os.path.isfile('./solder/static/inspected_image/') == True:
    print('EEE')
    shutil.rmtree('./solder/static/inspected_image/')
    os.makedirs('./solder/static/inspected_image/', exist_ok=True)

    # if os.path.isfile('./solder/static/masked_edge/') == True:
    shutil.rmtree('./solder/static/masked_edge/')
    os.makedirs('./solder/static/masked_edge/', exist_ok=True)
    
    files = glob.glob('./solder/static/inspected_image/*.png')
    cleared_row = {}
    cleared_row['num_files'] = str(len(files))
    return JsonResponse(cleared_row)