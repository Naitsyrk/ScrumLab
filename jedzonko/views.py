from datetime import datetime
from random import shuffle

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views import View
from django.core.paginator import Paginator
from django.db import OperationalError

from .models import Recipe, Plan, RecipePlan, DayName, Page
from django.db.models import F


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class Dashboard(View):
    template_name = 'dashboard.html'
    ctx = {}

    def get(self, request):
        all_plans = Plan.objects.all()
        plans_count = len(all_plans)
        self.ctx['plans_count'] = plans_count
        all_recipes = Recipe.objects.all()
        recipes_count = len(all_recipes)
        self.ctx['recipes_count'] = recipes_count
        last_added_plan = list(Plan.objects.all().order_by('-created'))[0]
        self.ctx['last_added_plan'] = last_added_plan
        self.ctx['last_added_plan_days'] = DayName.objects.all().order_by('order')
        self.ctx['last_added_plan_meals'] = RecipePlan.objects.all().filter(plan=last_added_plan).order_by('day_name__order', 'order')
        return render(request, self.template_name, self.ctx)


class LandingPage(View):

    def get(self, request):
        recipies_list = list(Recipe.objects.all())
        shuffle(recipies_list)
        ctx = {'recipe_1_name': recipies_list[0].name,
               'recipe_2_name': recipies_list[1].name,
               'recipe_3_name': recipies_list[2].name,
               'recipe_1_description': recipies_list[0].description,
               'recipe_2_description': recipies_list[1].description,
               'recipe_3_description': recipies_list[2].description,
               }

        last_added_plan = list(Plan.objects.all().order_by('-created'))[0]
        ctx['last_added_plan'] = last_added_plan
        ctx['last_added_plan_days'] = DayName.objects.all().order_by('order')
        ctx['last_added_plan_meals'] = RecipePlan.objects.all().filter(plan=last_added_plan).order_by('day_name__order',
                                                                                                      'order')
        try:
            contact_page = Page.objects.get(slug='/contact/')
            contact_slug = contact_page.slug
        except (Page.DoesNotExist, OperationalError):
            contact_slug = "#contact"
        ctx['contact_slug'] = contact_slug
        try:
            about_page = Page.objects.get(slug='/about/')
            about_slug = about_page.slug
        except (Page.DoesNotExist, OperationalError):
            about_slug = "#about"
        ctx['about_slug'] = about_slug
        return render(request, 'index.html', ctx)


class ContactPage(View):
    def get(self, request):
        ctx = {}
        try:
            about_page = Page.objects.get(slug='/about/')
            about_slug = about_page.slug
        except (Page.DoesNotExist, OperationalError):
            about_slug = "/#about"
        ctx['about_slug'] = about_slug

        page = Page.objects.get(slug='/contact/')
        ctx['page'] = page
        return render(request, 'contact.html', ctx)


class AboutPage(View):
    def get(self, request):
        ctx = {}
        try:
            contact_page = Page.objects.get(slug='/contact/')
            contact_slug = contact_page.slug
        except (Page.DoesNotExist, OperationalError):
            contact_slug = "/#contact/"
        ctx['contact_slug'] = contact_slug
        page = Page.objects.get(slug='/about/')
        ctx['page'] = page
        return render(request, 'about.html', ctx)


class RecipeList(View):

    def get(self, request):
        template = 'app-recipes.html'
        recipe_list = Recipe.objects.all().order_by('-votes', '-created')
        paginator = Paginator(recipe_list, 50)
        page = request.GET.get('page')
        recipe_page = paginator.get_page(page)
        ctx = {'recipe_page': recipe_page}
        return render(request, template, ctx)


class PlanList(View):

    def get(self, request):
        template = 'app-schedules.html'
        plan_list = Plan.objects.all().order_by('name')
        paginator = Paginator(plan_list, 50)
        page = request.GET.get('page')
        plan_page = paginator.get_page(page)
        ctx = {'plan_page': plan_page}
        return render(request, template, ctx)


