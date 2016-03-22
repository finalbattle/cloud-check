#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

import os
import requests
from scloud.const import act_actions
from scloud.config import logger, CONF
from scloud.celeryapp import celery
from scloud.models.act import Act_History, Act_Pro_History
from scloud.models.base import DataBaseService
from scloud.shortcuts import render_to_string
from scloud.utils.publish.tasks import publish_notice_tasks


@celery.task
def task_act_post(act_type=1, table_name="", table_doc=""):
    logger.info("------[celery task post act]------")
    logger.info("------[ act type %s ]------" % act_type)
    with DataBaseService({}) as svc:
        act = Act_History()
        act.act_type = act_type
        act.desc = act_actions[act_type].value % table_doc
        svc.db.add(act)


@celery.task
def task_post_action(act_type=1, content=u"", user_id=0):
    logger.info("------[celery task post action]------")
    logger.info("------[ act type %s ]------" % act_type)
    with DataBaseService({}) as svc:
        act = Act_History()
        act.act_type = act_type
        act.desc = content
        act.user_id = user_id
        svc.db.add(act)

@celery.task
def task_post_pro_res_apply_history(status=0, content=u"", pro_id=0, res_apply_id=0, user_id=0, checker_id=0):
    logger.info("------[celery task post action]------")
    with DataBaseService({}) as svc:
        act = Act_Pro_History()
        act.pro_id = pro_id
        act.res_apply_id = res_apply_id
        act.status = status
        act.desc = content
        act.user_id = user_id
        act.checker_id = checker_id
        svc.db.add(act)

    if checker_id:
        this_id = checker_id
        user_id = user_id
        action = "on_notice_user"
    else:
        this_id = user_id
        user_id = checker_id
        action = "on_notice_checker"
    logger.info("#"*30+" [user %s notice tasks] " % user_id+"#"*30)
    logger.info("[action]: %s, [user_id]: %s" % (action, user_id))
    # data = {
    #     "user_id": user_id,
    #     "action": action,
    #     "res_id": res_apply_id,
    #     "this_id": this_id
    # }
    # params = ["%s=%s" % (k, v) for k, v in data.items()]
    # url = "%s?%s" % (os.path.join(CONF("PUB_HOST"), "scloud/comet/tasks"), "&".join(params))
    # logger.info(url)
    # request_result = requests.get(url)
    request_result = publish_notice_tasks(action, user_id, this_id)
    logger.info(request_result)
    logger.info("#"*30+" [user %s notice tasks] " % user_id+"#"*30)
    # request_result = requests.get("%s?%s" % (os.path.join(CONF("DOMAIN_HOST"), "scloud/comet/tasks"), "&".join(params)))
        # logger.info(request_result)
