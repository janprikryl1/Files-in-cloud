from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('item', views.item, name='item'),
    path('download', views.download_file, name="download"),
    path('upload', views.upload, name='upload'),
    path('upload_file', views.upload_file, name="upload_file"),
    path('lg_out', views.log_out, name="lg_out"),
    path('register', views.register, name='register'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('del_file', views.del_file, name='del_file'),
    path('del_all_f', views.del_all_f, name='del_all_f'),
]
