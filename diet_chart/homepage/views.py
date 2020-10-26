'''
IMPORTATN STUFF:
A] The List names "item" which is used to log calories is cleared down there its not actually only clear its:
	1. Upload the data / items of previous meal into database with primnary key 
	2. Then clear the local list used to save it temporary

'''



import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime
import random 
import datetime

from django.shortcuts import render
from .form import meal_distribution_form
from .models import meal_distribution

# Create your views here.

plt.style.use('ggplot')
days = 0



def data_combine(folder):
	os.chdir(folder)
	extension = 'csv'
	all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

	#combine all files in the list
	combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ] , sort=True)
	#export to csv
	combined_csv.to_csv( "/home/shri/Desktop/final.csv", index=False, encoding='utf-8-sig')
	
	global days
	days = (len(all_filenames))


class data():
	time_format = ":00.000+05:30"
	total_calories = 0
	
	
	def __init__(self,meal):
		self.meal = meal 
		self.item = []
		self.length = days
		self.data = pd.read_csv('/home/shri/Desktop/final.csv')
	
	def calories(self,Bk,Lu):
		self.Breakfast = Bk.split(":")
		self.b_cal = ( self.data.loc[ ( self.data['Start time'] > ( str(int(self.Breakfast[0])+1).zfill(2))+ self.Breakfast[1] + data.time_format )  & ( self.data['Start time'] < (Lu + data.time_format) ),'Calories (kcal)' ].sum() / self.length )
		if self.b_cal <=10.0:
			self.b_cal = 200.00
		self.t_b_cal = self.b_cal
		

		

class food(data):
	def print(self):
		#print(self.b_cal)
		#print(self.item)
		return str(self.b_cal)

	





def logg(request):
	if request.method == "POST":
		obj = meal_distribution.objects.get(User_no="1")
		Meal_name = obj.Meal_names.split(",")
		Meal_time = obj.Meal_times.split(",")
		Meal_calories = obj.Meal_calories.split(",")
		slot , name = (request.POST.getlist('Meal_names')) , (request.POST.getlist('Meal_items'))
		final_data = []
		for i in range(len(slot)):
			final_data.append(slot[i]+"+"+name[i])
		obj.Meal_items = (",".join(final_data)+","+ obj.Meal_items)
		obj.save()
		dic = {"Meal_name":(Meal_name),"Meal_time":(Meal_time),"Meal_calories":(Meal_calories),"Meal_items":(obj.Meal_items.split(","))}
		return render(request,"food_log.html",dic)




def home_page(request):
	
	try:
		obj = meal_distribution.objects.get(User_no="1",Date="2020-10-28")
	except:
		try:
			meal_distribution_form().save()
		except:
			obj = meal_distribution.objects.get(User_no="n/a")
			obj.User_no = "1"
			obj.Date = "2020-10-28"
	
	obj.save()
	
	if request.method == "POST":
		data_combine("/home/shri/Desktop/Daily Aggregations")
		Meal_calories = []
		objects=[]
		
		Meal_name = (request.POST.getlist('Meal_name'))
		Meal_time = (request.POST.getlist('Meal_time'))

		for i in range(len(Meal_name)):
			objects.append(food(Meal_name[i]))

		for i in range(len(Meal_name)-1):
			objects[i].calories(Meal_time[i],Meal_time[i+1])
		
		objects[-1].calories(Meal_time[-1],Meal_time[0])

		c = 0

		for i in objects:
			Meal_calories.append(i.print())
			c+=1	

		#obj.Date = str(datetime.datetime.now()).split(" ")[0]
		
	else:
		Meal_name = ""
		Meal_time = ""
		Meal_calories = ""

	obj.Meal_names = ",".join(Meal_name)
	obj.Meal_times = ",".join(Meal_time)
	obj.Meal_calories = ",".join(Meal_calories)
	obj.Meal_items = ""
	obj.save()
	dic = {"Meal_name":(Meal_name),"Meal_time":(Meal_time),"Meal_calories":(Meal_calories),"Meal_items":(obj.Meal_items.split(","))}
	if request.method == "POST":
		return render(request,"food_log.html",dic)
	else:
		return render(request,"index.html",dic)
