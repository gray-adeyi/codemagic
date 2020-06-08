from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.contrib import messages
from django.views.generic import View, TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .forms import UserCreationForm, DemoForm
from .models import (
	Transmitter,
	Receiver,
	FinalData)
# Create your views here.

class SignupView(FormView):
	template_name = "web_forms/signup.html"
	form_class = UserCreationForm
	success_urls = reverse_lazy('web_forms:dashboard')

	def form_valid(self, form):
		response = super().form_valid(form)
		form.save()
		email = form.cleaned_data.get("email")
		raw_password = form.cleaned_data.get("password1")
		user = authenticate(email = email, password = raw_password)
		login(self.request, user)
		form.send_mail()
		messages.info(
			f"Welcome onboard {form.cleaned_data.get('first_name')}")
		return response

class LoginView(TemplateView):
	template_name = 'web_forms/login.html'


class ForgotPasswordView(TemplateView):
	template_name = 'web_forms/forgotpassword.html'

class AboutView(TemplateView):
	template_name = 'web_forms/about.html'


class DemoFormView(View):

	def get(self, request):
		"""
		This is a demo version of the original implementation
		i only did this to clear out doubts of the possibility
		It's not a big deal but its somewhat clever. front end for
		from ceation has not been implemented yet so you have to use
		the admin. but if it's possible in the admin, it's possible in
		the front end. the idea is that form creators are Transmitters
		they transmit there forms to Receivers who inturn populate the
		fields the transmitter emits. The concept is similar to Producers
		and Consumers but i chose Transmitter and Receiver incase of and
		name conflict. the forms are dynamically generated in the template
		check out BASE_DIR/web_forms/templates/web_forms/demo.html for details"""
		template_name = 'web_forms/demo.html'
		context = {}
		context['transmitter'] = get_object_or_404(Transmitter, pk= 1)
		return render(request, template_name, context)

	def post(self, request):
		transmitter = get_object_or_404(Transmitter, pk = 1)
		new_receiver_input = Receiver.objects.create(transmitter=transmitter)
		new_receiver_input.save()
		for basic_entry in transmitter.basicentry_set.all():
			field = slugify(basic_entry.field_name)
			new_field_entry = request.POST.get(field)
			new_final_data = FinalData.objects.create(
				receiver=new_receiver_input, 
				for_field=field, 
				data_entry=new_field_entry)
			new_final_data.save()
		messages.info(request, 'Your data has been successfully uploaded')
		return HttpResponseRedirect(reverse('web_forms:demo'))


class DemoFormDetail(DetailView):
	model = Transmitter
	template_name = 'web_forms/demo_detail.html'