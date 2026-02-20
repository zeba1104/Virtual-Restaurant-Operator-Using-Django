from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser,Contact,Package,Section1,Collaboration,Checkout,ServiceHome,Feedback,Consultation,Brand  # Import your custom user model
from .forms import RegisterForm,ContactForm,PackageForm,Section1_form,CollaborationForm,CheckoutForm,ServiceHomeForm,FeedbackForm,BrandForm  # Import your custom registration form
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models.functions import TruncDate
from django.db.models import Count
from django.http import JsonResponse
import json



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user to the database
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  # Redirect to login after signup
        else:
            # Print form errors for debugging
            print(form.errors)
            messages.error(request, 'There was an error in your form. Please check your input.')
    else:
        form = RegisterForm()

    return render(request, 'reg_login.html', {'form': form})

def admin_login(request):
    if request.method == "POST":
        phone_no = request.POST.get("phone_no")
        password = request.POST.get("password")

        user = authenticate(request, phone_no=phone_no, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                messages.success(request, "Admin login successful!")
                return redirect("/wp-admin/")  # Redirect to your custom admin dashboard
            else:
                messages.error(request, "Access denied. Only superusers can access the admin panel.")
                return redirect("/wp-login")  # Optional: refresh or stay on admin login
        else:
            messages.error(request, "Invalid phone number or password.")

    return render(request, "admin/login.html")

def user_login(request):
    if request.method == "POST":
        phone_no = request.POST.get("phone_no")
        password = request.POST.get("password")

        user = authenticate(request, username=phone_no, password=password)  # Assuming phone_no is in 'username'

        if user is not None:
            if user.is_superuser:
                messages.error(request, "Admins are not allowed to access the home page.")
                return redirect("login")  # or render a forbidden page if preferred

            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")
        else:
            messages.error(request, "Invalid phone number or password.")

    return render(request, "reg_login.html")


def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")

def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
        messages.success(request, "User deleted successfully.")
    return redirect('/display_user')  # Replace 'user_list' with your actual view name

def admin_logout(request):
    logout(request)
    messages.success(request, "Admin logged out successfully.")
    return redirect("/wp-login")

@login_required(login_url='login')
def home(request):
    section1 = Section1.objects.first()
    section2 = Section1.objects.all()[1] if Section1.objects.count() > 1 else None
    packages = Package.objects.all()[:3]
    services = ServiceHome.objects.all()
    feedback_list = Feedback.objects.all().order_by('-created_at')

    contact_form = ContactForm()
    feedback_form = FeedbackForm()

    if request.method == 'POST':
        if 'feedback' in request.POST:
            feedback_form = FeedbackForm(request.POST)
            if feedback_form.is_valid():
                feedback_form.save()
                messages.success(request, 'Your feedback has been submitted successfully!')
                return redirect('home')
        else:
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                contact_form.save()
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('home')
            else:
                messages.error(request, 'There was an error with your submission. Please correct the errors below.')

    return render(request, 'user/new/template.html', {
        'section1': section1,
        'section2': section2,
        'packages': packages,
        'services': services,
        'feedback_list': feedback_list,
        'contact_form': contact_form,
        'feedback_form': feedback_form,
    })



@login_required(login_url='wp-login')
def admin_home(request):
    # Group and format user data
    user_data = CustomUser.objects.annotate(date=TruncDate('date_joined')) \
        .values('date') \
        .annotate(count=Count('id')) \
        .order_by('date')

    # Group and format order data
    order_data = Checkout.objects.annotate(date=TruncDate('created_at')) \
        .values('date') \
        .annotate(count=Count('id')) \
        .order_by('date')

    # Convert date objects to strings for JavaScript
    user_data = [{'date': item['date'].strftime('%Y-%m-%d'), 'count': item['count']} for item in user_data]
    order_data = [{'date': item['date'].strftime('%Y-%m-%d'), 'count': item['count']} for item in order_data]

    # Calculate totals
    total_users = sum(item['count'] for item in user_data)
    total_orders = sum(item['count'] for item in order_data)

    return render(request, 'admin/dashboard.html', {
        'user': request.user,
        'user_data': user_data,
        'order_data': order_data,
        'total_users': total_users,
        'total_orders': total_orders,
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        if not phone_no:
            messages.error(request, "Phone number is required.")
            return redirect("/wp-admin")
        user.phone_no = phone_no
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("/wp-admin")
    return redirect("/wp-admin")


@login_required
def edit_user(request):
    if request.method == 'POST':
        user = request.user
        # user.email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        if not phone_no:
            messages.error(request, "Phone number is required.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        user.phone_no = phone_no
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='login')
def packages(request):
    return render(request, 'user/packages.html') 

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "We will contact you soon.")
            return redirect('/contact')  
        else:
            messages.error(request, "Oops! Something went wrong. Please try again.")
    else:
        form = ContactForm()
    
    return render(request, "user/contact.html", {"form": form})

def user(request):
    page_obj = CustomUser.objects.filter(is_superuser=False)
    #superuser = CustomUser.objects.filter(is_superuser=True).first()
    return render(request, 'admin/user.html', {'page_obj': page_obj})

def contact_list_view(request):
    contacts = Contact.objects.all().order_by('-id')  
    paginator = Paginator(contacts, 10)  # Show 10 contacts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "admin/contact_list.html", {"page_obj": page_obj})

def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    contact.delete()
    messages.success(request, "Contact message deleted successfully.")
    return redirect('contact_list')


def add_package(request):
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Package added successfully!")
            return redirect('package_list')  
    else:
        form = PackageForm()

    return render(request, 'admin/add_package.html', {'form': form})

@login_required(login_url='login')
def packages_form(request):
    if request.method == "POST":
        form = PackageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/packages-details')  
    else:
        form = PackageForm()

    return render(request, "admin/packages_form.html", {"form": form})

def package_list(request):
    packages = Package.objects.all()
    paginator = Paginator(packages, 10)  # Show 10 packages per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "admin/package_list.html", {"page_obj": page_obj})

def delete_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    if request.method == "POST":
        package.delete()
        messages.success(request, "Package deleted successfully.")
        return redirect("packages_list")  
    
    return redirect("packages_list")

def edit_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    
    if request.method == "POST":
        form = PackageForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, "Package updated successfully.")
            return redirect("packages_list")
    else:
        form = PackageForm(instance=package)
    
    return render(request, "admin/packages_form.html", {"form": form, "edit_mode": True, "package": package})

@login_required(login_url='login')
def package_list_user(request):
    """View to display the list of packages with short details."""
    packages = Package.objects.all()
    return render(request, 'user/packages.html', {'packages': packages})

@login_required(login_url='login')
def package_detail_user(request, package_id):
    """View to display the detailed description of a selected package."""
    package = get_object_or_404(Package, id=package_id)
    return render(request, 'user/indetail_package.html', {'package': package})

def section1(request):
    if request.method == "POST":
        form = Section1_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/content_details')  
        else:
            print("Form Errors:", form.errors) 
    else:
        form = Section1_form()
    
    return render(request, 'admin/section1_home.html', {'form': form})

def content_details(request):
    """View to display the list of sections with short details."""
    sections = Section1.objects.all()  # Fetch all records
    paginator = Paginator(sections, 5)  # Show 5 sections per page
    page_number = request.GET.get("page")  # Get current page number from request
    page_obj = paginator.get_page(page_number)  # Paginate sections
    
    return render(request, 'admin/content_details.html', {'page_obj': page_obj})

def edit_section(request, section_id):
    section = get_object_or_404(Section1, id=section_id)  
    if request.method == "POST":
        form = Section1_form(request.POST, request.FILES, instance=section)
        if form.is_valid():
            form.save()
            messages.success(request, "Section updated successfully.")
            return redirect('/content_details') 
    else:
        form = Section1_form(instance=section)

    return render(request, 'admin/section1_home.html', {'form': form})

def delete_section(request, section_id):
    section = get_object_or_404(Section1, id=section_id)  
    section.delete()
    messages.success(request, "Section deleted successfully.")
    return redirect('/content_details')  

@login_required(login_url='login')
def add_collaboration(request):
    if request.method == "POST":
        form = CollaborationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your collaboration request has been submitted successfully!")
            return redirect('/Collaborate')  
        else:
            messages.error(request, "There was an error in your submission. Please check the fields and try again.")
    else:
        form = CollaborationForm()

    return render(request, 'user/collaborate.html', {'form': form})


def collaboration_list(request):
    collaborations = Collaboration.objects.all().order_by('-id')  # Fetch all collaboration entries
    paginator = Paginator(collaborations, 10)  # Paginate with 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/collaborations.html', {'page_obj': page_obj})

def delete_collaboration(request, pk):
    collaboration = get_object_or_404(Collaboration, pk=pk)
    collaboration.delete()
    messages.success(request, "Collaboration request deleted successfully.")
    return redirect('collaboration_list')  

@login_required(login_url='login')
def checkout_view(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    return render(request, 'user/checkout.html', {'package': package})

@login_required(login_url='login')
def checkout(request, package_id):
    
    package = get_object_or_404(Package, id=package_id)
    
    # Handle form submission (POST request)
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        
        # Check if the form is valid
        if form.is_valid():
            # Save the form data (you can replace with actual save logic if needed)
            form.save()
            
            # Show success message
            messages.success(request, "Your order has been processed successfully!")
            
            # Redirect to a different page (like payment success or order summary)
            return redirect('order_success')  # Replace with your actual success page URL
        else:
            # If the form is not valid, show an error message
            messages.error(request, "There was an error with your form submission. Please check the fields and try again.")
    
    # Handle GET request, initialize empty form
    else:
        form = CheckoutForm()

    # Render the checkout page with package and form data
    return render(request, 'user/checkout.html', {
        'package': package,  
        'form': form,  
    })

@login_required(login_url='login')
def process_payment(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Save the form data
            checkout = form.save(commit=False)
            checkout.package_name = package.name
            checkout.package_price = package.price
            checkout.package_id = package.id
            checkout.save()

            messages.success(request, "Your details have been successfully saved. Proceeding to payment...")
            return redirect('payment_success')  
        else:
            
            messages.error(request, "Please fill in all the required fields.")
            return redirect('checkout', package_id=package.id)

    return redirect('checkout', package_id=package.id)  


def checkout_list(request):
    checkout_list = Checkout.objects.all().order_by('-id')
    paginator = Paginator(checkout_list, 10)  # Show 10 checkouts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin/checkout_list.html', {'page_obj': page_obj})

@login_required(login_url='login')
def payment_success(request):
    return render(request, 'user/payment_success.html')


@login_required(login_url='login')
def services(request):
    services = ServiceHome.objects.all()
    section3 = Section1.objects.all()[2] if Section1.objects.count() > 2 else None
    return render(request, 'user/services.html', {
        'services': services,
        'section3': section3
    })

@login_required(login_url='wp-login')
def service_home_create(request):
    form = ServiceHomeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('service_home_list')  
    return render(request, 'admin/service_home.html', {'form': form})

@login_required(login_url='wp-login')
def service_home_edit(request, pk):
    instance = get_object_or_404(ServiceHome, pk=pk)
    form = ServiceHomeForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('service_home_list')
    return render(request, 'admin/service_home.html', {'form': form})

@login_required(login_url='wp-login')
def service_home_list(request):
    services = ServiceHome.objects.all()
    return render(request, 'admin/service_home_list.html', {'services': services})

@login_required(login_url='wp-login')
def service_home_delete(request, pk):
    service = get_object_or_404(ServiceHome, pk=pk)
    if request.method == "POST":
        service.delete()
        return redirect('service_home_list')
    return redirect('service_home_list')

@login_required(login_url='wp-login')
def feedback_list(request):
    feedback_list = Feedback.objects.all().order_by('-created_at')
    paginator = Paginator(feedback_list, 10)  # Show 10 feedbacks per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/feedback_display.html', {'page_obj': page_obj})

@login_required(login_url='wp-login')
def delete_feedback(request, id):
    feedback = get_object_or_404(Feedback, id=id)

    if request.method == "POST":
        feedback.delete()
        messages.success(request, "Feedback deleted successfully.")
        return redirect('feedback_list')

    messages.error(request, "Invalid request.")
    return redirect('feedback_list')


@csrf_exempt
def consultation_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        topic = data.get("topic")
        details = data.get("details")

        if topic and details:
            Consultation.objects.create(topic=topic, details=details)
            return JsonResponse({"message": "Your message has been submitted!"})
        else:
            return JsonResponse({"message": "Both fields are required."}, status=400)

    return JsonResponse({"message": "Invalid request method."}, status=405)

@login_required(login_url='login')
def about(request):
    return render(request, 'user/about.html')

@login_required(login_url='login')
def brand(request):
    #services = ServiceHome.objects.all()
    brands = Brand.objects.all()  # Fetch all brand records from the database
    return render(request, 'user/brands.html', {'brands': brands})
    # section4 = Section1.objects.all()[3] if Section1.objects.count() > 3 else None
    

@login_required(login_url='wp-login')
def add_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('brands-list') # You can redirect to brand list page after adding
    else:
        form = BrandForm()
    
    return render(request, 'admin/add_brand.html', {'form': form})

@login_required(login_url='wp-login')
def brands_list(request):
    brands = Brand.objects.all().order_by('-id')  # Fetch all brand entries
    paginator = Paginator(brands, 10)  # Paginate with 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/brands_list.html', {'page_obj': page_obj})

@login_required(login_url='wp-login')
def edit_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, "Brand updated successfully!")
            return redirect('brands-list')
    else:
        form = BrandForm(instance=brand)
    return render(request, 'admin/add_brand.html', {'form': form})

@login_required(login_url='wp-login')
def delete_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    if request.method == 'POST':
        brand.delete()
        messages.success(request, "Brand deleted successfully!")
        return redirect('brands-list')
    return redirect('brands-list')

