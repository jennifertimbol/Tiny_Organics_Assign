from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer, Child
from .forms import childForm
import bcrypt
import requests
import json

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        errors = Customer.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        
        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

        customer = Customer.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_pw
        )

        request.session['curr_user'] = customer.id
        return redirect('/homepage')

def login(request):
    if request.method == 'POST':
        customer = Customer.objects.filter(email = request.POST['email'])

        if customer:
            log_user = customer[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                request.session['curr_user'] = log_user.id
                return redirect('/homepage')
        messages.error(request, 'Email or password are incorrect')
    return redirect('/')

def homepage(request):
    if 'curr_user' not in request.session:
        return redirect('/')
    #fetch allergens 
    response = requests.get('https://60f5adf918254c00176dffc8.mockapi.io/api/v1/allergens/')


    context = {
        'curr_user' : Customer.objects.get(id=request.session['curr_user']),
        'allergen_types' : response.json(),
    }
    return render(request, 'home.html', context)

    #use a regular form instead of djangoforms

# def fetchrecipes(request):
#     if request.method == 'POST':
#         user = Customer.objects.get(id=request.session['curr_user'])
#         postedChildForm = childForm(request.POST)
#         if postedChildForm.is_valid():
#             print('Its valid!')
#             form = postedChildForm.save(commit=False)
#             form.parent_id = user.id
#             form.save()
#             return redirect(f'/results/{form.id}')
#         else:
#             context = {
#                 'user' : Customer.objects.get(id=request.session['curr_user']),
#                 'childForm' : postedChildForm,
#             }
#             return render(request, 'home.html', context)
#     return redirect('/homepage')

def fetch_recipes(request):
    if request.method == 'POST':
        user = Customer.objects.get(id=request.session['curr_user'])

        child = Child.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            allergies = request.POST['allergies'],
            parent_id = user.id,
        )
        request.session['users_child'] = child.id
        return redirect(f'/results/{child.id}')
    return redirect('/homepage')
    
    # save child's info in the database
    #assign allergen post data to a variable    
    # save child's info in the database
    #assign allergen post data to a variable
    #create a function that will filter out the recipes
    # foorloop 
    # iterate through the recipes list and dict
    # O(n) complexity
    # nested forloops = O(n2) complexity
    # if/else?
    # assign results in a variable and use it as context to display in html

def results(request, child_id):
    user = Customer.objects.get(id=request.session['curr_user'])
    child = Child.objects.get(id=child_id)
    allergen = child.allergies
    response = requests.get('https://60f5adf918254c00176dffc8.mockapi.io/api/v1/recipes/')
    #parse json response
    recipes = json.loads(response.text)
    filtered_recipes = allergen_filter(allergen, recipes, child_id)

    context = {
        'recipes' : filtered_recipes,
        'user' : user,
        'child' : child,
        'allergen' : allergen,
        
    }
    return render(request, 'results.html', context)


def allergen_filter(allergen, recipes, child_id):
    child = Child.objects.get(id=child_id)
    childs_allergen = child.allergies
    response = requests.get('https://60f5adf918254c00176dffc8.mockapi.io/api/v1/recipes/')
    #parse json response
    recipes = json.loads(response.text)
    print(recipes)

#loop through list of dict
#access value of key 'allergen' inside dict
#loop through allergen values
#O(n) complexity
# nested forloops = O(n2) complexity
#if len(recipe['allergen']) == 0:
#results.append(recipe)
#else if: 
#use results as context 
#display in html

    results = []
    for recipe in recipes:
        #iterate through list
        for key in recipe:
            #iterate through dict
            print(recipe["allergens"])
            if (childs_allergen not in recipe["allergens"]):
                results.append(recipe)
                print("results", results)
                break
            else: 
                break
    print(results)
    return results


def logout(request):
    request.session.flush()
    return redirect('/')
