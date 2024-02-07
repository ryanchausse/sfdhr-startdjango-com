from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email
from django.http import HttpResponse
from django.forms import ValidationError


class NormSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email_address = user_email(sociallogin.user)
        email_domain = email_address.split("@")[1]
        if email_domain != 'gmail.com':
            return HttpResponse(f'Please log in with a Google account. You '
                                f'may have to log out of your current Gmail '
                                f'account. Try again at '
                                f'<a href="./">MeritBridge Replacement App</a>')
        # if email_address not in ['chausse@gmail.com',]:
        #     return HttpResponse(f'You are not authorized to log in.'
        #                         f'Try again at '
        #                         f'<a href="./">MeritBridge Replacement App</a>')
