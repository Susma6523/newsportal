from django.urls import path
from newspaper import views


urlpatterns =[
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("post-list/", views.PostListView.as_view(), name="post-list"),
    path("post-by-category/<int:category_id>/", views.PostByCategoryView.as_view(), name='post-by-category'),
    path("post-by-tag/<int:tag_id>/", views.PostbyTagView.as_view(), name='post-by-tag'),
    path("post-detail/<int:pk>/", views.PostDetailView.as_view(), name='post-detail'),
    path("post-comment/", views.CommentView.as_view(), name='post-comment'),
]