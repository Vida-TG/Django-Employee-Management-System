from django.contrib import admin
from polls.models import Question, Choice, Vote

admin.site.site_title = "EMS"
admin.site.site_header = "EMS Administration"

# Register your models here.
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Vote)