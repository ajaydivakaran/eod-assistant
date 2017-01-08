from django.contrib import admin

from .models import Contributor, Team, EndOfDayItem, DispatchRule

admin.site.register(Contributor)
admin.site.register(Team)
admin.site.register(EndOfDayItem)
admin.site.register(DispatchRule)
