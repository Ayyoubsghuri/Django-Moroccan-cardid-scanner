from django.contrib import admin
from .models import *
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib import messages


admin.site.site_header = "Province Rehamna Admin"
admin.site.site_title = "Portail Admin Province Rehamna "
admin.site.index_title = "Bienvenue dans le portail Province Rehamna"

class cityonn(admin.ModelAdmin):
    list_display = ('CIN', 'nom', 'prenom', 'sexe', 'Verified_Information')
    list_filter = ('Verified_Information', 'sexe')
    change_form_template = "admin/custom_change_template_cityonne.html"



class TypeCmd(admin.ModelAdmin):
    list_display = ('TypeCommand', 'Res')
    search_fields = ('TypeCommand',)
    # change_list_template = 'admin/change_lst.html'


class FilterUserAdmin(admin.ModelAdmin):
    list_display = ('CIN', 'TypeCommand')
    list_filter = ('TypeCommand', 'Done','add_on')
    search_fields = ('id', 'CIN__CIN',)
    readonly_fields = ('Res','TypeCommand','CIN')
    change_form_template = "admin/custom_change_template.html"
    change_list_template = 'admin/change_list_temp.html'
    # readonly_fields = ('Res',)

    def get_queryset(self, request):
        qs = super(FilterUserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(Res=request.user)

    def changelist_view(self, request, extra_context=None):
        chart_data = (
            Demande.objects.annotate(date=TruncDay("add_on"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )

        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}
        return super().changelist_view(request, extra_context=extra_context)

    def response_change(self, request, obj):
        if "exec" in request.POST:

            Cn = Cityonne.objects.filter(CIN__contains=obj.CIN)[0]
            if Cn.Verified_Information == False:
                messages.error(
                    request, "User Information isn't verified, We Recommend To Verify Cityonne Information before Save As Pdf.")
            else:
                request.session['Type'] = str(obj.TypeCommand)
                return HttpResponseRedirect("../../../../../PDF/"+str(obj.CIN))
            return HttpResponseRedirect("../")
        return super().response_change(request, obj)


admin.site.register(Demande, FilterUserAdmin)
admin.site.register(Type_Command, TypeCmd)
admin.site.register(Cityonne, cityonn)
