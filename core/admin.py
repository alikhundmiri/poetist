from django.contrib import admin
from .models import all_poems, all_authors,all_riddles,all_stories, taggers, all_about

class AboutAdmin(admin.ModelAdmin):
	list_display = ["question", "timestamp", "updated","show_about"]
	list_filter = ["question", "answer", "timestamp", "updated"]
	search_fields = ["question", "answer", "timestamp", "updated"]
	list_editable = ["show_about",]

	class Meta:
		model = all_about


class PoemAdmin(admin.ModelAdmin):
	list_display = ["title","timestamp", "updated","show_poem" ]
	list_filter = ["title", "timestamp", "updated"]
	search_fields = ["title","poem", "timestamp", "updated"]
	filter_horizontal = ["tags",]
	list_editable = ["show_poem",]

	class Meta:
		model = all_poems


class RiddleAdmin(admin.ModelAdmin):
	list_display = ["title", "timestamp", "updated","show_riddle"]
	list_filter = ["title", "timestamp", "updated"]
	search_fields = ["title","riddle", "timestamp", "updated"]
	filter_horizontal = ["tags",]
	list_editable = ["show_riddle",]

	class Meta:
		model = all_riddles

class StoryAdmin(admin.ModelAdmin):
	list_display = ["title", "timestamp", "updated", "show_story", "author"]
	list_filter = ["title", "timestamp", "updated", "author"]
	search_fields = ["title", "story", "timestamp", "updated", "author"]
	filter_horizontal = ["tags", "related_story"]
	list_editable = ["show_story",]

	class Meta:
		model = all_stories

class AuthorsAdmin(admin.ModelAdmin):
	list_display = ["user_name",]
	list_filter = ["user_name",]
	search_fields = ["user_name",]

	class Meta:
		model = all_authors


class TagAdmin(admin.ModelAdmin):
	list_display = ["tag_name","description"]
	list_filter = ["tag_name","description"]
	search_fields = ["tag_name","description"]

	class Meta:
		model = taggers


admin.site.register(all_about, AboutAdmin)
admin.site.register(all_poems, PoemAdmin)
admin.site.register(all_authors, AuthorsAdmin)
admin.site.register(all_riddles, RiddleAdmin)
admin.site.register(all_stories, StoryAdmin)
admin.site.register(taggers, TagAdmin)

