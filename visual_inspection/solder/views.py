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
    index = int(type_name)
    print(index)
    global raw_images
    raw_images = {}
    file_name_list = []
    path_list = []
    # pathはmanage.pyからの相対ぱすで良さそう
    for path in image_path:
        file_name_list.append(os.path.basename(path))
        path_list.append(path)
    raw_images[file_name_list[index]] = path_list[index]
    print(raw_images)
    return JsonResponse(raw_images)


import time

# 推論条件を作っておく
# }

def inspction_image(request, type_name):
    # opt_yolo = parse_opt()
    # opt_yolo.weights = './applications/yolov5/runs/train/masked_edge/weights/best.pt'
    # opt_yolo.project = '../../static/inspected_image/'
    # opt_yolo.conf = 0.66
    # opt_yolo.save_text = True
    # opt_yolo.name = ''
    # opt_yolo.exist_ok = True
    basename = type_name.replace('.jpeg', '.png')
    print(basename)
    inspected_dir = './solder/static/inspected_image/'
    masked_edge_image = './solder/static/masked_edge/' + basename
    masked_edge = crop_image(raw_images[type_name])
    cv2.imwrite(masked_edge_image, masked_edge)
    # ここまでOK
    run(
        weights='./solder/applications/yolov5/runs/runs_masked_edge/train/masked_edge/weights/best.pt',
        project='./solder/static/inspected_image/',
        source=masked_edge_image,
        conf_thres=0.66,
        save_conf=True,
        name='',
        exist_ok=True,  
    )
    inspected_path = inspected_dir + basename
    # inspected_path = inspected_dir
    inspected_row = {basename: inspected_path}
    print(inspected_row)
    return JsonResponse(inspected_row)

