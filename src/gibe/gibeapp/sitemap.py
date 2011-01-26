from django.contrib.sitemaps import Sitemap
from gibe.gibeapp import models

class PostSitemap(Sitemap):
    def items(self):
        return models.Post.objects()

    def changefreq(self, obj):
        return "daily"

    def priority(self, obj):
        return 0.5

    def lastmod(self, obj):
        return obj.published_date
