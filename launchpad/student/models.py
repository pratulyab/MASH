from django.core import validators
from django.db import models
from django.db.models.signals import pre_save
from django.db.utils import IntegrityError
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from college.models import College, Course
import re
from decimal import Decimal

# Create your models here.


class Domain(models.Model):
	name = models.CharField(_('Name'), max_length=60, unique=True)
	desc = models.TextField(_('Description'), blank=True)

	def __str__(self):
		return self.name.title()


class Student(models.Model):
	GENDER_CHOICES = (
			('M', _('Male')),
			('F', _('Female')),
			('O', _('Other')),
	)
	
	# Personal Details
	first_name = models.CharField(_('First Name'), max_length=40)
	last_name = models.CharField(_('Last Name'), max_length=40, blank=True)
	gender = models.CharField(_('Gender'), choices=GENDER_CHOICES, max_length=1, default=GENDER_CHOICES[0][0], blank=True)
	dob = models.DateField(_('Date Of Birth'), null=True, blank=True)
	email = models.EmailField(_('Email ID'), unique=True, 
				error_messages = {
					'unique': _("Student with email address already exists."),
				}
		)
	phone_number = models.CharField(_('Phone Number'), max_length=10, unique=True,
			help_text = "10 Digit IN Number",
			validators = [
				validators.RegexValidator(regex=r'^[7-9]\d{9}$', message="_('Invalid IN phone number. Make sure not to \
																			prefix the number with either +91 or 0.')"),
			],
			error_messages = {
				'unique': _("Student with that phone number already exists."),
			}
		)

	# Educational Details
	college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='students')
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
	year = models.CharField(_('Current Year'), choices=Course.YEAR_CHOICES, max_length=1)
#	resume = models.FileField(_('Resume'), upload_to='student/resume')
	resume = models.URLField(_('Dropbox Link'),
			help_text = _("Dropbox link to the student's recently uploaded resume."),
			validators = [
				validators.RegexValidator(
					regex=r'^https?://(www\.)?dropbox.*$',flags=re.I, message="Invalid dropbox folder link"
				), # Validating the dropbox url
			],
		)

	# Other Details
	work_from_home = models.BooleanField(default=False,
			help_text = "Prefer work from home?",
		)
#	is_intern = models.BooleanField(default=False)
	credits = models.DecimalField(max_digits=5, decimal_places=2, default=0, # Max 999.xx
			validators = [
				validators.MinValueValidator(Decimal('0'))
			],
		)
	availibility = models.BooleanField(default=True)
	interested_domains = models.ManyToManyField(Domain, verbose_name=_('Interests'), related_name="students",
			help_text = "Domains interested in for internship",
		)
	experiences = models.TextField(_('Domain Experiences'), blank=True,
			help_text = "Details about the experiences in the mentioned domains (if any)",
		)
#	date_joined = models.DateTimeField(_('Date Joined'), default=timezone.now)
	date_joined = models.DateTimeField(_('Date Joined'), auto_now_add=True)

	def get_full_name(self):
		return (("%s %s") % (self.first_name, self.last_name)).title()
	
	def __str__(self):
		return self.get_full_name()


@receiver(pre_save, sender=Student)
def validate_student(sender, **kwargs):
	student = kwargs.pop('instance')
	college = student.college
	course = student.course
	if college and course:
		if not college.courses.filter(pk=course.pk):
			raise IntegrityError(_("Invalid college and course options."))
		elif int(student.year) > int(student.course.max_years):
			raise IntegrityError(_("Invalid current year. Exceeds the max duration offered by the course."))
