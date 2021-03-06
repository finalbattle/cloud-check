# -*- coding: utf-8 -*-

from datetime import datetime
from tornado import gen
from scloud.services.base import BaseService
from scloud.models.base import MYSQL_POOL
from scloud.models.pt_user import PT_User
from scloud.models.project import Pro_Info, Pro_Resource_Apply
from scloud.config import logger, thrownException
from sqlalchemy import and_, or_
from scloud.utils.error_code import ERROR
from scloud.utils.error import NotFoundError
from scloud.const import pro_resource_apply_status_types, STATUS_RESOURCE
from scloud.services.svc_pro_resource_apply import mail_title_format
from scloud.services.svc_login import LoginService


class ProfileService(BaseService):

    @thrownException
    def get_profile(self):
        logger.info("------[get_profile]------")
        current_user_id = self.handler.current_user.id
        if current_user_id:
            pt_user = self.db.query(
                PT_User
            ).filter(
                PT_User.id == current_user_id
            ).first()
            return self.success(data=pt_user)
        else:
            return NotFoundError()

    @thrownException
    def set_profile(self):
        logger.info("------[set_profile]------")
        user_id = int(self.params.get("user_id"))
        username = self.params.get("username")
        email = self.params.get("email")
        mobile = self.params.get("mobile")
        current_user = self.handler.current_user
        if current_user:
            if current_user.id != user_id:
                raise NotFoundError()
            if not username:
                return self.failure(ERROR.username_empty_err)
            if not email:
                return self.failure(ERROR.email_empty_err)
            if not mobile:
                return self.failure(ERROR.mobile_empty_err)
            user = self.db.query(
                PT_User
            ).filter(
                PT_User.id == user_id
            ).first()
            username_duplicate = self.db.query(
                PT_User
            ).filter(
                PT_User.id != user_id, PT_User.username == username
            ).first()
            logger.info(username_duplicate)
            if username_duplicate:
                return self.failure(ERROR.username_duplicate_err)
            email_duplicate = self.db.query(
                PT_User
            ).filter(
                PT_User.id != user_id, PT_User.email == email
            ).first()
            if email_duplicate:
                return self.failure(ERROR.email_duplicate_err)
            mobile_duplicate = self.db.query(
                PT_User
            ).filter(
                PT_User.id != user_id, PT_User.mobile == mobile
            ).first()
            if mobile_duplicate:
                return self.failure(ERROR.mobile_duplicate_err)
            user.username = username
            user.email = email
            user.mobile = mobile.replace(' ', '')
            self.db.add(user)
            self.db.flush()
            logger.info("*" * 60)
            logger.info(user.username)
            logger.info("*" * 60)
            login = LoginService(self.handler)
            login.set_user_attrs(user)

            # res = project.as_dict()
            # logger.info("project: %s" % res)
            return self.success(data=user)
        else:
            return NotFoundError()

    @thrownException
    def reset_password(self):
        logger.info("------[reset_password]------")
        old_password = self.params.get("old_password")
        new_password = self.params.get("new_password")
        repeat_password = self.params.get("repeat_password")
        current_user = self.handler.current_user
        if not current_user:
            return self.failure(ERROR.not_found_err)
        
        if not old_password:
            return self.failure(ERROR.old_password_empty_err)
        if not new_password:
            return self.failure(ERROR.new_password_empty_err)
        if not repeat_password:
            return self.failure(ERROR.repeat_password_empty_err)
        if current_user.password != old_password:
            return self.failure(ERROR.password_err)
        if new_password != repeat_password:
            return self.failure(ERROR.repeat_password_err)

        user = self.db.query(
            PT_User
        ).filter(
            PT_User.id == current_user.id
        ).first()
        if user:
            user.password = new_password
            self.db.add(user)
            self.db.flush()
            return self.success(data=user)
        else:
            return self.failure(ERROR.not_found_err)
