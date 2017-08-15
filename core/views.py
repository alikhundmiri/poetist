from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import all_authors, all_poems, all_riddles, all_stories, taggers, all_about

def about(request):
	name = "about"
	qna = all_about.objects.filter(show_about = True)
	context = {
		"qna"  : qna,
		'name_nav' : name,
		'name' : "About",

	}
	return render(request, 'about.html', context)

def index(request):
	name = "Writers' Portfolio"
	p_status = True
	r_status = True
	s_status = True

	poems = all_poems.objects.filter(show_poem = True)
	riddles = all_riddles.objects.filter(show_riddle = True)
	stories = all_stories.objects.filter(show_story = True)
	authors = all_authors.objects.all()

	# This two lines below, check if the 'poems' is empty
	if bool(poems) == False:
		p_status = False # if empty, make p_status to False
	
	# This two lines below, check if the 'riddles' is empty
	if bool(riddles) == False:
		r_status = False
	
	# This two lines below, check if the 'stories' is empty
	if bool(stories) == False:
		s_status = False

	context = {
		'name' : name,
		'poems' : poems,
		'riddles' : riddles,
		'stories' : stories,
		'authors' : authors,
		'p_status' : p_status,
		'r_status' : r_status,
		's_status' : s_status,
	}
	return render(request, 'core/poetist_index.html', context)

def poem_list(request):
	p_status = True

	name = "All Poems"
	poems = all_poems.objects.filter(show_poem = True)
	# This two lines below, check if the 'poems' is empty
	if bool(poems) == False:
		p_status = False # if empty, make p_status to False
	

	context = {
		'name' : name,
		'name_nav' : 'poem',
		'poems' : poems,
		'breadcrumb_text_0' : "All Poems",
		'p_status' : p_status,
	}
	return render(request, 'core/poetist_list.html', context)

def story_list(request):
	s_status = True
	name = "All Stories"
	stories = all_stories.objects.filter(show_story = True)
	# This two lines below, check if the 'stories' is empty
	if bool(stories) == False:
		s_status = False

	context = {
		'name' : name,
		'name_nav' : 'story',
		'stories' : stories,
		'breadcrumb_text_0' : "All Stories",
		's_status' : s_status,
	}
	return render(request, 'core/poetist_list.html', context)

def riddle_list(request):
	r_status = True
	name = "All Riddles"
	riddles = all_riddles.objects.filter(show_riddle = True)
	# This two lines below, check if the 'riddles' is empty
	if bool(riddles) == False:
		r_status = False

	context = {
		'name' : name,
		'name_nav' : 'riddle',
		'riddles' : riddles,
		'breadcrumb_text_0' : "All Riddles",
		'r_status' : r_status,		
	}
	return render(request, 'core/poetist_list.html', context)

def author_list(request):
	name = "All Authors"
	authors = User.objects.all()
	user_poem = all_poems.objects.filter(show_poem = True)
	# print(authors)
	context = {
		'name' : name,
		'name_nav' : 'author',		
		'authors' : authors,
		'user_poem' : user_poem,
	}
	return render(request, 'core/poetist_profile_list.html', context)

#############################   D E T A I L    ######################################

#############################   D E T A I L    P O E M
def poem_detail(request, slug=None):
	name = "Poem"
	poem = get_object_or_404(all_poems, slug = slug, show_poem = True)

	context = {
		"name" : name,
		'name_nav' : 'poem',		
		"poems" : poem,
		'breadcrumb_text_0' : "All Poems",
		'breadcrumb_text_1' : "All Poems",		
	}
	return render(request, 'core/poetist_detail_poem.html', context)

#############################   D E T A I L    S T O R Y
def story_detail(request, slug=None):
	name = "Story"
	story = get_object_or_404(all_stories, slug=slug, show_story = True)

	context = {
		"name" : name,
		'name_nav' : 'story',		
		"stories" : story,
		'breadcrumb_text_0' : "All Stories",
		'breadcrumb_text_1' : "All Stories",	
	}
	return render(request, 'core/poetist_detail_story.html', context)

#############################   D E T A I L     R I D D L E
def riddle_detail(request, slug=None):
	name = "Riddle"
	riddle = get_object_or_404(all_riddles, slug=slug, show_riddle = True)
	
	context = {
		"name" : name,
		'name_nav' : 'riddle',		
		"riddles" : riddle,
		'breadcrumb_text_0' : "All Riddles",
		'breadcrumb_text_1' : "All Riddles",	
	}
	return render(request, 'core/poetist_detail_riddle.html', context)

#############################   D E T A I L     A U T H O R 
def author_detail(request, user_name=None):
	name = "Author"
	author = get_object_or_404(User, username = user_name)

	user_poem = all_poems.objects.filter(show_poem = True).filter(poet = author)
	user_story = all_stories.objects.filter(show_story = True).filter(author = author)
	user_riddle = all_riddles.objects.filter(show_riddle = True).filter(riddler = author)
	# print(user_poem)
	# print(user_story)
	# print(user_riddle)
	# print(author)

	context = {
		"name" : name,
		'name_nav' : 'author',				
		"author" : author,
		"poems" : user_poem,
		"stories" : user_story,
		"riddles" : user_riddle,
	}
	return render(request, "core/poetist_detail_author.html", context)


##############################   D E L E T E   #################################### 

#############################   D E L E T E    P O E M
@login_required
def delete_poem(request, slug=None):
	instance = get_object_or_404(all_poems, slug=slug)
	if instance.author != request.user:
		print("oops! " + str(request.user) + ", You can't delete " + str(instance.author) + "'s poem '" + str(instance.title) + "'." )
		raise Http404
	instance.delete()
	messages.success(request, "Poem deleted Successfully!!")
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#############################   D E L E T E    S T O R Y 
@login_required
def delete_story(request, slug=None):
	instance = get_object_or_404(all_stories, slug=slug)
	if instance.author != request.user:
		print("oops! " + str(request.user) + ", You can't delete " + str(instance.author) + "'s story '" + str(instance.title) + "'." )
		raise Http404
	instance.delete()
	messages.success(request, "Story deleted Successfully!!")
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#############################   D E L E T E    R I D D L E 
@login_required
def delete_riddle(request, slug=None):
	instance = get_object_or_404(all_stories, slug=slug)
	if instance.author != request.user:
		print("oops! " + str(request.user) + ", You can't delete " + str(instance.author) + "'s riddle '" + str(instance.title) + "'." )
		raise Http404
	instance.delete()
	messages.success(request, "Riddle deleted Successfully!!")
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

