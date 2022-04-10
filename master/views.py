from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View,CreateView,ListView,DetailView,UpdateView
from master.forms import UserRegisterForm,ExtendedUserForm,AddCategoryForm,AddMedicineForm,ContactUsForm,StaffRegisterForm,ExtendedStaffForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from master.models import AddMedicineModel,ContactUsModel,AddCartModel,UserRegisterModel,AddCategoryModel,StaffRegisterModel

from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.contrib.auth.models import User
from django.conf import settings
import requests
from django.db.models import Sum
from django.shortcuts import render
from Project.settings import EMAIL_HOST_USER
from . import forms
from django.core.mail import send_mail
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
# Create your views here.
 


# Create your views here.
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})

class HomeView(TemplateView):
	template_name='nwhome.html'

class AdminPanel(TemplateView):
	template_name='AdminPanel.html'

def adduser(request):
	if request.method=="POST":
		form=UserRegisterForm(request.POST)
		extend_form=ExtendedUserForm(request.POST,request.FILES)

		if form.is_valid() and extend_form.is_valid():
			user=form.save()
			extended_profile=extend_form.save(commit=False)
			extended_profile.user=user
			extended_profile.save()

			sub=forms.UserRegisterForm(request.POST)
			fname=str(sub["first_name"].value())
			lname=str(sub["last_name"].value())
			subject='welcome to PharmaLTD'
			message='Hi, %s %s,successfully registered' %(fname,lname)
			recepient=str(sub['email'].value())
			send_mail(subject,message,EMAIL_HOST_USER,[recepient],fail_silently=False)


			username_var=form.cleaned_data.get('username')
			password_var=form.cleaned_data.get('password1')
			user=authenticate(username=username_var,password=password_var)

			login(request,user)
			return redirect ('home')
	else:
		form=UserRegisterForm(request.POST)
		extend_form=ExtendedUserForm(request.POST,request.FILES)

	context={"form":form,"extend_form":extend_form}
	return render(request,'reg.html',context)

class AdminHome(TemplateView):
	template_name='AdminPanel.html' 

class StaffHome(TemplateView):
	template_name='StaffHome.html'

class UserLogin(View):
	def get(self,request):
		form=AuthenticationForm()
		context={'form':form}
		return render(request,'login.html',context)

	def post(self,request):
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(username=username,password=password)
		recaptcha_response = request.POST.get('g-recaptcha-response')
		print(recaptcha_response)
		data = {
			'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
			'response': recaptcha_response
			}
		r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
		result = r.json()
        
		if result['success']:
			user=authenticate(username=username,password=password)
			login(request,user,backend='django.contrib.auth.backends.ModelBackend')
        
		if user is not None :
			login(request,user)
		if user.is_superuser == True and user.is_staff == True:
			return redirect('adminhome')
		if user.is_staff == True and user.is_superuser == False:
			return redirect('staffhome')
		if user.is_staff == False and user.is_superuser == False:
			return redirect ('home')
		else:
			form=AuthenticationForm()
			context={'form':form}
		return render(request,'login.html',context)	

class AddCategoryView(CreateView):
	template_name='Add_Category.html'
	form_class=AddCategoryForm
	success_url='/master/admin/'

class AddMedicineView(CreateView):
	template_name='Add_Medicine.html'
	form_class=AddMedicineForm
	success_url='/master/admin/'

class MedicineListView(View):
	template_name='MedicineView.html'
	

	def get(self,request):
		context={
		'categoryname':AddCategoryModel.objects.all(),
		'Medicine':AddMedicineModel.objects.all()
		}
		return render(request,self.template_name,context)
# class MedicineListView(View):
# 	template_name='MedicineView.html'

# 	def get(self,request):
# 		cur_user=str(request.user)
# 		context={
# 		'usermedicine':AddMedicineModel.objects.all(),
# 		'cart_count':AddCartModel.objects.filter(user=cur_user,payment_status=False).count()
# 		}

class AboutView(TemplateView):
	template_name='abus.html'

class MedDetail(DetailView):
	template_name='MedicineDetail.html'
	model=AddMedicineModel

def logout_request(request):
	logout(request)
	return redirect('home')

class MedUpdateView(UpdateView):
	template_name='EditProduct.html'
	model=AddMedicineModel
	fields=['name','price','description','expiry_date','image','category','available_stock']
	success_url='/master/admin/'

class MedList(ListView):
	template_name='editlistview.html'
	model=AddMedicineModel
	context_object_name='Med'



