from wikitools import wiki, user, api, page
import datetime
import urllib2
import json
from pprint import pprint

def getUserContribs(user, limit = 10):
    querycontinue=False
    if limit is None:
        limit = 10
        querycontinue=True
    params = {'action':'query',
              'list':'usercontribs',
              'ucuser':user.name,
              'ucdir':'newer',
              'ucprop':'ids|timestamp'}
    req = api.APIRequest(user.site, params)
    info=req.query(querycontinue=querycontinue)
    edits = info['query']['usercontribs']
    return edits


def getFirstEdits(user_name, limit = None):
    """Return a dict {Page -> date) mapping pages to the date
    they were first edited by the user.

    If limit is not None, only looks at the user's last `limit` posts.
    """
    wikipedia = wiki.Wiki(url="http://en.wikipedia.org/w/api.php")
    editor = user.User(wikipedia, "mcstrother")
    contribs = getUserContribs(editor, limit)

    #find the first time the user edited each article
    first_edits = {} #dictionary mapping pageids to the datetime.date on which they were first edited
    for edit in contribs:
        if not edit['pageid'] in first_edits:
            year = int(edit['timestamp'][:4])
            month = int(edit['timestamp'][5:7])
            day = int(edit['timestamp'][8:10])            
            first_edits[int(edit['pageid'])] = datetime.date(year, month, day)
    #change all the pageids in first_edits to Page objects
    output = {}
    for pageid, date in first_edits.iteritems():
        output[page.Page(wikipedia, pageid=pageid)] = date
    return output

def add_one_month(dt0):
    """Get the 1st of the month after the month of the date dt0
    """
    dt1 = dt0.replace(day=1)
    dt2 = dt1 + datetime.timedelta(days=32)
    dt3 = dt2.replace(day=1)
    return dt3

def get_pageviews_since_date(page, date):
    """Get the number of timse th ePage has been viewed since the date

    uses the stats.grok.se api
    """
    base_url = "http://stats.grok.se/json/en"
    url_title = page.title.replace(' ', '_').encode('utf-8')
    total_views = 0
    first_month = True
    while date < datetime.date.today():
        url_month = date.strftime('%Y%m')  #e.g Feb 2012 is 201202
        url = '/'.join((base_url, url_month,url_title))
        stats = json.loads(
             urllib2.urlopen(url).read()
             )
        for date_str, views in stats['daily_views'].iteritems():
            if first_month:
                try:
                    view_date = datetime.date(int(date_str[:4]), int(date_str[5:7]),int(date_str[8:10]))
                except ValueError as ve:
                    # the json includes entries for non-existent dates
                    # like "2008-02-31:0",
                    continue
                if not first_month or view_date >= date:
                    total_views += views
            else:
                total_views += views
        first_month = False
        date = add_one_month(date)
    return total_views
        
    

if __name__ == '__main__':
    first_edits = getFirstEdits('mcstrother', limit = 10)
    first_key = first_edits.keys()[0]
    print first_key.title
    print get_pageviews_since_date(first_key, first_edits[first_key])

