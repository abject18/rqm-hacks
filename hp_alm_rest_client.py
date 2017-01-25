# -*- coding: utf-8 -*-
__author__ = 'Arkady.Babaev'

import requests
import xml.etree.ElementTree as ET

class ALMUrl:
    def __init__(self, ip, port, domain, project):
        self.__base = u'http://' + ip + u':' + port + u'/qcbin'
        self.__auth = self.__base + u'/authentication-point/authenticate'
        self.__logout = self.__base + u'/authentication-point/logout'
        self.__work = self.__base + u'/rest/domains/' + domain + u'/projects/' + project

    def get_auth(self):
        return self.__auth

    def get_logout(self):
        return self.__logout

    def __getattr__(self, *args):
        result = self.__work
        for arg in args:
            result += '/' + arg
        return result

class SMFile:
    def __init__(self):
        self.key = ''
        self.filename = ''
        self.size = 0
        self.body = ''

class ALMSession:
    def __init__(self, Logging, login, password):
        try:
            self.__Logging = Logging
            self.__headers = {"Accept":"application/xml",
                              "Content-Type":"application/xml",
                              "KeepAlive":"true",
                              "Cookie": None}#"Authorization":"Basic " + base64.b64encode(login + ':' + password)}
            self.__user_pass = (login, password)
        except:
            self.__Logging.error(u"Exception while creating ALMSession", self.__headers, self.__h)

    def parse_xml(self, obj, dict):
        almxml = ET.fromstring(obj)
        if almxml.__dict__.has_key("TotalResults") and almxml.attrib["TotalResults"] == 0:
            return

        one_dict = {}
        for fields in almxml.findall('.//Fields'):
            one_dict.clear()
            for field in fields:
                curval = field.find("Value")
                if curval is not None and curval.text is not None:
                    one_dict[field.get('Name').decode('utf-8')] = curval.text#field.find("Value").text
                    if isinstance(one_dict[field.get('Name')], str):
                        one_dict[field.get('Name').decode('utf-8')] = one_dict[field.get('Name')].decode('utf-8')
            dict.append(one_dict.copy())
        return

    def create_xml(self, entity_type, dictionary):
        entity = ET.Element('Entity')
        entity.set('Type', entity_type)
        fields = ET.SubElement(entity, 'Fields')
        for field_name in dictionary:
            field = ET.SubElement(fields, 'Field')
            field.set('Name', field_name)
            value = ET.SubElement(field, 'Value')
            if isinstance(dictionary[field_name], list):
                dictsum = u''
                for line in dictionary[field_name]:
                    dictsum += (line + u'\r\n')
                value.text = dictsum
            else:
                value.text = dictionary[field_name]
        return ET.tostring(entity, encoding="UTF-8", method="xml")

    def Open(self, ALMUrl):
        #head, context = self.__h.request(ALMUrl.get_auth(), "GET", headers=self.__headers)
        r = requests.get(ALMUrl.get_auth(), auth=self.__user_pass)
        #if head.status is 200:
        if r.status_code is 200:
            self.__Logging.info(u"Open ALM session success", u'AUTH URL:', ALMUrl.get_auth(), u'HEADERS:', self.__headers)
            self.__headers["Cookie"] = r.headers['set-cookie']
            return 0
        else:
            self.__Logging.error(u"Open ALM session", r.status_code, r.reason, u'AUTH URL:', ALMUrl.get_auth(), u'HEADERS:', self.__headers)
            return int(r.status_code)

    def Close(self, ALMUrl):
        if self.__headers["Cookie"] is not None:
            r = requests.get(ALMUrl.get_logout(), headers=self.__headers, auth=self.__user_pass)
            if r.status_code is 200:
                self.__Logging.info(u"Close ALM session success", u'LOGOUT URL:', ALMUrl.get_logout(), u'HEADERS:', self.__headers)
                return 0
            else:
                self.__Logging.error(u"Close ALM session", r.status_code, r.reason, u'LOGOUT URL:', ALMUrl.get_logout(), u'HEADERS:', self.__headers)
                return int(r.status_code)
        else:
            self.__Logging.error(u"Close ALM session", u"1", u"httplib2.Http was not initialized")
            return 1

    def GetAttachments(self, ALMUrl, *args):
        if self.__headers["Cookie"] is not None:
            path = ALMUrl.__getattr__(*args)
            r = requests.get(path + u'/attachments', headers=self.__headers, auth=self.__user_pass)
            if r.status_code == 200:
                files_descr = []
                headers = self.__headers.copy()
                headers["Accept"] = "application/octet-stream"
                self.parse_xml(r.content, files_descr)
                result = []
                for file in files_descr:
                    F = SMFile()
                    F.filename = file[u'name']
                    F.size = file[u'file-size']
                    F.key = file[u'id']
                    r = requests.get(path + u'/attachments/' + F.filename, headers=headers, auth=self.__user_pass)
                    if r.status_code == 200:
                        F.body = r.content
                        result.append(F)
                    else:
                        self.__Logging.info(u"[ALMSession] Get attach file problem", u"URL:", path + u'/attachments/' + F.filename, u"HEADERS:", headers, F.filename)
                        return int(r.status_code), None
                self.__Logging.info(u"[ALMSession] Get attach success", u"URL:", ALMUrl.__getattr__(*args), u"HEADERS:", self.__headers)
                return 0, result
            elif r.status_code == 500:
                try:
                    if isinstance(r.text, unicode):
                        exceptionxml = ET.fromstring(r.text.encode('utf8','ignore'))
                    else:
                        exceptionxml = ET.fromstring(r.text)
                    self.__Logging.error(u"[ALMSession] Get ALM function with errors", exceptionxml[0].text, exceptionxml[1].text, u"PATH:", ALMUrl.__getattr__(*args), u"HEADERS:", self.__headers)
                except ET.ParseError:
                    self.__Logging.error(u"[ALMSession] Get ALM function with errors, returned message is not XML", u"PATH:", ALMUrl.__getattr__(*args), u"HEADERS:", self.__headers, ET.ParseError.message)
                return int(r.status_code), None
            else:
                self.__Logging.error(u"[ALMSession] Get ALM function with errors", r.status_code, r.reason, u"PATH:", ALMUrl.__getattr__(*args), u"HEADERS:", self.__headers)
                return int(r.status_code), None
        else:
            self.__Logging.error(u"[ALMSession] Get ALM function with errors", u"1", u"httplib2.Http not initialized")
            return 1, None

    def Get(self, ALMUrl, *args):
        if self.__headers["Cookie"] is not None:
            r = requests.get(ALMUrl.__getattr__(*args), headers=self.__headers, auth=self.__user_pass)
            if r.status_code == 200:
                self.__Logging.info(u"[ALMSession] Get success", u"URL:", ALMUrl.__getattr__(*args), u"HEADERS:", self.__headers)
                res = []
                self.parse_xml(r.content, res)
                return 0, res
            elif r.status_code == 500:
                try:
                    if isinstance(r.text, unicode):
                        exceptionxml = ET.fromstring(r.text.encode('utf8','ignore'))
                    else:
                        exceptionxml = ET.fromstring(r.text)
                    self.__Logging.error(u"[ALMSession] Get ALM function with errors", exceptionxml[0].text, exceptionxml[1].text, u"PATH:", ALMUrl.__getattr__(*args), u"HEADERS:", self.__headers)
                except ET.ParseError:
                    self.__Logging.error(u"[ALMSession] Get ALM function with errors, returned message is not XML", u"PATH:", ALMUrl.__getattr__(*args), u"HEADERS:", self.__headers, ET.ParseError.message)
                return int(r.status_code), None
            else:
                self.__Logging.error(u"[ALMSession] Get ALM function with errors", r.status_code, r.reason, u"PATH:", ALMUrl.__getattr__(*args), u"HEADERS:", self.__headers)
                return int(r.status_code), None
        else:
            self.__Logging.error(u"[ALMSession] Get ALM function with errors", u"1", u"httplib2.Http not initialized")
            return 1, None

    def Update(self, ALMUrl, data, *args):
        if self.__headers["Cookie"] is not None:
            r = requests.put(ALMUrl.__getattr__(*args),
                              headers=self.__headers,
                              data=data,
                              auth=self.__user_pass)
            if r.status_code == 200:
                self.__Logging.info(u"[ALMSession] Update success", u"URL:", ALMUrl.__getattr__(*args))
                return 0
            elif r.status_code == 500:
                if isinstance(r.text, unicode):
                    exceptionxml = ET.fromstring(r.text.encode('utf8','ignore'))
                else:
                    exceptionxml = ET.fromstring(r.text)
                self.__Logging.error(u"[ALMSession] Update ALM function with errors", exceptionxml[0].text, exceptionxml[1].text, u"PATH:", ALMUrl.__getattr__(*args), u"DATA:", data, u"HEADERS:", self.__headers)
                return int(r.status_code)
            else:
                self.__Logging.error(u"[ALMSession] Update ALM function with errors", r.status_code, r.reason, u"PATH:", ALMUrl.__getattr__(*args), u"DATA:", data, u"HEADERS:", self.__headers)
                return int(r.status_code)
        else:
            self.__Logging.error(u"[ALMSession] Update ALM function with errors", u"1", u"httplib2.Http not initialized")
            return 1

    def AddFile(self, ALMUrl, files, *args):
        if self.__headers["Cookie"] is not None:
            fileToSend = {}
            for file in files:
                fileToSend[file.filename] = file.body

            locheaders = self.__headers.copy()
            #locheaders[u'Content-Type'] = u'application/octet-stream'
            r = requests.post(ALMUrl.__getattr__(*args),
                              headers=locheaders,
                              files=fileToSend,
                              auth=self.__user_pass)
            if r.status_code == 201:
                self.__Logging.info(u"[ALMSession] Create success", u"URL:", ALMUrl.__getattr__(*args))
                return 0, r.headers._store['location'][1].split('/')[-1]
            elif r.status_code == 500:
                if isinstance(r.text, unicode):
                    exceptionxml = ET.fromstring(r.text.encode('utf8','ignore'))
                else:
                    exceptionxml = ET.fromstring(r.text)
                self.__Logging.error(u"[ALMSession] Create ALM function with errors", exceptionxml[0].text, exceptionxml[1].text, u"PATH:", ALMUrl.__getattr__(*args), u"DATA:", data, u"HEADERS:", self.__headers)
                return int(r.status_code), ""
            else:
                self.__Logging.error(u"[ALMSession] Create ALM function with errors", r.status_code, r.reason, u"PATH:", ALMUrl.__getattr__(*args), u"HEADERS:", self.__headers)
                return int(r.status_status), ""
        else:
            self.__Logging.error(u"[ALMSession] Create ALM function with errors", u"1", u"httplib2.Http not initialized")
            return 1, ""

    def Create(self, ALMUrl, data, *args):
        if self.__headers["Cookie"] is not None:
            r = requests.post(ALMUrl.__getattr__(*args),
                              headers=self.__headers,
                              data=data,
                              auth=self.__user_pass)
            if r.status_code == 201:
                self.__Logging.info(u"[ALMSession] Create success", u"URL:", ALMUrl.__getattr__(*args))
                return 0, r.headers._store['location'][1].split('/')[-1]
            elif r.status_code == 500:
                if isinstance(r.text, unicode):
                    exceptionxml = ET.fromstring(r.text.encode('utf8','ignore'))
                else:
                    exceptionxml = ET.fromstring(r.text)
                self.__Logging.error(u"[ALMSession] Create ALM function with errors", exceptionxml[0].text, exceptionxml[1].text, u"PATH:", ALMUrl.__getattr__(*args), u"DATA:", data, u"HEADERS:", self.__headers)
                return int(r.status_code), ""
            else:
                self.__Logging.error(u"[ALMSession] Create ALM function with errors", r.status_code, r.reason, u"PATH:", ALMUrl.__getattr__(*args), u"HEADERS:", self.__headers)
                return int(r.status_status), ""
        else:
            self.__Logging.error(u"[ALMSession] Create ALM function with errors", u"1", u"httplib2.Http not initialized")
            return 1, ""

    def Delete(self, ALMUrl, *args):
        if self.__headers["Cookie"] is not None:
            r = requests.delete(ALMUrl.__getattr__(*args),
                              headers=self.__headers,
                              auth=self.__user_pass)
            if r.status_code == 200:
                self.__Logging.info(u"[ALMSession]Delete success", u"URL:", ALMUrl.__getattr__(*args))
                #r.store
                return 0
            elif r.status_code == 500:
                if isinstance(r.text, unicode):
                    exceptionxml = ET.fromstring(r.text.encode('utf8','ignore'))
                else:
                    exceptionxml = ET.fromstring(r.text)
                self.__Logging.error(u"[ALMSession] Delete ALM function with errors", exceptionxml[0].text, exceptionxml[1].text, u"PATH:", ALMUrl.__getattr__(*args), u"HEADERS:", self.__headers)
                return int(r.status_code)
            else:
                self.__Logging.error(u"[ALMSession] Delete ALM function with errors", r.status_code, r.reason, u"PATH:", ALMUrl.__getattr__(*args), u"HEADERS:", self.__headers)
                return int(r.status_status)
        else:
            self.__Logging.error(u"[ALMSession] Delete ALM function with errors", u"1", u"httplib2.Http not initialized")
            return 1
