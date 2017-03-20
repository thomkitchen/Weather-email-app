from django.core.management.base import BaseCommand, CommandError
from signup.models import Subscriber
import urllib2
from weather_email.send_email import SendEmail

import json

class Command(BaseCommand):
	help = 'Creates the body of the email'

	def get_current_weather(self, location):
		url = 'http://api.wunderground.com/api/675a3ab09ec5ada7/geolookup/conditions/q/' + location + '.json'
		f = urllib2.urlopen(url).read().decode('utf-8')
		parsed_json = json.loads(f)
		city = parsed_json['location']['city']
		state = parsed_json['location']['state']
		temp_f = parsed_json['current_observation']['temp_f']
		precipitation = float(parsed_json['current_observation']['precip_today_in'])
		weather_description = parsed_json['current_observation']['weather']
		image_url = parsed_json['current_observation']['icon_url']
		return city, state, temp_f, precipitation, weather_description, image_url

	def get_average_temp(self, location):
		url = 'http://api.wunderground.com/api/675a3ab09ec5ada7/almanac/q/' + location + '.json'
		f = urllib2.urlopen(url).read().decode('utf-8')
		parsed_json = json.loads(f)
		avg_temp_f = parsed_json['almanac']['temp_high']['normal']['F']
		return avg_temp_f

	def create_message(self, cust):
		city, state, temp, precip, weather_description, image_url = self.get_current_weather(cust.location)
		avg_temp = self.get_average_temp(cust.location)
		temp_difference = float(temp) - float(avg_temp)
		message = '<img src="' + image_url + '"><p>Current temperature in ' + city + ', ' + state + ' is: ' + str(temp) + ' F (as compared to the average temperature a year ago of ' + avg_temp +' F) and ' + weather_description.lower() + '.'
		if precip > 0:
			message += " Current accumulated precipitation of " + str(precip) + " inches."
		message += '</p>'
		status = 'average'
		nice_weather = ['sun', 'clear']
		if temp_difference > 5.0 or any( x in weather_description.lower() for x in nice_weather):
			status = 'nice_out'
		elif precip > 0 or temp_difference < -5.0:
			status = 'not_so_nice_out'
		return status, message

	def create_email(self, cust):
		weather, body = self.create_message(cust)
		recipient = cust.email
		subject = ''
		if weather == 'nice_out':
			subject = "It's nice out! Enjoy a discount on us."

		elif weather == 'not_so_nice_out':
			subject = "Not so nice out? That's okay, enjoy a discount on us."

		else:
			subject = "Enjoy a discount on us."
		return recipient, subject, body

	def send_emails(self):
		email = SendEmail()
		customers = Subscriber.objects.all()
		#Make sure there are actually users to email first. If not, print out and exit
		if len(customers) == 0:
			self.stdout.write("No users to email")
			return False
		for cust in customers:
			to, sub, body = self.create_email(cust)
			email.send( to, sub, body)

	def handle(self, *args, **options):
		self.send_emails()