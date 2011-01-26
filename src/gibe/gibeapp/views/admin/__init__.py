from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from gibe.gibeapp import models
from gibe.gibeapp.urlify_tweet import urlify_tweet

class WrappedStatus(object):
    def __init__(self, status):
        self.status = status

    @property
    def text(self):
        return urlify_tweet(self.status.text)

    @property
    def author_html(self):
        return urlify_tweet('@' + self.author_screen_name)

    @property
    def tweet_url(self):
        return "http://twitter.com/%s/status/%s" % (self.author_screen_name, self.status_id)

    def __getattr__(self, key):
        return getattr(self.status, key)

def _update_timeline():
    s = models.TwitterSettings.objects(key='twitter').first()
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
            ct.author_screen_name = status.author.screen_name
            ct.save()

def twitter(request):
    if request.POST.get("form_id") == "twitter_update_form":
        _update_timeline()
        return redirect("/admin/twitter")

    if request.POST.get("form_id") == "twitter_promote_form":
        status_to_promote = request.POST.getlist("status_to_promote")
        for status_id in status_to_promote:
            ct = models.CachedTweet.objects(status_id=status_id).first()
            if ct:
                t = models.TweetPost()
                t.tweet_id = str(ct.status_id)
                t.title = ""
                t.content = ct.text
                t.creation_date = ct.created_at
                t.published_date = ct.created_at
                t.canonical_url = "%04d-%02d-%02d-%s" % (ct.created_at.year, ct.created_at.month, ct.created_at.day, status_id)
                t.all_urls = [t.canonical_url]
                t.tweet_url = "http://twitter.com/%s/status/%s" % (ct.author_screen_name, ct.status_id)
                t.save()

        return redirect("/admin/twitter")

    timeline = models.CachedTweet.objects().order_by("-created_at").limit(25)

    if not timeline:
        _update_timeline()
        timeline = models.CachedTweet.objects().order_by("-created_at").limit(25)
    
    context = dict(
        timeline = [WrappedStatus(status) for status in timeline],
    )
    return render_to_response('twitter.xhtml.template', context, RequestContext(request))
