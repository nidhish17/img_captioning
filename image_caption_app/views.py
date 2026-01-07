from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .models import CaptionedImage, Tag
# import ml function -> defined inside the app! (ml_utils.py file)
from .ml_utils import generate_caption, extract_tags

import re

# Create your views here.
def homepage(request):

    context = {}

    return render(request, "img_caption/home.html", context=context)

@login_required(login_url="signin")
def gallery(request):
    search_keyword = request.GET.get("keyword")

    if not search_keyword:
        captioned_images = CaptionedImage.objects.filter(user=request.user)
    else:
        escaped = re.escape(search_keyword)
        pattern = rf"\b{escaped}\b".strip()
        captioned_images = CaptionedImage.objects.filter(Q(caption__iregex=pattern) | Q(tags__name__iregex=pattern), user=request.user).distinct().order_by("uploaded_at")
    paginator = Paginator(captioned_images, 9)
    page = request.GET.get("page", 1)
    paged_image_gallery = paginator.get_page(page)
    context = {"images": paged_image_gallery, "found_images_len": captioned_images.count(), "search_keyword": search_keyword, "current_page": int(page)}
    return render(request, "img_caption/gallery.html", context=context)


@login_required
def delete_img_frm_gallery(request, img_id):
    try:
        image_to_del = get_object_or_404(CaptionedImage, id=img_id)
        img_caption = image_to_del.caption[:50]
        image_to_del.delete()
        messages.success(request, f"successfully deleted: '{img_caption}...'")
    except CaptionedImage.DoesNotExist:
        messages.error(request, "Failed to delete image")

    return redirect("gallery")



@login_required(login_url="signin")
def upload_image(request):
    if request.method == "POST":
        files = request.FILES.getlist("images")

        if files:
            # generate captions and tags
            for img_file in files:
                captioned_image = CaptionedImage.objects.create(image=img_file, user=request.user)
                # generate caption for the uploaded image by user
                caption = generate_caption(img_file)
                print(caption, " :caption")
                captioned_image.caption = caption
                tags = extract_tags(caption)
                for tag_name in tags:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    captioned_image.tags.add(tag)

                captioned_image.save()

            messages.success(request, "Successfully processed images")
            return redirect("gallery")

    context = {}

    return render(request, "img_caption/upload.html", context=context)






