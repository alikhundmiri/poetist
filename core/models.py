from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.utils import timezone
from django.conf import settings

class all_about(models.Model):
	app_name = "About"
	question = models.CharField(max_length=1000, blank=False, null=False)
	answer = models.TextField(max_length=10000, blank=False, null=False)
	show_about = models.BooleanField(default=True)
	
	timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)
	updated = models.DateTimeField(auto_now = True, auto_now_add = False)

	def __str__(self):
		return self.question

	def get_absolute_url(self):
		return reverse("about")

	class Meta:
		ordering = ["-timestamp", "-updated"]
		verbose_name = "About"
		verbose_name_plural = "About"



class taggers(models.Model):
	app_name = "Tag"
	tag_name = models.CharField(max_length=20)
	slug = models.SlugField(unique=True)
	description = models.TextField(max_length=1000)

	def __str__(self):
		return self.tag_name

	def get_absolute_url(self):
		return reverse("writer:tag_list", kwargs={"slug" : self.slug})

	class Meta:
		ordering = ["-tag_name",]
		verbose_name = 'Tag'
		verbose_name_plural = 'Tags'

class all_authors(models.Model):
	app_name = "Author"
	user_name = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, unique=True)
	
	def get_absolute_url(self):
		return reverse("author_detail", kwargs={"user_name" : self.user_name})

	class Meta:
		verbose_name = "Author"
		verbose_name_plural = "Authors"
	
	def __str__(self):
		return self.user_name.get_username()

class all_poems(models.Model):
	app_name = "Poem"
	title = models.CharField(max_length=300, blank=False, null=False)
	slug = models.SlugField(unique=True)
	poem = models.TextField(max_length=300000, blank=False, null=False)
	show_poem = models.BooleanField(default=True)
	poet = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	tags = models.ManyToManyField(taggers, blank=True, null=True)

	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return (self.title)

	def get_absolute_url(self):
		return reverse("writer:poem_detail", kwargs={"slug" : self.slug})

	def get_edit_url(self):
		return reverse("writer:edit_poem", kwargs={"slug" : self.slug})

	def get_draft_toggle_url(self):
		return reverse("writer:draft_poem_toggle", kwargs={"slug" : self.slug})

	class Meta:
		ordering = ["-timestamp", "-updated"]
		verbose_name = "Poem"
		verbose_name_plural = "Poems"


class all_riddles(models.Model):
	app_name = "Riddle"
	title = models.CharField(max_length=300, blank=False, null=False)
	slug = models.SlugField(unique=True)
	riddle = models.TextField(max_length=30000, blank=False, null=False)
	answer = models.CharField(max_length=500, blank=True, null=True)
	explanation = models.TextField(max_length=30000, blank=True, null=True)
	show_riddle = models.BooleanField(default=True)
	riddler = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	tags = models.ManyToManyField(taggers, blank=True, null=True)

	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return (self.title)
		
	def get_absolute_url(self):
		return reverse("writer:riddle_detail", kwargs={"slug" : self.slug})

	def get_edit_url(self):
		return reverse("writer:edit_riddle", kwargs={"slug" : self.slug})

	def get_draft_toggle_url(self):
		return reverse("writer:draft_riddle_toggle", kwargs={"slug" : self.slug})

	class Meta:
		ordering = ["-timestamp", "-updated"]
		verbose_name = "Riddle"
		verbose_name_plural = "Riddles"


class all_stories(models.Model):
	app_name = "Story"
	title = models.CharField(max_length=300, blank=False, null=False)
	slug = models.SlugField(unique=True)
	story = models.TextField(max_length=30000, blank=False, null=False)
	show_story = models.BooleanField(default=True,)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	tags = models.ManyToManyField(taggers, blank=True, null=True)
	related_story = models.ManyToManyField("self", blank=True, null=True)

	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return (self.title)

	def this_user(self):
		return (self.author)

	def get_absolute_url(self):
		return reverse("writer:story_detail", kwargs={"slug" : self.slug})

	def get_edit_url(self):
		return reverse("writer:edit_story", kwargs={"slug" : self.slug})

	def get_draft_toggle_url(self):
		return reverse("writer:draft_story_toggle", kwargs={"slug" : self.slug})

	class Meta:
		ordering = ["-timestamp", "-updated"]
		verbose_name = "Story"
		verbose_name_plural = "Stories"


#################### SLUG CREATOR FOR POEMS #############################
def create_slug_poem(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = all_poems.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug_poem(instance, new_slug=new_slug)
	return slug


def pre_save_jd_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug_poem(instance)

pre_save.connect(pre_save_jd_receiver, sender=all_poems)

#################### SLUG CREATOR FOR RIDDLES #############################
def create_slug_riddle(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = all_riddles.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug_riddle(instance, new_slug=new_slug)
	return slug


def pre_save_jd_receiver_riddle(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug_riddle(instance)

pre_save.connect(pre_save_jd_receiver_riddle, sender=all_riddles)

#################### SLUG CREATOR FOR STORIES #############################
def create_slug_story(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = all_stories.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug_story(instance, new_slug=new_slug)
	return slug


def pre_save_jd_receiver_story(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug_story(instance)

pre_save.connect(pre_save_jd_receiver_story, sender=all_stories)

#################### SLUG CREATOR FOR TAGS #############################
def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = taggers.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_jd_receiver_poem(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug_tags(instance)

pre_save.connect(pre_save_jd_receiver_poem, sender=taggers)
