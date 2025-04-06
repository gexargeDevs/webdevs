from django import template
from decimal import Decimal
from datetime import date

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def discounted_price(product, today):
    discount = get_discount(product, today)
    if discount:
        percent = discount.discount_percent
        new_price = product.price * (Decimal('1.0') - (percent / Decimal('100')))
        return round(new_price, 2)
    return product.price

@register.filter
def days_left(discount):
    if not discount:
        return 0
    today = date.today()
    delta = (discount.valid_date - today).days
    return delta if delta > 0 else 0

@register.filter
def get_discount(product, today):
    # ვამოწმებთ რომ valid_date არ არის გასული თარიღი
    discounts = product.discount_set.filter(valid_date__gte=today).order_by('valid_date')
    return discounts.first() if discounts.exists() else None