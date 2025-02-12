from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.item_name

        Field('thumbnail_url', placeholder='Thumbnail URL'),


def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.thumbnail_url and instance.link:
            instance.thumbnail_url = self.fetch_thumbnail_url(instance.link)
        if commit:
            instance.save()
        return instance

def fetch_thumbnail_url(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            og_image = soup.find('meta', property='og:image')
            if og_image and og_image['content']:
                return og_image['content']
        except Exception as e:
            print(f"Error fetching thumbnail: {e}")
        return ''