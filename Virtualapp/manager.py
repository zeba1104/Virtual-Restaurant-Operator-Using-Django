from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_no, email, password=None, **extra_fields):
        if not phone_no:
            raise ValueError('Then phone number field must be set')
        email = self.normalize_email(email)
        user = self.model(phone_no=phone_no, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, phone_no, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        if extra_fields.get('is_staff')is not True:
            raise ValueError('superuser must have is_staff=True.')
        if extra_fields.get('is_superuser')is not True:
            raise ValueError('superuser must have is_superuser=True.')
        
        return self.create_user(phone_no, email, password, **extra_fields)