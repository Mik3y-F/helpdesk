from django.conf import settings
from rest_framework_nested import routers

from helpdesk.tickets.api.views import TicketStatusViewSet, TicketViewSet
from helpdesk.users.api.views import UserViewSet

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register("users", UserViewSet)
router.register("tickets", TicketViewSet, basename="tickets")

tickets_router = routers.NestedSimpleRouter(router, "tickets", lookup="ticket")
tickets_router.register("statuses", TicketStatusViewSet, basename="ticket-statuses")


app_name = "api"
urlpatterns = router.urls + tickets_router.urls
