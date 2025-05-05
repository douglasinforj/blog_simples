from django.apps import AppConfig


class AppBlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_blog'

    def ready(self):
        import app_blog.signals
