from django.contrib import admin
from .models import UserProfile,Product
from .models import DoctorProfile, PharmacistProfile

# Register your models here.


admin.site.register(UserProfile)
admin.site.register(Product)

admin.site.register(DoctorProfile)
admin.site.register(PharmacistProfile)