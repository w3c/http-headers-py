""" $Id$
    Module to make a HTTP Head
""" 

from urllib import *
import http_auth

class HEADURLopener(http_auth.ProtectedRedirectURLopener):
    def open_http(self, url):
        import httplib
        user_passwd = None
        if type(url) is type(""):
            host, selector = splithost(url)
            if host:
                user_passwd, host = splituser(host)
                host = unquote(host)
            realhost = host
        else:
            host, selector = url
            urltype, rest = splittype(selector)
            url = rest
            user_passwd = None
            if string.lower(urltype) != 'http':
                realhost = None
            else:
                realhost, rest = splithost(rest)
                if realhost:
                    user_passwd, realhost = splituser(realhost)
                if user_passwd:
                    selector = "%s://%s%s" % (urltype, realhost, rest)
            #print "proxy via http:", host, selector
        if not host: raise IOError, ('http error', 'no host given')
        if user_passwd:
            import base64
            auth = string.strip(base64.encodestring(user_passwd))
        else:
            auth = None
        h = httplib.HTTP(host) 
        h.putrequest('HEAD', selector)
        if auth: h.putheader('Authorization', 'Basic %s' % auth)
        if realhost: h.putheader('Host', realhost)
        for args in self.addheaders: apply(h.putheader, args)
        h.endheaders()
        errcode, errmsg, headers = h.getreply()
        fp = h.getfile()
        if errcode == 200:
            import urllib
            return urllib.addinfourl(fp, headers, "http:" + url)
        else:
            return self.http_error(url, fp, errcode, errmsg, headers)
