from django.core.urlresolvers import resolve
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import RedirectView

# Import from Python
from datetime import datetime



# FOR API TO LOAD GRAPHS
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from django.contrib.auth.models import User

from core.models import all_authors, all_poems, all_riddles, all_stories, taggers

# Import forms from core
from core.forms import PoemForm, RiddleForm, StoryForm

############################### I N D E X ##################################
@user_passes_test(lambda u: u.is_staff)
def index(request):
	poems = all_poems.objects.filter(poet = request.user)
	poem_published = all_poems.objects.filter(show_poem = True).filter(poet = request.user)
	poem_draft = all_poems.objects.filter(show_poem = False).filter(poet = request.user)

	stories = all_stories.objects.filter(author = request.user)
	stories_published = all_stories.objects.filter(show_story = True).filter(author = request.user)
	stories_draft = all_stories.objects.filter(show_story = False ).filter(author = request.user)

	riddles = all_riddles.objects.filter(riddler = request.user)
	riddles_published = all_riddles.objects.filter(show_riddle = True).filter(riddler = request.user)
	riddles_draft = all_riddles.objects.filter(show_riddle = False).filter(riddler = request.user)

	last_poem = poem_published.order_by('-updated')[:1]
	last_story = stories_published.order_by('-updated')[:1]
	last_riddle = riddles_published.order_by('-updated')[:1]
	
	context = {
		"name" : "d_index",

		"poems" : poems,
		"poem_draft" : poem_draft,
		"poem_published" : poem_published,
		
		"stories" : stories,
		"story_draft" : stories_draft,
		"story_published" : stories_published,
		
		"riddles" : riddles,
		"riddle_draft" : riddles_draft,
		"riddle_published" : riddles_published,

		"last_poem" : last_poem,
		"last_story" : last_story,
		"last_riddle" : last_riddle,

		"hide_area_chart" : False,
		"hide_donut" : False,
		"hide_task_panel" : False,
		"hide_transaction_panel" : False,

	}
	
	return render(request, 'dashboard/dashboard_base.html', context)

############################### P O E M S ##################################

############################### N E W   P O E M
@user_passes_test(lambda u: u.is_staff)
def new_poem(request):
	form = PoemForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			instance = form.save(commit=False)
			instance.poet = request.user
			instance.save()
			form.save_m2m()
			messages.success(request, "Successfully Created")
			return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"tab_text" : "New Poem",
		"head_text" : "Poem!",
		"small_head_text" : "Congratulations on writing a new poem. All the best",
		"breadcrumb_text" : "Writing new Poem",
		"sub_head_text" : "Please fill in all the boxes below",
		"button_text" : "Publish New Poem",
		"form": form,
		"name" : "d_n_poem",
	}
	return render(request, 'dashboard/form.html', context)

############################### E D I T   P O E M
@user_passes_test(lambda u: u.is_staff)
def edit_poem(request, slug = None):
	instance = get_object_or_404(all_poems, slug=slug)
	if instance.poet == request.user:
		form = PoemForm(request.POST or None, instance=instance)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, "Poem edited Succesfully")
			return HttpResponseRedirect(instance.get_absolute_url())
	else:
		print("oops! " + str(request.user) + ", You can't Edit " + str(instance.author) + "'s poem '" + str(instance.title) + "'." )
		raise Http404

	context = {
		"tab_text" : "Edit Poem",
		"head_text" : "Poem!",
		"small_head_text" : "This page should load all the contents of this poem. All the best",
		"breadcrumb_text" : "Editing old Poem",
		"sub_head_text" : "Please Edit all the necessary boxes below",
		"button_text" : "Publish Edited",
		"form": form,
		"name" : "d_e_poem",
		"this_poem" : instance,
	}	
	return render(request, 'dashboard/form.html', context)

############################### A L L   P O E M S
@user_passes_test(lambda u: u.is_staff)
def all_poem(request):
	cn = "All Poems"
	cnd = "These are the poems published on this site."
	poems = all_poems.objects.filter(poet = request.user)
	poem_published = all_poems.objects.filter(show_poem = True).filter(poet = request.user)
	poem_draft = all_poems.objects.filter(show_poem = False).filter(poet = request.user)

	context = {
		"name" : "d_a_poem",
		"content_name" : cn,
		"content_name_detail" : cnd,
		"poems" : poems,
		"poem_draft" : poem_draft,
		"poem_published" : poem_published,
	}
	return render(request, 'dashboard/all_poems_list.html', context)

