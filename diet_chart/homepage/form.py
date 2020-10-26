from django import forms
from .models import meal_distribution

class meal_distribution_form(forms.ModelForm):
	class Meta:
		model = meal_distribution
		fields={
			'User_no',
			'Date',
			'Meal_names',
			'Meal_times',
			'Meal_calories',
			'Meal_items'
		}
