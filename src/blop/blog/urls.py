# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *


from blop.blog.models import *

feeds = {
    'rss': RssLastEntriesFeed,
    'atom': AtomLastEntriesFeed,
    'rsscomments': RssLastCommentsFeed,
    'atomcomments': AtomLastCommentsFeed,
}

sitemaps = {
	'blog': BlogSitemap,
	'base': BaseSitemap,
}

urlpatterns = patterns('',
	(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
	(r'^archives/$', 'blop.blog.views.archives'),
	(r'^about/$', 'blop.blog.views.flatpages'),
	
	(r'^$', 'blop.blog.views.index'),
	(r'^page/(?P<page_id>\d+)/$', 'blop.blog.views.index'),
	(r'^(?P<year_id>\d+)/$', 'blop.blog.views.index'),
	(r'^(?P<year_id>\d+)/page/(?P<page_id>\d+)/$', 'blop.blog.views.index'),
	(r'^(?P<year_id>\d+)/(?P<month_id>\d+)/$', 'blop.blog.views.index'),
	(r'^(?P<year_id>\d+)/(?P<month_id>\d+)/page/(?P<page_id>\d+)/$', 'blop.blog.views.index'),
	(r'^(?P<year_id>\d+)/(?P<month_id>\d+)/(?P<day_id>\d+)/$', 'blop.blog.views.index'),
	(r'^(?P<year_id>\d+)/(?P<month_id>\d+)/(?P<day_id>\d+)/page/(?P<page_id>\d+)/$', 'blop.blog.views.index'),
	
	(r'^cat/(?P<category_slug>[0-9a-z-]+)/$', 'blop.blog.views.index'),
	(r'^cat/(?P<category_slug>[0-9a-z-]+)/page/(?P<page_id>\d+)/$', 'blop.blog.views.index'),
	(r'^cat/(?P<category_slug>[0-9a-z-]+)/(?P<year_id>\d+)/$', 'blop.blog.views.index'),
	(r'^cat/(?P<category_slug>[0-9a-z-]+)/(?P<year_id>\d+)/page/(?P<page_id>\d+)/$', 'blop.blog.views.index'),
	(r'^cat/(?P<category_slug>[0-9a-z-]+)/(?P<year_id>\d+)/(?P<month_id>\d+)/$', 'blop.blog.views.index'),
	(r'^cat/(?P<category_slug>[0-9a-z-]+)/(?P<year_id>\d+)/(?P<month_id>\d+)/page/(?P<page_id>\d+)/$', 'blop.blog.views.index'),
	(r'^cat/(?P<category_slug>[0-9a-z-]+)/(?P<year_id>\d+)/(?P<month_id>\d+)/(?P<day_id>\d+)/$', 'blop.blog.views.index'),
	(r'^cat/(?P<category_slug>[0-9a-z-]+)/(?P<year_id>\d+)/(?P<month_id>\d+)/(?P<day_id>\d+)/page/(?P<page_id>\d+)/$', 'blop.blog.views.index'),
	
	(r'^(?P<year_id>\d+)/(?P<month_id>\d+)/(?P<day_id>\d+)/(?P<slug>[0-9a-z-]+)/$', 'blop.blog.views.detail'),
	
	(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)
