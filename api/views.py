from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

import logging
import json
import provider.oauth2
from provider.oauth2.models import AccessToken

# OAuth exception class
class OAuthError(RuntimeError):
    def __init__(self, message='OAuth error occured.'):
        self.message = message

# Authenticates a two legged Oauth request 
def is_authenticated(request, **kwargs):

    try:
        key = request.GET.get('token')
        if not key:
            key = request.POST.get('token')
        if not key:
            auth_header_value = request.META.get('HTTP_AUTHORIZATION')
            if auth_header_value:
                key = auth_header_value.split(' ')[1]
        if not key:
            logging.error('OAuth20Authentication. No consumer_key found.')
            return False

        token = verify_access_token(key)

        # Set the request user to the token user for authorization if Oauth is successful
        request.user = token.user

        # Also set oauth_consumer_key on request.
        request.META['token'] = key

    except KeyError, e:
        logging.exception("Error in OAuth20Authentication.")
        request.user = AnonymousUser()
        return False
    except Exception, e:
        logging.exception("Error in OAuth20Authentication.")
        return False

    # Oauth successfull! Yay!
    return True

def verify_access_token(key):
    try:
        token = AccessToken.objects.get(token=key)

        if token.expires < timezone.now():
            raise OAuthError('AccessToken has expired.')
    except AccessToken.DoesNotExist, e:
        raise OAuthError("AccessToken not found at all.")

    logging.info('Valid access')
    return token

# Verifies a token sent by API client and sends back client's username
@csrf_exempt
def verify_token(request):

    if is_authenticated(request) == False:
        return HttpResponse(
            json.dumps({
                'error': 'invalid_request'
            }),
            status = 403
        )

    return HttpResponse(
        json.dumps({
            'user': request.user.username
        })
    )