import django.template
import django.http
import django.contrib

def home(request):
    #django.contrib.messages.add_message(request, django.contrib.messages.SUCCESS, 'welcome message')

    template = django.template.loader.get_template('home.html')
    context = django.template.RequestContext(request)
    #context.push({'autoplay':False})

    return django.http.HttpResponse(template.render(context))

def slides(request):
    #django.contrib.messages.add_message(request, django.contrib.messages.SUCCESS, 'welcome message')

    template = django.template.loader.get_template('slides.html')
    context = django.template.RequestContext(request)
    #context.push({'autoplay':False})

    return django.http.HttpResponse(template.render(context))


def about(request):
    #django.contrib.messages.add_message(request, django.contrib.messages.SUCCESS, 'contact message')

    template = django.template.loader.get_template('about.html')
    context = django.template.RequestContext(request)
    #context.push({'autoplay':False})

    return django.http.HttpResponse(template.render(context))

