from django.shortcuts import render,redirect,get_object_or_404

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from .models import Product
from .models import UserProfile  

from django.contrib.auth.decorators import login_required
from .models import Product, Purchase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile 
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import DoctorProfile

User = get_user_model()

# Create your views here.
def index(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')


def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

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
        return redirect('user_login')

    return render(request, 'register.html')


def register_doctor(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        specialization = request.POST['specialization']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        image = request.FILES.get('image')  # <-- Get uploaded image

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
            phone_number=phone_number,
            image=image
        )

        messages.success(request, "Doctor registration successful!")
        return redirect('doctor_login')

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
        return redirect('pharmacist_login')

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

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


from .models import DoctorProfile, PharmacistProfile  # import your models

# User login
def user_login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            # Ensure not a doctor or pharmacist
            if not DoctorProfile.objects.filter(user=user).exists() and not PharmacistProfile.objects.filter(user=user).exists():
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "You are not authorized to login as User.")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'login.html')


# Doctor login
def doctor_login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            if DoctorProfile.objects.filter(user=user).exists():
                login(request, user)
                return redirect("doctor_dashboard")
            else:
                messages.error(request, "You are not authorized to login as Doctor.")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'login_doctor.html')


# Pharmacist login
def pharmacist_login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            if PharmacistProfile.objects.filter(user=user).exists():
                login(request, user)
                return redirect("pharmacist_dashboard")
            else:
                messages.error(request, "You are not authorized to login as Pharmacist.")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'login_pharmacist.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('user_login')



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
from django.contrib.auth.decorators import login_required
from .forms import PrescriptionForm

@login_required
def upload_prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.patient = request.user
            prescription.save()
            return redirect('prescription_success')  # Replace with your success URL
    else:
        form = PrescriptionForm()
    return render(request, 'upload_prescription.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Prescription
# views.py
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Prescription
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Prescription

@login_required
def view_prescriptions(request):
    if request.user.user_type == 'doctor':
        prescriptions = Prescription.objects.filter(doctor=request.user)

        if request.method == 'POST':
            prescription_id = request.POST.get('prescription_id')
            action = request.POST.get('action')
            prescription = get_object_or_404(Prescription, id=prescription_id, doctor=request.user)

            if action == 'approve':
                prescription.status = 'approved'
            elif action == 'reject':
                prescription.status = 'rejected'
            elif action == 'send_to_pharmacist':
                if prescription.status == 'approved' and not prescription.sent_to_pharmacist:
                    prescription.sent_to_pharmacist = True
                    # Implement notification logic here (e.g., send email or create a notification entry)
            prescription.save()

            return redirect('view_prescriptions')

        return render(request, 'view_prescriptions.html', {'prescriptions': prescriptions})
    else:
        return redirect('unauthorized')



@login_required
def patient_prescriptions(request):
    if request.user.user_type == 'patient':
        prescriptions = Prescription.objects.filter(patient=request.user)
        return render(request, 'patient_prescriptions.html', {'prescriptions': prescriptions})
    else:
        return redirect('unauthorized')


def prescription_success(request):
    return render(request, 'prescription_success.html')




def all_doctors(request):
    doctors = DoctorProfile.objects.all()
    return render(request, 'all_doctors.html', {'doctors': doctors})


@login_required
def prescription_status(request):
    if request.user.user_type == 'patient':
        # ✅ Fetch all prescriptions this user submitted
        prescriptions = Prescription.objects.filter(patient=request.user).order_by('-uploaded_at')
        return render(request, 'prescription_status.html', {'prescriptions': prescriptions})
    else:
        return redirect('home')
    

@login_required
def my_prescriptions(request):
    prescriptions = Prescription.objects.filter(patient=request.user).order_by('-uploaded_at')
    return render(request, 'my_prescriptions.html', {'prescriptions': prescriptions})


@login_required
def pharmacist_dashboard(request):
    if request.user.user_type == 'pharmacist':
        prescriptions = Prescription.objects.filter(status='approved', sent_to_pharmacist=True)
        return render(request, 'pharmacist_dashboard.html', {'prescriptions': prescriptions})
    else:
        return redirect('unauthorized')
