from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Contributor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    display_name = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    team = models.ManyToManyField(Team)

    def __str__(self):
        return self.display_name


class EndOfDayItem(models.Model):
    description = models.TextField()
    story_id = models.CharField(max_length=30)
    contributors = models.ManyToManyField(Contributor)
    created_date = models.DateTimeField('End of day item done date', auto_now=True)
    team = models.ForeignKey(Team)

    def get_contributors(self):
        return [contributor.name for contributor in self.contributors.all()]

    def __str__(self):
        return self.story_id


def _validate_known_type(value):
    if value not in ['FIXED_TIME']:
        raise ValidationError(_('%(value) is not a known type'), params={'value': value}, )


class DispatchRule(models.Model):
    type = models.CharField(max_length=30, validators=[_validate_known_type])
    hour = models.IntegerField()
    minute = models.IntegerField()
    team = models.ForeignKey(Team)

    def __str__(self):
        return "Rule %s: hour: %s minute: %s" % (self.type, self.hour, self.minute)
