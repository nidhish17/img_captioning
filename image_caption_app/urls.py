from django.urls import path
from . import views


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("gallery/", views.gallery, name="gallery"),
    path("upload/", views.upload_image, name="upload-image"),
    path("del/<int:img_id>", views.delete_img_frm_gallery, name="delete-image"),
]

