from django import forms
from master.models import UserRegisterModel,AddMedicineModel,AddCategoryModel,ContactUsModel,StaffRegisterModel
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
	class Meta:
		model=User
		fields=["username","first_name","last_name","password1","password2","email"]

class ExtendedUserForm(forms.ModelForm):
	class Meta:
		model=UserRegisterModel
		fields=["age","address","id_card"]

class AddCategoryForm(forms.ModelForm):
	class Meta:
		model=AddCategoryModel
		exclude=('status','created_on')

class AddMedicineForm(forms.ModelForm):
	class Meta:
		model=AddMedicineModel
		exclude=('status','created_on')

class ContactUsForm(forms.ModelForm):
	class Meta:
		model=ContactUsModel
		exclude=("created_on",)

class StaffRegisterForm(UserCreationForm):
	class Meta:
		model=User
		fields=["username","first_name","last_name","password1","password2","email","is_staff"]

class ExtendedStaffForm(forms.ModelForm):
	class Meta:
		model=StaffRegisterModel
		fields=["age","address","id_card"]




		