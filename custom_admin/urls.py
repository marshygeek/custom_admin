from django.urls import path

from custom_admin import views

app_name = 'custom_admin'
urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),

    # PARTNERS
    path('partners/<int:partner_id>/', views.partner, name='partner'),
    path('partners/<int:partner_id>/edit', views.edit_partner, name='edit_partner'),
    path('partners/<int:partner_id>/delete', views.delete_partner, name='delete_partner'),
    path('partners/', views.partners, name='partners'),

    # INTEGRATIONS
    path('integrations/<int:integration_id>/', views.integration, name='integration'),
    path('integrations/<int:integration_id>/edit', views.edit_integration, name='edit_integration'),
    path('integrations/<int:integration_id>/delete', views.delete_integration, name='delete_integration'),
    path('integrations/', views.integrations, name='integrations'),

    # CALLS
    path('calls/<int:call_id>/', views.call, name='call'),
    path('calls/<int:call_id>/delete', views.delete_call, name='delete_call'),
    path('calls/', views.calls, name='calls'),

    # WEBHOOKS
    path('webhooks/<int:webhook_id>/', views.webhook, name='webhook'),
    path('webhooks/<int:webhook_id>/edit', views.edit_webhook, name='edit_webhook'),
    path('webhooks/<int:webhook_id>/delete', views.delete_webhook, name='delete_webhook'),
    path('webhooks/', views.webhooks, name='webhooks'),

    # ORDERS
    path('orders/<int:order_id>/', views.order, name='order'),
    path('orders/<int:order_id>/edit', views.edit_order, name='edit_order'),
    path('orders/<int:order_id>/delete', views.delete_order, name='delete_order'),
    path('orders/', views.orders, name='orders'),

    path('test-geo-syntax/', views.test_geo_syntax, name='test_geo_syntax'),
    path('tts-generation/', views.tts_generation, name='tts_generation'),
]
