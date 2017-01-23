import requests
import pprint
#
# First, check the source of the login form to get three
# pieces of information - the url that the form posts to, and the name
# attributes of the username and password fields. In his example, they are
# inUserName and inUserPass.
#
# Once you've got that, you can use a requests.Session() instance to make a
# post request to the login url with your login details as a payload. Making
# requests from a session instance is essentially the same as using requests
# normally, it simply adds persistence, allowing you to store and use
# cookies etc.
#
# Assuming your login attempt was successful, you can simply use the session
# instance to make further requests to the site. The cookie that identifies
# you will be used to authorise the requests.
#
PROTECTED_URL = 'https://rqm.intersane.xyz:9443/jts/admin'
LOGIN_URL = 'https://rqm.intersane.xyz:9443/jts/auth/j_security_check'
# Fill in your details here to be posted to the login form.
payload = {
    'j_username': 'jadmin',
    'j_password': 'jadmin17'
}
qm_context_root = "/qm"
clm_public_uri = "https://rqm.intersane.xyz:9443"
api_integration_root = \
    "/service/com.ibm.rqm.integration.service.IIntegrationService"
qm_integration_url = \
    clm_public_uri + qm_context_root + \
    api_integration_root + "/projects"

print("QM integration URL: ", '\n', " <<", qm_integration_url, ">>")
# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    r = s.get(qm_integration_url, verify=False)
    p = s.post(LOGIN_URL, data=payload, verify=False)
    # print the html returned or something more intelligent to see if it's a
    # successful login page.
    print ('===== p.* =====')
    pprint.pprint (vars(p))
    print ('^^^^^ p.* ^^^^^')

    # An authorised request.

    #
    # Just ask for a list of projects
    #


    r = s.get(qm_integration_url, data=payload, verify=False)
    print ('===== r.* =====')
    pprint.pprint (vars(r))
    print ('^^^^^ r.* ^^^^^')
    p = s.post(LOGIN_URL, data=payload, verify=False)
    print ('===== p2.* =====')
    pprint.pprint (vars(p))
    print ('^^^^^ p2.* ^^^^^')
    r = s.get(qm_integration_url, data=payload, verify=False)
    print ('===== r2.* =====')
    pprint.pprint (vars(r))
    print ('^^^^^ r2.* ^^^^^')
        # etc...
