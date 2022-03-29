"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from jedzonko.views import IndexView, Dashboard
from jedzonko import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view()),
    path('main/', Dashboard.as_view()),
    path('', views.LandingPage.as_view(), name="landingpage"),
    path('recipe/list/', views.RecipeList.as_view(), name="planlist"),
    path('plan/list/', views.PlanList.as_view()),
    path('recipe/add/', views.AddRecipe.as_view()),
    path('plan/add/', views.AddPlan.as_view()),
    path('plan/add-recipe/', views.AddRecipieToPlan.as_view()),
    path('recipe/<int:id>/', views.RecipeDetails.as_view()),
    path('plan/<int:id>/', views.PlanDetails.as_view()),
    path('recipe/modify/<int:pk>/', views.ModifyRecipe.as_view()),
    path('contact/', views.ContactPage.as_view()),
    path('plan/delete_recipe/<int:recipeplan_pk>/', views.DeleteRecipeFromPlan.as_view()),
    path('about/', views.AboutPage.as_view()),
]
