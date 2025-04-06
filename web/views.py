from django.shortcuts import render, get_object_or_404
from .models import Product, Discount
from datetime import date
from django.middleware.csrf import get_token
from django.core.mail import send_mail
from django.http import JsonResponse
def index(request):

    products = Product.objects.all()
    filter_settings = set(p.filter_setting for p in products if p.filter_setting)

    context = {
        'filter_settings': filter_settings
    }

    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def product(request):
    filter_value = request.GET.get('filter')

    # თუ არჩეულია ფასდაკლება
    if filter_value == "ფასდაკლება":
        today = date.today()
        active_discounts = Discount.objects.filter(valid_date__gte=today)
        products = Product.objects.filter(discount__in=active_discounts).distinct()
    elif filter_value:
        products = Product.objects.filter(filter_setting=filter_value)
    else:
        products = Product.objects.all()

    filter_settings = set(p.filter_setting for p in Product.objects.all() if p.filter_setting)
    sab_filter = set(p.filter_detal for p in Product.objects.all() if p.filter_detal)

    context = {
        'product': products,
        'filter_settings': filter_settings,
        'active_filter': filter_value,
        'sub_filter': sab_filter,
        'today': date.today(),  
    }
    return render(request, 'products.html', context)

def product_detail(request, product_code):
    product = get_object_or_404(Product, code=product_code)

    context = {
        'product': product,
        'today': date.today(),
    }
    return render(request, 'product_detail.html', context)

def carts(request):
    return render(request, 'cart.html')


def contact(request):
    csrf_token = get_token(request)

    return render(request, 'contact.html', {'csrf_token': csrf_token})


def emailsend(request):
    if request.method == "POST":  # **მხოლოდ POST მეთოდი დაიშვება**
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("ტელეფონი")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        full_message = f"""
        სახელი: {name}
        ელფოსტა: {email}
        ტელეფონი: {phone}
        თემა: {subject}
        
        შეტყობინება:
        {message}
        """

        send_mail(
            subject=f"gexar.ge: {subject}",
            message=full_message,
            from_email="info@gexar.ge",
            recipient_list=["info@gexar.ge"],
            fail_silently=False,
        )

        return JsonResponse({"message": "შეტყობინება წარმატებით გაიგზავნა!"})

    return JsonResponse({"error": "არასწორი მოთხოვნა"}, status=400)