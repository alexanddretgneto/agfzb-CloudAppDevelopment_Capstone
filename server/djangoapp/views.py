from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login_view.html', context)
    else:
        return render(request, 'djangoapp/login_view.html', context)


def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/dd273e21-8af8-4608-b838-529759a65be4/dealership-package/get-dealership"
        dealerships = get_dealers_from_cf(url)
        context = {}
        context["dealerships"] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, id):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/dd273e21-8af8-4608-b838-529759a65be4/dealership-package/get-dealership"
        dealer = get_dealer_by_id_from_cf(url, id)
        context["dealer"] = dealer
    
        review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/dd273e21-8af8-4608-b838-529759a65be4/dealership-package/get-review"
        reviews = get_dealer_reviews_from_cf(review_url, id=id)
        print(reviews)
        context["reviews"] = reviews
        
        return render(request, 'djangoapp/dealer_details.html', context)
# Create a `add_review` view to submit a review
def add_review(request, id):
    if request.user.is_authenticated:
        context = {}
        dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/dd273e21-8af8-4608-b838-529759a65be4/dealership-package/get-dealership"
        dealer = get_dealer_by_id_from_cf(dealer_url, id)
        context["dealer"] = dealer
        if request.method == "GET":
            cars = CarModel.objects.all()
            context["cars"] = cars
            print(context)
            return render(request, 'djangoapp/add_review.html', context)
        
        if request.method == "POST":
            review = {}
            review["name"] = request.user.first_name + " " + request.user.last_name
            form = request.POST
            review["dealership"] = id
            review["review"] = form["content"]
            if(form.get("purchasecheck") == "on"):
                review["purchase"] = True
            else:
                review["purchase"] = False
            if(review["purchase"]):
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
                car = CarModel.objects.get(pk=form["car"])
                review["car_make"] = car.make.name
                review["car_model"] = car.name
                review["car_year"] = car.year
            post_url = "https://us-south.functions.cloud.ibm.com/api/v1/namespaces/dd273e21-8af8-4608-b838-529759a65be4/actions/dealership-package/post-reviews"
            json_payload = { "review": review }
            post_request(post_url, json_payload, id=id)
            return redirect("djangoapp:dealer_details", id=id)
    else:
        return redirect("/djangoapp/login")

