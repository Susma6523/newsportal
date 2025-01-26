from newspaper.models import Category, Post, Tag

def navigation(request):
    tags = Tag.objects.all()[:12]
    categories = Category.objects.all()[:3]
    trending_posts = Post.objects.filter(
        published_at__isnull=False, status="active"
    ).order_by("-views_count")[:3]

    popular_posts = Post.objects.filter(
        published_at__isnull=False, status="active"
    ).order_by("-views_count", "-published_at")[:6]

    side_categories = Category.objects.all()[:6]

    return {
        "tags": tags,
        "categories": categories,
        "trending_posts": trending_posts,
        "side_categories": side_categories,
        "popular_posts": popular_posts,
    }
