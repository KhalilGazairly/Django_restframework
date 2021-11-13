from django.db import models

#
# class Cast(models.Model):
#     name = models.CharField(max_length=250)
#     job_title = models.CharField(max_length=200)
#     age = models.IntegerField()
#
#     def __str__(self):
#         return self.name
#
#
# class Category(models.Model):
#     type = models.CharField(max_length=200)
#
#     def __str__(self):
#         return self.type


class Media(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    poster = models.ImageField(upload_to='pinterest_poster')
    # cast = models.ManyToManyField('Cast')
    # categories = models.ManyToManyField('Category')

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Movie(Media):
    pass

    def __str__(self):
        return self.title


class Series(Media):
    season = models.CharField(max_length=250)
    episode = models.CharField(max_length=200)

    def __str__(self):
        return self.title

