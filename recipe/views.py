from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Recipe
from .form import RecipeForm, ContactForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def user_form(request):
    return render(request, 'recipe/userform.html')


def saveuser(request):
    if request.method == 'POST':
        print("-------->", request.POST)
        print("username ------>", request.POST['username'])
        print("first_name ---->", request.POST['first_name'])
        print("last_name ------>", request.POST['last_name'])
        print("email ------>", request.POST['email'])
        print("password ------>", request.POST['password'])
        user = User.objects.create_user(username=request.POST['username'],
                                        first_name=request.POST['first_name'],
                                        last_name=request.POST['last_name'],
                                        email=request.POST['email'],
                                        password=request.POST['password'])
        user.save()
        return render(request, 'recipe/login.html', {'msg': 'User is saved Successfully ....!'})


def login_form(request):
    return render(request, 'recipe/login.html')


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect("/app/")
    else:
        return HttpResponse("Invalid Credentials")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/app/login_form/")


def register_recipe(request):
    form = RecipeForm()
    return render(request, 'recipe/recipe_form.html', {"form": form})


@login_required(login_url="/app/login_form/")
def saverecepi(request):
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST)
        if recipe_form.is_valid():
            recipe_form.save()
            return HttpResponseRedirect("/app/")
        else:
            return render(request, 'recipe/recipe_form.html', {"errors": recipe_form.errors, "form": RecipeForm()})

        # recipe = Recipe(recipe_name=request.POST['recipe_name'],
        #                 recipe_type=request.POST['recipe_type'],
        #                 ingredients=request.POST['ingredients'],
        #                 procedure=request.POST['procedure'])
        # recipe.save()
    return render(request, 'recipe/recipe_form.html',
                  {'msg': 'Recipe is saved Successfully ....!', "form": RecipeForm()})


@login_required(login_url="/app/login_form/")
def recipe_booklet(request):
    recipe_list = Recipe.objects.all()
    return render(request, 'recipe/recipe.html', {'recipe_list': recipe_list})


@login_required(login_url="/app/login_form/")
def deleterecipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipes = Recipe.objects.all()
    print('Recipe-------->', recipe)
    recipe.delete()
    return render(request, 'recipe/recipe.html', {'msg': 'The recipe Deleted Successfully ...!',
                                                  'recipe_list': recipes})


@login_required(login_url="/app/login_form/")
def editrecipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipe/recipe_form.html', {"recipe": recipe})


def contact_form(request):
    if request.method == "GET":
        return render(request, "recipe/contact_form.html", {"form": ContactForm()})
    else:
        form = ContactForm(request.POST)
        recipe_form = RecipeForm(request.POST)
        if form.is_valid() and recipe_form.is_valid():
            cc_myself = form.cleaned_data["cc_myself"]
            return render(request, "recipe/contact_form.html", {"form": ContactForm()})
        else:
            return render(request, "recipe/contact_form.html", {"form": ContactForm(), "errors": form.errors})
