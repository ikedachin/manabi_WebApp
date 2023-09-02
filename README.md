- make env
```
python3 -m venv webapp_env
```
- install
```
pip install --upgrade pip
pip install Django
```
- プロジェクトの作成
```django-admin startproject manabi_webapp
```
- アプリの作成
```
cd visual_inspection
python3 manage.py startapp solder
```

- visual_inspection/urls.pyの修正
```
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('solder/', include('solder.urls')), <= add rooting
]
```

- make folders
visual_inspection/solder/applications # main app program
visual_inspection/solder/template # html
visual_inspection/solder/static # CSS,JavaScript

- yolov5をgit clone
cd solder/applications
git clone https://github.com/ultralytics/yolov5.git

