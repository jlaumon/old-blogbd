# -*- coding: utf-8 -*-

import datetime, random
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site
from django.db.models import Q
from blop.blog.models import *



mois = [
	u"Janvier", 
	u"Février",
	u"Mars",
	u"Avril",
	u"Mai",
	u"Juin",
	u"Juillet",
	u"Août",
	u"Septembre",
	u"Octobre",
	u"Novembre",
	u"Décembre",
]


def url_of(category_slug=None, year_id=None, month_id=None, day_id=None, page_id=None):
	url = '/'
	if category_slug:
		url += category_slug + '/'
	if year_id:
		url += year_id + '/'
	if month_id:
		url += month_id + '/'
	if day_id:
		url += day_id + '/'
	if page_id:
		url += 'page/' + str(page_id) + '/'
	return url
		
def index(request, category_slug=None, year_id=None, month_id=None, day_id=None, page_id=None):
	
	if year_id is None :
		entry_list = Entry.objects.filter(is_public=True, date__lte=datetime.datetime.today()).order_by('-date')
	elif month_id is None :
		entry_list = Entry.objects.filter(date__year=year_id, is_public=True, date__lte=datetime.datetime.today()).order_by('-date')
	elif day_id is None :
		entry_list = Entry.objects.filter(date__year=year_id, date__month=month_id, is_public=True, date__lte=datetime.datetime.today()).order_by('-date')
	else :
		entry_list = Entry.objects.filter(date__year=year_id, date__month=month_id, date__day=day_id, is_public=True, date__lte=datetime.datetime.today()).order_by('-date')
	
	if category_slug:
		try:
			category = Category.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current())).get(slug = category_slug)
		except:
			raise Http404
		entry_list = entry_list.filter(category=category)
	
	entry_list = entry_list.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current()))
	
	if page_id:
		page_id = int(page_id)
	else :
		page_id = 0
    	
	previous = None
	next = None
	
	if entry_list.count() > ((page_id+1)*5):
			previous = url_of(category_slug, year_id, month_id, day_id, page_id+1)
			
	if entry_list.count() and page_id > 0:
			next = url_of(category_slug, year_id, month_id, day_id, page_id-1)
   		
	entry_list = entry_list[(page_id*5):((page_id+1)*5)]
	
	entry_list2 = []
	for entry in entry_list:
		comment_count = Comment.objects.filter(entry=entry).count()
		try:
			comment_link_num = random.randint(0,CommentLink.objects.filter(Q(count__isnull=True)|Q(count=comment_count)).count()-1)
			comment_link = CommentLink.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current()))
			comment_link = comment_link.filter(Q(count__isnull=True)|Q(count=comment_count))[comment_link_num]
			if comment_link.position == "before":
				comment_link = "%d " % comment_count + comment_link.phrase
			elif comment_link.position == "after":
				comment_link = comment_link.phrase + "%d " % comment_count	
		except Exception:
			if comment_count <= 1:
				comment_link = "%d " % comment_count + u"commentaire"
			else:
				comment_link = "%d " % comment_count + u"commentaires"
		entry_list2.append(
			{'entry': entry, 'comment_link': comment_link}
		)
	
    
    # Get random image and banner
    # If no object in the DB, randint(0,0) will raise a value error...
	try:
		banner_num = random.randint(0,Banner.objects.filter(is_public=True).count()-1)
		banner = Banner.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current()))
		banner = banner.filter(is_public=True)[banner_num]
	except Exception:
		banner = []
	
	try:
		random_image_num = random.randint(0,RandomImage.objects.filter(is_public=True).count()-1)
		random_image = RandomImage.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current()))
		random_image = random_image.filter(is_public=True)[random_image_num]
	except Exception:
		random_image = []
	
	# Get links, categories and archives lists
	link_list = Link.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current())).order_by('name')
	category_list = Category.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current()))
	archive_list = []
	for archive_date in Entry.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current())).dates('date', 'month')[:10]:
		archive_list.append(
			{'label':u"%s %d" % (mois[archive_date.month - 1], archive_date.year),
			'url': u"/%d/%d/" % (archive_date.year, archive_date.month)}
		)

	return render_to_response(
		'index.html', {'entry_list': entry_list2, 'link_list': link_list, 
		'archive_list': archive_list, 'category_list': category_list,
		'random_image': random_image, 'banner': banner,
		'previous' : previous, 'next' : next, 'site': Site.objects.get_current(),}
		)
		
