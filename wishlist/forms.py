from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .models import WishlistItem
import requests
from bs4 import BeautifulSoup


class WishlistItemForm(forms.ModelForm):
    class Meta:
        model = WishlistItem
        fields = ['item_name', 'link', 'description', 'thumbnail_url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('item_name', placeholder='Item name'),
            Field('link', placeholder='Link'),
            Field('description', placeholder='Description'),
            Field('thumbnail_url', placeholder='Thumbnail URL'),
        )

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
