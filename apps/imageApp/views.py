from django.shortcuts import render, HttpResponse, redirect
from .forms import ImageUploadForm
from .models import Product, Review
from ..bestLogin.models import User
from .helpercsv import CSVSTUFF, deleteAllProducts
import bcrypt

def main(request):
    CSVSTUFF()
    #deleteAllProducts()
    return render(request, "imageApp/main_page.html")


def index(request):
    #return redirect('spring:showUser')
    CSVSTUFF()
    if request.method == 'POST':
        if deleteAllProducts():
            print "CSV AND DATABASE GONE!"
    form = ImageUploadForm()
    return render(request, "imageApp/index.html", {'form':form, 'stuff':Product.objects.all()})

def uploadImage(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        selected_user = User.userManager.get(id=request.session['currentUser'])
        if form.is_valid():
            selected_user.model_pic = form.cleaned_data['image']
            selected_user.save()
            return redirect('spring:showImage')
        else:
            print form.errors
    return redirect('spring:index')


def all_show(request):
    context = {
        'yall':Product.objects.all(),
        'currUser':User.userManager.get(id=request.session['currentUser']),
    }
    return render(request, "imageApp/all_show.html", context)

def see_product(request, id):
    context = {
        'currentProduct':Product.objects.get(id=id),
    }

    return render(request, "imageApp/see_product.html", context)

def cart():
    context = {
        'currUser':User.userManager.get(id=request.session['currentUser']),
        'cartItems':Product.objects.all(),
    }
    return render(request, "imageApp/cart.html", context)


def showUser(request):
    form = ImageUploadForm(request.POST, request.FILES)
    selected_user = User.userManager.get(id=request.session['currentUser'])
    if form.is_valid():
        selected_user.model_pic = form.cleaned_data['image']
        selected_user.save()
        return redirect('spring:showImage')
    else:
        print form.errors
    context = {
    'form':form,
    'userStuff':selected_user,
    }
    return render(request, "imageApp/userPage.html", context)


def changeUserDetails(request):
    user = User.userManager.get(id=request.session['currentUser'])
    if request.POST['changePassword'] == request.POST['changePasswordConfirm']:
        print "LOOKSEGEDSFSDF"
        hashed = bcrypt.hashpw(request.POST['changePassword'].encode(), bcrypt.gensalt())
        user.password = hashed
        user.save()
    return redirect('spring:showImage')

def changeUserIcon(request):
    form = ImageUploadForm(request.POST, request.FILES)
    selected_user = User.userManager.get(id=request.session['currentUser'])
    if form.is_valid():
        selected_user.model_pic = form.cleaned_data['image']
        selected_user.save()
    return redirect('spring:showImage')


def allImages(request):
    context = {
        'yall':Product.objects.all(),
        'currentUserImages':User.userManager.filter(id=request.session['currentUser']),
    }
    return render(request, "imageApp/index2.html", context)
