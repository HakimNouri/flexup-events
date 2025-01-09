#  ------- events/events/views.py 
from core.utils.print_context import _print_context
from .models import Event, Response, Status
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from events.forms import EventForm, ResponseForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.template.loader import render_to_string
from django.middleware.csrf import get_token



def events(request):
    
    # returns a list of dictionaries containing the name and verbose name of each field in the Events model
    # columns = [{"name": field.name, "title": field.verbose_name} for field in Event._meta.fields]
    columns = [
        {"name": "name", "title": "Title"},
        {"name": "start_datetime", "title": "Start date & time"},
        {"name": "end_datetime", "title": "End date & time"},
        {"name": "description", "title": "Description"},
        {"name": "location", "title": "Location"},
        {"name": "slug", "title": "Slug"},
    ]

    data = list(Event.objects.all())
    # append the registeration link and actions (buttons) for each row (to use in the auto generated table component)
    for row in data:
        row.link = reverse('event_register', args=[row.slug])
        row.actions = [
            {"url": reverse('event_register', args=[row.slug]), "class":"", "icon": "bi bi-eye", "onclick": None},
            {"url": "#", "class":"ms-3", "icon": "bi bi-trash", "onclick": f"deleteEvent(event,'{row.slug}')"}
        ]

    context = {"title": "Events", "columns": columns, "data": data,}
    return render(request, "events.html", context)



@require_POST
def delete_event(request, slug):
    print("Deleting event with slug:", slug)
    event_instance = get_object_or_404(Event, slug=slug)
    _print_context(event_instance, "slug")
    event_instance.delete()
    redirect_url = '/events/'
    print(f"Redirecting to: {redirect_url}")
    return HttpResponseRedirect(redirect_url)



def home(request):
    return render(request, 'home.html')



def event_view(request, slug=None, admin_code=None):
    """
    Handles both create (no slug) and view/edit (with slug) of Event objects.
    """
    if slug:

        event_instance = get_object_or_404(Event, slug=slug)
        if admin_code:
            isAdmin = Event.objects.filter(slug=slug, admin_code=admin_code).exists()
        else:
            isAdmin = False
         
        # returns a list of dictionaries containing the name and verbose name of each field in the Response model
        # columns = [{"name": field.name, "title": field.verbose_name} for field in Response._meta.fields]
        columns = [
            {"name": "participant", "title": "Name"},
            {"name": "status", "title": "Status"},
        ]

        # generate a list of response forms of each participant of the event
        forms = []
        participants = Response.objects.filter(event=event_instance)
        for participant in participants:
            form = ResponseForm(instance=participant, event=event_instance, isAdmin=isAdmin)
            form.slug = participant.slug
            forms.append(form)

        # append the class-name and actions (buttons) for each row (to use in the auto generated table component)
        if isAdmin:
            for form in forms:
                form.class_name = "update-form"
                form.actions = [
                    {"url": "#", "class":"btn btn-primary", "icon": "", "onclick": None, "text": "Update", "type":"submit",},
                    {"url": "#", "class":"btn btn-danger", "icon": "", "onclick": None, "text": "Delete", "type":"delete",},
                ]
    else:
        event_instance = None
        isAdmin = True
        columns = []
        forms = []

    # appending the creation form
    creationForm = ResponseForm(event=event_instance, request=request, isAdmin=isAdmin)
    if event_instance:
        creationForm.slug = event_instance.slug
    creationForm.class_name = "create-form"
    creationForm.actions = [
        {"url": "#", "class":"btn btn-success", "icon": "", "onclick": None, "text": "Add", "type":"submit",},
    ]
    forms.append(creationForm)

    if request.method == 'POST':
        # Submitting the form (Create or Update)
        form = EventForm(request.POST, instance=event_instance, request=request, isAdmin=isAdmin)
        if form.is_valid():
            form.save()
            return redirect('events')
    else:
        # GET request: render empty form (create) or filled form (view)
        form = EventForm(instance=event_instance, request=request, isAdmin=isAdmin)

    return render(request, 'event.html', {
        'form': form,
        'event': event_instance,
        'isAdmin': isAdmin,
        'columns': columns,
        'data':forms,
    })



def participation(request, slug=None):
    if request.method == 'POST':
        if slug:
            participation = get_object_or_404(Response, slug=slug)
            form = ResponseForm(request.POST, instance=participation)
        else:
            form = ResponseForm(request.POST)

        # TODO: handle form errors
        if form.is_valid():
            # saving the form with commit = false to add the is_admin value manually as it's not being added by the form (the form ignore the hidden field)
            saved_participation = form.save(commit=False)
            saved_participation.is_admin = request.POST.get('is_admin') == 'True'
            saved_participation.save()

            # if it's a creation form and it's submitted by a participant (not admin)
            if not slug and not saved_participation.is_admin:
                redirect_link = reverse('participant_view', args=[saved_participation.event.slug, saved_participation.slug])
                return JsonResponse({'redirect_link': redirect_link}, status=200)
            else:
                csrf_token = get_token(request)
                return HttpResponse(render_to_string('partials/participant_row.html', {'participation': saved_participation,'csrf_token': csrf_token}))

        return HttpResponse(status=400)
    

    
def delete_participation(request, slug):
    if request.method == "DELETE":
        participation_instance = get_object_or_404(Response, slug=slug)
        participation_instance.delete()    
        return HttpResponse(status=200)
    return HttpResponse(status=405)



def participant_view(request, slug, participant_code):
    
    event = get_object_or_404(Event, slug=slug)
    participation = get_object_or_404(Response, slug=participant_code)
    form = ResponseForm(instance=participation, request=request, event=event, isGuestAdmin=True)
    
    return render(request, 'participation.html', {
        'form': form,
        'event': event,
        'participation': participation, 
    })