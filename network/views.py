from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Count
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.expressions import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.paginator import Paginator
from django.utils.text import slugify
from network.context_processors.following_ctx import following_ctx
from network.context_processors.likehistory_ctx import likehistory_ctx
from network.context_processors.profile_ctx import profile_ctx
import json

from .models import Follow, Like, Post, User


def index(request):
    posts = []
    try:
        p_type = request.GET.get("nt")

        posts = (
            Post.objects.filter(is_active=True)
            .order_by("-published_date")
            .annotate(
                likes_count=Count("liked_posts"),
                likers=ArrayAgg("liked_posts__user__username"),
            )
        )

    except Exception as er:
        print("An exception occurred", er)

    # posts = json.loads(serialize('json', list(posts), fields=('user__username', 'content', 'published_date', 'is_active')))

    # for p in posts:
    #     p.add('img', "https://api.lorem.space/image/face?w=50&h=50")

    # apply paginator
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    ctx = {
        # "posts": posts,
        "nt": p_type,
        "page_obj": page_obj,
        "paginator": paginator,
    }

    return render(request, "network/index.html", ctx)


def profile(request, user_slug):
    posts = []
    p_ctx = {}
    p_type = request.GET.get("nt")

    try:
        if user_slug:
            p_ctx = profile_ctx(request, user_slug=user_slug)

        posts = (
            Post.objects.filter(is_active=True)
            .order_by("-published_date")
            .annotate(
                likes_count=Count("liked_posts"),
                likers=ArrayAgg("liked_posts__user__username"),
            )
        )

    except Exception as er:
        print("An exception occurred", er)

    for p in posts:
        p.img = "https://api.lorem.space/image/face?w=50&h=50"

    # apply paginator
    # paginator = Paginator(posts, 6)
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)

    ctx = {
        # "posts": posts,
        "nt": p_type or "profile",
        "usr_slg": user_slug,
        # "page_obj": page_obj,
        # "paginator": paginator,
        **p_ctx,
    }

    return render(request, "network/index.html", ctx)


def following(request, user_slug):
    posts = []
    p_ctx = {}
    try:
        if user_slug:
            p_ctx = following_ctx(request, user_slug=user_slug)

        p_type = request.GET.get("nt")

        posts = (
            Post.objects.filter(is_active=True)
            .order_by("-published_date")
            .annotate(
                likes_count=Count("liked_posts"),
                likers=ArrayAgg("liked_posts__user__username"),
            )
        )

    except Exception as er:
        print("An exception occurred", er)

    for p in posts:
        p.img = "https://api.lorem.space/image/face?w=50&h=50"

    # apply paginator
    # paginator = Paginator(posts, 6)
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)

    ctx = {
        # "posts": posts,
        "nt": p_type or "following",
        "usr_slg": user_slug,
        # "page_obj": page_obj,
        # "paginator": paginator,
        **p_ctx,
    }

    return render(request, "network/index.html", ctx)


