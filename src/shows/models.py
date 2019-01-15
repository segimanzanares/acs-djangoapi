from django.db import models
from django.urls import reverse

class Show(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=False, default='')
    created_at = models.DateTimeField(auto_now=False, null=False)
    updated_at = models.DateTimeField(auto_now=False, null=False)
    deleted_at = models.DateTimeField(auto_now=False, null=True)

    def get_absolute_url(self):
        return reverse('shows.detail', kwargs={'pk': self.pk})
    
    def get_update_url(self):
        return reverse('shows.update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('shows.delete', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ('created_at',)

def episodes_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/episodes/<id>/<filename>
    return 'episodes/' + ('{0}/{1}'.format(instance.id, filename))

class Episode(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=100, blank=False)
    cover = models.ImageField(upload_to=episodes_directory_path)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, null=False)
    updated_at = models.DateTimeField(auto_now=False, null=False)
    deleted_at = models.DateTimeField(auto_now=False, null=True)

    class Meta:
        ordering = ('created_at',)