############################### D R A F T    P O E M 
class draft_poem_toggle(RedirectView):
	# @user_passes_test(lambda u: u.is_staff)
	def get_redirect_url(self, *args, **kwargs):
		slug = self.kwargs.get("slug")
		instance = get_object_or_404(all_poems, slug = slug)
		url_ = (self.request.META['HTTP_REFERER'])
		if instance.poet == self.request.user:
			if instance.show_poem == True:
				instance.show_poem = False
				instance.save()
				messages.success(self.request, "Poem '" + instance.title + "' is successfully moved to Draft")
			else:
				instance.show_poem = True
				instance.save()
				messages.success(self.request, "Poem '" + instance.title + "' is successfully moved to Display")
			# After toggling the draft state, refresh the page
		else:
			messages.warning(self.request, "Oops! " + str(self.request.user) + ", You can't move " + str(instance.poet) + "'s poem '" + str(instance.title) + "' to and from Draft." )
			print("oops! " + str(self.request.user) + ", You can't move " + str(instance.poet) + "'s poem '" + str(instance.title) + "' to and from Draft." )
			# raise Http404
		return url_

############################### S T O R I E S ##################################

############################### N E W   S T O R Y 
@user_passes_test(lambda u: u.is_staff)
def new_story(request):
	form = StoryForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.author = request.user
		instance.save()
		messages.success(request, "New Story Published Successfully")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"tab_text" : "New Story",
		"head_text" : "Story Time!",
		"small_head_text" : "Congratulations on completing your new story. All the best",
		"breadcrumb_text" : "Writing a new Story",
		"sub_head_text" : "Please fill in all the boxes below",
		"name" : "d_n_story",
		"form" : form,
		"button_text" : "Publish New"
	}
	
	return render(request, 'dashboard/form.html', context)

############################### E D I T   S T O R Y 
@user_passes_test(lambda u: u.is_staff)
def edit_story(request, slug = None):
	instance = get_object_or_404(all_stories, slug = slug)
	if instance.author == request.user:
		form = StoryForm(request.POST or None, instance=instance)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, "Story edited Successfully")
			return HttpResponseRedirect(instance.get_absolute_url())
	else:
		print("oops! " + str(request.user) + ", You can't edit " + str(instance.author) + "'s story '" + str(instance.title) + "'." )
		raise Http404

	context = {
		"tab_text" : "Edit Story",
		"head_text" : "Story time!",
		"small_head_text" : "This page should load all the contents of this story. All the best",
		"breadcrumb_text" : "Editing old Story",
		"sub_head_text" : "Please edit all the necessary box below",
		"button_text" : "Publish Edited",
		"form": form,
		"name" : "d_e_story",
	}
	
	return render(request, 'dashboard/form.html', context)

############################### A L L   S T O R I E S
@user_passes_test(lambda u: u.is_staff)
def all_story(request):
	cn = "All Stories"
	cnd = "These are the stories published on this site."
	stories = all_stories.objects.filter(author = request.user)
	stories_published = all_stories.objects.filter(show_story = True).filter(author = request.user)
	stories_draft = all_stories.objects.filter(show_story = False ).filter(author = request.user)

	context = {
		"name" : "d_a_story",
		"content_name" : cn,
		"content_name_detail" : cnd,
		"stories" : stories,
		"story_draft" : stories_draft,
		"story_published" : stories_published,
	}
	return render(request, 'dashboard/all_stories_list.html', context)

############################### D R A F T    S T O R Y
class draft_story_toggle(RedirectView):
	# @user_passes_test(lambda u: u.is_staff)
	def get_redirect_url(self, *args, **kwargs):
		slug = self.kwargs.get("slug")
		instance = get_object_or_404(all_stories, slug = slug)
		url_ = (self.request.META['HTTP_REFERER'])
		if instance.author == self.request.user:
			if instance.show_story == True:
				instance.show_story = False
				instance.save()
				messages.success(self.request, "Story '" + instance.title + "' is successfully moved to Draft")
			else:
				instance.show_story = True
				instance.save()
				messages.success(self.request, "Story '" + instance.title + "' is successfully moved to Display")
			# After toggling the draft state, refresh the page
		else:
			messages.warning(self.request, "Oops! " + str(self.request.user) + ", You can't move " + str(instance.author) + "'s story '" + str(instance.title) + "' to and from Draft." )
			print("oops! " + str(self.request.user) + ", You can't move " + str(instance.author) + "'s story '" + str(instance.title) + "' to and from Draft." )
			# raise Http404
		return url_

############################### R I D D L E S ##################################

############################### N E W   R I D D L E
@user_passes_test(lambda u: u.is_staff)
def new_riddle(request):
	form = RiddleForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.riddler = request.user
		instance.save()
		messages.success(request, "New Riddle Published Successfully")
		return HttpResponseRedirect(instance.get_absolute_url())
		
	context = {
		"tab_text" : "New Riddle",
		"head_text" : "Time for a Riddle!",
		"small_head_text" : "Congratulations on making a new riddle. All the best",
		"breadcrumb_text" : "Creating a new Riddle",
		"sub_head_text" : "Please fill in all the boxes below",
		"form" : form,
		"button_text" : "Publish New",
		"name" : "d_n_riddle",
	}
	
	return render(request, 'dashboard/form.html', context)

