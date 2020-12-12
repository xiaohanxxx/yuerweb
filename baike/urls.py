from django.urls import path,re_path
from baike import views
from django.conf.urls import url



urlpatterns = [
    path('',views.baike),
    path('baike_list',views.baike_list),
    path('article',views.article),
    path('baikebigfl_list',views.baikebigfl_list),


    path('api/menuapi',views.baikemenuapi),
    path('api/sgbk_sjldapi',views.sjldapi),
    path('api/articlelistapi',views.articlelistapi),
    path('api/articleapi',views.articleapi),
    path('api/articletimelist',views.articletimelist),
    path('api/articleread',views.articleread),
    path('api/articlecommend',views.articlecommend),
    path('api/getmenuarticle',views.getmenuarticle),

    # path('api/sgbk_sjld',views.OrderView.as_view())
]
