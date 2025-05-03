from django.db import models
from django.conf import settings       
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="autor") 
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    aprovado = models.BooleanField(default=False)
    recusado = models.BooleanField(default=False)

    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    image = models.ImageField(upload_to='post_images/', null=True, blank=True)

    def publish(self):
        self.published_date = timezone.now()
        try:
            self.save()
            logger.info(
                f"Post '{self.title}' (ID: {self.id}) publicado por {self.author.username} em {self.published_date}."
            )
        except Exception:
            logger.error(f"Erro ao publicar o post '{self.title}' (ID: {self.id})", exc_info=True)

    def delete(self, *args, **kwargs):
        try:
            logger.warning(f"Post '{self.title}' (ID: {self.id}) será excluído por {self.author.username}.")
            super().delete(*args, **kwargs)
        except Exception:
            logger.error(f"Erro ao excluir o post '{self.title}' (ID: {self.id})", exc_info=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        try:
            super().save(*args, **kwargs)
            if is_new:
                logger.info(f"Post criado: '{self.title}' (ID: {self.id}) por {self.author.username}.")
            else:
                logger.info(f"Post atualizado: '{self.title}' (ID: {self.id}) por {self.author.username}.")
        except Exception:
            logger.error(f"Erro ao salvar o post '{self.title}'", exc_info=True)

    def __str__(self):         
        return self.title
