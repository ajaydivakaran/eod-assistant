from django.db import models


class Contributor(models.Model):
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class EndOfDayItem(models.Model):
    description = models.TextField()
    contributors = models.ManyToManyField(Contributor)
    done_date = models.DateTimeField('Task done date', auto_now=True)

    def get_contributors(self):
        return [contributor.name for contributor in self.contributors.all()]

    def __str__(self):
        contributors = ", ".join(self.get_contributors())
        return "eod item on %s by %s" % (self.done_date.strftime('%d, %b %Y'), contributors)
