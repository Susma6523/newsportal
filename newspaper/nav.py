from newspaper.models import Category, Post, Tag

def navigation(request):
    tags = Tag.objects.all()[:12]
    categories = Category.objects.all()[:3]
    trending_posts = Post.objects.filter(
        published_at_isnull=False,status="active"
    ).order_by("-views_count")[:3]

    return {
        "tags": tags,
        "categories": categories,
        "trending_posts": trending_posts,
    }