from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order, Product
from .forms import ContactForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.forms import UserCreationForm

import uuid

def home(request):
    products = Product.objects.all()  # Fetch all products dynamically
    return render(request, 'ecommerce/home.html', {'products': products})

@login_required
def place_order(request, product_id):
    product = Product.objects.get(id=product_id)

    # Create order
    order = Order.objects.create(
        user=request.user,
        order_id=str(uuid.uuid4()).split('-')[0].upper(),
        total_amount=product.price
    )

    # Send confirmation email
    send_mail(
        subject=f"Order Confirmation - {order.order_id}",
        message=f"Hi {request.user.username},\n\n"
                f"Thank you for your order!\n"
                f"Order ID: {order.order_id}\n"
                f"Product: {product.name}\n"
                f"Total Amount: ${order.total_amount}\n\n"
                f"We will notify you once your order is shipped.",
        from_email='noreply@yourstore.com',
        recipient_list=[request.user.email],
        fail_silently=False,
    )

    messages.success(request, f"Order placed successfully! Confirmation email sent to {request.user.email}.")
    return redirect('order_success')

def order_success(request):
    return render(request, 'order_success.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            send_mail(
                subject=f"Customer Query from {name}",
                message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                from_email='noreply@yourstore.com',
                recipient_list=['admin@yourstore.com'],
                fail_silently=False,
            )

            messages.success(request, "Your message has been sent to our team!")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'ecommerce/contact.html', {'form': form})
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'ecommerce/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'ecommerce/login.html', {'form': form})