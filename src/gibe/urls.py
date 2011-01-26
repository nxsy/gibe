from django.conf.urls.defaults import patterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from gibe.gibeapp.sitemap import PostSitemap
sitemaps = dict(post=PostSitemap)

urlpatterns = patterns('',
    # Example:
    # (r'^gibe/', include('gibe.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^$', 'gibe.gibeapp.views.index'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'gibeapp/static'}),
    #(r'^admin/settings/twitter', 'gibe.gibeapp.views.settings_twitter'),
    (r'^admin/twitter', 'gibe.gibeapp.views.admin.twitter'),
    (r'^feed/rss', 'gibe.gibeapp.views.feed.rss'),
    (r'^feed/atom', 'gibe.gibeapp.views.feed.atom'),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^', 'gibe.gibeapp.views.page'),
)
