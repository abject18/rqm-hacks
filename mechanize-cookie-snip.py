import mechanize
import cookielib
#
# Ruthlessly stolen from:
#   http://stockrt.github.io/p/emulating-a-browser-in-python-with-mechanize/
#
# It is always useful to know how to quickly instantiate a browser
# in the command line or inside your python scripts.
# Every time I need to automate any task regarding web systems
# I do use this recipe to emulate a browser in python:
#<snip>
# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), \
    max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', \
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#========
# Now you have this br object, this is your browser instance.
# With this its possible to open a page, to inspect or to interact with:
#
# Open some site, let's pick a random one, the first that pops in mind:
r = br.open('http://google.com')
html = r.read()

# Show the source
print html
# or
print br.response().read()

# Show the html title
print br.title()

# Show the response headers
print r.info()
# or
print br.response().info()

# Show the available forms
for f in br.forms():
    print f

# Select the first (index zero) form
br.select_form(nr=0)

# Let's search
br.form['q']='weekend codes'
br.submit()
print br.response().read()

# Looking at some results in link format
for l in br.links(url_regex='stockrt'):
    print l
#
# ====
#
# If you are about to access a password protected site (http basic auth):
#
# If the protected site didn't receive the authentication data you would
# end up with a 410 error in your face
br.add_password('http://safe-site.domain', 'username', 'password')
br.open('http://safe-site.domain')
#
# Thanks to the Cookie Jar we’ve added before, you do not have to bother about
# session handling for authenticated sites, as in when you are accessing a
# service that requires a POST (form submit) of user and password. Usually they
# ask your browser to store a session cookie and expects your browser to
# contain that same cookie when re-accessing the page. All this, storing and
# re-sending the session cookies, is done by the Cookie Jar, neat!
#=====
# You can also manage with browsing history:
#
# Testing presence of link (if the link is not found you would have to
# handle a LinkNotFoundError exception)
br.find_link(text='Weekend codes')

# Actually clicking the link
req = br.click_link(text='Weekend codes')
br.open(req)
print br.response().read()
print br.geturl()

# Back
br.back()
print br.response().read()
print br.geturl()
# =====
# Download a file
f = br.retrieve('http://www.google.com.br/intl/pt-BR_br/images/logo.gif')[0]
print f
fh = open(f)
# =====
