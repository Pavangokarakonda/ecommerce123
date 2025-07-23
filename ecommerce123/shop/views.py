from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Order,Category

def home(request):
    # Get all categories for buttons
    categories = Category.objects.all()

    # Default: Show T-Shirts products only
    default_category = Category.objects.filter(name__iexact='T-Shirts').first()
    category_products = {}

    if default_category:
        products = Product.objects.filter(category=default_category)
        category_products[default_category] = products

    return render(request, 'shop/home.html', {
        'categories': categories,
        'category_products': category_products
    })

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        address = request.POST.get("address")
        Order.objects.create(user=request.user, product=product, address=address)
        messages.success(request, "Order placed successfully.")
        return redirect("my_orders")
    return render(request, 'shop/place_order.html', {'product': product})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/my_orders.html', {'orders': orders})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.status = "Cancelled"
    order.save()
    messages.success(request, "Your order has been cancelled.")
    return redirect('my_orders')

def category_products(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/home.html', {
        'categories': categories,
        'category_products': {category: products}
    })

def profile_view(request):
    # If you store mobile in a separate Profile model, fetch it like this:
    profile = None
    try:
        profile = request.user.profile
    except:
        pass  # optional: handle if profile not found

    return render(request, 'shop/profile.html', {
        'user': request.user,
        'profile': profile,
    })