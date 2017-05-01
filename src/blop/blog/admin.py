# -*- coding: utf-8 -*-
from blop.blog.models import *
from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
import datetime


class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}
	list_display = ('title', 'description', 'date', 'site', 'is_invisible')
	fieldsets = (
		(None, {
			'fields': ('title', 'description', 'site')
		}),
		('Options avancées', {
			'classes': ('collapse',),
			'fields': ('slug', 'is_invisible', 'cssclass')
		}),
	)


class EntryAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}
	date_hierarchy = 'date'
	list_display = ('title', 'date', 'author', 'category', 'is_public')
	list_filter = ('date', 'is_public', 'category')
	search_fields = ['title', 'content']
	fieldsets = (
		(None, {
			'fields': ('title', 'category', 'content', 'date', 'site', 'is_public')
		}),
		('Options avancées', {
			'classes': ('collapse',),
			'fields': ('slug',)
		}),
	)
	def save_model(self, request, obj, form, change):
		if not change:
			obj.author = request.user
			if not obj.date:
				obj.date = datetime.datetime.today()
			obj.save()
			
		elif request.user.is_superuser or request.user == obj.author:
			if not obj.date:
				obj.date = datetime.datetime.today()
			obj.save()
		
class ReplyInline(admin.TabularInline):
	model = Reply
	extra = 1
	

class CommentAdmin(admin.ModelAdmin):
	date_hierarchy = 'date'
	list_display = ('author', 'entry', 'date', 'ip', 'has_reply')
	list_filter = ('date', 'has_reply')
	search_fields = ['author', 'content', 'ip']
	inlines = [
		ReplyInline,
	]
	
	# This is a dirty way to update automatically "has_reply" field
	def save_model(self, request, obj, form, change):
		obj.has_reply = False
		nb_reply = int(request.POST[u'reply_set-INITIAL_FORMS'])
		for i in range(nb_reply):
			try:
				request.POST[u'reply_set-' + unicode(i) + u'-DELETE']
			except KeyError:
				obj.has_reply = True
				break
		if obj.has_reply == False:
			if request.POST[
				u'reply_set-' +
				unicode(int(request.POST[u'reply_set-TOTAL_FORMS'])-1) + 
				u'-content'
			]:
				obj.has_reply = True
		obj.save()
		
	def save_formset(self, request, form, formset, change):
		instances = formset.save(commit=False)
		for instance in instances:
			instance.author = request.user
			instance.save()
			if change:
				if instance.comment.notice_by_email:
					subject = u'Nouvelle réponse à votre commentaire'
					from_email = u'plopounet@alwaysdata.net'
					to = instance.comment.email
					
					text_content  = u'Un auteur a répondu à l\'un de vos commentaires sur le blog BD de plop.\n'
					text_content += u'Vous pouvez lire cette réponse à l\'adresse http://'+ Site.objects.get_current().domain + instance.comment.entry.get_absolute_url() + u'\n\n'
					text_content += u'Ceci est un email automatique. Mais vous pouvez y répondre si ça vous amuse :D\nplop'
					
					html_content  = u'<p>Un auteur a répondu à l\'un de vos commentaires sur le blog BD de plop.</p>'
					html_content += u'<p><b>Article :</b><br/>'
					html_content += instance.comment.entry.title + u'<br/>'
					html_content += u'http://' + Site.objects.get_current().domain + instance.comment.entry.get_absolute_url() + u'</p>'
					html_content += u'<p><b>Votre commentaire :</b></p>'
					html_content += u'<blockquote>' + instance.comment.getHTML() + u'</blockquote>'
					html_content += u'<p><b>Réponse de ' + instance.author.username + u' :</b></p>'
					html_content += u'<blockquote><p>' + instance.content + u'</p></blockquote>'
					html_content += u'<p><i>Ceci est un message automatique. Mais vous pouvez y répondre si ça vous amuse :D</i><br/>'
					html_content += u'plop</p>'
					
					msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
					msg.attach_alternative(html_content, "text/html")
					msg.send()
					
		formset.save_m2m()
		
class BannerAdmin(admin.ModelAdmin):
	list_display = ('name', 'img', 'date', 'site', 'is_public')
	
class RandomImageAdmin(admin.ModelAdmin):
	list_display = ('name', 'img', 'caption', 'date', 'site', 'is_public')
	
class CommentLinkAdmin(admin.ModelAdmin):
	list_display = ('phrase', 'count', 'site')
	
class FlatPageAdmin(admin.ModelAdmin):
	list_display = ('title', 'site', 'is_public')

admin.site.register(Link)
admin.site.register(Banner, BannerAdmin)
admin.site.register(RandomImage, RandomImageAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(CommentLink, CommentLinkAdmin)
admin.site.register(FlatPage, FlatPageAdmin)
