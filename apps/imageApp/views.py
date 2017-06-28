from django.shortcuts import render, HttpResponse, redirect
from .forms import ImageUploadForm
from .models import Product, Review
from ..bestLogin.models import User
from .helpercsv import CSVSTUFF, deleteAllProducts
import bcrypt
from django.db.models import Count

def main(request):
    CSVSTUFF()
    #deleteAllProducts()
    #countlikes = Secret.sManager.annotate(num_likes=Count('user_likes')).order_by('-num_likes')[:5]

    if request.session['currentUser'] != None:
        context = {
            'currUser': User.userManager.get(id=request.session['currentUser']),
            'topLiked': Product.pManager.annotate(num_likes=Count('likes')).all()[:1],
            'mostLiked': Product.pManager.annotate(num_likes=Count('likes')).all()[1:5],
        }
    else:
        context = {
            'currUser': None,
            'topLiked': Product.pManager.annotate(num_likes=Count('likes')).all()[:1],
            'mostLiked': Product.pManager.annotate(num_likes=Count('likes')).all()[1:5],
        }
    return render(request, "imageApp/main_page.html", context)


def index(request):
    #return redirect('spring:showUser')
    CSVSTUFF()
    if request.method == 'POST':
        if deleteAllProducts():
            print "CSV AND DATABASE GONE!"
    form = ImageUploadForm()
    return render(request, "imageApp/index.html", {'form':form, 'stuff':Product.pManager.all()})

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
    # Show all products page even if user is not in session
    if request.session['currentUser']:
        context = {
            'yall':Product.pManager.all(),
            'currUser':User.userManager.get(id=request.session['currentUser']),
            'numLikes':Product.pManager.annotate(num_likes=Count('likes')),
        }
    else:
        context={
            'yall': Product.pManager.all(),
            'numLikes':Product.pManager.annotate(num_likes=Count('likes')),
        }
    return render(request, "imageApp/all_show.html", context)

def see_product(request, id):
    context = {
        'currentProduct':Product.pManager.get(id=id),
    }
    if request.session['currentUser']:
        context = {
            'currentProduct':Product.objects.get(id=id),
            'currentUser':User.userManager.get(id=request.session['currentUser']),
        }
    else:
        context={
            'currentProduct': Product.objects.get(id=id),
        }
    return render(request, "imageApp/see_product.html", context)

def cart(request, id):
    context = {
        'currUser':User.userManager.get(id=request.session['currentUser']),
        'cartItems':Product.pManager.all(),
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

def likeProduct(request, id):
    if request.method == "POST":
        result = Product.pManager.addNewLike(id, request.session['currentUser'])
    return redirect('spring:all_show');
def add_comment(request, id):
    return redirect('spring:see_product', id)
