# -*- coding: utf-8 -*-

from datetime import datetime
# from tornado import gen
from scloud.services.base import BaseService
# from scloud.models.base import MYSQL_POOL
# from scloud.models.pt_user import PT_User
from scloud.models.project import Pro_Info
from scloud.config import logger, thrownException
from sqlalchemy import and_
from scloud.utils.error_code import ERROR
# from scloud.utils.error import NotFoundError
from scloud.const import STATUS_PRO_TABLES
from scloud.models.project import Pro_Backup
from scloud.models.pt_user import PT_User 
import simplejson


class ApplyBackups(BaseService):

    @thrownException
    def get_backups(self):
        pro_id = self.params.get("pro_id")
        pro_info = self.db.query(
            Pro_Info
        ).filter(
            Pro_Info.id == pro_id
        ).first()
        applies = pro_info.pro_resource_applies
        last_apply = applies[-1]
        backups_plot = last_apply.backups_plot
        return self.success(data=backups_plot)

    @thrownException
    def get_info(self):
        id = self.params.get("id")
        pro_backup = self.db.query(
            Pro_Backup
        ).filter(
            Pro_Backup.id == id
        ).first()
        return self.success(data=pro_backup)

    @thrownException
    def get_list(self):
        id = self.params.get("id")
        pro_id = self.params.get("pro_id")
        search = self.params.get("search", "")
        status = self.params.get("status", -3)
        conditions = and_()
        user_id = self.params.get("user_id")
        if user_id:
            pt_user = self.db.query(
                PT_User
            ).filter(
                PT_User.id == user_id
            ).first()
            if pt_user and not pt_user.imchecker:
                conditions.append(Pro_Backup.user_id == user_id)
        if id:
            conditions.append(Pro_Backup.id == id)
        if pro_id:
            conditions.append(Pro_Backup.pro_id == pro_id)
        if search:
            conditions.append(Pro_Backup.title.like('%' + search + '%'))
        if status > -3:
            conditions.append(Pro_Backup.status == status)
        pro_backup_list = self.db.query(
            Pro_Backup
        ).filter(
            conditions
        ).order_by(
            Pro_Backup.id.desc()
        ).all()
        return self.success(data=pro_backup_list)

    @thrownException
    def do_backups(self):
        pro_id = self.params.get("pro_id")
        res_apply_id = self.params.get("res_apply_id")
        plot_str = self.params.get("backups", "")
        plot_s = simplejson.loads(plot_str) 
        g_plot_messages = []
        for index, plot_mem in enumerate(plot_s):
            disk = plot_mem['disk']
            plot = plot_mem['plot']
            interval = plot_mem['interval']
            backup_time = plot_mem['backup_time']
            plot_messages = []
            if not disk:
                plot_messages.append(self.failure(ERROR.pro_backups_disk_empty_err).return_message)
                g_plot_messages.append(self.failure(ERROR.pro_backups_disk_empty_err).return_message)
                # return self.failure(ERROR.pro_backups_disk_empty_err)
            if not plot:
                plot_messages.append(self.failure(ERROR.pro_backups_plot_empty_err).return_message)
                g_plot_messages.append(self.failure(ERROR.pro_backups_plot_empty_err).return_message)
                # return self.failure(ERROR.pro_backups_plot_empty_err)
            if plot in [u"月", u"周"] and not interval:
                plot_messages.append(self.failure(ERROR.pro_backups_interval_empty_err).return_message)
                g_plot_messages.append(self.failure(ERROR.pro_backups_interval_empty_err).return_message)
                # return self.failure(ERROR.pro_backups_interval_empty_err)
            if not backup_time:
                plot_messages.append(self.failure(ERROR.pro_backups_backup_time_empty_err).return_message)
                g_plot_messages.append(self.failure(ERROR.pro_backups_backup_time_empty_err).return_message)
                # return self.failure(ERROR.pro_backups_backup_time_empty_err)
            plot_mem["failures"] = plot_messages
        logger.info(plot_s)
        do_backups_info, created = Pro_Backup.get_or_create_obj(self.db, pro_id=pro_id)
        do_backups_info.pro_id = pro_id
        do_backups_info.res_apply_id = res_apply_id
        do_backups_info.user_id = self.handler.current_user.id
        logger.info("len(plot_messages): %s" % len(g_plot_messages))
        if len(g_plot_messages) == 0:
            do_backups_info.status = 0
            do_backups_info.plot = plot_str
            self.db.add(do_backups_info)
            self.db.flush()
            # do_backups_info.plot = plot_str
            return self.success(data=do_backups_info)
        else:
            do_backups_info.status = -1
            do_backups_info.plot = simplejson.dumps(plot_s)
            return self.failures(g_plot_messages, data=do_backups_info)

    @thrownException
    def do_del_pro_backup(self):
        id_list = self.params.get("id_list")
        for id in id_list:
            pro_backup = self.db.query(
                Pro_Backup
            ).filter(
                Pro_Backup.id == id    
            ).first()
            self.db.delete(pro_backup)
            self.db.flush()
        return self.success(data=None)
