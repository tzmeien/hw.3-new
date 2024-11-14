import json# hello
import sqlite3
movie = []


def mode(select):
    '''main def only select '''
    if select == 1:
        import_mov()
    elif select == 2:
        find()
    elif select == 3:
        add()
    elif select == 4:
        revise()
    elif select == 5:
        delete()
    elif select == 6:
        export()
    elif select == 7:
        print("系統已退出。")
    else:
        print("請輸入正確的選項\n")


def import_mov():
    '''import movie data to .db'''
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS movies
            (title TEXT PRIMARY KEY, director TEXT NOT NULL, genre TEXT NOT \
NULL, year INTEGER NOT NULL, rating REAL CHECK(rating >= 1.0 and rating<=10.0\
))'''
    )
    with open('movies.json', 'r', encoding='UTF-8') as f:
        movie = json.load(f)
    for m in movie:
        cursor.execute(
            "INSERT INTO movies VALUES(?, ?, ?, ?, ?)",
            (m['title'], m['director'], m['genre'], m['year'], m['rating']),
        )
    conn.commit()
    cursor.close()
    conn.close()
    print("電影已匯入")


def find():
    '''find movie, show all or only one'''
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies")
    all_movie = cursor.fetchall()
    if input("查詢全部電影嗎？(y/n): ") == 'y':
        if not all_movie:
            print("查無資料")
        else:
            print(f"{'電影名稱':　<7}{'導演':　<10}{'類型':　<4}{'上映年份':　<6}{'評分'}\
\n------------------------------------------------------------------------")
            for m in all_movie:
                print(f"{m[0]:　<7}{m[1]:　<10}{m[2]:　<4}{m[3]:　<8}{m[4]:　<4}")

    else:
        count = 0
        name = input("請輸入電影名稱: ")
        for m in all_movie:
            count += 1
            if name == m[0]:
                print(f"{'電影名稱':　<7}{'導演':　<10}{'類型':　<4}{'上映年份':　<6}{'評分'}\
\n------------------------------------------------------------------------")
                print(f"{m[0]:　<7}{m[1]:　<10}{m[2]:　<4}{m[3]:　<8}{m[4]}")
                break
            elif count == len(all_movie):
                print("查無資料")

    cursor.close()
    conn.close()


def add():
    '''add movie data'''
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    list = []
    list.append(input("電影名稱: "))
    list.append(input("導演: "))
    list.append(input("類型: "))
    list.append(input("上映年份: "))
    list.append(input("評分 (1.0 - 10.0): "))
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS movies
            (title TEXT PRIMARY KEY, director TEXT NOT NULL, genre TEXT NOT \
NULL, year INTEGER NOT NULL, rating REAL CHECK(rating >= 1.0 and rating<=10.0\
))'''
    )
    cursor.execute(
        '''INSERT INTO movies VALUES(?, ?, ?, ?, ?)''',
        (list[0], list[1], list[2], list[3], list[4]),
    )
    conn.commit()
    cursor.close()
    conn.close()
    print("電影已新增")


def revise():
    '''update movie data'''
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    n = input("請輸入要修改的電影名稱: ")
    name = input("請輸入新的電影名稱 (若不修改請直接按 Enter): ")
    director = input("請輸入新的導演 (若不修改請直接按 Enter): ")
    genre = input("請輸入新的類型 (若不修改請直接按 Enter): ")
    year = input("請輸入新的上映年份 (若不修改請直接按 Enter): ")
    rating = input("請輸入新的評分 (1.0 - 10.0) (若不修改請直接按 Enter): ")
    if director is not None:
        cursor.execute('UPDATE movies SET director = ? WHERE title = ?',
                       (director, n))
    if genre is not None:
        cursor.execute('UPDATE movies SET genre = ? WHERE title = ?',
                       (genre, n))
    if year is not None:
        cursor.execute('UPDATE movies SET year = ? WHERE title = ?',
                       (year, n))
    if rating is not None:
        cursor.execute('UPDATE movies SET rating = ? WHERE title = ?',
                       (rating, n))
    if name is not None:
        cursor.execute('UPDATE movies SET title = ? WHERE title = ?',
                       (name, n))
    conn.commit()
    cursor.close()
    conn.close()


def delete():
    '''delete one movie data'''
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    if input("刪除全部電影嗎？(y/n): ") == 'y':
        cursor.execute("DELETE FROM movies")
    else:
        name = input("請輸入電影名稱: ")
        cursor.execute("DELETE FROM movies WHERE title = ?", (name,))
    conn.commit()
    cursor.close()
    conn.close()
    print("電影已刪除")


def export():
    '''export .db data to .json'''
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    col = ["title", "director", "genre", "year", "rating"]
    if input("匯出全部電影嗎？(y/n): ") == 'y':
        cursor.execute("SELECT title, director, genre, year, rating FROM\
movies")
        row = cursor.fetchall()
        new = [dict(zip(col, r)) for r in row]
    else:
        name = input("請輸入要匯出的電影名稱: ")
        cursor.execute("SELECT title, director, genre, year, rating FROM\
movies WHERE title = ?", (name,))
        row = cursor.fetchone()
        new = [dict(zip(col, row))]
    with open('exported.json', 'w', encoding='utf-8') as m:
        json.dump(new, m, ensure_ascii=False, indent=4)
    cursor.close()
    conn.close()
    print("電影資料已匯出至 exported.json")
