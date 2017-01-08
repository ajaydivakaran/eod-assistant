from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=50)


class Contributor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    display_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    team = models.ForeignKey(Team)

    def __str__(self):
        return self.display_name


class EndOfDayItem(models.Model):
    description = models.TextField()
    story_id = models.CharField(max_length=30)
    contributors = models.ManyToManyField(Contributor)
    created_date = models.DateTimeField('End of day item done date', auto_now=True)

    def get_contributors(self):
        return [contributor.name for contributor in self.contributors.all()]

    def __str__(self):
        contributors = ", ".join(self.get_contributors())
        return "eod item id '%s on %s by %s" % (self.story_id, self.done_date.strftime('%d, %b %Y'), contributors)


class DispatchRule(models.Model):
    type = models.CharField(max_length=30)
    hour = models.IntegerField()
    minute = models.IntegerField()
