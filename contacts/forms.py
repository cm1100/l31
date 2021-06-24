from django.forms import ModelForm
from .models import CollegeName



class CollegeForm(ModelForm):

    class Meta:
        model = CollegeName
        fields=["name"]

