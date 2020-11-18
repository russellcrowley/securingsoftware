from django.urls import path
from .views import homePageView, confirmView, transferView, withdrawView, depositView, postmessageView, retrievemessageView

urlpatterns = [
    path('', homePageView, name='home'),
    path('transfer/', transferView, name='transfer'),
    path('confirm/', confirmView, name='confirm'),
    path('deposit/', depositView, name='deposit'),
    path('postmessage/', postmessageView, name='postmessage'),
    path('retrievemessage/', retrievemessageView, name='retrievemessage'),
]
