from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from django.utils.timezone import now as tz_now
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# repeated strs
CREATION_DATE = _("creation date")
MODIFIED_DATE = _("last modified")


class User(AbstractUser):
    phone = models.CharField(
        _("phone"), max_length=11, blank=True, null=True, unique=True
    )
    email = models.EmailField(
        _("email address"), max_length=100, null=True, unique=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class Post(models.Model):
    """Model definition for Post."""

    user = models.ForeignKey(
        get_user_model(),
        verbose_name=_("author"),
        on_delete=models.CASCADE,
        related_name="author",
    )
    content = models.TextField(_("content"))
    is_active = models.BooleanField(_("is_active"), default=True)
    creation_date = models.DateTimeField(CREATION_DATE, auto_now_add=True)
    modified_date = models.DateTimeField(MODIFIED_DATE, auto_now=True)
    published_date = models.DateTimeField(_("published date"), default=tz_now)

    class Meta:
        """Meta definition for Post."""

        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ("-published_date",)

    def __str__(self):
        """Unicode representation of Post."""
        return f"{self.content[:20]}... ({self.user.username})"


class Follow(models.Model):
    """Model definition for Follower."""

    user = models.OneToOneField(
        get_user_model(),
        verbose_name=_("follower"),
        on_delete=models.CASCADE,
        related_name="follower_user",
    )
    followings = models.ManyToManyField(
        get_user_model(),
        verbose_name=_("followings"),
        related_name="user_followings",
        blank=True,
    )
    creation_date = models.DateTimeField(CREATION_DATE, auto_now_add=True)
    modified_date = models.DateTimeField(MODIFIED_DATE, auto_now=True)

    class Meta:
        """Meta definition for Follow."""

        verbose_name = "Follow"
        verbose_name_plural = "Follows"
        ordering = ("-creation_date",)

    def __str__(self):
        """Unicode representation of Follow."""
        followed = ", ".join([str(p.username) for p in self.followings.all()][:5])
        return f"{self.user.username} - ({followed} )..."


class Like(models.Model):
    """Model definition for Like."""

    user = models.OneToOneField(
        get_user_model(),
        verbose_name=_("liker"),
        on_delete=models.CASCADE,
        related_name="liker_user",
    )
    posts = models.ManyToManyField(
        "post",
        verbose_name=_("liked Posts"),
        related_name="liked_posts",
        blank=True,
        through="LikePost",
    )
    creation_date = models.DateTimeField(CREATION_DATE, auto_now_add=True)
    modified_date = models.DateTimeField(MODIFIED_DATE, auto_now=True)

    class Meta:
        """Meta definition for Like."""

        verbose_name = "Like"
        verbose_name_plural = "Likes"
        ordering = ("-creation_date",)

    def __str__(self):
        """Unicode representation of Like."""
        posts = ", ".join(str(p.content[:20]) for p in self.posts.all())[:200]
        return f"{self.user.username} - ({posts}) ..."

    # def get_absolute_url(self):
    #     """Return absolute url for Like."""
    #     return ('')


class LikePost(models.Model):
    """Model definition for Liked Post intermediate."""

    like = models.ForeignKey(Like, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(_('time stamp'), auto_now_add=True)

    class Meta:
        """Meta definition for Liked post."""

        ordering = ("-time_stamp",)
        db_table = "network_like_post"
