from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig

class MessageboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messageboard'

class MessageboardAdminConfig(AdminConfig):
    default_site = 'admin.Comment8orAdminSite'