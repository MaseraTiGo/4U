# coding=UTF-8

'''
Created on 2016年7月28日

@author: Administrator
'''
import collections

from tuoen.utils.common.single import Single

class BaseServer(Single):
    
    def __init__(self,name, desc):
        self.name = name
        self.desc = desc
        self._register = {}
        
    def register(self,api):
        if api.name in self._register:
            raise Exception("api_name : {api_name} have registed!"\
                            .format(api_name = api.name))
        self._register[api.name] = api
    
    @property
    def apis(self):
        result = collections.OrderedDict()
        keys = list(self._register.keys())
        for key in sorted(keys, key = lambda obj : (obj.split(".")[0] + str(len(obj.split("."))) + obj.split(".")[1])):
            result[key] = self._register[key]
        return result
        
class PatientServer(BaseServer):
    
    def __init__(self):
        self.name = 'patient'
        self.desc = "针对患者端提供的API访问服务"
        super(PatientServer, self).__init__(self.name,self.desc)

PatientServer = PatientServer()

class DoctorServer(BaseServer):
    
    def __init__(self):
        self.name = 'doctor'
        self.desc = "针对医生端提供的API访问服务"
        super(DoctorServer, self).__init__(self.name, self.desc)
        
DoctorServer = DoctorServer()

class CrmServer(BaseServer):
    
    def __init__(self):
        self.name = 'crm'
        self.desc = "用于员工维护客户关系的系统"
        super(CrmServer, self).__init__(self.name, self.desc)
        
CrmServer = CrmServer()

class OrganizationServer(BaseServer):
    
    def __init__(self):
        self.name = 'organization'
        self.desc = "用于为第三方服务机构提供操作"
        super(OrganizationServer, self).__init__(self.name, self.desc)
        
OrganizationServer = OrganizationServer()
