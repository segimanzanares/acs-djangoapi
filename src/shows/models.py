from django.db import models
from django.urls import reverse

class Show(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=False, default='')
    created_at = models.DateTimeField(auto_now=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    deleted_at = models.DateTimeField(auto_now=False, null=True)

    def get_absolute_url(self):
        return reverse('shows.detail', kwargs={'pk': self.pk})
    
    def get_update_url(self):
        return reverse('shows.update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('shows.delete', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ('created_at',)