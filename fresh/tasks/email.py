import os
from flask_mail import Message
from fresh.app import celery
from fresh.extends import mail


def _send_mail(sub, content, to_list):
    """ 发送邮件
    :param sub: 标题
    :param content: 内容
    :pram to_list: 接受者邮件列表
    """
    if not isinstance(to_list, list):
        to_list = [to_list]

    msg = Message(
        subject=sub,
        recipients=to_list,
    )
    msg.body = content
    mail.send(msg)


@celery.task
def send_mail(sub, content, to_list):
    """ 发送邮件异步"""
    _send_mail(sub, content, to_list)