from django.db import models
from django.contrib.auth.models import (
	AbstractUser,
	BaseUserManager,
	)

# Create your models here.

# Start Managers ---------------

class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email: str, password: str, **extra_fields: dict):
		if not email:
			raise ValueError("The given email must be set")
		email = self.normalize_email(email)
		user = self.model(email = email, **extra_fields)
		user.set_password(password)
		user.save(using = self.db)
		return user

	def create_user(self, email: str, password = None, **extra_fields: dict):
		extra_fields.setdefault("is_staff", False)
		extra_fields.setdefault("is_superuser", False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email: str, password: str, **extra_fields: dict):
		extra_fields.setdefault("is_staff", True)
		extra_fields.setdefault("is_superuser", True)

		if extra_fields.get("is_staff") is not True:
			raise ValueError(
				"Superuser must have is_staff=True")
		if extra_fields.get("is_superuser") is not True:
			raise ValueError(
				"Superuser must have is_superuser=True")
		return self._create_user(email, password, **extra_fields)

# End Managers ---------------

class User(AbstractUser):
	username = None
	email = models.EmailField('email address', unique = True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()

# simple prototype of Alsaheem Forms

# Fields
class Transmitter(models.Model):
	"""
	(WebFormAdmin is a confusing models name as
	it would be difficult to identify in the admin.py
	file so i'm opting for Transmitter and the end user
	models be renamed to Receiver, could have opted for
	something simpler like Producer and Consumer...not
	too sure if it clashes with class names in django-channels)

	Transmitter formally WebFormAdmin is the model for form creators
	this models saves their form definitions and also
	stores other related data needed for routing"""
	form_name = models.CharField( max_length = 100)
	slug = models.SlugField(blank = True)
	D_I = models.TextField(help_text = 'Descriptions or Instructions\
		 on how to fill the form', blank = True)

	def __str__(self):
		return self.form_name



class BasicEntry(models.Model):
	"""
	BasicEntry provides the form fields that
	does not require complexities like options
	or needs to be toggled"""
	e_fields = (
		('text','Text Field'),
		('email', 'Email Field'),
		('textarea','Multiline Text Field'),
		('date', 'Date Field'),
		('datetime', 'Date & Time Field'),
		('number','Number Field'),
		)

	transmitter = models.ForeignKey(
		Transmitter, 
		on_delete = models.CASCADE)

	field_name = models.CharField(max_length = 100)
	field_type = models.CharField(max_length = 100, choices = e_fields)

	def __str__(self):
		return  f"{self.transmitter.form_name} => {self.field_name}"


class SelectEntry(models.Model):
	"""
	SelectEntry is an advanced entry that provides
	facilities needed for Select options
	"""
	transmitter = models.ForeignKey(
		Transmitter, 
		on_delete = models.CASCADE)

	field_name = models.CharField(max_length = 100)

	def __str__(self):
		return f"{self.transmitter.form_name} => {self.field_name}"

	class Meta:
		verbose_name_plural = 'select entries'

         
class CheckBoxEntry(models.Model):
	"""
	CheckBoxEntry is an advanced entry that provides
	facilities needed for Checkboxes
	"""
	transmitter = models.ForeignKey(
		Transmitter, 
		on_delete = models.CASCADE)

	field_name = models.CharField(max_length = 100)

	def __str__(self):
		return self.transmitter.form_name

	class Meta:
		verbose_name_plural = 'checkbox entries'



class RadioEntry(models.Model):
	"""	
	RadioEntry is an advanced entry that provides
	facilities needed for Radio buttons"""
	
	transmitter = models.ForeignKey(
		Transmitter, 
		on_delete = models.CASCADE)

	field_name = models.CharField(max_length = 100)

	def __str__(self):
		return self.transmitter.form_name

	class Meta:
		verbose_name_plural = 'radio entries'


class Option(models.Model):
	"""
	Option is an abstract model(if that's a thing)
	some advanced entry optons inherit from it.

	Note: It does not need to be initiated directly"""
	option = models.CharField(max_length = 100)

	def __str__(self):
		try:
			return self.option_for.transmitter.form_name
		except:
			raise Exception("Option is an abstract model.\
			 Do not try creating instances of this model")


class SelectOption(Option):
	"""
	Options for SelectEntry"""
	option_for = models.ForeignKey(
		SelectEntry, 
		on_delete = models.CASCADE, 
		related_name = 'options')


class CheckBoxOption(Option):
	"""
	Options for CheckBoxEntry"""
	option_for = models.ForeignKey(
		CheckBoxEntry, 
		on_delete = models.CASCADE, 
		related_name = 'choices')


class RadioOption(Option):
	"""
	Options for RadioEntry"""
	option_for = models.ForeignKey(
		RadioEntry, 
		on_delete = models.CASCADE, 
		related_name = 'choices')


class Receiver(models.Model):
	"""
	This models is responsible for storing
	the data supplied by an end user based on a
	form supplied by the Transmitter"""
	transmitter = models.ForeignKey(
		Transmitter, 
		on_delete = models.CASCADE, 
		related_name = 'end_user_data')

	def __str__(self):
		return self.transmitter.form_name


class FinalData(models.Model):
	"""
	Every Form data input can be reduced to a 
	single unit so, data supplied by enduser from
	from BasicEntry, SelectEntry... will be saved on
	this model"""
	receiver = models.ForeignKey(
		Receiver, 
		on_delete = models.CASCADE, 
		related_name = 'response_data')

	for_field = models.CharField(max_length = 100)
	data_entry = models.CharField(max_length = 100)

	def __str__(self):
		return self.receiver.transmitter.form_name