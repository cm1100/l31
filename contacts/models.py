from django.db import models

# Create your models here.



class CollegeName(models.Model):

    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)

class CollegeContact(models.Model):

    emails = models.TextField()
    numbers = models.TextField()
    college=models.ForeignKey(CollegeName,on_delete=models.CASCADE)

    def __str__(self):
        return self.college