class PaymentView(View):
	template_name="payment.html"

	def get(self,request):
		cur_user=str(request.user)
		data=AddCartModel.objects.filter(user=cur_user,payment_status=False).aggregate(Sum('price'))['price__sum']
		amount=int(data)*100
		currency = 'INR'
		# amount = 20000  # Rs. 200
 
		# Create a Razorpay Order
		razorpay_order = razorpay_client.order.create(dict(amount=amount,
			currency=currency,payment_capture='0'))
 
		# order id of newly created order.
		razorpay_order_id = razorpay_order['id']
		callback_url = '/master/paymenthandler/'
 
		# we need to pass these details to frontend.
		context = {'amount_rupee':data}
		context['razorpay_order_id'] = razorpay_order_id
		context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
		context['razorpay_amount'] = amount
		context['currency'] = currency
		context['callback_url'] = callback_url
 
		return render(request,self.template_name, context=context)
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
	# only accept POST request.
	if request.method == "POST":
		try:
           
			# get the required parameters from post request.
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}
 
			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			if result is None:
				# amount = 20000  # Rs. 200
				cur_user=str(request.user)
				data=AddCartModel.objects.filter(user=cur_user,payment_status=False).aggregate(Sum('price'))['price__sum']
				amount=int(data)*100
				try:
 
					# capture the payemt
					razorpay_client.payment.capture(payment_id, amount)
					data=AddCartModel.objects.filter(user=cur_user,payment_status=False)
					for i in data:
						medicine_name=i.name
						medicine_data=AddMedicineModel.objects.get(name=medicine_name)
						print(medicine_data)
						medicine_data.available_stock=medicine_data.available_stock-1
						medicine_data.save()
						i.payment_status=True
						i.save()
					# render success page on successful caputre of payment
					return render(request, 'paymentsuccess.html')
				except:
 
					# if there is an error while capturing payment.
					return render(request, 'paymentfail.html')
			else:
 
				# if signature verification fails.
				return render(request, 'paymentfail.html')
		except:
 
			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
		# if other than POST request is made.
		return HttpResponseBadRequest()

class ContactUsView(CreateView):
	template_name="contactus.html"
	form_class=ContactUsForm
	success_url="/master/home"


class FeedbackList(ListView):
	template_name='feedlist.html'
	model=ContactUsModel
	context_object_name='feedlist'

class StaffFeedbackList(ListView):
	template_name='stafffeed.html'
	model=ContactUsModel
	context_object_name='feedlist'


class AddCartView(View):
	def get(self,request,pk):
		data=AddMedicineModel.objects.get(id=pk)
		# print("DATA: ",data)
		user_data=UserRegisterModel.objects.get(user=request.user)
		address_var=user_data.address
		name_var=data.name
		price_var=data.price
		
		print(name_var)
		print(price_var)

		AddCartModel.objects.create(
			user=request.user,
			name=name_var,
			price=price_var,
			address=address_var
			)
		return redirect('view')

class ListCartView(View):
	template_name='cartlist.html'

	def get(self,request):
		cur_user=str(request.user)
		print("cur_user",cur_user)
		
		context={

		'cart_list':AddCartModel.objects.filter(user=cur_user,payment_status=False),
		'total_price':AddCartModel.objects.filter(user=cur_user,payment_status=False).aggregate(Sum('price'))['price__sum'],
		}
		return render(request,self.template_name,context)

class OrderHistoryView(View):
	template_name='orderhistory.html'

	def get(self,request):
		cur_user=int(request.user.id)-1
		context={
		'order_list':AddCartModel.objects.filter(user=cur_user,payment_status=True)
		}
		return render(request,self.template_name,context)

class CartRemoveView(View):
	def get(self,request,pk):
		AddCartModel.objects.get(id=pk).delete()
		return redirect('usercartlist')



class MedRemoveView(View):
	def get(self,request,pk):
		AddMedicineModel.objects.get(id=pk).delete()
		return redirect('adminhome')


class CategorywiseProducts(View):
	template_name="CategorywiseProducts.html"

	def get(self,request,pk):
		cur_user=request.user
		categoryname=AddCategoryModel.objects.get(id=pk)
		medicine=AddMedicineModel.objects.filter(category=categoryname)
		context={
		'products':medicine,
		'categoryname':categoryname,
		'catlist':AddCategoryModel.objects.all(),
		}

		return render(request,self.template_name,context)

# class StaffView(ListView):
# 	template_name='viewstaff.html'
# 	model=StaffRegisterModel
# 	context_object_name="stafflist"

# class StaffDetailView(DetailView):
# 	template_name='staffdetail.html'
# 	model=StaffRegisterModel

# class StaffEditView(UpdateView):
# 	template_name='staffedit.html'
# 	model=StaffRegisterModel
# 	fields=['age','address']
# 	# add user field**
# 	success_url='/master/admin/'

def adduser(request):
	if request.method=="POST":
		form=StaffRegisterForm(request.POST)
		extend_form=ExtendedStaffForm(request.POST,request.FILES)

		if form.is_valid() and extend_form.is_valid():
			user=form.save()
			extended_profile=extend_form.save(commit=False)
			extended_profile.user=user

			extended_profile.save()

			username_var=form.cleaned_data.get('username')
			password_var=form.cleaned_data.get('password1')
			user=authenticate(username=username_var,password=password_var)

			login(request,user)
			return redirect ('staffhome')
	else:
		form=StaffRegisterForm(request.POST)
		extend_form=ExtendedStaffForm(request.POST,request.FILES)

	context={"form":form,"extend_form":extend_form}
	return render(request,'addstaff.html',context)


class OrderList(View):
	template_name='order.html'

	def get(self,request):
		context={
		'order_data':AddCartModel.objects.filter(payment_status=True)
		}
		return render (request,self.template_name,context)