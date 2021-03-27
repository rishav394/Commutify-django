from django.conf.urls import url
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from commutify.restapis import views

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("whoami", views.whoami),
    path("users", views.users),
    path("login", views.login),
    path("sign-up", views.sign_up),
    path("logout", views.logout),
    # Domains
    path("domain", views.domains),
    path("domain-user", views.domain_users),
    # Friends
    path("friends", views.friends),
]
