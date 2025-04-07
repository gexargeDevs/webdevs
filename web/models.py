from django.db import models
import random
import string


def generate_product_code():
    """გენერირებს 5-ნიშნა შემთხვევით კოდს."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

class Partner(models.Model):
    fullname = models.CharField(max_length=100, verbose_name="სრული სახელი")
    companyName = models.CharField(max_length=100, verbose_name="კომპანიის სახელი")
    email = models.EmailField(verbose_name="ელ. ფოსტა")
    address = models.CharField(max_length=60,verbose_name="მისამართი")
    mobile = models.CharField(max_length=50,verbose_name="საკონტაქტო ნომერი",default='არ არის მითითებული')
    logo = models.ImageField(
        upload_to='partners/logos/',
        verbose_name="ლოგო",
        null=True,
        blank=True
    )
    partner_valid_date = models.DateField(verbose_name="პარტნიორობის ვადა")

    def __str__(self):
        return f"{self.companyName} ({self.fullname})"

    class Meta:
        verbose_name = "პარტნიორი"
        verbose_name_plural = "პარტნიორები"

class Discount(models.Model):
    valid_date = models.DateField(verbose_name="ფასდაკლების ვადა")
    discount_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="ფასდაკლების პროცენტი",
        default=0.00 
    )
    products = models.ManyToManyField(
        'Product',
        verbose_name="პროდუქტები"
    )
    set_date = models.DateField(
        auto_now_add=True,
        verbose_name="დაყენების თარიღი"
    )

    def __str__(self):
        return f"ფასდაკლება {self.discount_percent}% ({self.valid_date})"

    class Meta:
        verbose_name = "ფასდაკლება"
        verbose_name_plural = "ფასდაკლებები"

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="სახელი")
    description = models.TextField(verbose_name="აღწერა")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="ფასი"
    )
    storage_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="საწყობში რაოდენობა"
    )
    filter_setting = models.CharField(
        max_length=50,
        verbose_name="ფილტრის პარამეტრი",
        blank=True
    )
    code = models.CharField(
        max_length=5,
        unique=True,
        verbose_name="კოდი",
        editable=False,  
        blank=True,     
        null=True  
    )

    image = models.ImageField(
        upload_to='products/',
        verbose_name="ფოტო",
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        print("save() მეთოდი გამოიძახა")
        if not self.code:
            self.code = generate_product_code()
            print(f"გენერირებული კოდი: {self.code}")
            while Product.objects.filter(code=self.code).exists():
                self.code = generate_product_code()
                print(f"კოდი უკვე არსებობს, ახალი კოდი: {self.code}")
        super().save(*args, **kwargs)
        print("ობიექტი შეინახა კოდით:", self.code)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "პროდუქტი"
        verbose_name_plural = "პროდუქტები"

class Order(models.Model):
    id = models.CharField(max_length=100, verbose_name="ID",primary_key=True)
    products = models.CharField(max_length=100, verbose_name="პროდუქცია")
    clients = models.CharField(max_length=100, verbose_name="შემძენი")
    price = models.CharField(max_length=100, verbose_name="ფასი")
    addrs = models.CharField(max_length=100, verbose_name="მისამართი")
    date = models.CharField(max_length=100, verbose_name="შეკვეთის დრო")
    paymethod = models.CharField(max_length=100, verbose_name="გადახდის მეთოდი")
    status = models.CharField(max_length=100, verbose_name="სტატუსი", default='pedding')

    def __str__(self):
        return self.id
    
    class Meta:
        verbose_name = "შეკვეთა"



class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='images',  # ეს საშუალებას მოგვცემს product.images.all()-ის გამოყენებით ფოტოების წამოღებას
    )
    image = models.ImageField(
        upload_to='product_images/',
        verbose_name="ფოტო"
    )

    def __str__(self):
        return f"ფოტო {self.id} ({self.product.name})"