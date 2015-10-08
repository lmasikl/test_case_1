# coding=utf-8
import json

from django.core.serializers import serialize
from django.db.models import Model, QuerySet
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.views.generic import DetailView, ListView, View

from case.forms import AccountForm
from case.models import Account, Department, Payment, Project


# Application generic views
class JSONResponseMixin(object):
    """JSON mixin."""
    @staticmethod
    def render_to_json_response(context):
        if isinstance(context, Model):
            context = json.loads(serialize('json', [context]))[0]
        elif isinstance(context, QuerySet):
            items = json.loads(serialize('json', context))
            context = {'items': items, 'page': 1, 'limit': 20}

        return JsonResponse(context)


class ObjectView(JSONResponseMixin, View):
    """
    Single object view.
    Can object: create, update, get detail info, delete.
    """
    model = None
    form = None

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            data = {}
        else:
            data = form.errors

        return self.render_to_json_response(data)

    def get(self, request, *args, **kwargs):
        try:
            data = self.model.objects.get(pk=kwargs.get('pk'))
        except self.model.DoesNotExist:
            raise Http404

        return self.render_to_json_response(data)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return HttpResponseBadRequest()

        try:
            data = self.model.objects.get(pk=kwargs.get('pk'))
        except self.model.DoesNotExist:
            raise Http404

        put_data = json.loads(request.body.replace("'", '"').replace('u"', '"'))
        form = self.form(put_data, instance=data)
        if form.is_valid():
            form.save()
            data = {}
        else:
            data = form.errors

        return self.render_to_json_response(data)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return HttpResponseBadRequest()

        try:
            data = self.model.objects.get(pk=kwargs.get('pk'))
        except self.model.DoesNotExist:
            raise Http404

        data.delete()

        return self.render_to_json_response({})


class ObjectsView(JSONResponseMixin, View):
    """List objects view."""
    model = None

    def get(self, request, *args, **kwargs):
        data = self.model.objects.all()
        return self.render_to_json_response(data)


class PlanedPaymentsView(JSONResponseMixin, ListView):
    model = Payment

    def get_context_data(self):
        pass
        # filter get params where key starts with fl
        # group filtered params by field
        # create ORM filter
        # filter payments where closed=False


class FactPaymentsView(JSONResponseMixin, ListView):
    model = Payment

    def get_context_data(self):
        pass
        # filter payments where colosed=True


class PaymentView(JSONResponseMixin, DetailView):
    model = Payment


class ProjectsView(JSONResponseMixin, ListView):
    model = Project


class ProjectView(JSONResponseMixin, DetailView):
    model = Project


class DepartmentsView(JSONResponseMixin, ListView):
    model = Department


class DepartmentView(JSONResponseMixin, DetailView):
    model = Department


class AccountsView(ObjectsView):
    model = Account


class AccountView(ObjectView):
    model = Account
    form = AccountForm