def like(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Not Authenticated"}, status=401)

    if request.method == "POST":
        try:
            # print("data: ", json.loads(request.body))
            body = json.loads(request.body)
            post_pk = body["pk"]
        except Exception as er:
            print("An exception occurred", er)

        if not post_pk:
            return JsonResponse({"error", "No pk found"}, status=404)

        def add_post(entity):
            """add a new post in likes model"""
            entity.posts.add(post_pk)
            post = (
                Post.objects.filter(pk=post_pk)
                .annotate(
                    likes_count=Count("liked_posts"),
                )
                .first()
            )
            return {"post": post, "status": True}

        def remove_post(entity):
            """remove a post in likes model"""
            entity.posts.remove(post_pk)
            post = (
                Post.objects.filter(pk=post_pk)
                .annotate(
                    likes_count=Count("liked_posts"),
                )
                .first()
            )
            return {"post": post, "status": False}

        lyk = {}
        try:
            lyk, created = Like.objects.get_or_create(user=request.user)

            def resp_data(resp):
                return {
                    "pk": resp.get("post").id,
                    "likes_count": resp.get("post").likes_count,
                    "status": resp.get("status"),
                }

            # if like model found for the user
            if lyk:
                # get the post if found
                post = lyk.posts.get(pk=post_pk)

                if post:
                    # and remove/toggle it
                    resp = remove_post(lyk)

                    return JsonResponse(
                        resp_data(resp),
                        status=200,
                    )
            # if a new like model has created for this user
            if created:
                # then there are no posts have been liked yet, add this post to the list
                resp = add_post(lyk)
                return JsonResponse(
                    resp_data(resp),
                    status=200,
                )
        # if getting this post did an exception, then this post is not found in liked posts list for this user
        except Post.DoesNotExist:
            # so add it
            resp = add_post(lyk)
            return JsonResponse(
                resp_data(resp),
                status=200,
            )

        except Exception as er:
            print("An exception occurred", er)


def last_likes(request):
    # if not request.user.is_authenticated:
    #     return JsonResponse({"error": "Not Authenticated"}, status=401)

    try:
        last_likes = likehistory_ctx(request)
    except Exception as er:
        print("An exception occurred", er)
        return JsonResponse({"error": "Required data not supplied"}, status=404)

    return JsonResponse(
        {"last_likes_history": last_likes.get("last_likes_history")}, status=200
    )


def follow(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Not Authenticated"}, status=401)

    if request.method == "POST":
        follow_user = ""
        try:
            body = json.loads(request.body)
            follow_user = body["pk"]
        except Exception as er:
            print("An exception occurred", er)
            return JsonResponse({"error": "Required data not supplied"}, status=404)

        if not follow_user:
            return JsonResponse({"error", "User Not supplied"}, status=404)

        def add_follow(entity):
            """add a new user in follow model"""
            entity.followings.add(follow_user)
            user = User.objects.filter(pk=follow_user).first()
            return {"user": user.username, "status": True}

        def remove_follow(entity):
            """remove a follow in follow model"""
            entity.followings.remove(follow_user)
            f_user = User.objects.filter(pk=follow_user).first()
            return {"user": f_user.username, "status": False}

        follow = {}
        try:
            follow, created = Follow.objects.get_or_create(user=request.user)

            def resp_data(resp):
                return {
                    "user_followed": resp.get("user"),
                    "status": resp.get("status"),
                }

            # if a new follow model has created for this user
            if created:
                # then there are no followings have been added yet, add this user to the list
                resp = add_follow(follow)
                return JsonResponse(
                    resp_data(resp),
                    status=200,
                )

            # if follow model found for the user
            if follow:
                # get the user from followings if found
                follo = follow.followings.get(pk=follow_user)

                if follo:
                    # and remove/toggle it
                    resp = remove_follow(follow)

                    return JsonResponse(
                        resp_data(resp),
                        status=200,
                    )
        # if getting this follow did an exception, then this user is not found in followings list for this user
        except User.DoesNotExist:
            # so add it
            resp = add_follow(follow)
            return JsonResponse(
                resp_data(resp),
                status=200,
            )

        except Exception as er:
            print("An exception occurred", er)
            return JsonResponse({"error": er}, status=500)


def post(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Not Authenticated"}, status=401)

    if request.method == "POST":
        # handle post
        try:
            body = request.body

            if not body:
                return JsonResponse({"error": "No data has been provided"}, status=404)

            load = json.loads(body)
            pk = json.loads(body).get("pk") or json.loads(body).get("id")

            # del the pk to spread **load obj without dublicating pk err
            for k in load:
                if k in ["pk", "id"]:
                    del load[k]
                    break

            post, created = Post.objects.update_or_create(
                user=request.user, pk=pk, defaults={**load}
            )

            def resp_data(resp):
                return {
                    "pk": resp.pk,
                    "content": resp.content,
                    "is_active": resp.is_active,
                    "published_date": resp.published_date,
                    "likes_count": resp.likes_count,
                    "username": resp.user.username,
                }

            if created:
                post = (
                    Post.objects.filter(is_active=True, pk=post.pk).annotate(
                        likes_count=Count("liked_posts"),
                    )
                ).first()

                return JsonResponse(
                    {
                        "data": resp_data(post),
                        "success": True,
                        "message": "Post Created successfully",
                    },
                    status=200,
                )
            elif post and not created:
                return JsonResponse(
                    {"success": True, "message": "Post Updated successfully"},
                    status=204,
                )
        except ValueError as er:
            print("ValueError exception occurred", er)
        except Post.DoesNotExist as er:
            print("ValueError exception occurred", er)
        except Exception as er:
            print("An exception occurred", er)

    else:
        # handle others
        return JsonResponse({"error": "Not supported method"}, status=404)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        # username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            nt = request.GET.get("nt")
            return render(
                request,
                "network/index.html",
                {"message": "Invalid email and/or password.", "login": True, "nt": nt},
            )
    else:
        return redirect(reverse("index"))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        if username:
            slugify(username, allow_unicode=True)
            
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request,
                "network/index.html",
                {"message": "Passwords must match.", "register": True},
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            nt = request.GET.get("nt")
            return render(
                request,
                "network/index.html",
                {
                    "message": "Username/Email already taken.",
                    "register": True,
                    "nt": nt,
                },
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return redirect(reverse("index"))
