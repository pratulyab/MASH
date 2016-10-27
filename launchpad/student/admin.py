from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Student, Domain

# Register your models here.

class StudentAdmin(admin.ModelAdmin):
	fieldsets = (
		(_('Personal Details'), {'fields': ('first_name','last_name','email','gender','dob','phone_number',)}),
		(_('Education Details'), {'fields': ('college','course','year','resume')}),
		(_('Other Details'), {'fields': ('interested_domains','availibility','credits','work_from_home','experiences')})
	)

	list_display = ['full_name', 'email', 'phone_number', 'college', 'availibility', 'credits']

	def full_name(self, obj):
		return obj.get_full_name()
	
	full_name.short_description = 'Full Name'

admin.site.register(Student, StudentAdmin)
admin.site.register(Domain)
