from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    path("mine/", views.CourseList.as_view(), name="course_list"),
    path("create/", views.CourseCreate.as_view(), name="create_course"),
    path("<pk>/edit/", views.CourseUpdate.as_view(), name="edit_course"),
    path("<pk>/delete/", views.CourseDelete.as_view(), name="delete_course"),
]
