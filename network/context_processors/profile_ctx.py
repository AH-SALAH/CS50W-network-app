from django.contrib.postgres.aggregates.general import ArrayAgg
from django.db.models import Count
from django.db.models.query import Prefetch
from network.models import Follow, Post, User
from django.core.paginator import Paginator


def profile_ctx(request, user_slug=""):
    posts = []
    user_followings_count = 0
    user_followers_count = 0
    user_followed = {}

    try:
        user = (
            User.objects.filter(username=user_slug).first()
            if user_slug
            else request.user
        )
        # user posts
        posts = (
            Post.objects.filter(is_active=True, user=user)
            .order_by("-published_date")
            .annotate(
                likes_count=Count("liked_posts"),
                likers=ArrayAgg("liked_posts__user__username"),
            )
        )
        # user followings
        user_followings_count = (
            Follow.objects.filter(user=user)
            .aggregate(count=Count("followings"))
            .get("count")
        )
        # user in followings?
        if user_slug:
            user_follow = (
                Follow.objects.filter(user=request.user)
                .prefetch_related(
                    Prefetch(
                        "followings", queryset=User.objects.filter(username=user_slug)
                    )
                )
                .first()
            )
            # print("uf: ", user_follow.followings.first(), user)
            user_followed = user_follow.followings.first()

        # people followed the user
        user_followers_count = Follow.objects.filter(followings__in=[user]).count()

    except Exception as er:
        print("An exception occurred", er)

    for p in posts:
        p.img = "https://api.lorem.space/image/face?w=50&h=50"

    # apply paginator
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return {
        # "user_posts": posts,
        "user_followings_count": user_followings_count,
        "user_followers_count": user_followers_count,
        "is_user_followed": "true" if user_followed else "false",
        "user_followed": user.pk,
        "user_page_obj": page_obj,
        "user_paginator": paginator,
    }
