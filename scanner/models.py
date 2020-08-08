from django.db import models

class Scanner(models.Model):  
    input_Image = models.ImageField(upload_to='images/')
    image_Text = models.CharField(max_length=1000)  

# Create your models here.
