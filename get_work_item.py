def getWorkItem(self, itemNumber):
    self.headers['Content-type'] = 'text/xml'
    resp, content = self.http.request(self.base_url+'/oslc/workitems/'+ itemNumber +'.xml', 'GET', headers=self.headers)
    if resp.status != 200:
        raise Exception("JazzClient responce status != 200 !!!")
    return content 
