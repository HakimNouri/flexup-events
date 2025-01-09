from django import forms
from .models import Event, Response, Status
from django.urls import reverse


class EventForm(forms.ModelForm):
    
    adminLink = forms.CharField(
        label="Admin Link",
        required=False,
        widget=forms.TextInput(attrs={
            'title': 'This field is auto-generated to create a unique URL for changing the détails of the event. Click on it to copy it to the clipboard. Save it and don\'t share it with others.',
            'readonly': 'readonly',
            'style': 'cursor: help;'
        })
    )

    registrationLink = forms.CharField(
        label="Registration Link",
        required=False,
        widget=forms.TextInput(attrs={
            'title': 'This field is auto-generated to create a unique URL for the event. Click on it to copy it to the clipboard. Save it and share it with the participants.',
            'readonly': 'readonly',
            'style': 'cursor: help;'
        })
    )

    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'false'}), # to skip the browser warning
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'slug': forms.HiddenInput(),
            'admin_code': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        isAdmin = kwargs.pop('isAdmin', None)
        super().__init__(*args, **kwargs)
        if isAdmin:
            if self.instance and self.instance.slug:
                slug = self.instance.slug
                admin_code = getattr(self.instance, 'admin_code', '')
                # Generate full URLs for adminLink and registrationLink
                if request:
                    domain = request.build_absolute_uri('/')[:-1]  # Get the full domain name
                    self.fields['slug'].initial = slug
                    self.fields['admin_code'].initial = admin_code
                    self.fields['adminLink'].initial = f"{domain}{reverse('event_admin', kwargs={'slug': slug, 'admin_code': admin_code})}"
                    self.fields['registrationLink'].initial = f"{domain}{reverse('event_register', kwargs={'slug': slug,})}"
        else:
            self.fields.pop('adminLink') # don't include the field for non admins
            self.fields.pop('registrationLink') # don't include the field for non admins
            # don't allow editing for non admins
            for field_name in self.fields:
                self.fields[field_name].widget.attrs['readonly'] = 'readonly'



class ResponseForm(forms.ModelForm):

    adminLink = forms.CharField(
        label="Admin Link",
        required=False,
        widget=forms.TextInput(attrs={
            'title': 'This field is auto-generated to create a unique URL for changing the détails of the participation. Click on it to copy it to the clipboard. Save it and don\'t share it with others.',
            'readonly': 'readonly',
            'style': 'cursor: help;'
        })
    )

    class Meta:
        model = Response
        fields = ['participant', 'status', 'event', 'is_admin']
        widgets = {
            'is_admin': forms.HiddenInput(),
            'event': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        
        # Get the data passed from the view
        isAdmin = kwargs.pop('isAdmin', None)
        isGuestAdmin = kwargs.pop('isGuestAdmin', None)
        request = kwargs.pop('request', None)
        event = kwargs.pop('event', None)

        super().__init__(*args, **kwargs)

        if isAdmin is not None:
            self.fields['is_admin'].initial = isAdmin
        else:
            self.fields.pop('is_admin') # don't include the field for non admins

        if event:
            self.fields['event'].initial = event
            self.fields['event'].queryset = Event.objects.filter(id=event.id)

        if not isAdmin:
            # Otherwise, limit to specific choices
            allowed_choices = [Status.MAYBE, Status.CONFIRMED, Status.DECLINED]
            self.fields['status'].choices = [
                (status.name, status.value) for status in allowed_choices
            ]
        
        # if it's an edit form & user is not an admin (a guest)
        if not isAdmin and not isGuestAdmin and self.instance.pk:
            # make the fields readonly & change the select fields to readonly text fields
            for field_name in self.fields:
                if isinstance(self.fields[field_name].widget, forms.Select):
                    # Replace the widget of selects with a readonly TextInput widget
                    self.fields[field_name].widget = forms.TextInput(
                        attrs={
                            'readonly': 'readonly',
                        }
                    )
                    self.initial[field_name] = self.fields[field_name].initial
                else:
                    self.fields[field_name].widget.attrs['readonly'] = 'readonly'
        
        # Generate full URL for adminLink
        if self.instance and self.instance.slug:
            participant_code = self.instance.slug
            if event and request:
                slug = event.slug
                domain = request.build_absolute_uri('/')[:-1]  # Get the full domain name
                self.fields['adminLink'].initial = f"{domain}{reverse('participant_view', kwargs={'slug': slug, 'participant_code': participant_code})}"
            else:
                self.fields['adminLink'].initial = ''  # Ensure adminLink always has an initial value
        else:
            self.fields['adminLink'].initial = ''  # Ensure adminLink always has an initial value
            
