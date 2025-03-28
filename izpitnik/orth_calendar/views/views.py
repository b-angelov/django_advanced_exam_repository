from django.views.generic import TemplateView


class OrthodoxCalendarView(TemplateView):
    pass

class OrthodoxApiJsView(TemplateView):
    template_name = "orth_calendar/js/calendar_fetchery.js"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_url'] = self.request.build_absolute_uri('/') + 'orth_calendar'
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        response['Content-Type'] = 'application/javascript'
        return response
