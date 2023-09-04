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


- visual_inspection/visual_inspection/settings.pyの修正
    - staticフォルダに保存したJavaScript、CSSををリンクづける

```
STATICFILES_DIRS =[
    BASE_DIR / 'solder/static',
]
```

-   
    - アプリの定義を行う

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'solder', <= add
]
```

solder/urls.pyを作る
```
from django.urls import path
from . import views

urlpatterns = [
    path('index.html', views.image_path.as_view(), name='index')
]

```