from django.template.loader import select_template

def _select_themed_template(template_name):
    return select_template([template_name])

def gibe_context(request):
    context_vars = {
        'select_themed_template': _select_themed_template,
    }
    return context_vars
