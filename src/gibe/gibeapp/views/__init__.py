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
    p = models.Post.objects(all_urls=request.path_info).first()
    print request.path_info
    if p.canonical_url != request.path_info:
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
            ct.save()

#def twitter(request):
#    if request.POST.get("form_id") == "twitter_update_form":
#        _update_timeline()
#        return redirect("/admin/twitter")
#
#    if request.POST.get("form_id") == "twitter_promote_form":
#        status_to_promote = request.POST.getlist("status_to_promote")
#        for status_id in status_to_promote:
#            ct = models.CachedTweet.objects(status_id=status_id).first()
#            if ct:
#                t = models.TweetPost()
#                t.title = ""
#                t.content = ct.text
#                t.creation_date = ct.created_at
#                t.published_date = ct.created_at
#                t.canonical_url = "%04d-%02d-%02d-%s" % (ct.created_at.year, ct.created_at.month, ct.created_at.day, status_id)
#                t.all_urls = [t.canonical_url]
#                t.tweet_url = "http://twitter.com/%s/status/%s" % (ct.author.screen_name, ct.id)
#                t.save()
#
#        return redirect("/admin/twitter")
#
#    timeline = models.CachedTweet.objects().order_by("-created_at").limit(25)
#
#    if not timeline:
#        _update_timeline()
#        timeline = models.CachedTweet.objects().order_by("-created_at").limit(25)
#    
#    context = dict(
#        timeline = [WrappedStatus(status) for status in timeline],
#    )
#    return render_to_response('twitter.xhtml.template', context, RequestContext(request))
