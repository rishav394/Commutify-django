from django.urls import include, path

from khushiapp.restapis import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # Users
    path("users", views.users),
    path("login", views.login),
    path("sign-up", views.sign_up),
    path("logout", views.logout),
    # Domains
    path("domain", views.domains),
    path("domain-user", views.domain_users),
]
