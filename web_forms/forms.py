from django import forms
from django.contrib.auth.forms import (
	UserCreationForm as DjangoUserCreationForm)
from django.contrib.auth.forms import UsernameField
from django.core.mail import send_mail
from .models import User, Transmitter

class UserCreationForm(DjangoUserCreationForm):
	class Meta(DjangoUserCreationForm.Meta):
		model = User
		fields = ("email","first_name","last_name",)
		field_classes = {"email": UsernameField}

	def send_mail(self):
		message = f"{self.cleaned_data['first_name']}\
		 welcome to Rapid Forms\nYou can start creating\
		  your forms\nBest Regards,"
		send_mail(
			"Welcome to Rapid Forms",
			message,
			"info@rapidforms.com",
			[self.cleaned_data["email"]],
			fail_silently = True,
			)


class DemoForm(forms.ModelForm):
	class Meta:
		model = Transmitter
		fields = '__all__'