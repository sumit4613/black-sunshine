from django.views import generic

from . import mixins


class CourseList(mixins.OwnerCourseMixin, generic.ListView):
    template_name = "courses/manage/course/list.html"
    permission_required = "courses.view_course"


class CourseCreate(mixins.OwnerCourseEditMixin, generic.CreateView):
    permission_required = "courses.create_course"


class CourseUpdate(mixins.OwnerCourseEditMixin, generic.UpdateView):
    permission_required = "courses.change_course"


class CourseDelete(mixins.OwnerCourseMixin, generic.DeleteView):
    template_name = "courses/manage/course/delete.html"
    permission_required = "courses.delete_course"
