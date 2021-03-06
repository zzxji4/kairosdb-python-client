from abc import abstractmethod
from kairosdbclient.exceptions import RequestException
from datetime import datetime
import calendar


class Request(object):
    def __init__(self):
        if not hasattr(self, 'uri'):
            raise RequestException("Request %s needs to have uri attribute." % self.__class__.__name__)

        if not hasattr(self, 'resource'):
            raise RequestException("Request %s needs to have resource attribute." % self.__class__.__name__)

        if not hasattr(self, 'success_status_code'):
            raise RequestException("Request %s needs to have success_status_code attribute." % self.__class__.__name__)

        if not hasattr(self, 'request_method'):
            raise RequestException("Request %s needs to have request_method attribute." % self.__class__.__name__)

    @abstractmethod
    def payload(self):
        pass

    def to_resource(self, response):
        resource = getattr(self, 'resource')
        return resource(self, response) if resource and response.status_code is not 204 else None

    def _format_time(self, prefix, time):
        if isinstance(time, int):
            return {prefix + '_absolute': time}

        if isinstance(time, datetime):
            timestamp = calendar.timegm(time.utctimetuple()) * 1000
            return {prefix + '_absolute': timestamp}

        if isinstance(time, (list, tuple)):
            value, unit = time
            return {prefix + '_relative': {
                'value': value,
                'unit': unit
            }}

        raise RequestException("Invalid time format %s." % time)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               getattr(self, 'uri') == getattr(other, 'uri') and \
               getattr(self, 'resource') == getattr(other, 'resource') and \
               getattr(self, 'success_status_code') == getattr(other, 'success_status_code') and \
               getattr(self, 'request_method') == getattr(other, 'request_method') and \
               self.payload() == other.payload()

    def __ne__(self, other):
        return not self.__eq__(other)