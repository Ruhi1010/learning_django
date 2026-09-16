from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class ChaiVarity(models.Model):
    CHAI_TYPE_CHOICE = [
        ('ML', 'MASALA'),
        ('GR', 'GREEN'),
        ('BL', 'BLACK'),
        ('HE', 'HERBAL'),
    ]
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='chai_images/')
    date = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=2, choices=CHAI_TYPE_CHOICE)
    description = models.TextField(default='')
    numbers = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.name
    
    
# One to Many relationship with User model
class ChaiReview(models.Model):
    chai = models.ForeignKey(ChaiVarity, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    comment = models.TextField(default='')
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES, default=0)
    date_added = models.DateTimeField(default=timezone.now)
    
    
    def __str__(self):
        return f'{self.user.username} review for {self.chai.name}'
    

# Many to Many relationship with User model
class Store(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    chai_varieties = models.ManyToManyField(ChaiVarity, related_name='stores')
    
    
    def __str__(self):
       return self.name 
   
   

# One to One relationship with User model
class ChaiCertificate(models.Model):
    chai = models.OneToOneField(ChaiVarity, on_delete=models.CASCADE, related_name='certificate')
    certificate_number = models.CharField(max_length=100)
    issued_date = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField()
    
    
    def __str__(self):
        return f'Certificate for {self.name.chai}'