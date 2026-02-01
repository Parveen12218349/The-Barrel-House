from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Product
from django.contrib.auth.decorators import login_required
from .models import Product, Category


# ✅ Anyone can see the product dashboard
from .models import Product, Category

def dashboard(request):

    category_name = request.GET.get('category')
    products = Product.objects.all()

    if category_name and category_name != "All":
        products = products.filter(category__name=category_name)

    categories = Category.objects.all()
    return render(request, 'products/dashboard.html', {
        'products': products,
        'categories': categories
    })


# ✅ Anyone can see all products
def my_products(request):
    products = Product.objects.all()
    return render(request, 'products/my_products.html', {'products': products})

# ✅ Add/Edit/Delete restricted to logged-in users
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('my_products')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('my_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/edit_product.html', {'form': form})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('my_products')
    return render(request, 'products/confirm_delete.html', {'product': product})




def home_view(request):
    featured_products = Product.objects.filter(featured=True)[:9]  # Show only 9
    return render(request, 'index.html', {'featured_products': featured_products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/product_detail.html', {'product': product})