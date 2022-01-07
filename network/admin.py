from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Post, Follow, Like, User
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm,
)
from django.utils.timezone import now as tz_now


class UserCreationForm(UserCreationForm):
    """A form for creating users."""

    class Meta:
        model = get_user_model()
        fields = ("username", "email")

class UserChangeForm(UserChangeForm):
    """A form for updating users."""

    class Meta:
        model = get_user_model()
        fields = "__all__"

@admin.register(get_user_model())
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "phone")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )


admin.site.register(Post)


class FollowChangeForm(forms.ModelForm):
    """
    customize field queryset
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print("instance: ", self.current_user.pk)
        # self.fields["followings"].queryset = User.objects.exclude(
        #     pk=self.current_user.pk
        # )

    class Meta:
        model = Follow
        fields = "__all__"

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    form = FollowChangeForm
    filter_horizontal = ("followings",)

    def get_form(self, request, *args, **kwargs):
        form = super(FollowAdmin, self).get_form(request, *args, **kwargs)
        form.current_user = request.user
        return form


class LikeChangeForm(forms.ModelForm):
    """
    customize field queryset
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["posts"].queryset = Post.objects.exclude(user=self.current_user)

    class Meta:
        model = Like
        fields = "__all__"

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    form = LikeChangeForm
    filter_horizontal = ("posts",)

    def get_form(self, request, *args, **kwargs):
        form = super(LikeAdmin, self).get_form(request, *args, **kwargs)
        form.current_user = request.user
        return form
