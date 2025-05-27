from django.shortcuts import render,redirect,get_object_or_404

from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from .models import Product
from .models import UserProfile  

from django.contrib.auth.decorators import login_required
from .models import Product, Purchase



# Create your views here.
def index(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')


def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile  # Adjust the import based on your project structure

User = get_user_model()

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        date_of_birth = request.POST['date_of_birth']
        gender = request.POST['gender']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        errors = {}

        if User.objects.filter(username=username).exists():
            errors['username'] = "Username already exists!"

        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = "Invalid email format!"

        if password != confirm_password:
            errors['password'] = "Passwords do not match!"

        if errors:
            return render(request, 'register.html', {'errors': errors})

        # Create user
        user = User.objects.create_user(username=username, password=password, email=email, first_name=name)
        user.user_type = 'user'
        user.save()

        # Create profile
        UserProfile.objects.create(
            user=user,
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            phone_number=phone_number
        )

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')

    return render(request, 'register.html')


from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import DoctorProfile

User = get_user_model()

def register_doctor(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        specialization = request.POST['specialization']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        errors = {}

        if User.objects.filter(username=username).exists():
            errors['username'] = "Username already exists!"
        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = "Invalid email format!"
        if password != confirm_password:
            errors['password'] = "Passwords do not match!"
        if errors:
            return render(request, 'doctor_register.html', {'errors': errors})

        user = User.objects.create_user(username=username, password=password, email=email, first_name=name)
        user.user_type = 'doctor'
        user.save()

        DoctorProfile.objects.create(
            user=user,
            specialization=specialization,
            phone_number=phone_number
        )

        messages.success(request, "Doctor registration successful!")
        return redirect('login')

    return render(request, 'doctor_register.html')


from .models import PharmacistProfile

def register_pharmacist(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        pharmacy_name = request.POST['pharmacy_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        errors = {}

        if User.objects.filter(username=username).exists():
            errors['username'] = "Username already exists!"
        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = "Invalid email format!"
        if password != confirm_password:
            errors['password'] = "Passwords do not match!"
        if errors:
            return render(request, 'pharmacist_register.html', {'errors': errors})

        user = User.objects.create_user(username=username, password=password, email=email, first_name=name)
        user.user_type = 'pharmacist'
        user.save()

        PharmacistProfile.objects.create(
            user=user,
            pharmacy_name=pharmacy_name,
            phone_number=phone_number
        )

        messages.success(request, "Pharmacist registration successful!")
        return redirect('login')

    return render(request, 'pharmacist_register.html')

def register_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        errors = {}

        if User.objects.filter(username=username).exists():
            errors['username'] = "Username already exists!"
        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = "Invalid email format!"
        if password != confirm_password:
            errors['password'] = "Passwords do not match!"
        if errors:
            return render(request, 'admin_register.html', {'errors': errors})

        user = User.objects.create_user(username=username, password=password, email=email, first_name=name)
        user.user_type = 'admin'
        user.is_staff = True
        user.is_superuser = True  # Only if needed
        user.save()

        messages.success(request, "Admin registered successfully!")
        return redirect('login')

    return render(request, 'admin_register.html')


@login_required
def doctor_dashboard(request):
    if request.user.user_type != 'doctor':
        return render(request, 'unauthorized.html')  # Optional: show if non-doctor tries to access

    # Fetch doctor profile or any other data here if needed
    doctor_profile = request.user.doctorprofile  # if OneToOneField exists

    return render(request, 'doctor_dashboard.html', {'doctor': doctor_profile})







from django.contrib.auth import authenticate, login
from django.contrib import messages


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")

            # Redirect to 'next' if present, else to home
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect("home")  # Replace with your homepage URL name
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')



@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop-single.html', {'product': product})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product  # adjust as needed

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'product_id': product.id,
            'name': product.name,
            'price': float(product.price),
            'image': product.image.url,
            'quantity': 1
        }

    request.session['cart'] = cart
    return redirect('cart')

@login_required
def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for item_id, item in cart.items():
        subtotal = item['price'] * item['quantity']
        total += subtotal
        cart_items.append({
            'product': item,
            'quantity': item['quantity'],
            'subtotal': subtotal,
            'id': item_id,
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'subtotal': total  # you can split subtotal and tax if needed
    })



from django.shortcuts import redirect

@login_required
def remove_cart_item(request, item_index):
    cart = request.session.get('cart', [])
    if 0 <= item_index < len(cart):
        del cart[item_index]
        request.session['cart'] = cart
    return redirect('cart')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'checkout.html', {'total': total})


@login_required
def purchase_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        Purchase.objects.create(user=request.user, product=product)
        messages.success(request, f"You have successfully purchased {product.name}!")
        return redirect('purchase_confirmation', product_id=product.id)
    return redirect('product_detail', product_id=product.id)

def purchase_confirmation(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        # Simulate payment processing here if needed
        return redirect('payment_success')

    return render(request, 'purchase_confirmation.html', {'product': product})

def payment_success_view(request):
    # Simulated total amount (or you can retrieve it from session/db)
    total_price = 1250

    return render(request, 'payment_success.html', {'total_price': total_price})


from django.shortcuts import render, get_object_or_404
from .models import DoctorProfile

def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    return render(request, 'doctor_detail.html', {'doctor': doctor})


from django.shortcuts import render, redirect
from .forms import PrescriptionUploadForm

def upload_prescription(request):
    if request.method == 'POST':
        form = PrescriptionUploadForm(request.POST, request.FILES)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.patient = request.user
            prescription.save()
            # Optionally, send notification to doctor
            return redirect('prescription_list')  # Replace with your desired redirect
    else:
        form = PrescriptionUploadForm()
    return render(request, 'upload_prescription.html', {'form': form})
