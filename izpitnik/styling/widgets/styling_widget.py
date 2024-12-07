from django.forms import Widget, renderers


class StylingWidget(Widget):

    template_name = 'admin/widgets/styling_widget.html'

    def __init__(self, mode='txt', attrs=None):
        super().__init__(attrs)
        self.mode = mode

    def render(self, *args, **kwargs):
        kwargs['renderer'] = renderers.TemplatesSetting()
        return super().render(*args,**kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['mode'] = self.mode.lower()
        return context