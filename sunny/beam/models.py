""" Models """
from django.db import models


class Day(models.Model):
    """ A Day """
    date = models.DateField()
    today = models.FloatField(null=True)
    total = models.FloatField(null=True)

    def __unicode__(self):
        return "%s" % self.date


class Hour(models.Model):
    """ An Hour """
    day = models.ForeignKey('Day', on_delete=models.CASCADE)
    time = models.TimeField()
    hour = models.IntegerField()
    power = models.FloatField()

    def __unicode__(self):
        return "%s %0.3f" % (self.time, self.power)

# EOF
