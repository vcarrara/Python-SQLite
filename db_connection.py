import sqlite3

conn = sqlite3.connect('social.db', check_same_thread=False)


def retrieve_companies():
    c = conn.cursor()
    c.execute("SELECT * FROM Companies")
    return c.fetchall()


def count_posts(company_id, source):
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
    if min_date is None and max_date is None:
        c.execute("SELECT Count(*), Source FROM Interactions JOIN Posts ON Interactions.PostId = Posts.Id JOIN Companies ON Posts.CompanyId = Companies.Id WHERE companyId = ? GROUP BY Source", company_id)
    elif min_date is not None and max_date is None:
        c.execute("SELECT Count(*), Source FROM Interactions JOIN Posts ON Interactions.PostId = Posts.Id JOIN Companies ON Posts.CompanyId = Companies.Id WHERE companyId = ? AND strftime('%s', Interactions.Date) >= strftime('%s', ?) GROUP BY Source", (company_id, min_date))
    elif min_date is None and max_date is not None:
        c.execute("SELECT Count(*), Source FROM Interactions JOIN Posts ON Interactions.PostId = Posts.Id JOIN Companies ON Posts.CompanyId = Companies.Id WHERE companyId = ? AND strftime('%s', Interactions.Date) <= strftime('%s', ?) GROUP BY Source", (company_id, max_date))
    elif min_date is not None and max_date is not None:
        c.execute("SELECT Count(*), Source FROM Interactions JOIN Posts ON Interactions.PostId = Posts.Id JOIN Companies ON Posts.CompanyId = Companies.Id WHERE companyId = ? AND strftime('%s', Interactions.Date) BETWEEN strftime('%s', ?) AND strftime('%s', ?) GROUP BY Source", (company_id, min_date, max_date))
    return c.fetchall()
