from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from todoapp.consumers import TodoConsumer 
application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket' : AllowedHostsOriginValidator(
            SessionMiddlewareStack(
                AuthMiddlewareStack(
                    URLRouter(
                        [
                            url(r'^groups/$',TodoConsumer),
                            url(r'^groups/(?P<grp_id>[0-9]+)/$',TodoConsumer),
                        ]
                    )
                )
            )
        )
})