class AddRecipe(View):

    def get(self, request):
        ctx = {}
        html = "app-add-recipe.html"
        return render(request, html, ctx)

    def post(self, request):
        recipe_name = request.POST.get('recipe_name')
        recipe_desc = request.POST.get('recipe_desc')
        recipe_time = request.POST.get('recipe_time')
        how_to_prepare = request.POST.get('how_to_prepare')
        ingredients = request.POST.get('ingredients')

        if recipe_name and recipe_desc and recipe_time and how_to_prepare and ingredients:
            Recipe.objects.create(name=recipe_name,
                                  ingredients=ingredients,
                                  description=recipe_desc,
                                  preparation_time=recipe_time,
                                  how_to_prepare=how_to_prepare)
            return redirect('planlist')
        else:
            ctx = {'error_message': "Wypełnij poprawnie wszystkie pola"}
            return render(request, 'app-add-recipe.html', ctx)


class AddPlan(View):
    html = "app-add-schedules.html"

    def get(self, request):
        ctx = {}
        return render(request, self.html, ctx)

    def post(self, request):
        ctx = {}
        plan_name = request.POST.get('plan_name')
        plan_description = request.POST.get('plan_description')
        if plan_name and plan_description:
            Plan.objects.create(name=plan_name, description=plan_description)
            new_plan = Plan.objects.last()
            return redirect(f'/plan/{new_plan.id}/')
        else:
            ctx['error_message'] = "Uzupełnij poprawnie formularz"
            return render(request, self.html, ctx)


class AddRecipieToPlan(View):

    def get(self, request):
        ctx = {}
        ctx['plan_list'] = Plan.objects.all()
        ctx['recipe_list'] = Recipe.objects.all()
        ctx['day_list'] = DayName.objects.all()
        html = "app-schedules-meal-recipe.html"
        return render(request, html, ctx)

    def post(self, request):
        plan_id = request.POST.get('plan_id')
        plan = Plan.objects.get(id=plan_id)
        recipe_id = request.POST.get('recipe_id')
        recipe = Recipe.objects.get(id=recipe_id)
        meal_name = request.POST.get('meal_name')
        day_id = request.POST.get('day')
        day = DayName.objects.get(id=day_id)
        order = request.POST.get('order')

        new_recipeplan = RecipePlan()
        new_recipeplan.meal_name = meal_name
        new_recipeplan.recipe = recipe
        new_recipeplan.plan = plan
        new_recipeplan.order = order
        new_recipeplan.day_name = day
        new_recipeplan.save()
        return redirect(f'/plan/{plan_id}/')


class RecipeDetails(View):
    def get(self, request, id):
        recipe = Recipe.objects.get(id=id)
        context = {
            'id': id,
            'recipe_name': recipe.name,
            'recipe_ingredients': recipe.ingredients.split(", "),
            'recipe_description': recipe.description,
            'recipe_preparation_time': recipe.preparation_time,
            'recipe_votes': recipe.votes,
            'recipe_how_to_prepare': recipe.how_to_prepare
        }
        return render(request, 'app-recipe-details.html', context)

    def post(self, request, id):

        if 'like_button' in request.POST:
            Recipe.objects.filter(id=id).update(votes=F('votes') + 1)
            recipe = Recipe.objects.get(id=id)
            context = {
                'id': id,
                'recipe_name': recipe.name,
                'recipe_ingredients': recipe.ingredients.split(", "),
                'recipe_description': recipe.description,
                'recipe_preparation_time': recipe.preparation_time,
                'recipe_votes': recipe.votes,
                'recipe_how_to_prepare': recipe.how_to_prepare,
                'msg': "Dziękuję za polubienie!!!",
            }
            return render(request, 'app-recipe-details.html', context)

        elif 'hate_button' in request.POST:
            Recipe.objects.filter(id=id).update(votes=F('votes') - 1)
            recipe = Recipe.objects.get(id=id)
            context = {
                'id': id,
                'recipe_name': recipe.name,
                'recipe_ingredients': recipe.ingredients.split(", "),
                'recipe_description': recipe.description,
                'recipe_preparation_time': recipe.preparation_time,
                'recipe_votes': recipe.votes,
                'recipe_how_to_prepare': recipe.how_to_prepare,
                'msg': "Przykro nam :(",
            }
            return render(request, 'app-recipe-details.html', context)
        else:
            recipe = Recipe.objects.get(id=id)
            context = {
                'id': id,
                'recipe_name': recipe.name,
                'recipe_ingredients': recipe.ingredients.split(", "),
                'recipe_description': recipe.description,
                'recipe_preparation_time': recipe.preparation_time,
                'recipe_votes': recipe.votes,
                'recipe_how_to_prepare': recipe.how_to_prepare
            }
            return render(request, 'app-recipe-details.html', {})



