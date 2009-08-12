
import urllib2
try:
    import json
except ImportError:
    import simplejson as json

class UntinyError(Exception):
    pass


class untiny(object):
    def __init__(self, url_base="http://untiny.me"):
        self._url_base = url_base
        self._urllib = urllib2

    def _GetUrl(self, url):
        opener = self._urllib.build_opener()
        responce = opener.open(url).read()
        opener.close()
        data = json.loads(responce)
        return data

    def GetFullUrl(self, url):
        data = self._GetUrl("%s/api/1.0/extract?format=json&url=%s"%(self._url_base, url))
        if data.has_key("error"):
            raise UntingError(str(data['error']))
        elif data.has_key("org_url"):
            return data["org_url"]
        else:
            raise UntinyError(u"Unknown responce from server: %s"%(str(data)))

    def GetServices(self):
        data = self._GetUrl("%s/api/1.0/services?format=json"%(self._url_base))
        if len(data) > 0:
            return data.keys()
        else:
            raise UntinyError(u"Unknown responce from server: %s"%(str(data)))