############################### E D I T   R I D D L E
@user_passes_test(lambda u: u.is_staff)
def edit_riddle(request, slug = None):
	instance = get_object_or_404(all_riddles, slug = slug)
	if instance.riddler == request.user:		
		form = RiddleForm(request.POST or None, instance=instance)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, "Riddle edited Successfully")
			return HttpResponseRedirect(instance.get_absolute_url())
	else:
		print("oops! " + str(request.user) + ", You can't edit " + str(instance.author) + "'s riddle '" + str(instance.title) + "'." )
		raise Http404
		
	context = {
		"tab_text" : "Edit Riddle",
		"head_text" : "Time for a Riddle!",
		"small_head_text" : "This page should load all the contents of this riddle. All the best",
		"breadcrumb_text" : "Editing old Riddles",
		"sub_head_text" : "Please edit all the necessary boxes below",
		"button_text" : "Publish Edited",
		"form": form,
		"name" : "d_e_riddle",
	}
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	# return render(request, 'dashboard/form.html', context)
	
############################### A L L   R I D D L E S
@user_passes_test(lambda u: u.is_staff)
def all_riddle(request):
	cn = "All Riddles"
	cnd = "These are the riddles published on this site."
	riddles = all_riddles.objects.filter(riddler = request.user)
	riddles_published = all_riddles.objects.filter(show_riddle = True).filter(riddler = request.user)
	riddles_draft = all_riddles.objects.filter(show_riddle = False).filter(riddler = request.user)
	context = {
		"name" : "d_a_riddle",
		"content_name" : cn,
		"content_name_detail" : cnd,
		"riddles" : riddles,
		"riddle_draft" : riddles_draft,
		"riddle_published" : riddles_published,
	}
	return render(request, 'dashboard/all_riddles_list.html', context)

############################### D R A F T    R I D D L E S 
class draft_riddle_toggle(RedirectView):
	# @user_passes_test(lambda u: u.is_staff)
	def get_redirect_url(self, *args, **kwargs):
		slug = self.kwargs.get("slug")
		instance = get_object_or_404(all_riddles, slug = slug)
		url_ = (self.request.META['HTTP_REFERER'])
		if instance.riddler == self.request.user:
			if instance.show_riddle == True:
				instance.show_riddle = False
				instance.save()
				messages.success(self.request, "Riddle '" + instance.title + "' is successfully moved to Draft")
			else:
				instance.show_riddle = True
				instance.save()
				messages.success(self.request, "Riddle '" + instance.title + "' is successfully moved to Display")
			# After toggling the draft state, refresh the page
		else:
			messages.warning(self.request, "Oops! " + str(self.request.user) + ", You can't move " + str(instance.riddler) + "'s riddle '" + str(instance.title) + "' to and from Draft." )
			print("oops! " + str(self.request.user) + ", You can't move " + str(instance.riddler) + "'s riddle '" + str(instance.title) + "' to and from Draft." )
			# raise Http404
		return url_

############################### C H A R T S ##################################
@user_passes_test(lambda u: u.is_staff)
def charts(request):
	poems = all_poems.objects.filter(poet = request.user)
	poem_published = all_poems.objects.filter(show_poem = True).filter(poet = request.user)
	poem_draft = all_poems.objects.filter(show_poem = False).filter(poet = request.user)

	stories = all_stories.objects.filter(author = request.user)
	stories_published = all_stories.objects.filter(show_story = True).filter(author = request.user)
	stories_draft = all_stories.objects.filter(show_story = False ).filter(author = request.user)

	riddles = all_riddles.objects.filter(riddler = request.user)
	riddles_published = all_riddles.objects.filter(show_riddle = True).filter(riddler = request.user)
	riddles_draft = all_riddles.objects.filter(show_riddle = False).filter(riddler = request.user)

	########       C A L C U L A T I O N S    S T A R T S     H E R E 
	total_writings = poems.count() + stories.count() + riddles.count()
	total_publish = poem_published.count() + stories_published.count() + riddles_published.count()
	# time share
	poem_ts = 0
	story_ts = 0
	riddle_ts = 0
	total_ts = 0

	if total_publish != 0:
		poem_ts = round((poem_published.count() / total_publish) * 100,1)
		story_ts = round((stories_published.count() / total_publish) * 100,1)
		riddle_ts = round((riddles_published.count() / total_publish) * 100,1)
		total_ts = poem_ts+story_ts+riddle_ts

	
	# writer Confidence
	poem_c = 0
	story_c = 0
	riddle_c = 0
	total_c = 0

	if poems.count() != 0:
		poem_c = round((poem_published.count()/poems.count())*100,1)
	if stories.count() != 0:
		story_c = round((stories_published.count()/stories.count())*100,1)
	if riddles.count() != 0:
		riddle_c = round((riddles_published.count()/riddles.count())*100,1)	
	if total_writings != 0:
		total_c = round((total_publish/total_writings)*100,1)

	context = {
		"name" : "d_charts",

		"poems" : poems,
		"poem_draft" : poem_draft,
		"poem_published" : poem_published,
		
		"stories" : stories,
		"story_draft" : stories_draft,
		"story_published" : stories_published,
		
		"riddles" : riddles,
		"riddle_draft" : riddles_draft,
		"riddle_published" : riddles_published,

		"poem_ts" : poem_ts,
		"story_ts" : story_ts,
		"riddle_ts" : riddle_ts,
		"total_ts" : total_ts,

		"poem_c" : poem_c,
		"story_c" : story_c,
		"riddle_c" : riddle_c,
		"total_c" : total_c,

		"hide_area_chart" : False,
		"hide_donut" : False,
		"hide_task_panel" : False,
		"hide_transaction_panel" : False,


	}

	return render(request, 'dashboard/charts.html', context)


	
