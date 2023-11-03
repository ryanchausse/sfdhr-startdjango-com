from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email
from django.http import HttpResponse
from django.forms import ValidationError


class NormSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email_address = user_email(sociallogin.user)
        email_domain = email_address.split("@")[1]
        if email_domain != 'gmail.com':
            return HttpResponse('Please log in with a Google account. You \
                                may have to log out of your current Gmail account. \
                                Try again at <a href="./">Norm Form</a>')
        elif email_address not in ['chausse@gmail.com',]:
            return HttpResponse('You are not authorized to log in. \
                                Try again at <a href="./">MeritBridge Replacement App</a>')
