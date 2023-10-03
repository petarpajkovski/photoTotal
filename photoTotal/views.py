from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from . import models, forms
import json


# Create your views here.

# --------LOGIN--------
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('get_homepage')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == "POST":
        form = forms.SingUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('get_homepage')
        else:
            form = forms.SingUpForm()
            return render(request, 'register.html', {'form': form})

    form = forms.SingUpForm()
    return render(request, 'register.html', {'form': form})


# --------HOMEPAGE--------
def get_homepage(request):
    products = models.Product.objects.all()[:10]
    return render(request, 'home.html', {'products': products})


# --------USER--------
def profile(request):
    user_photos = models.Photos.objects.filter(user=request.user).all()
    context = {"photos": user_photos}
    return render(request, 'profile.html', context)


def photos_delete(request, pk):
    delete_photo = models.Photos.objects.get(id=pk)
    models.Photos.delete(delete_photo)
    return redirect('profile')


# --------BRANDS--------
def add_brand(request):
    if request.method == "POST":
        form_data = forms.BrandForm(request.POST, request.FILES)
        if form_data.is_valid():
            brand_input = form_data.save(commit=False)
            brand_input.save()
            return redirect('add_brand')
    form = forms.BrandForm
    qs = models.Brand.objects.all()
    context = {'form': form, 'brands': qs}
    return render(request, 'admin_brands.html', context)


def delete_brand(request, pk):
    delete_id = models.Brand.objects.get(id=pk)
    delete_id.delete()
    return redirect('add_brand')


# --------CAMERAS--------
def admin_camera(request):
    form = forms.ProductForm
    qs = models.Product.objects.filter(category__name='Camera')
    context = {"form": form, "cameras": qs}
    return render(request, "admin_cameras.html", context)


def add_camera(request):
    form_data = forms.ProductForm(request.POST, request.FILES)
    if form_data.is_valid():
        camera = form_data.save(commit=False)
        camera.image = form_data.cleaned_data['image']
        camera.category = models.Category.objects.get(name="Camera")
        camera.save()
        return redirect("admin_camera")
    return redirect("admin_camera")


def delete_camera(request, pk):
    delete_id = models.Product.objects.get(id=pk)
    delete_id.delete()
    return redirect('admin_camera')


def camera_page(request):
    qs = models.Product.objects.filter(category__name='Camera')
    context = {"cameras": qs}
    return render(request, "cameras.html", context)


# --------LENSES--------
def admin_lens(request):
    form = forms.ProductForm
    qs = models.Product.objects.filter(category__name="Lens")
    context = {"form": form, "lenses": qs}
    return render(request, "admin_lenses.html", context)


def add_lens(request):
    form_data = forms.ProductForm(request.POST, request.FILES)
    if form_data.is_valid():
        lens = form_data.save(commit=False)
        lens.image = form_data.cleaned_data['image']
        lens.category = models.Category.objects.get(name="Lens")
        lens.save()
        return redirect("admin_lenses")


def delete_lens(request, pk):
    lens = models.Product.objects.get(id=pk)
    lens.delete()
    return redirect('admin_lenses')


def lens_page(request):
    lenses = models.Product.objects.filter(category__name="Lens")
    context = {"lenses": lenses}
    return render(request, "lenses.html", context)


# --------ACCESSORIES--------
def admin_accessories(request):
    form = forms.ProductForm
    qs = models.Product.objects.filter(category__name="Accessories")
    context = {"form": form, "accessories": qs}
    return render(request, "admin_accessories.html", context)


def add_accessories(request):
    form_data = forms.ProductForm(request.POST, request.FILES)
    if form_data.is_valid():
        acc_input = form_data.save(commit=False)
        acc_input.image = form_data.cleaned_data["image"]
        acc_input.category = models.Category.objects.get(name="Accessories")
        acc_input.save()
        return redirect("admin_accessories")


def delete_accessories(request, pk):
    accessories = models.Product.objects.get(id=pk)
    accessories.delete()
    return redirect("admin_accessories")


def accessories_page(request):
    qs = models.Product.objects.filter(category__name="Accessories")
    context = {"items": qs}
    return render(request, "accessories.html", context)


# --------PRODUCT--------
def product_page(request, pk):
    product = models.Product.objects.get(id=pk)
    if product.category.name == 'Camera':
        rel_prods = models.Product.objects.filter(category__name='Camera').all()[:5]
    elif product.category.name == 'Lens':
        rel_prods = models.Product.objects.filter(category__name='Lens').all()[:5]
    elif product.category.name == 'Accessories':
        rel_prods = models.Product.objects.filter(category__name='Accessories').all()[:5]

    context = {'product': product, "rel_prods": rel_prods}

    return render(request, "product.html", context)


# --------CART--------
def cart(request):
    if request.user.is_authenticated:
        costumer = request.user
        order, created = models.Order.objects.get_or_create(costumer=costumer, complete=False)
        items = order.orderitem_set.all()
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        items = []
        order = {'get_cart_total': 0}

        for i in cart:
            product = models.Product.objects.get(id=i)
            order['get_cart_total'] += product.price

            item = {
                'product': {
                    'id': product.id,
                    'brand': product.brand,
                    'name': product.name,
                    'card_title': product.card_title,
                    'price': product.price,
                    'image': product.image.url
                },
            }
            items.append(item)

    context = {"items": items, "order": order}
    return render(request, 'cart.html', context)


# --------CHECKOUT--------
def checkout(request):
    if request.user.is_authenticated:
        costumer = request.user
        order, created = models.Order.objects.get_or_create(costumer=costumer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0}
    context = {"items": items, "order": order}
    return render(request, 'checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    costumer = request.user
    product = models.Product.objects.get(id=productId)
    order, created = models.Order.objects.get_or_create(costumer=costumer, complete=False)

    orderItem, created = models.OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


# --------SEARCH--------

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        products = models.Product.objects.filter(
            Q(name__contains=searched) |
            Q(brand__name__contains=searched)
        )
        return render(request, 'search.html', {'products': products})
    else:
        return render(request, 'search.html')


# --------PHOTOS--------
# :TODO Give users ability to upload photos, view and like other user's photos

def photos(request):
    context = {'photos': models.Photos.objects.all()}
    return render(request, 'photos.html', context)


def photos_form(request):
    if request.method == "POST":
        form_data = forms.PhotoForm(request.POST, request.FILES)
        if form_data.is_valid():
            photo_data = form_data.save(commit=False)
            photo_data.image = form_data.cleaned_data["image"]
            photo_data.user = request.user
            photo_data.save()
            return redirect("photos")
    return render(request, 'add_photo.html', {'form': forms.PhotoForm})
