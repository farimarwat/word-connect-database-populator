from django.shortcuts import render
from wordapp.models import Chapter, Level, Solution
import sqlite3
import shutil


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
            details = request.POST.get("solution_details")
            if word != "":
                solution = Solution(level_id=levelid, solution_word=word, solution_details=details)
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


def create_tables(connection):
    cursor = connection.cursor()

    # Chapter table
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS wordapp_chapter (
            id INTEGER PRIMARY KEY NOT NULL,
            chapter_name TEXT NOT NULL,
            chapter_completed INTEGER NOT NULL
        )
    ''')

    # Level table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wordapp_level (
            id INTEGER PRIMARY KEY NOT NULL,
            level_serial INTEGER NOT NULL,
            level_letters TEXT NOT NULL,
            level_completed INTEGER NOT NULL,
            chapter_id INTEGER NOT NULL
        )
    ''')

    # Solution table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wordapp_solution (
            id INTEGER PRIMARY KEY NOT NULL,
            solution_word TEXT NOT NULL,
            solution_details TEXT,
            level_id INTEGER NOT NULL
        )
    ''')

    connection.commit()


def copy_tables_data(from_db, to_db):
    try:
        # Connect to the source database (from_db)
        source_connection = sqlite3.connect(from_db)
        source_connection.row_factory = sqlite3.Row
        source_cursor = source_connection.cursor()

        # Connect to the destination database (to_db)
        destination_connection = sqlite3.connect(to_db)
        destination_cursor = destination_connection.cursor()

        # Tables to copy
        tables_to_copy = ['wordapp_solution', 'wordapp_level', 'wordapp_chapter']

        for table_name in tables_to_copy:
            print(f"Copying data from table: {table_name}")

            # Get the column names from the source table
            source_cursor.execute(f"PRAGMA table_info('{table_name}');")
            columns = source_cursor.fetchall()
            column_names = [column['name'] for column in columns]

            # Create the table in the destination database
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_names)})"
            destination_cursor.execute(create_table_query)

            # Copy data from the source table to the destination table
            select_query = f"SELECT * FROM {table_name}"
            source_cursor.execute(select_query)
            data = source_cursor.fetchall()

            # Prepare the INSERT query for the destination table
            insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['?' for _ in column_names])})"
            destination_cursor.executemany(insert_query, data)

            # Commit changes for each table
            destination_connection.commit()

        # Close the connections
        source_connection.close()
        destination_connection.close()

        print("Tables and data copied successfully.")
    except Exception as ex:
        print("Error copying tables and data:", ex)


def preparedatabase(request):
    result = ""
    error = ""
    try:
        # Create the SQLite database
        connection = sqlite3.connect("wordgame.db")

        # Create tables in the database
        create_tables(connection)
        from_db = "wordgame.sqlite3"
        to_db = "wordgame.db"
        copy_tables_data(from_db,to_db)
        # Close the connection
        connection.close()
        result = "Database created"
    except Exception as ex:
        error = ex
    data = {
        "result": result,
        "error": error
    }
    return render(request, "preparedatabase.html", data)