def detail(request, year_id, month_id, day_id, slug):
	try:
		entry = Entry.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current())).get(date__year=year_id, date__month=month_id, date__day=day_id, slug=slug)
	except:
		raise Http404
		
	if request.method == 'POST':
		if request.POST['age']=="": #age -> honeypot
			instance = Comment(
				date = datetime.datetime.today(),
				ip = request.META['REMOTE_ADDR'],
				entry = entry,
				)
			form = CommentForm(request.POST, instance=instance)
			if form.is_valid():
				form.save()
		form = CommentForm()
	else:
		form = CommentForm()	
	
	# Get random image and banner
    # If no object in the DB, randint(0,0) will raise a value error...
	try:
		banner_num = random.randint(0,Banner.objects.filter(is_public=True).count()-1)
		banner = Banner.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current()))
		banner = banner.filter(is_public=True)[banner_num]
	except Exception:
		banner = []
	
	try:
		random_image_num = random.randint(0,RandomImage.objects.filter(is_public=True).count()-1)
		random_image = RandomImage.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current()))
		random_image = random_image.filter(is_public=True)[random_image_num]
	except Exception:
		random_image = []
	
	# Get links, categories and archives lists
	link_list = Link.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current())).order_by('name')
	category_list = Category.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current()))
	archive_list = []
	for archive_date in Entry.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current())).dates('date', 'month')[:10]:
		archive_list.append(
			{'label':u"%s %d" % (mois[archive_date.month - 1], archive_date.year),
			'url': u"/%d/%d/" % (archive_date.year, archive_date.month)}
		)
		
	comment_list = []
	for comment in Comment.objects.filter(entry=entry).order_by('date'):
		comment_list.append(
			{'comment': comment,
			'reply_list': Reply.objects.filter(comment=comment)}
		)

	return render_to_response(
		'detail.html', {'entry': entry, 'link_list': link_list, 
		'archive_list': archive_list, 'category_list': category_list,
		'comment_list': comment_list, 'form': form, 
		'banner': banner, 'random_image': random_image,'site': Site.objects.get_current(),}
		)
		
def archives(request):
	all_archive_list = []
	for archive in Entry.objects.dates('date', 'month'):
		all_archive_list.append(
			{'label':u"%s %d" % (mois[archive.month - 1], archive.year),
			'url': u"/%d/%d/" % (archive.year, archive.month)}
		)
	
	# Get random image and banner
    # If no object in the DB, randint(0,0) will raise a value error...
	try:
		banner_num = random.randint(0,Banner.objects.filter(is_public=True).count()-1)
		banner = Banner.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current()))
		banner = banner.filter(is_public=True)[banner_num]
	except Exception:
		banner = []
	
	try:
		random_image_num = random.randint(0,RandomImage.objects.filter(is_public=True).count()-1)
		random_image = RandomImage.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current()))
		random_image = random_image.filter(is_public=True)[random_image_num]
	except Exception:
		random_image = []
	
	# Get links, categories and archives lists
	link_list = Link.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current())).order_by('name')
	category_list = Category.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current()))
	archive_list = []
	for archive_date in Entry.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current())).dates('date', 'month')[:10]:
		archive_list.append(
			{'label':u"%s %d" % (mois[archive_date.month - 1], archive_date.year),
			'url': u"/%d/%d/" % (archive_date.year, archive_date.month)}
		)

	return render_to_response(
		'archives.html', {'all_archive_list': all_archive_list, 'link_list': link_list, 
		'archive_list': archive_list, 'category_list': category_list, 
		'banner': banner, 'random_image': random_image,'site': Site.objects.get_current(),}
		)

def flatpages(request):
	
	try:
		flatpage = FlatPage.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current())).get(path=request.path)
	except:
		raise Http404
	if not flatpage.is_public:
		raise Http404
	
	# Get random image and banner
    # If no object in the DB, randint(0,0) will raise a value error...
	try:
		banner_num = random.randint(0,Banner.objects.filter(is_public=True).count()-1)
		banner = Banner.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current()))
		banner = banner.filter(is_public=True)[banner_num]
	except Exception:
		banner = []
	
	try:
		random_image_num = random.randint(0,RandomImage.objects.filter(is_public=True).count()-1)
		random_image = RandomImage.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current()))
		random_image = random_image.filter(is_public=True)[random_image_num]
	except Exception:
		random_image = []
	
	# Get links, categories and archives lists
	link_list = Link.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current())).order_by('name')
	category_list = Category.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current()))
	archive_list = []
	for archive_date in Entry.objects.filter(Q(site__isnull=True)|Q(site=Site.objects.get_current())).dates('date', 'month')[:10]:
		archive_list.append(
			{'label':u"%s %d" % (mois[archive_date.month - 1], archive_date.year),
			'url': u"/%d/%d/" % (archive_date.year, archive_date.month)}
		)
	
	return render_to_response(
		'flatpage.html', {'flatpage': flatpage, 'link_list': link_list, 
		'archive_list': archive_list, 'category_list': category_list,
		'banner': banner, 'random_image': random_image,
		'site': Site.objects.get_current(),}
		)
