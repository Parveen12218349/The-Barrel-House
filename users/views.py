from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from datetime import date

from products.models import Product
from users.forms import RegisterForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            dob = form.cleaned_data.get('date_of_birth')
            if dob is None:
                messages.error(request, "Date of birth is required.")
                return render(request, 'users/register.html', {'form': form})

            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 21:
                messages.error(request, "You must be at least 21 years old to register.")
                return render(request, 'users/register.html', {'form': form})

            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("🔍 Username entered:", username)
        print("🔍 Password entered:", password)

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            print("✅ Logged in user:", user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('product_dashboard')  # 👈 safer redirect
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'users/login.html')

    return render(request, 'users/login.html')





def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def buyer_dashboard(request):
    products = Product.objects.all()  # or filter based on some buyer preferences
    return render(request, 'users/dashboard.html',{
        'users': request.user,
        'products': products
})




