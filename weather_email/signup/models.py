from django.db import models

#Database model. Just need email and location which will be in the form of "StateAbbrv/City" for wunderground weather api
class Subscriber(models.Model):
	email = models.EmailField( unique = True )
	location = models.CharField( max_length=250 )

	def __str__(self):
		return self.email