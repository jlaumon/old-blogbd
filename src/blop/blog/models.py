# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.html import escape
from django.contrib.sitemaps import Sitemap
from django.db.models import Q
import datetime, re

DISPLAY_NAME_CHOICES = ( ('left', 'left'), ('center', 'center'), ('right', 'right'), ('none','none'),)
COUNT_POSITION = ( ('before', 'before'), ('after', 'after'), ('none','none'),)

def addlink(g):
	url = g.group('url')
	return u"<a href=" + url + u" target=_blank>" + url + u"</a>"

class Category(models.Model):
	title = models.CharField(max_length=50)
	slug = models.SlugField(unique=True)
	description = models.CharField(max_length=200)
	cssclass = models.CharField(
		u"classe css associée", 
		help_text=u"Permet de définir l'icone à afficher devant le titre de l'article (entre autres).", 
		max_length=30,  
		default=u"icon_page_white_edit"
	)
	date = models.DateTimeField(auto_now_add=True)
	is_invisible = models.BooleanField(
		help_text=u"Si vrai, le titre de la catégorie ne sera pas affichée a côté du titre des articles (utile uniquement pour la catégorie \"sans catégorie\"", 
		default=False
	)
	
	site = models.ForeignKey(Site, blank=True, null=True)
	
	class Meta:
		verbose_name = u"catégorie"
		
	def get_absolute_url(self):
		return u"/cat/%s/" % (self.slug)
	def __unicode__(self):
		return self.title

class Entry(models.Model):
	title = models.CharField(max_length=50)
	slug = models.SlugField()
	content = models.TextField()
	date = models.DateTimeField(
		u'date de publication', 
		help_text=u"Si la date est future, l'article ne sera pas visible.<br/>Mis à la date et heure courante si laissé blanc.",
		blank=True)
	is_public = models.BooleanField(default=True)
	
	# Relations
	author = models.ForeignKey(User)
	category = models.ForeignKey(Category)
	site = models.ForeignKey(Site, blank=True, null=True)
	
	class Meta:
		verbose_name = u"article"
	
	def get_absolute_url(self):
		return u"/%d/%d/%d/%s/" % (self.date.year, self.date.month, self.date.day, self.slug)
	def __unicode__(self):
		return self.title
        
        
class Comment(models.Model):
	author = models.CharField(u'nom ou pseudo :', max_length=50)
	email = models.EmailField(u'email :')
	url = models.URLField(u'site internet :', verify_exists=True, blank = True)
	content = models.TextField(u'message :')
	date = models.DateTimeField(u'date de publication :')
	ip = models.CharField(max_length=50)
	has_reply = models.BooleanField(u'repondu ?',default=False, editable = False)
	notice_by_email = models.BooleanField(default=True)
	
	# Relations
	entry = models.ForeignKey(Entry)
	
	class Meta:
		verbose_name = u"commentaire"
	
	def getHTML(self):
		content = escape(self.content)
		content = re.sub(r"(?P<url>http://[0-9a-zA-z.%-_/#?=&~]+)", addlink, self.content)
		content_list = content.split('\n')
		content = ""
		for i in range(len(content_list)):
			content_list[i] = "<p>" + content_list[i] + "</p>"	
			content += content_list[i]
		return content
	
	def __unicode__(self):
		return self.content

class Reply(models.Model):
	author = models.ForeignKey(User, blank=True, null=True)
	comment = models.ForeignKey(Comment)
	content = models.TextField()
	date = models.DateTimeField(default = datetime.datetime.today())
	
	class Meta:
		verbose_name = u"réponse"
	
	def __unicode__(self):
		return self.comment.author
		
class Link(models.Model):
	name = models.CharField(max_length=30)
	url = models.URLField()
	img_pict = models.ImageField(upload_to='links')
	img_name = models.ImageField(upload_to='links')
	
	site = models.ForeignKey(Site, blank=True, null=True)
	
	class Meta:
		verbose_name = u"lien"
	
	def __unicode__(self):
		return self.name
		
