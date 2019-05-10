# coding=UTF-8

'''
Created on 2016年7月23日

@author: Administrator
'''

from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField, DatetimeField, DateField, BooleanField
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.exception.business_error import BusinessError

from tuoen.agile.apis.base import StaffAuthorizedApi
from tuoen.abs.service.account.manager import StaffAccountServer
from tuoen.abs.service.user.manager import StaffServer
from tuoen.abs.service.permise.manager import StaffPermiseServer

from tuoen.abs.service.authority import UserRightServer


class Add(StaffAuthorizedApi):
    """添加员工"""
    request = with_metaclass(RequestFieldSet)
    request.user_info = RequestField(DictField, desc="员工详情", conf={
        'name': CharField(desc="姓名"),
        'birthday': DateField(desc="生日", is_required=False),
        'phone': CharField(desc="手机", is_required=False),
        'email': CharField(desc="邮箱", is_required=False),
        'gender': CharField(desc="性别(man,woman)", is_required=False),
        'identity': CharField(desc="身份证", is_required=False),
        'emergency_contact': CharField(desc="紧急联系人", is_required=False),
        'emergency_phone': CharField(desc="紧急联系人电话", is_required=False),
        'address': CharField(desc="家庭住址", is_required=False),
        'entry_time': DateField(desc="入职时间", is_required=False),
        'education': CharField(desc="学历", is_required=False),
        'bank_number': CharField(desc="招行卡号", is_required=False),
        'contract_b': CharField(desc="合同编号（必）", is_required=False),
        'contract_l': CharField(desc="合同编号（立）", is_required=False),
        'expire_time': DateField(desc="到期时间", is_required=False),
        'is_working': BooleanField(desc="是否在职(0离职，1在职)", is_required=False),
        'role_ids': ListField(desc='所属角色', is_required=False, fmt=IntField(desc="角色ID")),
        'main_dept': IntField(desc="员工主部门", is_required=False),
        'department_ids': ListField(desc='所属部门', is_required=False, fmt=IntField(desc="部门ID")),
        'p_start_time': DatetimeField(desc="入组时间", is_required=False),
        'p_end_time': DatetimeField(desc="保护截止时间", is_required=False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "添加员工接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        """判断是否为管理员"""
        staff_admin = self.auth_user
        """身份证号是否存在"""
        StaffServer.check_exist(request.user_info['identity'])

        """创建员工"""
        staff = StaffServer.register(**request.user_info)

        """添加权限关系"""
        if 'role_ids' in request.user_info:
            StaffPermiseServer.generate_staff_access(request.user_info['role_ids'], "role", staff)

        if 'department_ids' in request.user_info:
            StaffPermiseServer.generate_staff_access(request.user_info['department_ids'], "department", staff)

        if 'main_dept' in request.user_info:
            StaffPermiseServer.generate(request.user_info['main_dept'], 'department', staff, is_main='yes')

    def fill(self, response):
        return response


class Get(StaffAuthorizedApi):
    """获取个人中心详情"""
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.user_info = ResponseField(DictField, desc="用户详情", conf={
        'name': CharField(desc="姓名"),
        'identity': CharField(desc="身份证"),
        'gender': CharField(desc="性别"),
        'birthday': CharField(desc="生日"),
        'phone': CharField(desc="电话"),
        'email': CharField(desc="邮箱"),
        'number': CharField(desc="员工工号"),
        'department': CharField(desc="员工部門"),
        'role': CharField(desc="员工角色"),
        'is_admin': BooleanField(desc="是否是管理员"),
    })

    @classmethod
    def get_desc(cls):
        return "员工个人中心详情接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        return StaffServer.user_info(self.auth_user)

    def fill(self, response, staff):
        response.user_info = {
            'name': staff.name,
            'number': staff.number,
            'identity': staff.identity,
            'gender': staff.gender,
            'birthday': staff.birthday,
            'phone': staff.phone,
            'email': staff.email,
            'department': staff.department,
            'role': staff.role,
            'is_admin': staff.is_admin
        }
        return response


class Update(StaffAuthorizedApi):
    """修改个人中心详情"""
    request = with_metaclass(RequestFieldSet)
    request.user_info = RequestField(DictField, desc="用户详情", conf={
        'name': CharField(desc="姓名", is_required=False),
        'gender': CharField(desc="性别", is_required=False),
        'birthday': DateField(desc="生日", is_required=False),
        'phone': CharField(desc="电话", is_required=False),
        'email': CharField(desc="邮箱", is_required=False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "员工个人中心修改接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        staff = self.auth_user

        StaffServer.update(staff, **request.user_info)

    def fill(self, response):
        return response


class Match(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.keyword = RequestField(CharField, desc="匹配信息")
    request.size = RequestField(IntField, desc="返回数量", is_required=False)

    response = with_metaclass(ResponseFieldSet)
    response.match_list = ResponseField(ListField, desc='账号列表', fmt=DictField(desc="账号列表", conf={
        'id': IntField(desc="员工id"),
        'name': CharField(desc="姓名"),
        'gender': CharField(desc="性别"),
        'number': CharField(desc="工号"),
        'phone': CharField(desc="手机号"),
    }))

    @classmethod
    def get_desc(cls):
        return "通过员工部分姓名匹配员工基础信息"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        staff_list = StaffServer.match(request.keyword, request.size)
        return staff_list

    def fill(self, response, staff_list):
        response.match_list = [{
            'id': staff.id,
            'name': staff.name,
            'gender': staff.gender,
            'number': staff.number,
            'phone': staff.phone,
            'email': staff.email,
        } for staff in staff_list]
        return response


class Roster(StaffAuthorizedApi):
    """员工花名册列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc="当前查询页码")
    request.search_info = RequestField(DictField, desc='搜索条件', conf={
        'keyword': CharField(desc="关键词", is_required=False),
        'department': IntField(desc="部门查询", is_required=False),
        'role': IntField(desc="角色查询", is_required=False),
        'is_working': BooleanField(desc="是否在职", is_required=False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc='员工列表', fmt=DictField(desc="员工列表", conf={
        'id': IntField(desc="员工id"),
        'username': CharField(desc="账号"),
        'name': CharField(desc="姓名"),
        'gender': CharField(desc="性别"),
        'number': CharField(desc="工号"),
        'phone': CharField(desc="手机号"),
        'email': CharField(desc="邮箱"),
        'status': CharField(desc="账号状态"),
        'birthday': DateField(desc="生日"),
        'identity': CharField(desc="身份证"),
        'address': CharField(desc="家庭住址"),
        'emergency_contact': CharField(desc="紧急联系人"),
        'emergency_phone': CharField(desc="紧急联系人电话"),
        'entry_time': DateField(desc="入职时间"),
        'education': CharField(desc="学历"),
        'bank_number': CharField(desc="招行卡号"),
        'contract_b': CharField(desc="合同编号（必）"),
        'contract_l': CharField(desc="合同编号（立）"),
        'expire_time': DateField(desc="到期时间"),
        'quit_time': DateField(desc="离职时间", is_required=False),
        'is_working': IntField(desc="是否在职(0离职，1在职)"),
        'last_login_time': DatetimeField(desc="最后登陆时间"),
        'last_login_ip': CharField(desc="最后登陆ip"),
        'p_start_time': DatetimeField(desc="入组时间"),
        'p_end_time': DatetimeField(desc="保护截止时间时间"),
        'main_dept': IntField(desc="员工主部门"),
        'main_dept_name': CharField(desc="主部门名称"),
        'role_list': ListField(desc='所属角色', fmt=DictField(desc="角色信息", conf={
            'role_id': IntField(desc="角色id"),
            'role_name': CharField(desc="角色名称"),
        })),
        'department_list': ListField(desc='所属部门', fmt=DictField(desc="部门信息", conf={
            'department_id': IntField(desc="部门id"),
            'department_name': CharField(desc="部门名称"),
        })),
    }))
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")

    @classmethod
    def get_desc(cls):
        return "员工列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        staff_pages = StaffServer.search(request.current_page, **request.search_info)
        staff_list = StaffPermiseServer.hung_permise_forstaffs(staff_pages.data)
        staff_list = StaffAccountServer.hung_account_forstaffs(staff_list)
        staff_pages.data = staff_list
        return staff_pages

    def fill(self, response, staff_pages):
        response.data_list = [{
            'id': staff.id,
            'username': staff.account.username if staff.account else "",
            'name': staff.name,
            'gender': staff.gender,
            'number': staff.number,
            'phone': staff.phone,
            'email': staff.email,
            'status': staff.account.status if staff.account else "",
            'birthday': staff.birthday if staff.birthday else "",
            'identity': staff.identity,
            'emergency_contact': staff.emergency_contact,
            'emergency_phone': staff.emergency_phone,
            'address': staff.address,
            'entry_time': staff.entry_time if staff.entry_time else "",
            'education': staff.education,
            'bank_number': staff.bank_number,
            'contract_b': staff.contract_b,
            'contract_l': staff.contract_l,
            'expire_time': staff.expire_time if staff.expire_time else "",
            'quit_time': staff.quit_time if staff.quit_time else "",
            'is_working': staff.is_working,
            'p_start_time': staff.p_start_time,
            'p_end_time': staff.p_end_time,
            'main_dept': staff.main_dept,
            'main_dept_name': staff.main_dept_name,
            'last_login_time': staff.account.last_login_time if staff.account and staff.account.last_login_time else "",
            'last_login_ip': staff.account.last_login_ip if staff.account else "",
            'role_list': [{
                'role_id': role.id,
                'role_name': role.name
            } for role in staff.role_list],
            'department_list': [{
                'department_id': department.id,
                'department_name': department.name,
            } for department in staff.department_list]
        } for staff in staff_pages.data]
        response.total = staff_pages.total
        response.total_page = staff_pages.total_page
        return response


class Search(StaffAuthorizedApi):
    """员工搜索列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc="当前查询页码")
    request.search_info = RequestField(DictField, desc='搜索条件', conf={
        'keyword': CharField(desc="关键词", is_required=False),
        'department': IntField(desc="部门查询", is_required=False),
        'role': IntField(desc="角色查询", is_required=False),
        'is_working': BooleanField(desc="是否在职", is_required=False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc='员工列表', fmt=DictField(desc="员工列表", conf={
        'id': IntField(desc="员工id"),
        # 'username': CharField(desc = "账号"),
        'name': CharField(desc="姓名"),
        'gender': CharField(desc="性别"),
        'number': CharField(desc="工号"),
        'phone': CharField(desc="手机号"),
        'email': CharField(desc="邮箱"),
        'status': CharField(desc="账号状态"),
        'birthday': DateField(desc="生日"),
        # 'identity': CharField(desc = "身份证"),
        # 'address': CharField(desc = "家庭住址"),
        # 'emergency_contact': CharField(desc = "紧急联系人"),
        # 'emergency_phone': CharField(desc = "紧急联系人电话"),
        'entry_time': DateField(desc="入职时间"),
        # 'education': CharField(desc = "学历"),
        # 'bank_number': CharField(desc = "招行卡号"),
        # 'contract_b': CharField(desc = "合同编号（必）"),
        # 'contract_l': CharField(desc = "合同编号（立）"),
        # 'expire_time': DateField(desc = "到期时间"),
        'quit_time': DateField(desc="离职时间"),
        'is_working': IntField(desc="是否在职(0离职，1在职)"),
        'last_login_time': DatetimeField(desc="最后登陆时间"),
        'last_login_ip': CharField(desc="最后登陆ip"),
        'role_list': ListField(desc='所属角色', fmt=DictField(desc="角色信息", conf={
            'role_id': IntField(desc="角色id"),
            'role_name': CharField(desc="角色名称"),
        })),
        'department_list': ListField(desc='所属部门', fmt=DictField(desc="部门信息", conf={
            'department_id': IntField(desc="部门id"),
            'department_name': CharField(desc="部门名称"),
        })),
    }))
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")

    @classmethod
    def get_desc(cls):
        return "员工列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        cur_user = self.auth_user
        user_pro = UserRightServer(cur_user)
        request.search_info['cur_user'] = user_pro
        staff_pages = StaffServer.search(request.current_page, **request.search_info)
        staff_list = StaffPermiseServer.hung_permise_forstaffs(staff_pages.data)
        staff_list = StaffAccountServer.hung_account_forstaffs(staff_list)
        staff_pages.data = staff_list
        return staff_pages

    def fill(self, response, staff_pages):
        response.data_list = [{
            'id': staff.id,
            # 'username': staff.account.username if staff.account else "",
            'name': staff.name,
            'gender': staff.gender,
            'number': staff.number,
            'phone': staff.phone,
            'email': staff.email,
            'status': staff.account.status if staff.account else "",
            'birthday': staff.birthday if staff.birthday else "",
            # 'identity': staff.identity,
            # 'emergency_contact': staff.emergency_contact,
            # 'emergency_phone': staff.emergency_phone,
            # 'address': staff.address,
            'entry_time': staff.entry_time if staff.entry_time else "",
            # 'education': staff.education,
            # 'bank_number': staff.bank_number,
            # 'contract_b': staff.contract_b,
            # 'contract_l': staff.contract_l,
            'expire_time': staff.expire_time if staff.expire_time else "",
            'quit_time': staff.quit_time if staff.quit_time else "",
            'is_working': staff.is_working,
            'last_login_time': staff.account.last_login_time if staff.account and staff.account.last_login_time else "",
            'last_login_ip': staff.account.last_login_ip if staff.account else "",
            'role_list': [{
                'role_id': role.id,
                'role_name': role.name
            } for role in staff.role_list],
            'department_list': [{
                'department_id': department.id,
                'department_name': department.name
            } for department in staff.department_list]
        } for staff in staff_pages.data]
        response.total = staff_pages.total
        response.total_page = staff_pages.total_page
        return response


class SearchAll(StaffAuthorizedApi):
    """员工列表"""
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(DictField, desc='搜索条件', conf={
        'keyword': CharField(desc="关键词", is_required=False),
        'is_working': CharField(desc="是否在职", is_required=False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc='账号列表', fmt=DictField(desc="账号列表", conf={
        'id': IntField(desc="员工id"),
        'name': CharField(desc="姓名"),
        'number': CharField(desc="员工工号"),
    }))

    @classmethod
    def get_desc(cls):
        return "员工列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        staff_list = StaffServer.search_all(**request.search_info)

        return staff_list

    def fill(self, response, staff_list):
        response.data_list = [{
            'id': staff.id,
            'name': staff.name,
            'number': staff.number,
        } for staff in staff_list]
        return response


class SearchAllFaker(StaffAuthorizedApi):
    """员工列表"""
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(DictField, desc='搜索条件', conf={
        'keyword': CharField(desc="关键词", is_required=False),
        'is_working': CharField(desc="是否在职", is_required=False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc='账号列表', fmt=DictField(desc="账号列表", conf={
        'id': IntField(desc="员工id"),
        'name': CharField(desc="姓名"),
        'number': CharField(desc="员工工号"),
    }))

    @classmethod
    def get_desc(cls):
        return "员工列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        cur_user = self.auth_user
        user_pro = UserRightServer(cur_user)
        request.search_info.update({"id__in": user_pro._staff_id_list})
        staff_list = StaffServer.search_all(**request.search_info)
        return staff_list

    def fill(self, response, staff_list):
        response.data_list = [{
            'id': staff.id,
            'name': staff.name,
            'number': staff.number,
        } for staff in staff_list]
        return response


class UpdateByAdmin(StaffAuthorizedApi):
    """修改员工账号信息"""
    request = with_metaclass(RequestFieldSet)
    request.user_id = RequestField(IntField, desc='员工id')
    request.user_info = RequestField(DictField, desc="员工详情", conf={
        'name': CharField(desc="姓名"),
        'birthday': DateField(desc="生日", is_required=False),
        'phone': CharField(desc="手机", is_required=False),
        'email': CharField(desc="邮箱", is_required=False),
        'gender': CharField(desc="性别(man,woman)", is_required=False),
        'identity': CharField(desc="身份证", is_required=False),
        'emergency_contact': CharField(desc="紧急联系人", is_required=False),
        'emergency_phone': CharField(desc="紧急联系人电话", is_required=False),
        'address': CharField(desc="家庭住址", is_required=False),
        'entry_time': DateField(desc="入职时间", is_required=False),
        'education': CharField(desc="学历", is_required=False),
        'bank_number': CharField(desc="招行卡号", is_required=False),
        'contract_b': CharField(desc="合同编号（必）", is_required=False),
        'contract_l': CharField(desc="合同编号（立）", is_required=False),
        'expire_time': DateField(desc="到期时间", is_required=False),
        'is_working': BooleanField(desc="是否在职(0离职，1在职)", is_required=False),
        'quit_time': DateField(desc="离职时间", is_required=False),
        'role_ids': ListField(desc='所属角色', is_required=False, fmt=IntField(desc="角色ID")),
        'department_ids': ListField(desc='所属部门', is_required=False, fmt=IntField(desc="部门ID")),
        'p_start_time': DatetimeField(desc="入组时间", is_required=False),
        'p_end_time': DatetimeField(desc="保护截止时间", is_required=False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "修改员工接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        """获得员工信息"""
        staff = StaffServer.get(request.user_id)
        """判断身份证号是否存在"""
        if "identity" in request.user_info:
            StaffServer.check_exist(request.user_info['identity'], staff)

        StaffServer.update(staff, **request.user_info)
        '''更新账号信息
        account = StaffAccountServer.get_account_bystaff(staff)
        StaffAccountServer.update(account, **request.user_info)
        '''

        '''更新权限信息'''
        StaffPermiseServer.update_staff_access(request.user_info['role_ids'], "role", staff)
        StaffPermiseServer.update_staff_access(request.user_info['department_ids'], "department", staff)
        if 'p_start_time' in request.user_info:
            StaffServer.add_work_time(request.user_id, **request.user_info)

    def fill(self, response):
        return response


class GetByadmin(StaffAuthorizedApi):
    """获取员工账号及个人信息"""
    request = with_metaclass(RequestFieldSet)
    request.user_id = RequestField(IntField, desc='员工id')

    response = with_metaclass(ResponseFieldSet)
    response.user_info = ResponseField(DictField, desc='员工详情', conf={
        'id': IntField(desc="员工id"),
        'name': CharField(desc="姓名"),
        'gender': CharField(desc="性别"),
        'number': CharField(desc="工号"),
        'phone': CharField(desc="手机号"),
        'email': CharField(desc="邮箱"),
        'birthday': DateField(desc="生日"),
        'identity': CharField(desc="身份证"),
        'emergency_contact': CharField(desc="紧急联系人"),
        'emergency_phone': CharField(desc="紧急联系人电话"),
        'address': CharField(desc="家庭住址"),
        'entry_time': DateField(desc="入职时间"),
        'education': CharField(desc="学历"),
        'bank_number': CharField(desc="招行卡号"),
        'contract_b': CharField(desc="合同编号（必）"),
        'contract_l': CharField(desc="合同编号（立）"),
        'expire_time': DateField(desc="到期时间"),
        'quit_time': DateField(desc="离职时间"),
        'is_working': IntField(desc="是否在职(0离职，1在职)"),
        'role_list': ListField(desc='所属角色', fmt=DictField(desc="角色信息", conf={
            'role_id': IntField(desc="角色id"),
            'role_name': CharField(desc="角色名称"),
        })),
        'department_list': ListField(desc='所属部门', fmt=DictField(desc="部门信息", conf={
            'department_id': IntField(desc="部门id"),
            'department_name': CharField(desc="部门名称"),
        })),
    })

    @classmethod
    def get_desc(cls):
        return "账号员工详情接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        staff_admin = self.auth_user
        StaffServer.judge_staff_role(staff_admin)

        staff = StaffServer.get(request.user_id)

        staff = StaffPermiseServer.hung_permise_bystaff(staff)
        # staff_list = StaffAccountServer.hung_account_forstaffs(staff_list)

        return staff

    def fill(self, response, staff):
        response.user_info = {
            'id': staff.id,
            'name': staff.name,
            'gender': staff.gender,
            'number': staff.number,
            'phone': staff.phone,
            'email': staff.email,
            'birthday': staff.birthday,
            'identity': staff.identity,
            'emergency_contact': staff.emergency_contact,
            'emergency_phone': staff.emergency_phone,
            'address': staff.address,
            'entry_time': staff.entry_time,
            'education': staff.education,
            'bank_number': staff.bank_number,
            'contract_b': staff.contract_b,
            'contract_l': staff.contract_l,
            'expire_time': staff.expire_time,
            'is_working': staff.is_working,
            'role_list': [{
                'role_id': role.id,
                'role_name': role.name
            } for role in staff.role_list],
            'department_list': [{
                'department_id': department.id,
                'department_name': department.name
            } for department in staff.department_list]
        }
        return response


class InputWorkTime(StaffAuthorizedApi):
    """添加入组时间"""
    request = with_metaclass(RequestFieldSet)
    request.staff_id = RequestField(IntField, desc="员工ID")
    request.input_info = RequestField(DictField, desc="", conf={
        'p_start_time': DatetimeField(desc="入组时间"),
        'p_end_time': DatetimeField(desc="保护截止时间", is_required=False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "添加员工入组时间接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        StaffServer.add_work_time(request.staff_id, **request.input_info)

    def fill(self, response):
        return response


class PositionTransfer(StaffAuthorizedApi):
    """调岗接口"""
    request = with_metaclass(RequestFieldSet)
    request.staff_id = RequestField(IntField, desc="员工ID")
    request.input_info = RequestField(DictField, desc="", conf={
        'transfer_time': DatetimeField(desc="调岗时间"),
        'src_dept': IntField(desc="原部门ID"),
        'desc_dept': IntField(desc="目标部门ID"),
        'remark': CharField(desc="备注", is_required=False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "员工调岗接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        user = self.auth_user
        request.input_info.update({'operator': user})
        StaffServer.transfer_position(request.staff_id, **request.input_info)

    def fill(self, response):
        return response
