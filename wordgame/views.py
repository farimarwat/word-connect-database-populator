from django.shortcuts import render
from wordapp.models import Chapter, Level, Solution


def index(request):
    return render(request, "index.html")


def chapters(request):
    error = ""
    if request.method == "POST":
        try:
            name = request.POST.get("chapter_name")
            if name != "":
                chapter = Chapter(chapter_name=name)
                chapter.save()
            else:
                error = "Error: Input field is required"
        except Exception as ex:
            error = ex
    chapters = Chapter.objects.all()
    data = {
        "chapters": chapters,
        "error": error
    }
    return render(request, "chapters.html", data)


def levels(request, chapterid):
    error = ""
    if request.method == "POST":
        try:
            level_serial = int(request.POST.get("level_serial"))
            level_letters = request.POST.get("level_letters")
            if level_serial is not None and level_letters != "":
                level = Level(chapter_id=chapterid, level_serial=level_serial, level_letters=level_letters)
                level.save()
        except Exception as ex:
            error = ex
    chapter = Chapter.objects.get(id=chapterid)
    print("Chapter:", chapter.chapter_name)
    levels = Level.objects.filter(chapter=chapter)
    data = {
        "chapter": chapter,
        "levels": levels,
        "error": error
    }
    return render(request, "levels.html", data)


def solutions(request, levelid):
    error = ""
    if request.method == "POST":
        try:
            word = request.POST.get("solution_word")
            if word != "":
                solution = Solution(level_id=levelid, solution_word=word)
                solution.save()
            else:
                error = "Error: Input field is required"
        except Exception as ex:
            error = ex
    level = Level.objects.get(id=levelid)
    solutions = Solution.objects.filter(level_id=levelid)
    data = {
        "level": level,
        "solutions": solutions,
        "error": error
    }
    return render(request, "solutions.html", data)
