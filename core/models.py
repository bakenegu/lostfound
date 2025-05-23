from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
    @property
    def match_count(self):
        from .models import Match  # local import to avoid circular import
        return Match.objects.filter(
            models.Q(lost_item__user=self.user) |
            models.Q(found_item__user=self.user)
        ).count()

class LostItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_lost = models.DateField()
    location = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

class FoundItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='found_photos/')
    location = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

class Match(models.Model):
    lost_item = models.ForeignKey(LostItem, on_delete=models.CASCADE)
    found_item = models.ForeignKey(FoundItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Match: {self.lost_item.title} ↔ {self.found_item.title}"
