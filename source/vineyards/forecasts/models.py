from django.db import models


class ExistingVineyard(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return 'x - {0}, y - {1}, name - {2}'.format(self.x, self.y, self.name)
