from django.urls import path,re_path
from baike import views
from django.conf.urls import url



urlpatterns = [
    path('',views.baike),

    path('api/menu',views.baikemenu),
    path('api/sgbk_sjld',views.sjld),
    path('api/artcle',views.artcle),

    # path('api/sgbk_sjld',views.OrderView.as_view())
]
