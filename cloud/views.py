import mimetypes
import os
from wsgiref.util import FileWrapper

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ImageFileUploadForm
from .models import Item, File
from django.conf import settings

# Create your views here.
def index(request):
    form = ImageFileUploadForm()
    return render(request, "index.html", {"number": str(len(Item.objects.all())), "form": form})


def register(request):
    username = str(request.POST['name'])
    for n in User.objects.all():
        if username == n.username:
            return JsonResponse({"status": "name"})
    User.objects.create_user(username=username, email=str(request.POST['email']),
                             password=str(request.POST['password']))
    return JsonResponse({"status": "ok"})


def sign_in(request):
    username = request.POST['name']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"status": "ok"})

    return JsonResponse({"status": "error"})


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')
    else:
        return redirect('index')


def upload_file(request):
    form = ImageFileUploadForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return JsonResponse({'id': File.objects.last().id})


def search(request):
    if request.user.is_authenticated:
        name = request.GET['name']
        itm = Item.objects.all()
        l = []
        for a in itm:
            if name in a.name:
                l.append(a)
        return render(request, "search.html", {"items": l, "title": item})
    else:
        return redirect("index")

def item(request):
    i = request.GET['item']
    itm = get_object_or_404(Item, name=i)
    return render(request, "item.html", {"item": itm})


def download_file(request):
    file_name = str(request.GET['file'])

    file_path = os.path.join(settings.MEDIA_ROOT,file_name)
    file_wrapper = FileWrapper(open(file_path, 'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype)
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    #file_name = file_name.split("/")[3]
    response['Content-Disposition'] = 'attachment; filename=' + file_name
    return response


def upload(request):
    it = Item(name=request.POST['name'], author=request.user, description=request.POST['popisek'])
    it.save()

    files = request.POST['files']
    f = files.split(",")
    for i in f:
        it.files.add(File.objects.get(id=i))

    return JsonResponse({"status": "ok"})

def del_file(request):
    File.objects.get(id=int(request.POST['id'])).delete()
    return JsonResponse({"status":True})

def del_all_f(request):
    ids = request.POST['ids']
    ids = ids.split(",")
    for a in ids:
        File.objects.get(id=int(a)).delete()
    return JsonResponse({"status":True})