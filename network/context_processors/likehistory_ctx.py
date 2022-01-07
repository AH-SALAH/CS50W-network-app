from datetime import datetime, timedelta
from django.contrib.postgres.aggregates.general import ArrayAgg
from django.db.models import Count, Prefetch, F
from network.models import Like, LikePost, Post, User
from django.utils.timezone import now as tz_now


def likehistory_ctx(request):
    last_likes_history = {}
    try:
        last_likes_posts = LikePost.objects.all()[:5]
        last_likes_history = Post.objects.filter(
            is_active=True,
            likepost__pk__in=[p.get("id") for p in last_likes_posts.values()],
        ).annotate(
            liker=F("likepost__like__user__username"),
            timestamp=F("likepost__time_stamp"),
        ).order_by('-timestamp')
        # print("lastlikes: ", last_likes_posts)
    except Exception as er:
        print("An exception occurred", er)

    return {"last_likes_history": [p for p in last_likes_history.values()]}
