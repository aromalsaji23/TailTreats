from random import shuffle, random
from .forms import ProductRequestForm
from dateutil import parser
from django.db.models import Q
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from .models import *
from datetime import date
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from .models import Category, Product, Profile, Cart
from django.contrib import messages
from django.contrib import messages
from .models import Product
from .forms import PetProfileForm
# Create your views here.

def Home(request):
    search = request.GET.get('search', 0)
    print(search,1112332)
    search_pro = None

    if search == "":
        pass
    elif search==0:
        pass
    else:
        search_pro = Product.objects.filter(Q(name__icontains=search) | Q(category__name__icontains=search))
    cat = ""
    pro = ""
    cat = ""
    num = 0
    num1 = 0
    cat = Category.objects.all()
    pro = Product.objects.all()
    num = []
    num1 = 0
    product = None
    try:
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user=user)
        cart = Cart.objects.filter(profile=profile)
        product = recommended_product(request)
        for i in cart:
            num1 += 1

    except:
        pass
    a = 1
    li = []

    for j in pro:
        b = 1
        for i in cat:
            if i.name == j.category.name:
                if not j.category.name in li:
                    li.append(j.category.name)
                    if b == 1:
                        num.append(a)
                        b = 2
        a += 1

    d = {'pro': pro, 'cat': cat, 'num': num, 'num1': num1, 'product': product, 'search_pro': search_pro}
    return render(request, 'all_product.html', d)


def About(request):
    return render(request, 'about.html')


def Contact(request):
    return render(request, 'contact.html')


def Signup(request):
    error = False
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        p = request.POST['pwd']
        d = request.POST['date']
        c = request.POST['city']
        ad = request.POST['add']
        e = request.POST['email']
        i = request.FILES['img']
        con = request.POST['contact']
        user = User.objects.create_user(username=u, email=e, password=p, first_name=f, last_name=l)
        Profile.objects.create(user=user, dob=d, city=c, address=ad, contact=con, image=i)
        error = True
    d = {'error': error}
    return render(request, 'signup.html', d)


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def Login(request):
    error = ""
    if request.method == "POST":
        u = request.POST.get('uname')
        p = request.POST.get('pwd')
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)
            # Redirect the user to the view product page
            return redirect('view_product', pid=0)
        else:
            error = "Invalid username or password"
    d = {'error': error}
    return render(request, 'login.html', d)



def Admin_Login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "yes"
            else:
                error = "not"
        except:
            error = "not"
    d = {'error': error}
    return render(request, 'loginadmin.html', d)


def Logout(request):
    logout(request)
    return redirect('home')


