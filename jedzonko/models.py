from django.db import models


class Recipe(models.Model):

    name = models.CharField(max_length=128)
    ingredients = models.TextField(null=True)  # Right now type of this field is an open matter
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    preparation_time = models.PositiveSmallIntegerField(null=True)
    votes = models.IntegerField(default=0)
    how_to_prepare = models.TextField(null=True)


class Plan(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through='RecipePlan')


class DayName(models.Model):
    name = models.CharField(max_length=64)
    order = models.IntegerField(unique=True)


class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=64)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.IntegerField()
    day_name = models.ForeignKey(DayName, on_delete=models.CASCADE)


class Page(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    slug = models.CharField(max_length=64, unique=True)

    def save(self, *args, **kwargs):
        self.slug = f'/{self.title.replace(" ", "-")}/'
        super(Page, self).save(*args, **kwargs)
