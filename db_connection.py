import sqlite3

conn = sqlite3.connect('social.db', check_same_thread=False)


def retrieve_companies():
    c = conn.cursor()
    c.execute("SELECT * FROM Companies")
    return c.fetchall()


def retrieve_count_posts(company_id, source):
    c = conn.cursor()
    if source is None:
        c.execute("SELECT COUNT(*) FROM Posts JOIN Companies ON Posts.companyId = Companies.id WHERE Companies.id = ?", company_id)
    else:
        c.execute("SELECT COUNT(*) FROM Posts JOIN Companies ON Posts.companyId = Companies.id WHERE Companies.id = ? AND Posts.Source = ?", (company_id, source))
    return c.fetchall()


def retrieve_posts(company_id, source):
    c = conn.cursor()
    c.execute("SELECT * FROM Posts JOIN Companies ON Posts.companyId = Companies.id WHERE Companies.id = ? AND Posts.Source = ?", (company_id, source))
    return c.fetchall()


def retrieve_interactions(company_id, min_date, max_date):
    c = conn.cursor()
    if not min_date and not max_date:
        c.execute("SELECT Source, SUM(Likes), SUM(Comments), Sum(Shares) FROM Interactions JOIN Posts ON Interactions.PostId = Posts.Id WHERE Posts.companyId = ? GROUP BY Source", company_id)
    elif min_date and not max_date:
        c.execute("SELECT Source, SUM(Likes), SUM(Comments), Sum(Shares) FROM Interactions JOIN Posts ON Interactions.PostId = Posts.Id WHERE Posts.companyId = ? AND strftime('%s', Interactions.Date) >= strftime('%s', ?) GROUP BY Source", (company_id, min_date))
    elif not min_date and max_date:
        c.execute("SELECT Source, SUM(Likes), SUM(Comments), Sum(Shares) FROM Interactions JOIN Posts ON Interactions.PostId = Posts.Id WHERE Posts.companyId = ? AND strftime('%s', Interactions.Date) <= strftime('%s', ?) GROUP BY Source", (company_id, max_date))
    elif min_date and max_date:
        c.execute("SELECT Source, SUM(Likes), SUM(Comments), Sum(Shares) FROM Interactions JOIN Posts ON Interactions.PostId = Posts.Id WHERE Posts.companyId = ? AND strftime('%s', Interactions.Date) BETWEEN strftime('%s', ?) AND strftime('%s', ?) GROUP BY Source", (company_id, min_date, max_date))
    return c.fetchall()


def retrieve_evolution(company_id):
    c = conn.cursor()
    c.execute("""
        SELECT
        strftime('%W', Posts.Date) Interval,
        SUM(Likes),
        Source,
        Posts.id as IdPost
        FROM Interactions
        JOIN Posts ON Interactions.PostId = Posts.Id
        WHERE Posts.companyId = ? AND Interactions.Date IN (
            SELECT MAX(Interactions.Date) FROM Interactions JOIN Posts ON Interactions.PostId = Posts.Id WHERE Posts.Id = IdPost
        )
        GROUP BY Interval, Source
        ORDER BY Posts.Id, Interactions.Date;
    """, company_id)
    return c.fetchall()
