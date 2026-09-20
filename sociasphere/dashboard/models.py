from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class Post(models.Model):
    user = models.ForeignKey(
        User,
        related_name="posts",
        on_delete=models.CASCADE,
    )
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="post_like", blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user} ({self.created_at:%Y-%m-%d %H:%M}): {self.body}..."


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True,
    )
    date_modified = models.DateTimeField(auto_now=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    profile_bio = models.CharField(null=True, blank=True, max_length=500)
    homepage_link = models.CharField(null=True, blank=True, max_length=100)
    facebook_link = models.CharField(null=True, blank=True, max_length=100)
    instagram_link = models.CharField(null=True, blank=True, max_length=100)
    linkedin_link = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.user.username


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile.objects.create(user=instance)
        user_profile.follows.add(user_profile)


post_save.connect(create_profile, sender=User)
