# from django.shortcuts import render

# # Create your views here.
# from .models import Category, Post, Tag
# from django.views.generic import ListView, TemplateView
# from django.utils import timezone
# from datetime import timedelta

# class HomeView(ListView):
#     model = Post
#     template_name = "aznews/home.html"
#     context_object_name = "posts"
#     queryset = Post.objects.filter(
#         published_at__isnull=False,status="active"
#     ).order_by("-published_at")[:5]

#     def get_context_data(self, **kwargs):
#         context=super().get_context_data(**kwargs)
#         context['featured_post']=(
#             Post.objects.filter(published_at__isnull=False, status="active")
#             .order_by("-published_at", "-views_count")
#             .first()
#         )
#         context["featured_posts"]= Post.objects.filter(
#             published_at__isnull=False, status="active"
#         ).order_by("-published_at","-views_count")[1:4]
        
#         context["recent_posts"]= Post.objects.filter(
#             published_at__isnull=False, status="active"
#         ).order_by("-published_at")[:7]

#         one_week_ago = timezone.now() - timedelta(days=7)
#         context["weekly_top_posts"] = Post.objects.filter(
#             published_at__isnull=False, status="active", published_at__lte=one_week_ago
#         ).order_by("-published_at", "-views_count")[:7]
#         print( context["weekly_top_posts"] )

#         # context["trending_posts"]=Post.objects.filter(
#         #     published_at__isnull=False, status="active"
#         # ).order_by("-views_count")[:3]
#         # print(context["trending_posts"])

#         # context['categories']= Category.objects.all()[:3]
#         # context['tags']=Tag.objects.all()[:12]

#         return context
    
# class AboutView(TemplateView):
#     template_name= "aznews/about.html"

#     # def get_context_data(self, **kwargs):
#     #     context=super().get_context_data(**kwargs)

#     #     context["trending_posts"]=Post.objects.filter(
#     #         published_at__isnull=False, status="active"
#     #     ).order_by("-views_count")[:3]



#     #     context['categories']= Category.objects.all()[:3]
#     #     context['tags']=Tag.objects.all()[:12]

#     #     return context
    
# class PostListView(ListView):
#     model = Post
#     template_name = "aznews/list/list.html"
#     context_object_name = "posts"
#     paginate_by = 1

#     def get_queryset(self):
#         return Post.objects.filter(
#             published_at__isnull=False, status="active"
#         ).order_by("-published_at")
    
# class PostByCategoryView(ListView):
#     model = Post
#     template_name = "aznews/list/list.html"
#     context_object_name = "posts"
#     paginate_by = 1

#     def get_queryset(self):
#         query = super().get_queryset()
#         query - query.filter(
#             published_at__isnull=False,
#             status = "active",
#             Category__is=self.kwargs["category_id"],

#         ).order_by("-published_at")
#         return query
    
# class PostbyTagView(ListView):
#     model = Post
#     template_name = "aznews/list/list.html"
#     context_object_name = "posts"
#     paginate_by = 1

#     def get_queryset(self):
#         query = super().get_queryset()
#         query = query.filter(
#             published_at__isnull=False,
#             status="active",
#             tag__id=self.kwargs["tag_id"],

#         ).order_by("-published_at")
#         return query



from django.shortcuts import redirect, render
from django.views.generic import ListView, TemplateView, DetailView, View
from django.utils import timezone
from datetime import timedelta
from .models import Category, Post, Tag
from newspaper.forms import CommentForm


class HomeView(ListView):
    model = Post
    template_name = "aznews/home.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(
        published_at__isnull=False, status="active"
    ).order_by("-published_at")[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_post"] = (
            Post.objects.filter(published_at__isnull=False, status="active")
            .order_by("-published_at", "-views_count")
            .first()
        )
        context["featured_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at", "-views_count")[1:4]

        context["recent_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")[:7]

        one_week_ago = timezone.now() - timedelta(days=7)
        context["weekly_top_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active", published_at__lte=one_week_ago
        ).order_by("-published_at", "-views_count")[:7]

        return context


class AboutView(TemplateView):
    template_name = "aznews/about.html"


class PostListView(ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")


class PostByCategoryView(ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            published_at__isnull=False,
            status="active",
            category__id=self.kwargs["category_id"],
        ).order_by("-published_at")
        return query


class PostbyTagView(ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            published_at__isnull=False,
            status="active",
            tag__id=self.kwargs["tag_id"],
        ).order_by("-published_at")
        return query


class PostDetailView(DetailView):
    model = Post
    template_name = "aznews/detail/detail.html"
    context_object_name = "post"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(published_at__isnull=False, status="active")
        return query
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        obj.views_count += 1
        obj.save()

        context["previous_post"]=(
            Post.objects.filter(
                published_at__isnull=False, status="active", id__lt=obj.id
            )
            .order_by("-id")
            .first()

        )

        context["next_post"]=(
            Post.objects.filter(
                published_at__isnull=False, status="active", id__gt=obj.id
            )
            .order_by("id")
            .first()
        )

        return context
    
class CommentView(View):
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        post_id = request.POST["post"]
        if form.is_valid():
            form.save()
            return redirect("post-detail", post_id)
        
        post = Post.objects.get(pk=post_id)
        return render(
            request,
            "aznews/detail/detail.html",
            {"post":post,"form":form},
        )





