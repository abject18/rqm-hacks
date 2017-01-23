import requests
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
# Fill in your details here to be posted to the login form.
payload = {
    'inUserName': 'username',
    'inUserPass': 'password'
}

# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    p = s.post('LOGIN_URL', data=payload)
    # print the html returned or something more intelligent to see if it's a
    # successful login page.
    print p.text

    # An authorised request.
    r = s.get('A protected web page url')
    print r.text
        # etc...
