from django.contrib.syndication.views import Feed as ContribFeed
from django.utils.feedgenerator import Atom1Feed

from gibe.gibeapp import models
from gibe.gibeapp.render import PostRenderer

class Feed(ContribFeed):
    def title(self):
        s = models.BlogSettings.objects(key="blogsettings").first()
        return s.feed_title or s.title

    def description(self):
        s = models.BlogSettings.objects(key="blogsettings").first()
        return s.feed_title or s.title

    def link(self):
        return "/"

    def items(self):
        return models.Post.objects.order_by("-published_date").limit(10)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return PostRenderer(item).excerpt

    def item_link(self, item):
        return item.canonical_url or ""

    def item_pubdate(self, item):
        return item.published_date

class AtomFeed(Feed):
    feed_type = Atom1Feed

rss = Feed()
atom = AtomFeed()
