from django.contrib import admin

from eod.models import Contributor, EndOfDayItem

admin.site.register(Contributor)
admin.site.register(EndOfDayItem)
