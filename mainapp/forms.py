import django.forms

import mainapp.models

class EndsForm(django.forms.ModelForm):
    
    class Meta:
        model = mainapp.models.Ends
        fields = [ 'ends_date', 'ends_time', 'orig_city', 'dest_city', 'ends_datetime', 'orig_long', 'orig_lati', 'dest_long', 'dest_lati']

