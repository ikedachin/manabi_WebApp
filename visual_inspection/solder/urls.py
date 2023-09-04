from django.urls import path
from . import views
from django.conf.urls.static import static # 画像フォルダ追加時
from django.conf import settings # 画像フォルダ追加時


urlpatterns = [
    path('index.html', views.Image_path.as_view(), name='index'),
    path('get_imge_path/<str:type_name>', views.get_image_path, name='get_image_path'),
    path('inspction_image/<str:type_name>', views.inspction_image, name='inspction_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # 画像フォルダ追加時
