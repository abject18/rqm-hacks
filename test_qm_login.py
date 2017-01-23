import requests
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
#   http://stackoverflow.com/questions/11892729/how-to-log-in-to-a-website-using-pythons-requests-module
#
# Fill in your details here to be posted to the login form.
payload = {
    'j_username': 'jadmin',
    'j_password': 'jadmin17'
}
# Add your server public root URL.
clm_root_URL = 'https://rqm.intersane.xyz:9443'
#
# Use protected URL to get an authrequired. Then use the login URL
PROTECTED_URL = clm_root_URL + '/jts/admin'
LOGIN_URL = clm_root_URL + '/jts/auth/j_security_check'
# authrequired is returned with the header key
# 'x-com-ibm-team-repository-web-auth-msg'
auth_req_key = 'x-com-ibm-team-repository-web-auth-msg'
auth_req_value = 'authrequired'
# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    #
    # Try the protected URL; expect status 200 and "authrequired"
    #
    r = s.get(PROTECTED_URL, verify=False)
    assert r.status_code == 200
    assert (auth_req_key in r.headers)
    assert r.headers[auth_req_key] == auth_req_value
    print ('===== r.* =====')
    pprint.pprint (vars(r.headers))
    print ('^^^^^ r.* ^^^^^')
    # Try to login. 
    p = s.post(LOGIN_URL, data=payload, verify=False)
    #assert p.headers['status_code'] = '200'

    # print the html returned or something more intelligent to see if it's a
    # successful login page.
    print ('===== p.* =====')
    pprint.pprint (vars(p))
    print ('^^^^^ p.* ^^^^^')
    #r = s.get(qm_integration_url, data=payload, verify=False)
    #print ('===== r2.* =====')
    #pprint.pprint (vars(r))
    #print ('^^^^^ r2.* ^^^^^')
