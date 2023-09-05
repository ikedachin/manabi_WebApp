from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpRequest
import glob
import os
import shutil
import cv2
import argparse
from .applications.yolov5.detect import run, main
from .applications.preprosess.mask_edge_image import crop_image

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
    print(type_name)
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

def inspction_image(request, type_name):
    basename = type_name.replace('.jpeg', '.png')
    print(basename)
    inspected_dir = './solder/static/inspected_image/'
    masked_edge_image = './solder/static/masked_edge/' + basename
    masked_edge = crop_image(raw_images[type_name.split('.')[0]])
    cv2.imwrite(masked_edge_image, masked_edge)
    # ここまでOK
    # # 最もスコアの良かったモデルを使って予測する
    # !python detect.py --source /content/working/test/images --weights runs/train/masked_edge/weights/best.pt --conf 0.632 --save-txt
    run(
        weights='./solder/applications/yolov5/runs/runs_masked_edge/train/masked_edge/weights/best.pt',
        source=masked_edge_image,
        data='.solder/applications/yolov5/data/pbl02.yaml',
        imgsz=(640, 640),  # inference size (height, width)
        conf_thres=0.632,
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img=False,  # show results
        save_txt = True,
        save_conf = True,
        save_crop=False,  # save cropped prediction boxes
        nosave=False,  # do not save images/videos
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        update=False,  # update all models
        project='./solder/static',
        name='inspected_image',
        exist_ok=True,
        line_thickness=3,  # bounding box thickness (pixels)
        hide_labels=False,  # hide labels
        hide_conf=False,  # hide confidences
        half=False,  # use FP16 half-precision inference
        dnn=False,  # use OpenCV DNN for ONNX inference
        vid_stride=1,  # video frame-rate stride
    )
    inspected_path = inspected_dir + basename
    # inspected_path = inspected_dir
    inspected_row = {basename: inspected_path}
    # print(inspected_row)
    return JsonResponse(inspected_row)

"""
'runs/train/color2/weights/best.pt'], 
source=/content/working/test/images, 
data=data/coco128.yaml, 
imgsz=[640, 640], 
conf_thres=0.66, 
iou_thres=0.45, 
max_det=1000, 
device=, 
view_img=False, 
save_txt=True, 
save_conf=False, 
save_crop=False, 
nosave=False, 
classes=None, 
agnostic_nms=False, 
augment=False, 
visualize=False, 
update=False, 
project=runs/detect, 
name=exp, 
exist_ok=False, 
line_thickness=3, 
hide_labels=False, 
hide_conf=False, 
half=False, 
dnn=False, 
vid_stride=1

"""