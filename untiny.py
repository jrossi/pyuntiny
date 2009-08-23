# Copyright (c) 2009, Jeremy Rossi
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY Jeremy Rossi ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Jeremy Rossi BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
        self._services = []

    def _GetUrl(self, url):
        opener = self._urllib.build_opener()
        responce = opener.open(url).read()
        opener.close()
        data = json.loads(responce)
        return data

    def SupportedUrl(self, url):
        svc = self.GetServices()
        for i in svc:
            if i in url:
                return True
        return False

    def GetFullUrl(self, url):
        data = self._GetUrl("%s/api/1.0/extract?format=json&url=%s"%(self._url_base, url))
        if data.has_key("error"):
            raise UntinyError(str(data['error']))
        elif data.has_key("org_url"):
            return data["org_url"]
        else:
            raise UntinyError(u"Unknown responce from server: %s"%(str(data)))

    def GetServices(self):
        if not self._services:
            data = self._GetUrl("%s/api/1.0/services?format=json"%(self._url_base))
            if len(data) > 0:
                return data.keys()
            else:
                raise UntinyError(u"Unknown responce from server: %s"%(str(data)))
            self._services = data
        return self._services
