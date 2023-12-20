from django.conf import settings
from django.db import models
from django.utils import timezone

class Post(models.Model):
        models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete = models.CASCADE)
        title = models.CharField(max_length=200)
        text = models.TextField()
        created_date = models.DateTimeField(
            default=timezone.now)
        published_date = models.DateTimeField(
            blank=True, null=True)
        
        image = models.ImageField(upload_to='introducer_image/%Y/%m/%d/')
        meal = models.IntegerField(default=0)
        
        def save(self, *args, **kwargs):
        # Set meal based on the hour of the published_date
            if self.published_date:
                hour = self.published_date.hour
                if 6 <= hour < 12:
                    self.meal = 0
                elif 12 <= hour < 17:
                    self.meal = 1
                elif 17 <= hour <= 24:
                    self.meal = 2
                    
            super().save(*args, **kwargs)
        
        def publish(self):
            self.published_date = timezone.now()
            self.save()


        def __str__(self):
            return self.title