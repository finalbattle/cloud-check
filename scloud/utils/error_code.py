# -*- coding: utf-8 -*-

from collections import namedtuple
from tornado.util import ObjectDict
from code import interact

error = namedtuple("operate", ["errvalue", "errcode"])


class ERROR(object):
    system_err = error(errcode=-999999, errvalue=u"系统错误")
    captcha_err = error(errcode=-999409, errvalue=u"验证码错误")
    captcha_empty_err = error(errcode=-999408, errvalue=u"验证码不能为空")
    captcha_expired_err = error(errcode=-999407, errvalue=u"验证码已过期，请刷新重试")
    params_err = error(errcode=-999406, errvalue=u"参数错误")
    params_empty_err = error(errcode=-999405, errvalue=u"参数不能为空")
    not_found_err = error(errcode=-999404, errvalue=u"对不起！您正在访问的数据资源未找到")
    xsrf_err = error(errcode=-999403, errvalue=u"缺少xsrf参数，禁止提交表单")
    database_save_err = error(errcode=-999402, errvalue=u"数据库保存错误")
    # 注册和登录
    username_empty_err      = error(errcode=-100001, errvalue=u"用户名不能为空")
    username_duplicate_err  = error(errcode=-100017, errvalue=u"该用户名已经被使用")
    username_err            = error(errcode=-100002, errvalue=u"该用户名不存在")
    password_empty_err      = error(errcode=-100003, errvalue=u"密码不能为空")
    password_err            = error(errcode=-100004, errvalue=u"密码错误")
    email_empty_err         = error(errcode=-100005, errvalue=u"邮箱不能为空")
    email_format_err        = error(errcode=-100015, errvalue=u"邮箱格式错误")
    email_duplicate_err     = error(errcode=-100016, errvalue=u"该邮箱已经被使用")
    email_err               = error(errcode=-100006, errvalue=u"邮箱错误")
    mobile_empty_err        = error(errcode=-100007, errvalue=u"手机号不能为空")
    mobile_duplicate_err    = error(errcode=-100018, errvalue=u"该手机号已经被使用")
    mobile_format_err       = error(errcode=-100019, errvalue=u"手机号格式不正确")
    mobile_err              = error(errcode=-100008, errvalue=u"手机号错误")
    user_empty_err          = error(errcode=-100009, errvalue=u"操作用户不能为空")
    checker_empty_err       = error(errcode=-100010, errvalue=u"审核用户不能为空")
    old_password_empty_err  = error(errcode=-100011, errvalue=u"旧密码不能为空")
    new_password_empty_err  = error(errcode=-100012, errvalue=u"新密码不能为空")
    repeat_password_empty_err = error(errcode=-100013, errvalue=u"重复密码不能为空")
    repeat_password_err     = error(errcode=-100014, errvalue=u"重复密码与新密码不一致")

    # 创建项目
    pro_id_empty_err        = error(errcode=-100020, errvalue=u"请选择项目")
    pro_name_empty_err        = error(errcode=-100021, errvalue=u"项目名称不能为空")
    pro_name_duplicate_err    = error(errcode=-100022, errvalue=u"项目名称已经存在，请重新输入")
    pro_owner_empty_err       = error(errcode=-100023, errvalue=u"项目负责人不能为空")
    pro_owner_email_empty_err = error(errcode=-100024, errvalue=u"项目负责人邮箱不能为空")
    pro_env_empty_err         = error(errcode=-100025, errvalue=u"项目环境不能为空")

    # 创建资源
    res_id_empty_err              = error(errcode=-100040, errvalue=u"请选择申请资源编号")
    res_computer_empty_err        = error(errcode=-100041, errvalue=u"申请云主机不能为空")
    res_cpu_empty_err             = error(errcode=-100042, errvalue=u"申请CPU不能为空")
    res_memory_empty_err          = error(errcode=-100043, errvalue=u"申请内存不能为空")
    res_disk_empty_err            = error(errcode=-100044, errvalue=u"申请云磁盘不能为空")
    res_disk_amount_empty_err            = error(errcode=-100045, errvalue=u"申请云磁盘不能为空")
    res_disk_backup_empty_err     = error(errcode=-100046, errvalue=u"申请云磁盘备份不能为空")
    res_disk_backup_amount_empty_err     = error(errcode=-100047, errvalue=u"申请云磁盘备份不能为空")
    res_out_ip_empty_err          = error(errcode=-100048, errvalue=u"申请外部IP不能为空")
    res_snapshot_empty_err        = error(errcode=-100049, errvalue=u"申请快照不能为空")
    res_loadbalance_empty_err     = error(errcode=-100050, errvalue=u"申请应用负载均衡不能为空")
    res_internet_ip_empty_err     = error(errcode=-100051, errvalue=u"申请互联网IP不能为空")
    res_bandwidth_empty_err = error(errcode=-100053, errvalue=u"申请是否需要SSL卸载不能为空")
    res_internet_ip_ssl_empty_err = error(errcode=-100052, errvalue=u"申请是否需要SSL卸载不能为空")
    res_start_date_empty_err      = error(errcode=-100054, errvalue=u"申请启动时间不能为空")
    res_period_empty_err          = error(errcode=-100055, errvalue=u"申请资源运行期限不能为空")
    res_unit_fee_empty_err        = error(errcode=-100056, errvalue=u"申请资源费用不能为空")
    res_total_fee_empty_err       = error(errcode=-100057, errvalue=u"申请资源总费用不能为空")
    res_apply_id_empty_err       = error(errcode=-100058, errvalue=u"资源申请不能为空")
    res_reason_empty_err       = error(errcode=-100059, errvalue=u"请填写拒绝资源申请的原因")

    res_computer_invalid_err        = error(errcode=-100060, errvalue=u"申请云主机数据不合法")
    res_cpu_invalid_err             = error(errcode=-100061, errvalue=u"申请CPU数据不合法")
    res_memory_invalid_err          = error(errcode=-100062, errvalue=u"申请内存数据不合法")
    res_disk_invalid_err            = error(errcode=-100063, errvalue=u"申请云磁盘数据不合法")
    res_disk_amount_invalid_err     = error(errcode=-100064, errvalue=u"申请云磁盘容量不合法")
    res_disk_backup_invalid_err     = error(errcode=-100065, errvalue=u"申请云磁盘备份数据不合法")
    res_disk_backup_amount_invalid_err = error(errcode=-100066, errvalue=u"申请云磁盘文件备份空间不合法")
    res_out_ip_invalid_err          = error(errcode=-100067, errvalue=u"申请外部IP数据不合法")
    res_snapshot_invalid_err        = error(errcode=-100068, errvalue=u"申请快照数据不合法")
    res_loadbalance_invalid_err     = error(errcode=-100069, errvalue=u"申请应用负载均衡数据不合法")
    res_internet_ip_invalid_err     = error(errcode=-100070, errvalue=u"申请互联网IP数据不合法")
    res_bandwidth_invalid_err = error(errcode=-100072, errvalue=u"申请是否需要SSL卸载数据不合法")
    res_internet_ip_ssl_invalid_err = error(errcode=-100071, errvalue=u"申请是否需要SSL卸载数据不合法")
    res_start_date_invalid_err      = error(errcode=-100073, errvalue=u"申请启动时间数据不合法")
    res_period_invalid_err          = error(errcode=-100074, errvalue=u"申请资源运行期限数据不合法")
    res_unit_fee_invalid_err        = error(errcode=-100075, errvalue=u"申请资源费用数据不合法")
    res_total_fee_invalid_err       = error(errcode=-100076, errvalue=u"申请资源总费用数据不合法")

    res_do_resource_action_err = error(errcode=-100100, errvalue=u"资源审核操作参数有误")
    res_new_apply_err = error(errcode=-100101, errvalue=u"当前状态不允许申请新的资源配额")
    res_revoke_err = error(errcode=-100102, errvalue=u"当前状态不允许资源撤销")
    res_delete_err = error(errcode=-100103, errvalue=u"当前状态不允许资源删除")
    res_re_apply_err = error(errcode=-100104, errvalue=u"当前状态不允许重复申请资源配额")

    res_check_err = error(errcode=-100105, errvalue=u"当前状态不允许对申请资源配额进行审核")
    res_refuse_err = error(errcode=-100106, errvalue=u"当前状态不允许对申请资源配额进行审核")
    res_pay_err = error(errcode=-100107, errvalue=u"当前状态不允许对申请资源配额进行支付")
    res_confirmpay_err = error(errcode=-100108, errvalue=u"当前状态不允许对申请资源配额进行支付确认")
    res_start_err = error(errcode=-100109, errvalue=u"当前状态不允许对申请资源配额启用")
    res_close_err = error(errcode=-100110, errvalue=u"当前状态不允许对申请资源配额关闭")

    env_name_empty_err = error(errcode=-100120, errvalue=u"环境名称不能为空")
    env_desc_empty_err = error(errcode=-100121, errvalue=u"环境说明不能为空")

    env_internet_ip_name_empty_err = error(errcode=-100140, errvalue=u"互联网IP类型名称不能为空")
    env_internet_ip_name_duplicate_err= error(errcode=-100141, errvalue=u"互联网IP类型名称已经存在，不能重复")
    env_internet_ip_fee_invalid_err= error(errcode=-100142, errvalue=u"费用格式不合法")

    # 互联网发布
    pro_publish_domain_empty_err = error(errcode=-100160, errvalue=u"域名不能为空")
    pro_publish_domain_invalid_err = error(errcode=-100161, errvalue=u"域名不合法")
    pro_publish_domain_port_empty_err = error(errcode=-100162, errvalue=u"互联网端口不能为空")
    pro_publish_domain_port_invalid_err = error(errcode=-100163, errvalue=u"互联网端口必须为大于80小于65535的正整数") 
    pro_publish_network_address_empty_err = error(errcode=-100164, errvalue=u"内网地址不能为空") 
    pro_publish_network_address_invalid_err = error(errcode=-100165, errvalue=u"内网地址不合法")
    pro_publish_network_port_empty_err = error(errcode=-100166, errvalue=u"内网端口不能为空")
    pro_publish_network_port_invalid_err = error(errcode=-100167, errvalue=u"内网端口必须为大于1024小于65535的正整数")

    # 定期备份
    pro_backups_disk_empty_err = error(errcode=-100180, errvalue=u"磁盘不能为空") 
    pro_backups_plot_empty_err = error(errcode=-100181, errvalue=u"备份策略不能为空")
    pro_backups_interval_empty_err = error(errcode=-100182, errvalue=u"时间间隔不能为空")
    pro_backups_backup_time_empty_err =error(errcode=-100183, errvalue=u"备份时间不能为空")

    # 负载均衡
    pro_balance_member_port_empty_err = error(errcode=-100200, errvalue=u"端口不能为空")
    pro_balance_member_address_empty_err = error(errcode=-100201, errvalue=u"ip不能为空")

    # 事件
    pro_event_id_empty_err = error(errcode=-100220, errvalue=u"事件编码不能为空")
    pro_event_title_empty_err = error(errcode=-100221, errvalue=u"事件标题不能为空")
    pro_event_title_duplicate_err = error(errcode=-100222, errvalue=u"不允许提交重复事件")
    pro_event_content_empty_err = error(errcode=-100223, errvalue=u"事件内容不能为空")
    pro_event_reply_content_empty_err = error(errcode=-100224, errvalue=u"事件回复内容不能为空")


ERR = ObjectDict()
for attr in dir(ERROR):
    err = getattr(ERROR, attr)
    if isinstance(err, error):
        setattr(ERR, attr.upper(), err.errcode)
        setattr(ERR, str(err.errcode), err.errvalue)

if __name__ == '__main__':
    # interact(local=locals())
    print ERROR.username_err
