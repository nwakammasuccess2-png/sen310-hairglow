from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, Appointment, Order, OrderItem
import datetime
from django.utils import timezone

# Helper function to load shopping cart items and compute pricing
def get_cart_data(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, item in list(cart.items()):
        try:
            product = Product.objects.get(id=int(product_id))
            quantity = int(item.get('quantity', 1))
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
        except (Product.DoesNotExist, ValueError):
            if product_id in cart:
                del cart[product_id]
                request.session['cart'] = cart
                request.session.modified = True
    return cart_items, total

def home(request):
    featured_products = Product.objects.filter(is_available=True)[:3]
    return render(request, 'home.html', {'featured_products': featured_products})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to HairGlow, {user.username}! Registration successful.")
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out. See you soon!")
    return redirect('home')

@login_required
def book_appointment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date_str = request.POST.get('date')
        time_slot = request.POST.get('time_slot')
        service_type = request.POST.get('service_type', 'Hair Consultation')
        notes = request.POST.get('notes', '')
        
        if not (name and email and phone and date_str and time_slot):
            messages.error(request, "Please fill in all required fields.")
            return redirect('book_appointment')
            
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('book_appointment')
            
        if date < datetime.date.today():
            messages.error(request, "You cannot book an appointment in the past.")
            return redirect('book_appointment')
            
        # Check double booking
        existing_booking = Appointment.objects.filter(date=date, time_slot=time_slot).exclude(status='Cancelled').exists()
        if existing_booking:
            messages.error(request, f"The time slot '{time_slot}' on {date_str} is already booked. Please choose another slot.")
            return redirect('book_appointment')
            
        # Save appointment
        Appointment.objects.create(
            user=request.user,
            name=name,
            email=email,
            phone=phone,
            date=date,
            time_slot=time_slot,
            service_type=service_type,
            notes=notes,
            status='Pending'
        )
        messages.success(request, f"Appointment successfully booked for {date_str} at {time_slot}!")
        return redirect('dashboard')
        
    context = {
        'time_slots': Appointment.TIME_SLOT_CHOICES,
        'min_date': datetime.date.today().strftime('%Y-%m-%d')
    }
    return render(request, 'booking.html', context)

# API endpoint to check booked slots for a specific date
def check_availability(request):
    date_str = request.GET.get('date', '')
    if not date_str:
        return JsonResponse({'error': 'Date parameter is required'}, status=400)
    try:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        booked_slots = list(Appointment.objects.filter(date=date).exclude(status='Cancelled').values_list('time_slot', flat=True))
        return JsonResponse({'booked_slots': booked_slots})
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

def product_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(is_available=True)
    if query:
        products = products.filter(name__icontains=query) | products.filter(description__icontains=query)
    return render(request, 'products.html', {'products': products, 'query': query})

def cart_detail(request):
    cart_items, total = get_cart_data(request)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    
    qty = int(request.POST.get('quantity', 1))
    if qty <= 0:
        qty = 1
        
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] = cart[str(product_id)]['quantity'] + qty
    else:
        cart[str(product_id)] = {
            'quantity': qty,
            'price': str(product.price)
        }
        
    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, f"Added {product.name} to your cart.")
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        product = Product.objects.filter(id=product_id).first()
        name = product.name if product else "Product"
        del cart[str(product_id)]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f"Removed {name} from your cart.")
    return redirect('cart_detail')

def cart_update(request, product_id):
    cart = request.session.get('cart', {})
    try:
        qty = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        qty = 1
        
    if qty <= 0:
        return cart_remove(request, product_id)
        
    product = get_object_or_404(Product, id=product_id)
    if qty > product.stock:
        qty = product.stock
        messages.warning(request, f"Only {product.stock} items of {product.name} are available in stock.")
        
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] = qty
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f"Updated quantity for {product.name}.")
    return redirect('cart_detail')

@login_required
def checkout(request):
    cart_items, total = get_cart_data(request)
    if not cart_items:
        messages.warning(request, "Your cart is empty. Please add some products before checking out.")
        return redirect('product_list')
        
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        
        if not (first_name and last_name and email and phone and address and city and postal_code):
            messages.error(request, "Please fill in all checkout fields.")
            return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})
            
        # Verify stock and availability
        for item in cart_items:
            product = item['product']
            qty = item['quantity']
            if product.stock < qty:
                messages.error(request, f"Sorry, {product.name} only has {product.stock} items left in stock.")
                return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})
                
        # Create order
        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            postal_code=postal_code,
            total_price=total,
            paid=False,
            status='Pending'
        )
        
        # Create order items and decrement stock
        for item in cart_items:
            product = item['product']
            qty = item['quantity']
            OrderItem.objects.create(
                order=order,
                product=product,
                price=product.price,
                quantity=qty
            )
            product.stock -= qty
            if product.stock <= 0:
                product.is_available = False
            product.save()
            
        # Clear cart
        request.session['cart'] = {}
        request.session.modified = True
        
        messages.success(request, "Order successfully placed! Thank you for shopping with HairGlow.")
        return redirect('order_success', order_id=order.id)
        
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_success.html', {'order': order})

@login_required
def dashboard(request):
    appointments = Appointment.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'appointments': appointments, 'orders': orders})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    if appointment.status == 'Pending':
        appointment.status = 'Cancelled'
        appointment.save()
        messages.success(request, "Your appointment has been successfully cancelled.")
    else:
        messages.error(request, "This appointment cannot be cancelled because it is already confirmed or cancelled.")
    return redirect('dashboard')