from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    path("mine/", views.CourseList.as_view(), name="course_list"),
    path("create/", views.CourseCreate.as_view(), name="create_course"),
    path("<pk>/edit/", views.CourseUpdate.as_view(), name="edit_course"),
    path("<pk>/delete/", views.CourseDelete.as_view(), name="delete_course"),
    path(
        "<pk>/module/", views.CourseModuleUpdate.as_view(), name="course_module_update"
    ),
    path(
        "module/<int:module_id>/content/<model_name>/create/",
        views.ContentCreateUpdate.as_view(),
        name="module_content_create",
    ),
    path(
        "module/<int:module_id>/content/<model_name>/<id>/",
        views.ContentCreateUpdate.as_view(),
        name="module_content_update",
    ),
    path(
        "content/<int:id>/delete/",
        views.ContentDelete.as_view(),
        name="module_content_delete",
    ),
    path(
        "module/<int:module_id>/",
        views.ModuleContentList.as_view(),
        name="module_content_list",
    ),
    path(
        "module/order/",
        views.ModuleOrder.as_view(),
        name="module_order",
    ),
    path(
        "content/order/",
        views.ContentOrder.as_view(),
        name="content_order",
    ),
]
