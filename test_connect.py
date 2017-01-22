import requests
from pprint import pprint

qm_context_root = "/qm"
clm_public_uri = "https://rqm.intersane.xyz:9443"
api_integration_root = "/service/com.ibm.rqm.integration.service.IIntegrationService"
#
# Just ask for a list of projects
#
qm_integration_url = \
    clm_public_uri + qm_context_root + \
    api_integration_root + "/projects"

print("QM integration URL: <<", qm_integration_url, ">>")

qm_user = "jadmin"
qm_pass = "jadmin17"

auth_cookie = {'j_username': qm_user, 'j_password' : qm_pass}

r = requests.post(qm_integration_url, cookies=auth_cookie, verify=False)

print("First response")
pprint (vars(r))
# assert once you know what's in there

content_str = str(r._content, r.encoding)

print(content_str)

print ("Second response")

auth_r = requests.post("https://")
