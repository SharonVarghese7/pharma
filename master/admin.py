from django.contrib import admin

from master.models import UserRegisterModel,AddCategoryModel,AddMedicineModel,ContactUsModel,AddCartModel

# Register your models here.
admin.site.register(UserRegisterModel)
admin.site.register(AddCategoryModel)
admin.site.register(AddMedicineModel)
admin.site.register(ContactUsModel)
admin.site.register(AddCartModel)