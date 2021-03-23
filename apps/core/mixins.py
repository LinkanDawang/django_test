from rest_framework_tracking.models import APIRequestLog
from rest_framework_tracking.base_mixins import BaseLoggingMixin


class LogRequestMixin(BaseLoggingMixin):
    need_log = False
    logging_actions = []

    def should_log(self, request, response):
        """
        Method that should return a value that evaluated to True if the request should be logged.
        By default, check if the request method is in logging_methods.
        """
        if self.need_log or self.action in self.logging_actions:
            return True
        return False

    def finalize_response(self, request, response, *args, **kwargs):
        response = super(LogRequestMixin, self).finalize_response(request, response, *args, **kwargs)
        return response

    def handle_log(self):
        """
        Hook to define what happens with the log.

        Defaults on saving the data on the db.
        """
        APIRequestLog(**self.log).save()

