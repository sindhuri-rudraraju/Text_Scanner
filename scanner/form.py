from django import forms 
from .models import *
  
class ImageForm(forms.ModelForm): 
  
    class Meta: 
        model = Scanner
        fields = ['input_Image'] 
