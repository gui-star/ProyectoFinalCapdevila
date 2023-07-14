from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

class Blog(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='blogImages', blank=True, null=True)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.title

    def calculate_average_rating(self):
        average_rating = self.ratings.aggregate(Avg('rating'))['rating__avg']
        if average_rating is not None:
            self.rating = round(average_rating, 1)
        else:
            self.rating = 0.0
        self.save()

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]
    
from django.contrib.auth.models import User

class Rating(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(0.1), MaxValueValidator(5.0)])
