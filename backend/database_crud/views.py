from django.shortcuts import render, redirect 
from django.http import HttpResponse, request, FileResponse# Create your views here.
from .models import *
from .forms import OrderForm,CustomerForm
from django.core.paginator import Paginator


def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	paginator=Paginator(orders,5)
	page=request.GET.get('page') #?page=2
	orders=paginator.get_page(page)

	context = { 
                'orders':orders, 
                'customers':customers,
	            'total_orders':total_orders,
                'delivered':delivered,
	            'pending':pending 
                }

	return render(request, 'pages/dashboard.html', context)
def is_valid_queryparam(param):
    return param!="" and param is not None

def products(request):
	products = Product.objects.all()
	product = request.GET.get('product')
	category = request.GET.get('category')

	if is_valid_queryparam(product) and product != 'Choose...':
		products = products.filter(name__icontains=product)
	if is_valid_queryparam(category) and category != 'Choose...':
		products = products.filter(category__icontains=category)

	number=products.count()

	return render(request, 'pages/products.html', {'n' : number,'products':products})

def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()

	context = {'customer':customer, 'orders':orders, 'order_count':order_count}
	return render(request, 'pages/customer.html',context)

def createCustomer(request):
	form = CustomerForm()
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = CustomerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'pages/customer_form.html', context)


def createOrder(request):
	form = OrderForm()
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		# if form.is_valid():
    	# 		form.save()
		# 	return redirect('/')
		if form.is_valid():
			with open( 'file_test.txt', 'a+')as f:
				f.write("ok \n")
				return FileResponse(f, as_attachment=True, filename='some_file.txt')
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'pages/order_form.html', context)

def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'pages/order_form.html', context)

def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'pages/delete.html', context)