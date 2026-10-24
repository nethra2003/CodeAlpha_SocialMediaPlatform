from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username

class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(
        upload_to="post_images/",
        blank=True,
        null=True
    )

    video = models.FileField(
        upload_to="post_videos/",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Post by {self.author.username}"

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="social_comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username}"


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="social_likes"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["post", "user"],
                name="unique_user_post_like"
            )
        ]

    def __str__(self):
        return f"{self.user.username} likes post {self.post_id}"


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
    )
    followed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "followed"],
                name="unique_user_follow"
            ),
            models.CheckConstraint(
                condition=~models.Q(follower=models.F("followed")),
                name="prevent_self_follow"
            ),
        ]

    def __str__(self):
        return (
            f"{self.follower.username} follows "
            f"{self.followed.username}"
        )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
