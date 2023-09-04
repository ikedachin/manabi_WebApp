from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpRequest
import glob
import os
import shutil

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

def inspction_image(request, type_name):
    print('aaa')
    inspected_dir = './solder/static/inspected_image/'
    shutil.copy(raw_images[type_name], inspected_dir) # ここの代わりにYOLOでの推論を入れる

    basename = os.path.basename(type_name)
    inspected_path = inspected_dir + basename
    inspected_row = {os.path.basename(type_name): inspected_path}
    print(inspected_row)
    time.sleep(1)
    return JsonResponse(inspected_row)


