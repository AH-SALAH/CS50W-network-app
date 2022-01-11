from django.contrib.postgres.aggregates.general import ArrayAgg
from django.db.models import Count
from network.models import Follow, Post, User
from django.core.paginator import Paginator


def following_ctx(request, user_slug=""):
    posts = []
    followings_count = 0
    try:

        if user_slug:
            user = User.objects.filter(username=user_slug).first()
        else:
            user = User.objects.filter(username=request.user).first()

        f = Follow.objects.filter(user=user)
        followings_posts = f.aggregate(
            result=ArrayAgg("followings__author"),
        )
        followings_count = f.aggregate(count=Count("followings")).get("count")

        posts = (
            Post.objects.filter(
                is_active=True, pk__in=[n for n in followings_posts.values()][0]
            )
            .order_by("-published_date")
            .annotate(
                likes_count=Count("liked_posts"),
                likers=ArrayAgg("liked_posts__user__username"),
            )
        )

    except Exception as er:
        print("An exception occurred:following_ctx: ", er)

    for p in posts:
        p.img = "https://api.lorem.space/image/face?w=50&h=50"

    # apply paginator
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return {
        # "followings_posts": posts,
        "followings_count": followings_count or 0,
        "followings_page_obj": page_obj,
        "followings_paginator": paginator,
    }