class RandomImage(models.Model):
	name = models.CharField(max_length=30)
	url = models.URLField(blank=True, verify_exists=True)
	display_name= models.CharField(max_length=30, choices=DISPLAY_NAME_CHOICES, default=u"left")
	img = models.ImageField(upload_to='random_image')
	transition = models.CharField(max_length=30, blank=True, default=u"dit :")
	caption = models.TextField(
		u"légende", 
		help_text=u"Balises HTML de type inline autorisées. <br/>/!\ Aucune validation de code n'est effectuée.", 
		max_length=200, 
		blank=True
	)
	cssclass = models.CharField(
		u"classe css associée", 
		help_text=u"Permet de définir l'icone à afficher devant le nom de l'image (entre autres).", 
		max_length=30, 
		blank=True, 
		default=u"icon_comment"
	)
	date = models.DateTimeField(auto_now_add=True)
	is_public = models.BooleanField(default=True)
	
	site = models.ForeignKey(Site, blank=True, null=True)
	
	class Meta:
		verbose_name = u"image aléatoire"
		
	def box(self):
		return (self.display_name!=u"no" or self.caption!="")
	
	def __unicode__(self):
		return self.name
		
class Banner(models.Model):
	name = models.CharField(max_length=30)
	img = models.ImageField(upload_to='banner')
	date = models.DateTimeField(auto_now_add=True)
	is_public = models.BooleanField(default=True)
	
	site = models.ForeignKey(Site, blank=True, null=True)
	
	class Meta:
		verbose_name = u"bannière"
	
	def __unicode__(self):
		return self.name

class CommentLink(models.Model):
	phrase = models.CharField(max_length=100)
	count = models.IntegerField(blank=True,null=True)
	position = models.CharField(max_length=10, choices=COUNT_POSITION, default=u"before")
	
	site = models.ForeignKey(Site, blank=True, null=True)
	
	class Meta:
		verbose_name = u"Lien de commentaire"
	
	def __unicode__(self):
		return self.phrase
		
class FlatPage(models.Model):
	title = models.CharField(max_length=50)
	content = models.TextField()
	path = models.CharField(max_length=200)
	is_public = models.BooleanField(default=True)
	
	site = models.ForeignKey(Site, blank=True, null=True)
	
	class Meta:
		verbose_name = u"Pages statiques"
	
	def get_absolute_url(self):
		return u"/%s/" % (self.path)
		
	def __unicode__(self):
		return self.title
		
		
		
		
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'email', 'url', 'content')
        

class RssLastEntriesFeed(Feed):
    title = u"Le blog BD de plop"
    link = u"/"
    description = u"Les derniers articles du blog de plop"

    def items(self):
        return Entry.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current())).filter(is_public=True, date__lte=datetime.datetime.today()).order_by('-date')[:10]

class AtomLastEntriesFeed(RssLastEntriesFeed):
    feed_type = Atom1Feed
    subtitle = RssLastEntriesFeed.description

class RssLastCommentsFeed(Feed):
    title = u"Le blog BD de plop"
    link = u"/"
    description = u"Les derniers commentaires du blog de plop"
    
    def item_link(self, item):
    	return item.entry.get_absolute_url() + u"#" + item.author + item.date.isoformat()

    def items(self):
        return Comment.objects.order_by('-date')[:25]
        
class AtomLastCommentsFeed(RssLastCommentsFeed):
    feed_type = Atom1Feed
    subtitle = RssLastCommentsFeed.description
    
class BlogSitemap(Sitemap):
	priority = 0.5

	def items(self):
		return Entry.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current())).filter(is_public=True, date__lte=datetime.datetime.today()).order_by('-date')

	def lastmod(self, obj):
		return obj.date

class BaseSitemap(Sitemap):
	priority = 0.8
	def items(self):
		return [
        	'/',
        	'/about',
        	'/archives/', 
        	'/feeds/rss/', 
        	'/feeds/atom/', 
        	'/feeds/rsscomments/',
        	'/feeds/atomcomments/'
        ]

	def location(self, obj):
		return obj
