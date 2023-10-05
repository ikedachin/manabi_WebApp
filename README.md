# 動作イメージ
<img src='../image.png'>

# 準備

- make env
```
python3 -m venv webapp_env
```
- install
```
pip install --upgrade pip
pip install -r requirements.txt # Djangoの環境インストール
```

- yolov5をgit clone
```
cd solder/applications
git clone https://github.com/ultralytics/yolov5.git
pip install -r requiremants.txt # YOLOv5の環境インストール
```


# Django設定

- プロジェクトの作成
```
django-admin startproject manabi_webapp
```
- アプリの作成
```
cd visual_inspection
python3 manage.py startapp solder
```

- make folders
visual_inspection/solder/applications # main app program
visual_inspection/solder/template # html
visual_inspection/solder/static # CSS,JavaScript




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

# URL設定
- visual_inspection/urls.pyの修正
solderのurlパス設定
```
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('solder/', include('solder.urls')), <= add rooting
]
```
- solder/urls.pyを作る
solder以下のurlパス設定
```
from django.urls import path
from . import views

urlpatterns = [
    # index.htmlのパス
    path('index.html', views.Image_path.as_view(), name='index'),
    # 入力画像のパスを取得するパス
    path('get_imge_path/<str:type_name>', views.get_image_path, name='get_image_path'),
    # 推論を行うためのパス
    path('inspction_image/<str:type_name>', views.inspction_image, name='inspction_image'),
    # 推論結果のファイルを消すためのパス
    path('clear_result/<str:type_name>', views.clear_result, name='clear_result'),
    # メディアフォルダの設定
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # 画像フォルダ追加時
```
JavaScriptからそれぞれのurlにfetchすると"solder/views.py"の中の関数に処理がリクエストされる。（get_image_path,inspection_imageなど）
