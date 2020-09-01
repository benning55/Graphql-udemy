from django.db import models


class Director(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Directors"


class Movies(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField(default=2000)
    director = models.ForeignKey(Director, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Movies"
