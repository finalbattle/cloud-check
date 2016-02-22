# -*- coding: utf-8 -*-

from datetime import datetime
from tornado import gen
from scloud.services.base import BaseService
from scloud.models.base import MYSQL_POOL
from scloud.models.pt_user import PT_User, PT_User_Role
from scloud.config import logger, thrownException
from sqlalchemy import and_
from scloud.utils.permission import GROUP, OP
from scloud.utils.error_code import ERROR


class RegisterService(BaseService):
    @thrownException
    def do_register(self):
        email = self.params.get("email", "").strip()
        mobile = self.params.get("mobile", "").strip().replace(' ', '')
        password = self.params.get("password", "").strip()
        if email == "":
            return self.failure(ERROR.email_empty_err)
        if mobile == "":
            return self.failure(ERROR.mobile_empty_err)
        if password == "":
            return self.failure(ERROR.password_empty_err)
        instance, created = PT_User.get_or_create(email=email, mobile=mobile, password=password)
        PT_User_Role.get_or_create(user_id=instance.id, role_id=2)
        conditions = and_()
        conditions.append(PT_User.id == instance.id)
        conditions.append(PT_User.is_enable == 1)
        user_info = self.db.query(
            PT_User
        ).filter(
            conditions
        ).first()
        if user_info:
            # LOGIN SUCCESS
            user_roles = user_info.user_roles
            current_perms = {}
            for user_role in user_roles:
                group_ops = user_role.role.group_ops
                for group_op in group_ops:
                    g_keyword = GROUP[group_op.group_keycode].keyword
                    op_keyword = OP[group_op.op_keycode].keyword
                    g_keycode = group_op.group_keycode
                    op_keycode = group_op.op_keycode
                    current_perms.update({"%s.%s" % (g_keyword, op_keyword): "%s.%s" % (g_keycode, op_keycode)})
            setattr(user_info, "current_perms", current_perms)
            result = self.success(data=user_info)
            user_info.last_login = datetime.now()
            self.db.add(user_info)
            self.db.commit()
            return result
        else:
            return self.failure(ERROR.username_err)