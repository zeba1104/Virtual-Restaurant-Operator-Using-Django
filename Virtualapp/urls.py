from django.urls import path
from Virtualapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
        path("", views.home, name="home"),
        path("register/", views.register, name="register"),
        path("login/", views.user_login, name="login"),
        path("logout/", views.user_logout, name="logout"),
        path('wp-login', views.admin_login, name='wp-login'),  # must match the decorator!

    
        path('wp-logout/', views.admin_logout, name='admin_logout'),  # Admin logout
        path("wp-admin/", views.admin_home, name="admin"),
        path("display_user/", views.user, name="user"),
        path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),

        path("contact/", views.contact_view, name="contact"),
        path("contact-list/", views.contact_list_view, name="contact_list"),  
        path("delete-contact/<int:contact_id>/", views.delete_contact, name="delete_contact"),
        path("add-packages/", views.packages_form, name="packages_form"),
        path("packages-details/", views.package_list, name="packages_list"),
        path("packages-details/delete/<int:package_id>/", views.delete_package, name="delete_package"),
        path("packages-details/edit/<int:package_id>/", views.edit_package, name="edit_package"),
        path("packages/", views.package_list_user, name="package_list"), 
        path("packages/<int:package_id>/", views.package_detail_user, name="package_detail_user"),
        path("Collaborate/", views.add_collaboration, name="Collaborate"), 
        path("Section1/", views.section1, name="Collaborate_section"), 
        path("content_details/", views.content_details, name="Collaborate"), 
        path('section/edit/<int:section_id>/', views.edit_section, name='edit_section'),
    path('section/delete/<int:section_id>/', views.delete_section, name='delete_section'),
   path('collaborations/', views.collaboration_list, name='collaboration_list'),
    path('collaborations/delete/<int:pk>/', views.delete_collaboration, name='delete_collaboration'),
 path('checkout/<int:package_id>/', views.checkout, name='checkout'),  # Checkout page
    path('process_payment/<int:package_id>/', views.process_payment, name='process_payment'),  # Process payment page
    path('payment_success/', views.payment_success, name='payment_success'),  
    path('checkout-list/', views.checkout_list, name='checkout_list'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    path('edit-user/', views.edit_user, name='edit_user'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('services/add/', views.service_home_create, name='service_home_create'),
    path('services/edit/<int:pk>/', views.service_home_edit, name='service_home_edit'),
    path('home_services/', views.service_home_list, name='service_home_list'),
    path('services/delete/<int:pk>/', views.service_home_delete, name='service_home_delete'),
    path('add_feedback/', views.home, name='add_feedback'),
    path('feedbacks/', views.feedback_list, name='feedback_list'),
    path('feedbacks/delete/<int:id>/', views.delete_feedback, name='delete_feedback'),
    path('consultation/', views.consultation_view, name='submit_consultation'),
    path('brand/', views.brand, name='brand'),
    path('add-brand/', views.add_brand, name='add-brand'),
    path('brand-list/', views.brands_list, name='brands-list'),
    path('edit-brand/<int:brand_id>/', views.edit_brand, name='edit-brand'),
    path('delete-brand/<int:brand_id>/', views.delete_brand, name='delete-brand'),

]