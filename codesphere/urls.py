"""codesphere URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignUpView.as_view(),name='signup'),
    path('signin/',views.SignInView.as_view(),name='signin'),
    path('index/',views.IndexView.as_view(),name='index'),
    path('logout/',views.SignoutView,name='signout'),
    path('profile/change/',views.UserProfileEditView.as_view(), name='profile-edit'),
    path('project/add/',views.ProjectCreateView.as_view(),name="project-add"),
    path('project/all/',views.MyProjectListView.as_view(),name="my-work"),
    path('project/<int:pk>/change/',views.ProjectUpdateView.as_view(),name="project-update"),    
    path('project/<int:pk>/view',views.ProjectViewMore.as_view(), name='project-view-more'),
    path('project/<int:pk>/add-to-wishlist/',views.AddToWishListView.as_view(), name='addto-wishlist'),
    path('project/wishlist/',views.MyWishListItemView.as_view(),name="my-wishlist"),
    path('project/<int:pk>/remove/',views.WishListItemDeleteView.as_view(), name='wishlist-delete'),
    path('checkout/',views.CheckOutView.as_view(),name="checkout"),
    path('payment/verify/',views.PaymentVerification.as_view(),name="payment-verify"),
    path('orders/',views.MyoderView.as_view(),name="orders"),
    path('reset/',views.PasswordResetView.as_view(),name='reset'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