def View_user(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    pro = Profile.objects.all()
    d = {'user': pro}
    return render(request, 'view_user.html', d)


def Add_Product(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    
    cat = Category.objects.all()
    error = False
    
    if request.method == "POST":
        c = request.POST['cat']
        p = request.POST['pname']
        pr = request.POST['price']
        i = request.FILES['img']
        d = request.POST['desc']
        s = request.POST['stock']  # New line to retrieve stock quantity
        ct = Category.objects.get(name=c)
        Product.objects.create(category=ct, name=p, price=pr, image=i, desc=d, stock=s)  # Include stock in Product creation
        error = True
    
    d = {'cat': cat, 'error': error}
    return render(request, 'add_product.html', d)


def All_product(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    cart = Cart.objects.filter(profile=profile)
    num1 = 0
    for i in cart:
        num1 += 1
    cat = Category.objects.all()
    pro = Product.objects.all()
    d = {'pro': pro, 'cat': cat, 'num1': num1}
    return render(request, 'all_product.html', d)


def Admin_View_Booking(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    book = Booking.objects.all()
    d = {'book': book}
    return render(request, 'admin_viewBokking.html', d)


def View_feedback(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    feed = Send_Feedback.objects.all()
    d = {'feed': feed}
    return render(request, 'view_feedback.html', d)



def View_prodcut(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    
    cat = ""
    cat1 = ""
    pro1 = ""
    num1 = 0
    user = ""
    profile = ""
    cart = ""
    pro = ""
    num = ""
    
    if not request.user.is_staff:
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user=user)
        cart = Cart.objects.filter(profile=profile)
        for i in cart:
            num1 += 1

    if pid == 0:
        cat = "All Product"
        pro1 = Product.objects.all()
    else:
        try:
            cat1 = Category.objects.get(id=pid)
            pro1 = Product.objects.filter(category=cat1).all()
        except Category.DoesNotExist:
            cat1 = None  # Assign None if category doesn't exist
            pro1 = None  # Assign None for products
    
    # Search functionality
    search_query = request.GET.get('q', '')
    if search_query:
        pro1 = pro1.filter(Q(name__icontains=search_query) | Q(price__icontains=search_query))

    cat = Category.objects.all()
    pro = Product.objects.all()
    num = []
    b = 1
    for j in cat:
        a = 1
        for i in pro:
            if j.name == i.category.name:
                if a == 1:
                    num.append(i.id)
                    a = 2
    
    prod = recommended_product(request)
    d = {'pro': pro, 'cat': cat, 'cat1': cat1, 'num': num, 'pro1': pro1, 'num1': num1, 'prod': prod}
    return render(request, 'view_product.html', d)

def Add_Categary(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    error = False
    if request.method == "POST":
        n = request.POST['cat']
        Category.objects.create(name=n)
        error = True
    d = {'error': error}
    return render(request, 'add_category.html', d)


def View_Categary(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    pro = Category.objects.all()
    d = {'pro': pro}
    return render(request, 'view_category.html', d)


def View_Booking(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    cart = Cart.objects.filter(profile=profile)
    book = Booking.objects.filter(profile=profile)
    pro = recommended_product(request)
    num1 = 0
    for i in cart:
        num1 += 1
    d = {'book': book, 'num1': num1, 'pro': pro}
    return render(request, 'view_booking.html', d)


def Feedback(request, pid=None):
    if not request.user.is_authenticated:
        return redirect('login')

    error = False
    user1 = request.user
    profile = Profile.objects.get(user=user1)
    cart = Cart.objects.filter(profile=profile)
    num1 = cart.count()

    date1 = date.today()

    # Handle missing or invalid pid
    user = get_object_or_404(User, id=pid) if pid else request.user
    pro = Profile.objects.filter(user=user).first()

    if request.method == "POST":
        d = request.POST.get('date')
        u = request.POST.get('uname')
        e = request.POST.get('email')
        con = request.POST.get('contact')
        m = request.POST.get('desc')

        user = User.objects.filter(username=u, email=e).first()
        pro = Profile.objects.filter(user=user, contact=con).first()

        if pro:  # Ensure profile exists before saving
            Send_Feedback.objects.create(profile=pro, date=d, message1=m)
            error = True

    context = {'pro': pro, 'date1': date1, 'num1': num1, 'error': error}
    return render(request, 'feedback.html', context)


def Change_Password(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = ""
    num1 = 0
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    cart = Cart.objects.filter(profile=profile)
    for i in cart:
        num1 += 1
    if request.method == "POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error = "yes"
        else:
            error = "not"
    d = {'error': error, 'num1': num1}
    return render(request, 'change_password.html', d)

from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Cart, Profile


def Add_Cart(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        # Retrieve the product and profile instances
        user = request.user
        profile = Profile.objects.get(user=user)
        product = get_object_or_404(Product, id=pid)

        # Ensure the product has enough stock
        if product.stock > 0:
            # Decrement the stock by 1
            product.stock -= 1
            product.save()

            # Add the product to the cart
            Cart.objects.create(profile=profile, product=product)
            return redirect('cart')
        else:
            # Handle out of stock scenario
            # For example, you can redirect with a message
            return redirect('view_product', pid=pid)

    # Handle GET request or other scenarios
    # Redirect to the product view page
    return redirect('view_product', pid=pid)



def recommended_product(request):
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    book = Booking.objects.filter(profile=profile).order_by('-id')[:2]
    recommend = []
    for i in book:
        recommend += i.booking_id.split('.')[1:]
    pro1 = Product.objects.filter(id__in=recommend)
    cat = []
    for i in pro1:
        if not i.category.id in cat:
            cat.append(i.category.id)
    pro = Product.objects.filter(category__id__in=cat).order_by('?')
    return pro

from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Cart, Profile

def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = User.objects.get(id=request.user.id)
    
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        # Handle the case where the Profile object doesn't exist
        # You can create the Profile object here if needed
        profile = None
    
    if profile:
        cart = Cart.objects.filter(profile=profile).all()
        total = 0
        num1 = 0
        book_id = request.user.username
        message1 = "Here ! No Any Product"
        for i in cart:
            total += i.product.price
            num1 += 1
            book_id = book_id + "." + str(i.product.id)
        d = {'profile': profile, 'cart': cart, 'total': total, 'num1': num1, 'book': book_id, 'message': message1}
        return render(request, 'cart.html', d)
    else:
        # Handle the case where the Profile object doesn't exist
        # Redirect or show an error message to the user
        pass



def remove_cart(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        cart = Cart.objects.get(id=pid)
        product = cart.product
        
        # Increment the stock count by 1
        product.stock += 1
        product.save()
        
        # Delete the item from the cart
        cart.delete()
        
        return redirect('cart')
    
    except Cart.DoesNotExist:
        # Handle the case where the cart item doesn't exist
        return HttpResponseNotFound("Cart item not found")


def Booking_order(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')
    
    data1 = User.objects.get(id=request.user.id)
    data = Profile.objects.filter(user=data1).first()
    cart = Cart.objects.filter(profile=data).all()
    
    total = sum(i.product.price for i in cart)  # Optimized total calculation
    num1 = len(cart)  # Count the number of items in the cart
    
    user1 = data1.username
    li = pid.split('.')
    li2 = [int(j) for j in li if user1 != j]
    
    date1 = date.today()
    
    if request.method == "POST":
        d = request.POST.get('date1', '')
        c = request.POST.get('name', '')
        c1 = request.POST.get('city', '')
        e = request.POST.get('email', '')
        con = request.POST.get('contact', '')  # ✅ This remains unchanged
        b = request.POST.get('book_id', '')
        t = request.POST.get('total', '')

        user = User.objects.get(username=c)
        profile = Profile.objects.get(user=user)

        status = Status.objects.get(name="pending")

        book1 = Booking.objects.create(
            profile=profile,
            book_date=date1,
            booking_id=b,
            total=t,
            quantity=num1,
            status=status
        )

        Cart.objects.filter(profile=profile).delete()

        return redirect('payment', book1.total)
    
    context = {
        'data': data,
        'data1': data1,
        'book_id': pid,
        'date1': date1,
        'total': total,
        'num1': num1
    }
    
    return render(request, 'booking.html', context)
from django.utils.timezone import now
from django.db.models import Sum
def monthly_sales_report(request):
    today = now().date()
    first_day = today.replace(day=1)
    
    # Get total sales and number of bookings for the current month
    total_sales = Booking.objects.filter(book_date__gte=first_day, book_date__lte=today).aggregate(total_amount=Sum('total'))
    total_orders = Booking.objects.filter(book_date__gte=first_day, book_date__lte=today).count()
    
    # Get details of customers who made purchases
    purchases = Booking.objects.filter(book_date__gte=first_day, book_date__lte=today).select_related('profile__user')
    
    customers = []
    for booking in purchases:
        customers.append({
            'username': booking.profile.user.username,
            'product': booking.booking_id,  # You may want to include actual product details
            'quantity': booking.quantity,
            'total': booking.total,
            'date': booking.book_date
        })
    
    context = {
        'total_sales': total_sales['total_amount'] if total_sales['total_amount'] else 0,
        'total_orders': total_orders,
        'month': today.strftime('%B %Y'),
        'customers': customers
    }
    return render(request, 'sales_report.html', context)

def payment(request, total):
    if not request.user.is_authenticated:
        return redirect('login')
    error = False
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    cart = Cart.objects.filter(profile=profile).all()
    if request.method == "POST":
        error = True
    d = {'total': total, 'error': error}
    return render(request, 'payment2.html', d)


def delete_admin_booking(request, pid, bid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    book = Booking.objects.get(booking_id=pid, id=bid)
    book.delete()
    return redirect('admin_viewBooking')

from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from django.contrib import messages
from .models import Booking  # Ensure Booking model is imported correctly

def delete_booking(request, bid):
    # Fetch the booking object or return 404 if not found
    booking = get_object_or_404(Booking, id=bid)

    # Check if the booking is not already delivered
    if booking.status != "Delivered":  # Use `booking.status` if it's a CharField
        with transaction.atomic():
            # Restore stock if an item is associated with the booking
            if hasattr(booking, 'item') and booking.item:
                print(f"Before cancellation: {booking.item.name} stock = {booking.item.stock}")  # Debugging
                booking.item.stock += booking.quantity
                booking.item.save()
                print(f"After cancellation: {booking.item.name} stock = {booking.item.stock}")  # Debugging

            # Delete the booking
            booking.delete()
        
        messages.success(request, "Your booking has been canceled, and stock has been restored.")
    else:
        messages.error(request, "You cannot cancel a delivered order.")

    # Redirect back to the view booking page
    return redirect('view_booking')



def delete_user(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('view_user')


def delete_feedback(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    feed = Send_Feedback.objects.get(id=pid)
    feed.delete()
    return redirect('view_feedback')


def booking_detail(request, pid, bid):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    cart = Cart.objects.filter(profile=profile).all()
    product = Product.objects.all()
    book = Booking.objects.get(booking_id=pid, id=bid)
    total = 0
    num1 = 0
    user1 = user.username
    li = book.booking_id.split('.')
    li2 = []
    for j in li:
        if user1 != j:
            li2.append(int(j))
    for i in cart:
        total += i.product.price
        num1 += 1
    d = {'profile': profile, 'cart': cart, 'total': total, 'num1': num1, 'book': li2, 'product': product, 'total': book}
    return render(request, 'booking_detail.html', d)


def admin_booking_detail(request, pid, bid, uid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    user = User.objects.get(id=uid)
    profile = Profile.objects.get(user=user)
    cart = Cart.objects.filter(profile=profile).all()
    product = Product.objects.all()
    book = Booking.objects.get(booking_id=pid, id=bid)
    total = 0
    num1 = 0
    user1 = user.username
    li = book.booking_id.split('.')
    li2 = []
    for j in li:
        if user1 != j:
            li2.append(int(j))
    for i in cart:
        total += i.product.price
        num1 += 1
    d = {'profile': profile, 'cart': cart, 'total': total, 'num1': num1, 'book': li2, 'product': product, 'total': book}
    return render(request, 'admin_view_booking_detail.html', d)


def Edit_status(request, pid, bid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    book = Booking.objects.get(booking_id=pid, id=bid)
    stat = Status.objects.all()
    if request.method == "POST":
        n = request.POST['book']
        s = request.POST['status']
        book.booking_id = n
        sta = Status.objects.filter(name=s).first()
        book.status = sta
        book.save()
        return redirect('admin_viewBooking')
    d = {'book': book, 'stat': stat}
    return render(request, 'status.html', d)


def Admin_View_product(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    pro = Product.objects.all()
    d = {'pro': pro}
    return render(request, 'admin_view_product.html', d)


def delete_product(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    pro = Product.objects.get(id=pid)
    pro.delete()
    return redirect('admin_view_product')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = User.objects.get(id=request.user.id)
    pro = Profile.objects.get(user=user)
    
    try:
        cart_items = Cart.objects.filter(profile=pro)
        total = sum(item.product.price for item in cart_items)
        num1 = cart_items.count()
    except Cart.DoesNotExist:
        total = 0
        num1 = 0
    
    d = {'pro': pro, 'user': user, 'num1': num1, 'total': total}
    return render(request, 'profile.html', d)

def Edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    error = False
    user = User.objects.get(id=request.user.id)
    pro = Profile.objects.get(user=user)
    
    cart = Cart.objects.filter(profile=pro)
    total = sum(item.product.price for item in cart)
    num1 = cart.count()

    if request.method == 'POST':
        f = request.POST.get('fname', '')
        l = request.POST.get('lname', '')
        u = request.POST.get('uname', '')
        c = request.POST.get('city', '')
        ad = request.POST.get('add', '')
        e = request.POST.get('email', '')
        con = request.POST.get('contact', '')
        d = request.POST.get('date', '')

        try:
            i = request.FILES['img']
            pro.image = i
            pro.save()
        except:
            pass

        if d:
            try:
                pro.dob = d
                pro.save()
            except:
                pass

        user.first_name = f
        user.last_name = l
        user.email = e
        user.save()

        pro.user.username = u
        pro.contact = con
        pro.city = c
        pro.address = ad
        pro.save()

        error = True

    d = {'error': error, 'pro': pro, 'num1': num1, 'total': total}
    return render(request, 'edit_profile.html', d)

def Admin_Home(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')

    # Get all bookings, customers, and products
    bookings = Booking.objects.all()
    customers = Profile.objects.all()
    products = Product.objects.all()

    # Count total bookings, customers, and products
    total_bookings = bookings.count()
    total_customers = customers.count()
    total_products = products.count()

    # Check for out-of-stock products
    out_of_stock_products = check_out_of_stock(products)

    # Context data
    context = {
        'total_pro': total_products,
        'total_customer': total_customers,
        'total_book': total_bookings,
        'out_of_stock_products': out_of_stock_products
    }

    return render(request, 'admin_home.html', context)

def check_out_of_stock(products):
    """Check for out-of-stock products"""
    return products.filter(stock=0)


def delete_category(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    cat = Category.objects.get(id=pid)
    cat.delete()
    return redirect('view_categary')


def edit_product(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')

    cat = Category.objects.all()
    product = Product.objects.get(id=pid)
    error = ""

    if request.method == "POST":
        c = request.POST['cat']
        p = request.POST['pname']
        pr = request.POST['price']
        d = request.POST['desc']
        s = request.POST['stock']  # Retrieve stock from the form data
        ct = Category.objects.get(name=c)
        
        # Update product attributes
        product.category = ct
        product.name = p
        product.price = pr
        product.desc = d
        product.stock = s  # Update the stock attribute
        
        try:
            product.save()
            error = "no"
        except Exception as e:
            error = "yes"

        try:
            # Handle image upload if provided
            i = request.FILES['img']
            product.image = i
            product.save()
        except:
            pass  # Do nothing if image is not provided

    d = {'cat': cat, 'error': error, 'product': product}
    return render(request, 'edit_product.html', d)



def edit_category(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    category = Category.objects.get(id=pid)
    error=""
    if request.method=="POST":
        c = request.POST['cat']
        category.name = c
        try:
            category.save()
            error = "no"
        except:
            error = "yes"
    d = {'error':error,'category':category}
    return render(request, 'edit_category.html', d)

def search_booking(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    terror = ""
    book=""
    sd=""
    if request.method == "POST":
        sd = request.POST['searchdata']
        try:
            book = Booking.objects.get(booking_id=sd)
            terror = "found"
        except:
            terror="notfound"
    d = {'book':book,'terror':terror,'sd':sd}
    return render(request,'search_booking.html',d)


def bookingbetweendate_reportdetails(request):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    return render(request, 'bookingbetweendate_reportdetails.html')



def bookingbetweendate_report(request):
    if not request.user.is_authenticated:
        return redirect('loginadmin')
    if request.method == "POST":
        fd = request.POST['fromdate']
        td = request.POST['todate']
        booking = Booking.objects.filter(book_date__range=[fd,td])
        d = {'booking':booking,'fd':fd,'td':td}
        return render(request, 'bookingbetweendate_reportdetails.html', d)
    return render(request, 'bookingbetweendate_report.html')



def add_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.user  # Assuming the user is logged in
        blog = Blog.objects.create(title=title, content=content, author=author)
        return redirect('view_my_blog')
    else:
        return render(request, 'add_blog.html')

def view_my_blog(request):
    user_blogs = Blog.objects.filter(author=request.user)
    return render(request, 'view_my_blog.html', {'user_blogs': user_blogs})

def view_all_blogs(request):
    all_blogs = Blog.objects.all()
    return render(request, 'view_all_blogs.html', {'all_blogs': all_blogs})


def edit_blog(request, blog_id):
    # Retrieve the blog object using the blog_id
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method == 'POST':
        # Retrieve the updated blog content from the request
        updated_title = request.POST.get('title')
        updated_content = request.POST.get('content')
        
        # Update the blog object with the new content
        blog.title = updated_title
        blog.content = updated_content
        blog.save()
        
        return redirect('view_my_blog')

    return render(request, 'edit_blog.html', {'blog': blog})

def delete_blog(request, blog_id):
    if request.method == 'POST':
        try:
            blog = Blog.objects.get(pk=blog_id)
            if request.user == blog.author:
                blog.delete()
                return redirect('view_my_blog')
            else:
                return HttpResponseForbidden("You are not authorized to delete this blog")
        except Blog.DoesNotExist:
            return HttpResponseNotFound("Blog not found")
    else:
        return HttpResponseNotAllowed(['POST'])








@login_required


@login_required
def create_pet_profile(request):
    if request.method == 'POST':
        try:
            if not request.user.is_authenticated:  # Ensure user is logged in
                return HttpResponseBadRequest("You must be logged in to create a pet profile.")

            owner = request.user  # ✅ Assign the currently logged-in user
            name = request.POST.get('name', '').strip()
            breed = request.POST.get('breed', '').strip()
            age = request.POST.get('age', '').strip()
            image = request.FILES.get('image', None)
            veterinarian = request.POST.get('veterinarian', '').strip()
            visit_date = request.POST.get('visit_date', '').strip()

            if not (name and breed and age and veterinarian and visit_date):
                return HttpResponseBadRequest("All fields are required.")

            try:
                age = int(age)  # ✅ Ensure age is an integer
            except ValueError:
                return HttpResponseBadRequest("Age must be a number.")

            # ✅ Create and save the pet profile with an owner
            pet_profile = PetProfile.objects.create(
                owner=owner,  # ✅ This ensures the NOT NULL constraint is satisfied
                name=name,
                breed=breed,
                age=age,
                image=image,
                veterinarian=veterinarian,
                visit_date=visit_date
            )

            return redirect('view_pet_profiles')  # Redirect to the pet profiles page

        except KeyError:
            return HttpResponseBadRequest("Required fields are missing.")

    return render(request, 'create_pet_profile.html')


from django.shortcuts import render
from .models import PetProfile

def view_pet_profiles(request):
    pets = PetProfile.objects.filter(owner=request.user)    # Fetch all pet profiles
    print(pets)  # Debugging: Print pet objects in the console
    return render(request, 'view_pet_profiles.html', {'pets': pets})




from django.shortcuts import render, get_object_or_404, redirect
from .models import PetProfile

def edit_pet_profile(request, pk):
    pet_profile = get_object_or_404(PetProfile, pk=pk)
    
    if request.method == 'POST':
        # Extract updated pet profile data from the request
        pet_profile.name = request.POST.get('name', pet_profile.name)
        pet_profile.breed = request.POST.get('breed', pet_profile.breed)
        pet_profile.age = request.POST.get('age', pet_profile.age)
        pet_profile.veterinarian = request.POST.get('veterinarian', pet_profile.veterinarian)
        pet_profile.visit_date = request.POST.get('visit_date', pet_profile.visit_date)
        
        # Handle image upload
        if 'image' in request.FILES:
            pet_profile.image = request.FILES['image']
        
        pet_profile.save()
        
        # Redirect to all pet profiles
        return redirect('view_pet_profiles')

    # Pass pet profile data to the template
    context = {
        'pet_profile': pet_profile,
        'current_image': pet_profile.image,
        'current_visit_date': pet_profile.visit_date,
    }
    return render(request, 'edit_pet_profile.html', context)






def delete_pet_profile_confirm(request, pk):
    pet_profile = get_object_or_404(PetProfile, pk=pk)
    
    if request.method == 'POST':
        # Delete the pet profile if confirmed
        pet_profile.delete()
        return redirect('view_pet_profiles')  # Redirect to the list of pet profiles
    
    return render(request, 'delete_pet_profile_confirm.html', {'pet_profile': pet_profile})



from django.contrib import messages

def my_view(request):
    if request.user.is_superuser:
        messages.info(request, "You are a superuser!")
    
    return render(request, 'admin_dashboard.html')

def check_stock_quantity(request):
    out_of_stock_products = Product.objects.filter(stock=0)
    for product in out_of_stock_products:
        message = f"The stock for {product.name} is out."
        messages.info(request, message)

def admin_dashboard(request):
    check_stock_quantity(request)  # Pass the request object to the function
    return render(request, 'admin_dashboard.html', {'messages': messages.get_messages(request)})

from .forms import SupplierRegistrationForm

def register_supplier(request):
    if request.method == 'POST':
        form = SupplierRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Supplier.objects.create(user=user)
            return redirect('supplier_dashboard')
    else:
        form = SupplierRegistrationForm()
    return render(request, 'register_supplier.html', {'form': form})

def login_supplier(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('supplier_dashboard')
    return render(request, 'login_supplier.html')

from .models import Product

def supplier_dashboard(request):
    # Retrieve all products from the database
    products = Product.objects.all()
    return render(request, 'supplier_dashboard.html', {'products': products})

def view_products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

from django.http import HttpResponse
def product_details_view(request, product_id):
    # Your view logic here
    return HttpResponse(f"You are viewing details for product with ID {product_id}.")



def product_request_list(request):
    product_requests = ProductRequest.objects.filter(supplier=request.user)
    return render(request, 'product_request_list.html', {'product_requests': product_requests})

@login_required
def respond_to_product_request(request, request_id):
    product_request = ProductRequest.objects.get(pk=request_id)
    if request.method == 'POST':
        response = request.POST.get('response')
        product_request.response = response
        product_request.is_responded = True
        product_request.save()
        return redirect('product_request_list')
    return render(request, 'respond_to_product_request.html', {'product_request': product_request})

# views.py
# views.py
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  # Import login_required decorator
from .models import ProductRequest, Supplier
@login_required
def create_product_request(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        if product_name and description:
            ProductRequest.objects.create(product_name=product_name, description=description)
            return redirect('view_requests')
    return render(request, 'create_product_request.html')


# views.py


@login_required
def view_requests(request):
    # Retrieve all product requests from the database
    product_requests = ProductRequest.objects.all()
    return render(request, 'view_requests.html', {'product_requests': product_requests})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import ProductRequest  # Adjust the model name to match your actual model

@require_POST
@csrf_exempt
def delete_request(request):
    request_id = request.POST.get('request_id')
    try:
        product_request = ProductRequest.objects.get(id=request_id)
        product_request.delete()
        return JsonResponse({'success': True})
    except ProductRequest.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Request not found'})

    


def product_details(request):
    # Retrieve the latest product request instance
    latest_request = ProductRequest.objects.latest('request_date')

    # Render the template and pass the product request instance as context
    return render(request, 'product_details.html', {'latest_request': latest_request})






from django.shortcuts import render
from .models import ProductRequest
from django.contrib.auth.decorators import login_required


def view_admin_requests(request):
    # Retrieve admin requests
    admin_requests = ProductRequest.objects.all()
    return render(request, 'view_admin_requests.html', {'admin_requests': admin_requests})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import ProductRequest  # Adjust the model name to match your actual model

@require_POST
@csrf_exempt
def update_request_status(request):
    request_id = request.POST.get('request_id')
    status = request.POST.get('status')
    try:
        product_request = ProductRequest.objects.get(id=request_id)
        product_request.status = status
        product_request.save()
        return JsonResponse({'success': True, 'status': status})
    except ProductRequest.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Request not found'})


from django.contrib import messages
from django.dispatch import receiver
from grocery.signals import admin_product_request

def handle_admin_product_request(sender, request, **kwargs):
    supplier = request.product.supplier  # Assuming each product has a supplier field
    messages.info(supplier.user, "New product request: {}".format(request.product.name))

def create_admin_product_request(admin_user, product_details):
    # Logic to create admin product request
    # After creating the request, emit the signal
    admin_product_request.send(sender=None, admin_user=admin_user, product_details=product_details)


from .models import SupplierRequest
def product_request_list(request):
    # Retrieve all product requests
    supplier_requests = SupplierRequest.objects.all()

    return render(request, 'product_request_list.html', {'supplier_requests': supplier_requests})