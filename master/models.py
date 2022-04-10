from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserRegisterModel(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	age=models.IntegerField(default=18)
	address=models.TextField(max_length=80)
	id_card=models.ImageField(upload_to='idcard/')
	status=models.BooleanField(default=True)
	created_on=models.DateTimeField(auto_now=True)
	def __str__(self):
		return (self.user.first_name+" "+self.user.last_name)
		
class AddCategoryModel(models.Model):
	name=models.CharField(max_length=100)
	status=models.BooleanField(default=True)
	created_on=models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.name

class AddMedicineModel(models.Model):
	name=models.CharField(max_length=100)
	price=models.IntegerField(default=18)
	description=models.TextField(max_length=200)
	expiry_date=models.DateField()
	image=models.ImageField(upload_to='Prod_images/')
	status=models.BooleanField(default=True)
	created_on=models.DateTimeField(auto_now=True)
	category=models.ForeignKey(AddCategoryModel,on_delete=models.CASCADE)
	available_stock=models.IntegerField(default=18)

	def __str__(self):
		return self.name

class ContactUsModel(models.Model):
	name=models.CharField(max_length=20)
	email=models.CharField(max_length=40)
	message=models.TextField()
	created_on=models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.name


class AddCartModel(models.Model):
	user=models.CharField(max_length=30,unique=False)
	name=models.CharField(max_length=50)
	price=models.IntegerField(default=100)
	address=models.TextField(max_length=100,default="none")
	payment_status=models.BooleanField(default=False)
	status=models.BooleanField(default=True)
	created_on=models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

class StaffRegisterModel(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	age=models.IntegerField(default=18)
	address=models.CharField(max_length=80)
	id_card=models.ImageField(upload_to="idcard/")
	status=models.BooleanField(default=True)
	created_on=models.DateTimeField(auto_now=True)

	def __str__(self):
		return (self.user.first_name+" "+self.user.last_name)






	
	