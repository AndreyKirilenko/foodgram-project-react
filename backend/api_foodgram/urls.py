urlpatterns = [
    path('api/', include('users.urls')),
    path('api/', include('foodgram.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('admin/', admin.site.urls),
]
