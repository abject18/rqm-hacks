import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pprint
#
# For all IBM CLM apps, the "login" form is:
#   https://<server>:<port>/jts/auth/j_security_check
#
# The form fields for the user ID and password are:
#   j_username
#   j_password
#
# Use a requests.Session() instance to make a post request to the login url
# with login details as a payload. Making requests from a session instance
# is essentially the same as using requests normally, it simply adds
# persistence, allowing you to store and use cookies, etc.
#
# Assuming your login attempt was successful, you can simply use the session
# instance to make further requests to the site. The cookie that identifies
# you will be used to authorise the requests.
#
# IBM warns that for some Tomcat configs, you can't go directly to the auth
# form, you must go to a protected URL, get an "authrequired" and get
# redirected there. This test ignores that case. For now.
#
# This code mostly stolen from:
#   http://stackoverflow.com/questions/11892729/
#       how-to-log-in-to-a-website-using-pythons-requests-module
#
# Stop annoying, distracting self-signed cert warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# Fill in login details here to be posted to the login form.
payload = {
    'j_username': 'jadmin',
    'j_password': 'jadmin17'
}
# Add your server public root URL.
clm_root_url = 'https://rqm.intersane.xyz:9443'
#
# Use this protected URL to ask for a list of projects. If we're not logged in,
# we'll get an "authrequired" value for the header key
# x-com-ibm-team-repository-web-auth-msg
#
qm_context_root = "/qm"
api_integration_root = \
    "/service/com.ibm.rqm.integration.service.IIntegrationService"
qm_integration_url = \
    clm_root_url + qm_context_root + api_integration_root + "/projects"
login_url = clm_root_url + '/jts/auth/j_security_check'
# authrequired is returned with the header key
# 'x-com-ibm-team-repository-web-auth-msg'
auth_req_key = 'x-com-ibm-team-repository-web-auth-msg'
auth_req_value = 'authrequired'
# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    #
    # Try the protected URL; expect status 200 and "authrequired"
    #
    r = s.get(qm_integration_url, verify=False)
    assert r.status_code == 200
    assert (auth_req_key in r.headers)
    assert r.headers[auth_req_key] == auth_req_value
    print ('===== r.* =====')
    pprint.pprint (vars(r))
    print ('^^^^^ r.* ^^^^^')
    # Try to login. If it succeeds, we get the requested protected page
    p = s.post(login_url, data=payload, verify=False)
    assert p.headers['status_code'] = '200'
    # print the html returned
    print ('===== p.* =====')
    pprint.pprint (vars(p))
    print ('^^^^^ p.* ^^^^^')
    # Now, see if jauth-revoke-token logs us out...
    logout_url = clm_root_url + '/jts/jauth-revoke-token'
    q = s.post(logout_url, verify=False)
    print('===== q =====')
    pprint.pprint(vars(q))
    print('^^^^^ q ^^^^^')
    #
    # ... by trying a protrected URL again
    #
    r2 = s.get(qm_integration_url, verify=False)
    print ('===== r2 =====')
    pprint.pprint (vars(r))
    print ('^^^^^ r2 ^^^^^')

    #r = s.get(qm_integration_url, data=payload, verify=False)
    #print ('===== r2.* =====')
    #pprint.pprint (vars(r))
    #print ('^^^^^ r2.* ^^^^^')