###############################    M A S T E R   ##################################
@user_passes_test(lambda u: u.is_superuser)
def master(request):
	currentDay = datetime.now().day
	currentMonth = datetime.now().month
	currentYear = datetime.now().year
	
	poems = all_poems.objects.all()
	poem_published = all_poems.objects.filter(show_poem = True)

	stories = all_stories.objects.all()
	stories_published = all_stories.objects.filter(show_story = True)

	riddles = all_riddles.objects.all()
	riddles_published = all_riddles.objects.filter(show_riddle = True)
	
	poem_month = poem_published.filter(updated__month = currentMonth).count()
	story_month = stories_published.filter(updated__month = currentMonth).count()
	riddle_month = riddles_published.filter(updated__month = currentMonth).count()

	all_users = User.objects.all().count()
	active_users = User.objects.filter(is_active=True).count()
	super_users = User.objects.filter(is_superuser=True).count()
	staff_users = User.objects.filter(is_staff=True).count()


	########       C A L C U L A T I O N S    S T A R T S     H E R E 
	total_writings = poems.count() + stories.count() + riddles.count()
	total_publish = poem_published.count() + stories_published.count() + riddles_published.count()
	# time share
	poem_ts = 0
	story_ts = 0
	riddle_ts = 0
	total_ts = 0

	if total_publish != 0:
		poem_ts = round((poem_published.count() / total_publish) * 100,1)
		story_ts = round((stories_published.count() / total_publish) * 100,1)
		riddle_ts = round((riddles_published.count() / total_publish) * 100,1)
		total_ts = poem_ts+story_ts+riddle_ts

	
	# writer Confidence
	poem_c = 0
	story_c = 0
	riddle_c = 0
	total_c = 0

	if poems.count() != 0:
		poem_c = round((poem_published.count()/poems.count())*100,1)
	if stories.count() != 0:
		story_c = round((stories_published.count()/stories.count())*100,1)
	if riddles.count() != 0:
		riddle_c = round((riddles_published.count()/riddles.count())*100,1)	
	if total_writings != 0:
		total_c = round((total_publish/total_writings)*100,1)


	inactive_users = all_users - active_users
	context = {
		"name" : "d_master",

		"poems" : poems,
		"poem_published" : poem_published,
		"poem_month" : poem_month,

		"stories" : stories,
		"story_published" : stories_published,
		"story_month" : story_month,

		"riddles" : riddles,
		"riddle_published" : riddles_published,
		"riddle_month" : riddle_month,

		"users" : all_users,
		"users_active" : active_users,
		"users_super" : super_users,
		"users_staff" : staff_users,
		"users_inactive" : inactive_users,

		"poem_ts" : poem_ts,
		"story_ts" : story_ts,
		"riddle_ts" : riddle_ts,
		"total_ts" : total_ts,

		"poem_c" : poem_c,
		"story_c" : story_c,
		"riddle_c" : riddle_c,
		"total_c" : total_c,
	}

	return render(request, 'dashboard/master.html', context)



############################### G U I D E  ##################################
@user_passes_test(lambda u: u.is_staff)
def guide(request):
	context = {
		"name" : "d_guide",
	}

	return render(request, 'dashboard/guide.html', context)

###############################    T E S T I N G    C H A R T S . J S   ##################################
# Trying from CFE videos

class ChartData(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request, format=None):
		# user_this = self.request.user
		# User_s = get_user_model()

		labels = ["Poems", "Riddles", "Stories"]
		data = {
				"labels" : labels,
				
			}
		return Response(data)








