import os
from django.core.mail import EmailMultiAlternatives
def send_emali(to_email,context):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'untitled2.settings'
    subject, from_email, to = '来自唐林的的一份测试邮件', '1753215994@qq.com', to_email
    text_content = '欢迎'
    html_content = '<p>%s</p>'%(context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()