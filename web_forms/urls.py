from django.urls import path
from .views import (
	SignupView,
	LoginView,
	ForgotPasswordView,
	AboutView,
	DemoFormView,)

app_name = 'web_forms'

urlpatterns = [
	path(
		"",
		LoginView.as_view(),
		name = 'login'),
	path(
		"signup/",
		SignupView.as_view(),
		name = 'signup'),
	path(
		"forgot-password/",
		ForgotPasswordView.as_view(),
		name = 'forgot-password'),
	path(
		"about/",
		AboutView.as_view(),
		name = 'about'),
	path(
		'demo',
		DemoFormView.as_view(),
		name = 'demo'),
	]