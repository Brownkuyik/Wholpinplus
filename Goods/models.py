from django.db import models

# Create your models here.


class CompanyId(models.Model):
    name = models.CharField(max_length=100, help_text='Name of the company')
    street = models.CharField(max_length=300, help_text='company street name and number')
    L_G_A = models.CharField(max_length=70, help_text='local govername of location')
    state = models.CharField(max_length=90, help_text='Company state')
    country = models.CharField(max_length=50, help_text='country of location', default='NIGERIA')
    Email  = models.EmailField(editable=True, unique=True)
    contact = models.IntegerField()
    twitter_handel = models.CharField(max_length=300, help_text='company twitter profile', unique=True)
    facebook = models.CharField(max_length=300, help_text='Facebook account')
    instagram = models.CharField(max_length=700, help_text='instagram handel')
    skype = models.CharField(max_length=700, help_text='skype handel')
    linkin = models.CharField(max_length=700, help_text='linkage handel')
    logo = models.ImageField(upload_to='companyLogo')


    def __str__(self):
        return f'{self.name} company located at {self.L_G_A} at {self.state}, {self.country}. You can contact them at [+234] {self.contact}'

