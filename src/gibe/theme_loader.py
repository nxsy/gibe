"""
Wrapper class that takes a list of template loaders as an argument and attempts
to load templates from them in order, applying theme directory to the template
name to apply overrides.
"""

from django.template import TemplateDoesNotExist
from django.template.loader import BaseLoader, get_template_from_string, find_template_loader, make_origin

class Loader(BaseLoader):
    is_usable = True

    def __init__(self, loaders):
        self._loaders = loaders
        self._cached_loaders = []

    @property
    def loaders(self):
        # Resolve loaders on demand to avoid circular imports
        if not self._cached_loaders:
            for loader in self._loaders:
                self._cached_loaders.append(find_template_loader(loader))
        return self._cached_loaders

    def _find_template(self, name, dirs=None):
        for loader in self.loaders:
            try:
                template, display_name = loader(name, dirs)
                return (template, make_origin(display_name, loader, name, dirs))
            except TemplateDoesNotExist:
                pass
        raise TemplateDoesNotExist(name)

    def find_template(self, name, dirs=None):
        theme_prefixes = ["themes/techgeneral/"]
        for theme_prefix in theme_prefixes + [""]:
            try:
                return self._find_template(theme_prefix + name, dirs)
            except TemplateDoesNotExist:
                pass

        raise TemplateDoesNotExist(name)

    def load_template(self, template_name, template_dirs=None):
        template, origin = self.find_template(template_name, template_dirs)
        if not hasattr(template, 'render'):
            try:
                template = get_template_from_string(template, origin, template_name)
            except TemplateDoesNotExist:
                # If compiling the template we found raises TemplateDoesNotExist,
                # back off to returning the source and display name for the template
                # we were asked to load. This allows for correct identification (later)
                # of the actual template that does not exist.
                return template, origin

        return template, None
