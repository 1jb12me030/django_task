from django.shortcuts import render

# Create your views here.
# views.py

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import *
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'testapp/registration.html', {'form': form})
from django.contrib import messages
def custom_login(request):
    if request.method == 'POST':
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']
        user = authenticate(request, mobile_number=mobile_number, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('testapp/login.html')
        else:
            # Handle invalid login credentials
            messages.error(request, 'Invalid login credentials. Please try again.')
    return render(request, 'testapp/login.html')

# views.py

from django.shortcuts import render

# views.py

from django.shortcuts import render
from .models import Dashboard

def dashboard(request):
    # Fetch the latest dashboard data from the database
    latest_dashboard = Dashboard.objects.latest('id')

    context = {
        'latest_dashboard': latest_dashboard,
    }

    return render(request, 'testapp/dashboard.html', context)

from django.shortcuts import render
from .models import Dashboard, Order  # Import the Order model

def place_order(request):
    # Fetch the latest dashboard data from the database
    latest_dashboard = Dashboard.objects.latest('id')

    # Retrieve all orders
    orders = Order.objects.all()

    context = {
        'latest_dashboard': latest_dashboard,
        'orders': orders,  # Pass the orders to the template
    }

    return render(request, 'testapp/dashboard.html', context)

# views.py

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order, Address
from .serializers import OrderSerializer, AddressSerializer

# views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Order, Address, Dashboard
from .serializers import OrderSerializer, AddressSerializer

@api_view(['POST'])
def place_order1(request):
    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            # Update the Dashboard model with the order total
            total_sales = serializer.validated_data.get('total', 0)  # Replace 'total' with the correct field name
            dashboard = Dashboard.objects.latest('id')
            dashboard.total_sales += total_sales
            dashboard.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_address(request):
    if request.method == 'POST':
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
