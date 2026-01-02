from django.shortcuts import render,get_object_or_404,redirect
from .models import Products
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request,'store/home.html')

def products(request):
    products = Products.objects.all()
    return render(request,'store/products.html',{'products':products})

def product_detail(request,id):
    product = get_object_or_404(Products,id=id)
    return render(request,'store/product_detail.html',{'product':product})

@login_required(login_url='login')
def checkout(request):
    # CHANGE FROM [] to {}
    cart = request.session.get('cart', {})  # Fix 1: Default to dictionary
    
    # Get product IDs from cart (cart is a dict: {'1': 2, '3': 1})
    product_ids = list(cart.keys())
    products = Products.objects.filter(id__in=product_ids)
    
    # Calculate total
    total = 0
    for product in products:
        quantity = cart[str(product.id)]
        total += product.price * quantity

    if request.method == "POST":
        # CHANGE FROM [] to {}
        request.session['cart'] = {}  # Fix 2: Clear cart as dictionary
        return render(request, 'store/order_success.html', {'total': total})
    
    return render(request, 'store/checkout.html', {'products': products, 'total': total})


def add_to_cart(request, id):
    # Get cart or create empty dict
    cart = request.session.get('cart', {})
    
    # Ensure cart is a dictionary (not a list)
    if not isinstance(cart, dict):
        cart = {}
    
    id = str(id)  # Convert to string
    
    # Add item to cart
    if id in cart:
        cart[id] += 1
    else:
        cart[id] = 1

    # Save back to session
    request.session['cart'] = cart
    
    return redirect('products')


def cart(request):
    # Make sure this gets a dictionary
    cart_dict = request.session.get('cart', {})  # Renamed to avoid confusion
    
    product_ids = list(cart_dict.keys())
    products_in_cart = Products.objects.filter(id__in=product_ids)
    
    cart_items = []
    total = 0

    for product in products_in_cart:
        quantity = cart_dict[str(product.id)]
        sub_total = product.price * quantity
        total += sub_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': sub_total,
        })
    
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})


def increase_qyt(request, id):
    cart = request.session.get('cart', {})
    cart[str(id)] += 1
    request.session['cart'] = cart
    return redirect('cart')

def decrease_qyt(request, id):
    cart = request.session.get('cart', {})
    if cart[str(id)] > 1:
        cart[str(id)] -= 1
    else:
        del cart[str(id)]
    request.session['cart'] = cart
    return redirect('cart')

    
def remove_from_cart(request,id):
    cart =request.session.get('cart',{})
    del cart[str(id)]
    request.session['cart']=cart
    return redirect('cart')


# Add this temporary view to reset your cart
def reset_cart(request):
    request.session['cart'] = {}  # Set cart as empty dictionary
    return redirect('home')  # Redirect to home page

def signup(request):
    if request.method =="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('products')
    else:
        form = UserCreationForm()

    return render(request,'store/signup.html',{'form':form})

def user_login(request):
    if request.method=='POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            messages.success(request,f"Welcome, {user.username} 👋")
            return redirect('products')
        
    else:
        form = AuthenticationForm()
    
    return render(request,'store/login.html',{'form':form})

def user_logout(request):
    logout(request)
    messages.info(request,f"You have successfully logged.")
    return redirect('home')

def remove_from_cart(request, id):
    cart = request.session.get('cart', {})
    del cart[str(id)]
    request.session['cart'] = cart
    return redirect('cart')
