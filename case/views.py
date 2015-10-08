# coding=utf-8
import itertools
import json
from django.core.paginator import Paginator

from django.core.serializers import serialize
from django.db.models import Q, Model, QuerySet
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.views.generic import View

from case.forms import AccountForm, DepartmentForm, PaymentForm, ProjectForm
from case.models import Account, Department, Payment, Project


# Application generic views
class JSONResponseMixin(object):
    """JSON mixin."""

    def render_to_json_response(self, context, page=1, per_page=20):
        if isinstance(context, Model):
            context = json.loads(serialize('json', [context]))[0]
            context['meta'] = {}
            for field in self.model._meta.fields:
                context['meta'][field.name] = {
                    'label': field.verbose_name,
                    'type': field.get_internal_type()
                }
        elif isinstance(context, QuerySet):
            paginator = Paginator(context, per_page)
            items = json.loads(
                serialize('json', paginator.page(page).object_list)
            )
            context = {
                'items': items,
                'page': page,
                'num_pages': paginator.num_pages,
                'limit': paginator.per_page
            }

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


class ObjectsListView(JSONResponseMixin, View):
    """List objects view."""
    model = None

    def get_queryset(self, grouped):
        orm_filter = {}
        _op = filter(lambda x: x[0] == '_op', grouped)
        if _op:
            grouped.pop(grouped.index(_op[0]))
            _op = list(list(_op)[0][1])[0][1]

        if _op == 'or':
            queries = []
            for key, value in grouped:
                value = value[0][1]
                queries.append(Q(**{key: value}))

            query = queries.pop()
            for item in queries:
                query |= item

            return self.model.objects.filter(query)

        else:
            for key, value in grouped:
                key = '{0}__in'.format(key)
                value = map(lambda x: x[1], value)
                orm_filter[key] = value

            return self.model.objects.filter(**orm_filter)

    def get_data(self, request, *args, **kwargs):
        filters = filter(
            lambda x: x[0].startswith('fl'), request.GET.iteritems()
        )
        if filters:
            grouped = map(lambda x: (x[0], list(x[1])), itertools.groupby(
                filters, lambda x: x[0][3:-1].split('][')[0]
            ))
            return self.get_queryset(grouped)

        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        data = self.get_data(request, *args, **kwargs)
        return self.render_to_json_response(data)


class PlanedPaymentsListView(ObjectsListView):
    model = Payment

    def get_data(self, request, *args, **kwargs):
        data = super(PlanedPaymentsListView, self).get_data(
            request, *args, **kwargs
        )
        return data.obejcts.filter(status=1)


class FactPaymentsListView(ObjectsListView):
    model = Payment

    def get_data(self, request, *args, **kwargs):
        data = super(FactPaymentsListView, self).get_data(
            request, *args, **kwargs
        )
        return data.obejcts.filter(status=2)


class PaymentView(ObjectView):
    model = Payment
    form = PaymentForm


class ProjectsListView(ObjectsListView):
    model = Project


class ProjectView(ObjectView):
    model = Project
    form = ProjectForm


class DepartmentsListView(ObjectsListView):
    model = Department


class DepartmentView(ObjectView):
    model = Department
    form = DepartmentForm


class AccountsListView(ObjectsListView):
    model = Account


class AccountView(ObjectView):
    model = Account
    form = AccountForm
