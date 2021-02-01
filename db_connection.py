import sqlite3

conn = sqlite3.connect('social.db', check_same_thread=False)


def retrieve_companies():
    c = conn.cursor()
    c.execute("SELECT * FROM Companies")
    return c.fetchall()


def count_posts(companyId, source):
    c = conn.cursor()
    if source is None:
        c.execute("SELECT COUNT(*) FROM Posts JOIN Companies ON Posts.companyId = Companies.id WHERE Companies.id = ?", companyId)
    else:
        c.execute("SELECT COUNT(*) FROM Posts JOIN Companies ON Posts.companyId = Companies.id WHERE Companies.id = ? AND Posts.Source = ?", (companyId, source))
    return c.fetchall()


def retrieve_posts(companyId, source):
    c = conn.cursor()
    c.execute("SELECT * FROM Posts JOIN Companies ON Posts.companyId = Companies.id WHERE Companies.id = ? AND Posts.Source = ?", (companyId, source))
    return c.fetchall()


def retrieve_interactions(companyId, minDate, maxDate):
    c = conn.cursor()
    if minDate is None and maxDate is None:
        c.execute("SELECT Count(*), Source FROM Interactions JOIN Posts ON Interactions.PostId = Posts.Id JOIN Companies ON Posts.CompanyId = Companies.Id WHERE companyId = ? GROUP BY Source", companyId)
    elif minDate is not None and maxDate is None:
        c.execute("SELECT Count(*), Source FROM Interactions JOIN Posts ON Interactions.PostId = Posts.Id JOIN Companies ON Posts.CompanyId = Companies.Id WHERE companyId = ? AND strftime('%s', Interactions.Date) >= strftime('%s', ?) GROUP BY Source", (companyId, minDate))
    elif minDate is None and maxDate is not None:
        c.execute("SELECT Count(*), Source FROM Interactions JOIN Posts ON Interactions.PostId = Posts.Id JOIN Companies ON Posts.CompanyId = Companies.Id WHERE companyId = ? AND strftime('%s', Interactions.Date) <= strftime('%s', ?) GROUP BY Source", (companyId, maxDate))
    elif minDate is not None and maxDate is not None:
        c.execute("SELECT Count(*), Source FROM Interactions JOIN Posts ON Interactions.PostId = Posts.Id JOIN Companies ON Posts.CompanyId = Companies.Id WHERE companyId = ? AND strftime('%s', Interactions.Date) BETWEEN strftime('%s', ?) AND strftime('%s', ?) GROUP BY Source", (companyId, minDate, maxDate))
    return c.fetchall()
