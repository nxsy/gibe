from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from gibe.gibeapp import models
from gibe.gibeapp.render import PostRenderer
from gibe.gibeapp.urlify_tweet import urlify_tweet

def index(request):
    posts = models.Post.objects.order_by('-published_date').limit(15)
    context = dict(
        posts=[PostRenderer(post) for post in posts],
        title='Index',
    )
    return render_to_response("index.xhtml.template", context, RequestContext(request))

def page(request):
    p = models.Page.objects(content__all_urls=request.path_info).first()
    print request.path_info
    if p.content.canonical_url != request.path_info:
        return redirect(p.canonical_url, permanent=True)

    context = dict(
        post = PostRenderer(p),
    )
    return render_to_response("page.xhtml.template", context, RequestContext(request))

class WrappedStatus(object):
    def __init__(self, status):
        self.status = status

    @property
    def text(self):
        return urlify_tweet(self.status.text)

    def __getattr__(self, key):
        return getattr(self.status, key)

def _update_timeline():
    s = models.TwitterSettings.objects.first()
    import tweepy
    auth = tweepy.OAuthHandler(s.consumer_key, s.consumer_secret)
    auth.set_access_token(s.oauth_token, s.oauth_token_secret)
    api = tweepy.API(auth)
    timeline = api.user_timeline()
    for status in timeline:
        if not models.CachedTweet.objects(status_id=str(status.id)).first():
            ct = models.CachedTweet()
            ct.status_id = str(status.id)
            ct.text = status.text
            ct.created_at = status.created_at
            ct.save()
