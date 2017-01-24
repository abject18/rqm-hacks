def changeProgress(self, itemNumber, progress):
     changeRequest = """
             <oslc_cm:changerequest xmlns:atom="http://www.w3.org/2005/Atom" xmlns:calm="http://jazz.net/xmlns/prod/jazz/calm/1.0/" xmlns:dc="http://purl.org/dc/terms/" xmlns:jd="http://jazz.net/xmlns/prod/jazz/discovery/1.0/" xmlns:jp="http://jazz.net/xmlns/prod/jazz/process/1.0/" xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/" xmlns:oslc_cm="http://open-services.net/xmlns/cm/1.0/" xmlns:oslc_disc="http://open-services.net/xmlns/discovery/1.0/" xmlns:oslc_qm="http://open-services.net/xmlns/qm/1.0/" xmlns:oslc_rm="http://open-services.net/xmlns/rm/1.0/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" xmlns:rtc_cm="http://jazz.net/xmlns/prod/jazz/rtc/cm/1.0/">
             <rtc_cm:progress>%s</rtc_cm:progress>
             </oslc_cm:changerequest>"""% (progress)
     self.headers['Content-type'] = 'text/xml'
     resp, content = self.http.request(self.base_url+'/oslc/workitems/'+ itemNumber +'.xml' , 'PUT', headers=self.headers, body=changeRequest)
     if resp.status != 200:
         raise Exception("JazzClient.responce status != 200 !!!")

     return content
