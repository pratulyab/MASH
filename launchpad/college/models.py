from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Course(models.Model):
	YEAR_CHOICES = (
		('1','1'),
		('2','2'),
		('3','3'),
		('4','4'),
		('5','5'),
		('6','6'),
	)
	name = models.CharField(_('Course Name'), max_length=64, unique=True)
	desc = models.TextField(_('Description'), blank=True)
	max_years = models.CharField(_('Years'), max_length=1, choices=YEAR_CHOICES,
			help_text = "Maximum duration this course offers.",
		)

	def __str__(self):
		return self.name.strip()

class College(models.Model):
	name = models.CharField(_('College Name'), max_length=200, unique=True)
	details = models.TextField(blank=True)
	courses = models.ManyToManyField(Course, related_name="colleges")
	website = models.URLField(blank=True)

	def __str__(self):
		return self.name.strip()
