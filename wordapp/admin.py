from django.contrib import admin
from wordapp.models import Chapter,Level,Solution


class ChapterAdmin(admin.ModelAdmin):
    list_display = ("chapter_name",)


class LevelAdmin(admin.ModelAdmin):
    list_display = ("level_serial", "level_letters")


class SolutionAdmin(admin.ModelAdmin):
    list_display = ("solution_word",)


# Register your models here.

admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Level,LevelAdmin)
admin.site.register(Solution,SolutionAdmin)
