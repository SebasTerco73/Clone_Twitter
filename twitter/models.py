from django.db import models
# tabla usuario, predefinida por django
from django.contrib.auth.models import User
# zona horaria
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Char = max_length (obligatorio), y se almacena como VARCHAR
    bio = models.CharField(default="Hola twitteer", max_length=100)
    image = models.ImageField(default='default.png')

    def __str__(self):
        return f'Perfil de {self.user.username}'
    
    def following(self):
        user_ids = Relationship.objects.filter(from_user=self.user).values_list('to_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)
    
    def followers(self):
        user_ids = Relationship.objects.filter(to_user=self.user).values_list('from_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)


    
class Post(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    # Text = No necesita max_length, y se almacena como TEXT
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    class Meta:
        # ordering modelo interno de django, necesita tener el nombre exacto
        ordering = ['-timestamp']

    def __str__(self):
        return self.content

class Relationship(models.Model):
     from_user = models.ForeignKey(User, related_name='relationships', on_delete=models.CASCADE)
     to_user = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)

     def __str__(self):
         return f'{self.from_user} to {self.to_user}'