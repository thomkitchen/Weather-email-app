from django import forms
from .models import Subscriber as sub
from .choices import cities

#Create the forms to be used to capture user input
class AddSub(forms.ModelForm):
	email = forms.EmailField( label="Email: ", initial='', widget=forms.EmailInput(attrs={'class':'form-control'}), required = True)
	location = forms.ChoiceField( choices = sorted( cities ), label= "Location: ", widget=forms.Select(attrs={'class':'form-control'}), required = True)
	class Meta:
		model = sub
		fields = ('email', 'location')