class PlanDetails(View):

    def get(self, request, id):
        plan = Plan.objects.get(id=id)
        days = DayName.objects.all().order_by('order')
        meals = RecipePlan.objects.all().filter(plan=plan).order_by('day_name__order', 'order')
        context = {
        'plan': plan,
        'days': days,
        'meals': meals
        }
        return render(request, 'app-details-schedules.html', context)

    # def post(self, request, id):
    #
    #     like_value = request.POST.get("like_recipe", None)
    #
    #     if int(like_value) == 1:
    #         Recipe.objects.filter(id=id).update(votes=F('votes') + 1)
    #         recipe = Recipe.objects.get(id=id)
    #         context = {
    #             'id': id,
    #             'recipe_name': recipe.name,
    #             'recipe_ingredients': recipe.ingredients.split(", "),
    #             'recipe_description': recipe.description,
    #             'recipe_preparation_time': recipe.preparation_time,
    #             'recipe_votes': recipe.votes,
    #             'recipe_how_to_prepare': recipe.how_to_prepare
    #         }
    #         return render(request, 'app-recipe-details.html', context)
    #     else:
    #         recipe = Recipe.objects.get(id=id)
    #         context = {
    #             'id': id,
    #             'recipe_name': recipe.name,
    #             'recipe_ingredients': recipe.ingredients.split(", "),
    #             'recipe_description': recipe.description,
    #             'recipe_preparation_time': recipe.preparation_time,
    #             'recipe_votes': recipe.votes,
    #             'recipe_how_to_prepare': recipe.how_to_prepare
    #         }
    #         return render(request, 'app-recipe-details.html', {})


class ModifyRecipe(View):
    template_name = 'app-edit-recipe.html'
    ctx = {}

    def get(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            raise Http404

        self.ctx['recipe'] = recipe
        return render(request, self.template_name, self.ctx)

    def post(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        self.ctx['recipe'] = recipe

        name = request.POST.get('name')
        ingredients = request.POST.get('ingredients')
        description = request.POST.get('description')
        preparation_time = request.POST.get('preparation_time')
        how_to_prepare = request.POST.get('how_to_prepare')

        if name and name != '' \
                and ingredients and ingredients != '' \
                and description and description != '' \
                and preparation_time and preparation_time != '' \
                and how_to_prepare and how_to_prepare != '':
            recipe.name = name
            recipe.ingredients = ingredients
            recipe.description = description
            recipe.preparation_time = preparation_time
            recipe.how_to_prepare = how_to_prepare
            recipe.updated = datetime.now()
            recipe.save()
            return redirect('/recipe/list/')
        else:
            error_message = "Wypełnij poprawnie wszystkie pola"
            self.ctx['error_message'] = error_message
            return render(request, self.template_name, self.ctx)


class DeleteRecipeFromPlan(View):

    def get(self, request, recipeplan_pk):
        ctx = {}
        recipeplan = RecipePlan.objects.get(pk=recipeplan_pk)
        ctx['recipeplan'] = recipeplan
        html = "app-schedules-meal-recipe-delete.html"
        return render(request, html, ctx)

    def post(self, request, recipeplan_pk):
        recipeplan = RecipePlan.objects.get(pk=recipeplan_pk)
        plan_id = recipeplan.plan.id
        recipeplan.delete()
        return redirect(f'/plan/{plan_id}/')
