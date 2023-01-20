from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from accounts import views as acc_view
from posts import views as posts_view

acc_router = DefaultRouter()
acc_router.register('register', acc_view.ProfileRegisterAPIView)

posts_router = DefaultRouter()
posts_router.register('tweet', posts_view.TweetViewSet)

status_router = DefaultRouter()
status_router.register('status', posts_view.StatusViewSet)



schema_view = get_schema_view(
   openapi.Info(
      title="Twitter Clone API",
      default_version='v-0.01-alpha',
      description="API для взаимодействия с Твиттер API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="nursultan@gmail.com"),
      license=openapi.License(name="No Licence"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),
    path('api/auth/token/', obtain_auth_token),

    path('api/accounts/', include(acc_router.urls)),
    path('api/posts/', include(posts_router.urls)),
    path('api/posts/tweet/<int:tweet_id>/comment/', posts_view.CommentListCreateAPIView.as_view()),

    # documentation URL
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_doc'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc_doc'),

]


# urlpatterns = [
#    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
#    ...
# ]