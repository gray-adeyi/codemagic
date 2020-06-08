from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import (
	Transmitter,
	Receiver,
	BasicEntry,
	SelectEntry,
	CheckBoxEntry,
	RadioEntry,
	SelectOption,
	CheckBoxOption,
	RadioOption,
	FinalData,
	User)

# Start Inlines --------------------------------------

class BasicEntryInline(admin.StackedInline):
	model = BasicEntry
	extra = 1

class SelectEntryInline(admin.StackedInline):
	model = SelectEntry
	extra = 1

class CheckBoxEntryInline(admin.StackedInline):
	model = CheckBoxEntry
	extra = 1

class RadioEntryInline(admin.StackedInline):
	model = RadioEntry
	extra = 1

class SelectOptionInline(admin.StackedInline):
	model = SelectOption
	extra = 1

class CheckBoxOptionInline(admin.StackedInline):
	model = CheckBoxOption
	extra = 1

class RadioOptionInline(admin.StackedInline):
	model = RadioOption
	extra = 1

class ReceiverInline(admin.StackedInline):
	model = Receiver
	extra = 1

class FinalDataInline(admin.StackedInline):
	model = FinalData
	extra = 1
# End Inlines --------------------------------------



# Start ModelAdmin --------------------------------------

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
	fieldsets = (
		(None, {'fields':('email','password')}),
		(
			"Personal Info",
			{"fields":("first_name", "last_name")},
			),
		(
			"Permissions",
			{
			"fields":(
				"is_active",
				"is_staff",
				"is_superuser",
				"groups",
				"user_permissions",
				)
			},
			),
		(
			"Important Dates",
			{"fields": ('last_login','date_joined')},
			),
		)

	add_fieldsets = (
		(
			None,
			{
			"classes":("wide",),
			"fields":("email","password1","password2"),
			},
			),
		)
	list_display = (
		"email",
		"first_name",
		"last_name",
		)
	ordering = ("email",)

@admin.register(Transmitter)
class TransmitterAdmin(admin.ModelAdmin):
	
	inlines = [
		BasicEntryInline,
		SelectEntryInline,
		CheckBoxEntryInline,
		ReceiverInline,]

	prepopulated_fields = {"slug": ("form_name",)}
	search_fields = ('form_name',)

@admin.register(SelectEntry)
class SelectEntryAdmin(admin.ModelAdmin):

	autocomplete_fields = ('transmitter',)
	search_fields = ('transmitter__form_name',)
	list_display = ('transmitter_tag','field_name',)
	inlines = [SelectOptionInline,]

	def transmitter_tag(self, obj):
		return obj.transmitter.form_name

@admin.register(CheckBoxEntry)
class CheckBoxEntryAdmin(admin.ModelAdmin):

	autocomplete_fields = ('transmitter',)
	search_fields = ('transmitter__form_name',)
	list_display = ('transmitter_tag','field_name',)
	inlines = [CheckBoxOptionInline,]

	def transmitter_tag(self, obj):
		return obj.transmitter.form_name


@admin.register(RadioEntry)
class RadioEntryAdmin(admin.ModelAdmin):

	autocomplete_fields = ('transmitter',)
	search_fields = ('transmitter__form_name',)
	list_display = ('transmitter_tag','field_name',)
	inlines = [RadioOptionInline,]

	def transmitter_tag(self, obj):
		return obj.transmitter.form_name


@admin.register(Receiver)
class ReceiverAdmin(admin.ModelAdmin):
	inlines = [
		FinalDataInline,]

	list_display = ('transmitter',)

	def transmitter(self, obj):
		return obj.transmitter.form_name


# End ModelAdmin --------------------------------------

