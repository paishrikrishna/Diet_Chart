from django.db import models

# Create your models here.
class meal_distribution(models.Model):
	User_no = models.TextField(default='n/a')
	Date = models.TextField(default='N/A')
	Meal_names = models.TextField(default='N/A')
	Meal_times = models.TextField(default='N/A')
	Meal_calories = models.TextField(default='N/A')
	Meal_items = models.TextField(default='N/A')
