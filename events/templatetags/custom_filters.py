from django import template

register = template.Library()


@register.filter
def get_item(obj, attr):
    return getattr(obj, attr)


@register.filter
def get_form_item(form, field_name):
    if field_name in form.fields:
        return form[field_name]  # This returns the HTML widget for the field
    return None

@register.filter
def get_form_item_value(form, field_name):
    if field_name in form.fields:
        return form[field_name].value()  # This returns the value of the field
    return None