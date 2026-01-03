from django.shortcuts import render, get_object_or_404, redirect
from .models import Products, Cart, CartItem, Order, OrderItem
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


# Home page
def home(request):
    return render(request,'store/home.html')

# Products list page
def products(request):
    products = Products.objects.all()
    return render(request,'store/products.html',{'products':products})

# Product detail page
def product_detail(request, id):
    product = get_object_or_404(Products, id=id)
    return render(request,'store/product_detail.html',{'product':product})

@login_required(login_url='login')
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    product_ids = list(cart.keys())
    products = Products.objects.filter(id__in=product_ids)

    total = 0
    for product in products:
        quantity = cart[str(product.id)]
        total += product.price * quantity

    if request.method == "POST":
        # 1️⃣ Create Order
        order = Order.objects.create(
            user=request.user,
            total_price=total
        )

        # 2️⃣ Build order items + HTML rows
        table_rows = ""

        for product in products:
            quantity = cart[str(product.id)]
            subtotal = product.price * quantity

            OrderItem.objects.create(
                order=order,
                product_name=product.name,
                price=product.price,
                quantity=quantity
            )

            table_rows += f"""
                <tr>
                    <td>{product.name}</td>
                    <td>{quantity}</td>
                    <td>R{product.price}</td>
                    <td>R{subtotal}</td>
                </tr>
            """

        # 3️⃣ HTML Email Content
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Thank you for your order, {request.user.first_name} 👋</h2>

            <p>Your order has been successfully placed.</p>

            <h3>Order ID: #{order.id}</h3>

            <table border="1" cellpadding="10" cellspacing="0" width="100%">
                <thead>
                    <tr style="background-color:#f2f2f2;">
                        <th>Product</th>
                        <th>Quantity</th>
                        <th>Price</th>
                        <th>Subtotal</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>

            <h3>Total Amount: R{total}</h3>

            <p>We’ll notify you once your items are shipped.</p>

            <p><strong>Kativation E-Commerce</strong></p>
        </body>
        </html>
        """

        # 4️⃣ Send HTML Email
        email = EmailMultiAlternatives(
            subject=f"Order Confirmation #{order.id}",
            body="Your order has been placed successfully.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[request.user.email],
        )

        email.attach_alternative(html_content, "text/html")
        email.send()

        # 5️⃣ Clear cart
        request.session['cart'] = {}

        return render(request, 'store/order_success.html', {
            'total': total,
            'order': order
        })

    return render(request, 'store/checkout.html', {
        'products': products,
        'total': total
    })


# Add product to cart
def add_to_cart(request, id):
    cart = request.session.get('cart', {})
    id = str(id)
    if id in cart:
        cart[id] += 1
    else:
        cart[id] = 1
    request.session['cart'] = cart
    return redirect('products')

# Cart page
def cart(request):
    cart_dict = request.session.get('cart', {})
    product_ids = list(cart_dict.keys())
    products_in_cart = Products.objects.filter(id__in=product_ids)

    cart_items = []
    total = 0
    for product in products_in_cart:
        quantity = cart_dict[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

# Increase quantity
def increase_qyt(request, id):
    cart = request.session.get('cart', {})
    cart[str(id)] += 1
    request.session['cart'] = cart
    return redirect('cart')

# Decrease quantity
def decrease_qyt(request, id):
    cart = request.session.get('cart', {})
    if cart[str(id)] > 1:
        cart[str(id)] -= 1
    else:
        del cart[str(id)]
    request.session['cart'] = cart
    return redirect('cart')

# Remove item from cart
def remove_from_cart(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        del cart[str(id)]
    request.session['cart'] = cart
    return redirect('cart')

# Reset cart
def reset_cart(request):
    request.session['cart'] = {}
    return redirect('home')

# Signup
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(
                request,
                f"Welcome {user.first_name}! Your account is ready 🎉"
            )
            return redirect('products')
    else:
        form = CustomUserCreationForm()
    return render(request,'store/signup.html',{'form':form})

# Login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request,f"Welcome, {user.username} 👋")
            return redirect('products')
    else:
        form = AuthenticationForm()
    return render(request,'store/login.html',{'form':form})

# Logout
def user_logout(request):
    logout(request)
    messages.info(request,f"You have successfully logged out.")
    return redirect('home')

# Get or create a cart for a user
def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

