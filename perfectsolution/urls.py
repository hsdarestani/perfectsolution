from django.contrib import admin
from django.urls import include,path
admin.site.site_header="Perfect Solution Verwaltung"
admin.site.site_title="Perfect Solution"
admin.site.index_title="Shop Verwaltung"
urlpatterns=[path("admin/",admin.site.urls),path("",include("shop.urls"))]
