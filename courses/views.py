from braces import views
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views import generic
from django.views.generic.base import TemplateResponseMixin

from . import mixins
from .forms import ModuleFormSet
from .models import Content
from .models import Course
from .models import Module


class CourseList(mixins.OwnerCourseMixin, generic.ListView):
    template_name = "courses/manage/course/list.html"
    permission_required = "courses.view_course"


class CourseCreate(mixins.OwnerCourseEditMixin, generic.CreateView):
    permission_required = "courses.add_course"


class CourseUpdate(mixins.OwnerCourseEditMixin, generic.UpdateView):
    permission_required = "courses.change_course"


class CourseDelete(mixins.OwnerCourseMixin, generic.DeleteView):
    template_name = "courses/manage/course/delete.html"
    permission_required = "courses.delete_course"


class CourseModuleUpdate(TemplateResponseMixin, generic.View):
    template_name = "courses/manage/module/formset.html"
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super(CourseModuleUpdate, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({"course": self.course, "formset": formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect("courses:course_list")
        return self.render_to_response({"course": self.course, "formset": formset})


class ContentCreateUpdate(TemplateResponseMixin, generic.View):
    module = None
    model = None
    obj = None
    template_name = "courses/manage/content/form.html"

    def get_model(self, model_name):
        if model_name in ["text", "video", "image", "file"]:
            return apps.get_model(app_label="courses", model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        form = modelform_factory(
            model, exclude=["owner", "order", "created", "updated"]
        )
        return form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(
            Module, id=module_id, course__owner=request.user
        )
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)
        return super(ContentCreateUpdate, self).dispatch(
            request, module_id, model_name, id
        )

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({"form": form, "object": self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(
            self.model, instance=self.obj, data=request.POST, files=request.FILES
        )

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # new content
                Content.objects.create(module=self.module, item=obj)
            return redirect("courses:module_content_list", self.module.id)
        return self.render_to_response({"form": form, "object": self.obj})


class ContentDelete(generic.View):
    def post(self, request, id):
        content = get_object_or_404(Content, id=id, module__course__owner=request.owner)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect("courses:module_content_list", module.id)


class ModuleContentList(LoginRequiredMixin, TemplateResponseMixin, generic.View):
    template_name = "courses/manage/module/content_list.html"

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        return self.render_to_response({"module": module})


class ModuleOrder(views.CsrfExemptMixin, views.JsonRequestResponseMixin, generic.View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner=request.user).update(order=order)
        return self.render_json_response({"saved": "OK"})


class ContentOrder(views.CsrfExemptMixin, views.JsonRequestResponseMixin, generic.View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id, course__owner=request.user).update(
                order=order
            )
        return self.render_json_response({"saved": "OK"})
