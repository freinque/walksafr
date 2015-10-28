from django.conf.urls import url
import mainapp.views

urlpatterns = [
    #url(r'^$', barbiturythme_app.views.DefaultFormView.as_view(), name='index'),
    url(r'^input/$', mainapp.views.form_input, name='input'),
    url(r'^output/$', mainapp.views.form_output, name='output'),
    url(r'^slides/$', mainapp.views.pdf_view, name='slides'),
    #url(r'^(?P<beat_n>[0-9]+)/$', barbiturythme_app.views.edit_form, name='edit_form'),
    ]
