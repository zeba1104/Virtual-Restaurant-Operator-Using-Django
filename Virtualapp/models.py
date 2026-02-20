from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager 

class CustomUser(AbstractUser):  
    username = None  # Remove default username field
    phone_no = models.CharField(unique=True, max_length=10)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'phone_no'
    REQUIRED_FIELDS = ['email']  

    objects = UserManager()  

    def __str__(self):  
        return self.phone_no
    
class Contact(models.Model):
    SUBJECT_CHOICES = [
        ('General Inquiry', 'General Inquiry'),
        ('Collaboration inquiry', 'Collaboration inquiry'),
        ('Accounting inquiry', 'Accounting inquiry'),
        ('Marketing inquiry', 'Marketing inquiry'),

    ]
    
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, default='General Inquiry')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    

class Package(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    features = models.TextField(help_text="Enter features separated by commas")
    detailed_description = models.TextField()

    def get_features_list(self):
        return self.features.split(",")

    def __str__(self):
        return self.name
    

class Section1(models.Model):
    title = models.CharField(max_length=255)
    heading = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='uploads/')
    button_name = models.CharField(max_length=100)
    button_link = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    
class Collaboration(models.Model):
    COLLABORATION_CHOICES = [
        ('restaurant', 'Restaurant'),
        ('entrepreneur', 'Food Entrepreneur'),
        ('cloud-kitchen', 'Cloud Kitchen'),
        ('delivery-platform', 'Delivery Platform'),
        ('influencer', 'Influencer / Chef'),
    ]

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    business_name = models.CharField(max_length=255)
    collaboration_type = models.CharField(max_length=50, choices=COLLABORATION_CHOICES)
    message = models.TextField()

    def __str__(self):
        return self.full_name
    

class Checkout(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    package_name = models.CharField(max_length=255)
    package_price = models.DecimalField(max_digits=10, decimal_places=2)
    package_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class ServiceHome(models.Model):
    image = models.ImageField(upload_to='service_images/')
    heading = models.CharField(max_length=255)
    subheading = models.TextField(help_text="Limit to approximately 3 lines of text.")
    url = models.CharField(max_length=100, verbose_name="url")

    def __str__(self):
        return self.heading

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])
    feedback = models.TextField()
    company_type = models.CharField(max_length=100, help_text="e.g. Founder, Multi-Outlet Chain Owner")  # NEW FIELD
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.rating} Stars'

class Consultation(models.Model):
    topic = models.CharField(max_length=255)
    details = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic
    

class Brand(models.Model):
    brand_image = models.ImageField(upload_to='brand_images/')
    brand_name = models.CharField(max_length=255)
    short_description = models.TextField(max_length=500)
    swiggy_url = models.URLField(max_length=500)
    zomato_url = models.URLField(max_length=500)

    def __str__(self):
        return self.brand_name