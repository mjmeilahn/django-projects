from django.db import models

class Project (models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='resume/images/')
    url = models.URLField(blank=True)

    # DISPLAYS TITLE IN ADMIN
    def __str__ (self):
        return self.title