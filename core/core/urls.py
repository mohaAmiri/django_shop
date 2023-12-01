from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from home.sitemaps import ProductViewSitemap

sitemaps = {
    'product': ProductViewSitemap,
}

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('home.urls', namespace='home')),
                  path('accounting/', include('accounting.urls', namespace='accounting')),
                  path('cart/', include('cart.urls', namespace='cart')),
                  path('order/', include('order.urls', namespace='order')),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('sitemaps.xml/', sitemap, {'sitemaps': sitemaps}),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
