from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from wagtail.models import Page
from home.utils import send_email


def handle_page_published(sender, instance, **kargs):
    # published_page = sender  # The 'sender' argument will be the page that was published
    # You can also use the 'instance' argument, which represents the page revision
    # that was published, to access the published page
    published_page = instance

    # Now you can work with the 'published_page' object
    page_title = published_page.title
    page_url = published_page.url
    print('page title', page_title)
    print('page url', page_url)
    # subject = 'Page Change Approval'
    # message = f'A page has been updated and is pending approval: {instance.title}'
    # from_email = 'your@email.com'
    # recipient_list = ['testemail@gmail.com']  # Add your moderator emails
    # send_email('gomak0887@gmail.com', message, message, is_html=False)


# @receiver(post_save, sender=Page)
# def send_approval_email(sender, instance, **kwargs):
#     print('===============Wagtail================')
#
#     # Check if the page has been submitted for moderation
#     if instance.get_latest_revision().submitted_for_moderation:
#         subject = 'Page Change Approval'
#         message = f'A page has been updated and is pending approval: {instance.title}'
#         from_email = 'your@email.com'
#         recipient_list = ['moderator1@email.com', 'moderator2@email.com']  # Add your moderator emails
#         send_mail(subject, message, from_email, recipient_list)
