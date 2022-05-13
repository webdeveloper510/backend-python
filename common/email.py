from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail


def send_email(to, subject, message):
    from_email = 'notification@moppetto.com'
    # subject = 'Subject here'
    # message = 'Here is the message.'
    # to = ['patelsmit566@gmail.com']
    send_mail(
        subject,
        message,
        from_email,
        to,
        fail_silently=False,
    )


def send_multi_email(to, subject, message_text, message_html):
    '''
    send_multi_email("patelsmit566@gmail.com", "This is test subject", 'This is an important message.', '<p>This is an <strong>important</strong> message.</p>')
    '''

    subject, from_email, to = subject, 'notification@moppetto.com', to

    # text_content = 'This is an important message.'
    # html_content = '<p>This is an <strong>important</strong> message.</p>'
    text_content = message_text
    html_content = message_html

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    ret = msg.send()
    return ret
