import urllib
import httplib2
from xml.dom.minidom import parse, parseString
from exceptions import Exception
# From: http://opekar.blogspot.com.au/2010/10/working-with-ibm-jazz-via-python.html


class JazzClient(object):
    def __init__(self, server_url, user, password):
        self.base_url = server_url

        self.http = httplib2.Http()
        self.http.follow_redirects = True
        self.headers = {'Content-type': 'text/xml'}

        #1) before authentification one needs to go first to a "restricted resource"
        resp, content = self.http.request( self.base_url + "/oslc/workitems/1.xml", 'GET', headers=self.headers)
        #TODO sometimes returns capital X-
        #TODO check before if the key is in dictionary, if not something is wrong as well
        if resp['x-com-ibm-team-repository-web-auth-msg'] != 'authrequired':
            raise Exception("something is wrong seems the server doesn't expect authentication!")


        self.headers['Cookie']=  resp['set-cookie']
        self.headers['Content-type'] = 'application/x-www-form-urlencoded'

        #2 now we can start the authentication via j_security_check page
        resp, content = self.http.request(self.base_url+'/j_security_check' , 'POST', headers=self.headers, \
                    body=urllib.urlencode({'j_username': user, 'j_password': password}))
        #TODO check auth worked fine, if not throw exception
        #3 get the requested resource - finish the authentication
        resp, content = self.http.request( self.base_url + "/oslc/workitems/1.xml", 'GET', headers=self.headers)
