import re, urllib2, httplib
from bs4 import BeautifulSoup
from cookielib import CookieJar

#Return full article list from the datasource config data
def getarticlelist(sourceconfigs):
    #Article list we return will be a dictionary with keys = article urls
    #and values = datasource code string, e.g. "wsj"
    article_list = dict()
    for s, sdata in sourceconfigs.iteritems():
        print 'Getting article URLs for '+sdata['code']
        for u in sdata['urls']:
            urlstring = u['url']
            o = urllib2.Request(urlstring)

            #Build opener with a cookie processor (required for some sites)
            cj = CookieJar()
            newopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            try:
                response = newopener.open(o)
                soup = BeautifulSoup(response.read())

                #Get all <a> tags
                links = soup.find_all(name='a',href=True)
            
                #Compile the regexes in the list of patterns
                patterns = []
                patternlist = u['patterns']
                for p in patternlist:
                    r = re.compile(p['regex'])
                    patterns.append([r,p['baseurl']])

                #Find all links that match one of the patterns in the config
                #Add them to article list if they match
                #Text contents of the <a> tag is added as article title
                for a in links:
                    for p in patterns:
                        if p[0].match(a['href']):
                            trimmedurl = p[1]+trim(a['href'])
                            article_list[trimmedurl] = (sdata['code'],clean(a.get_text()))
                            
            except urllib2.HTTPError:
                print('HTTPError')
            except urllib2.URLError:
                print('URLError')
            except httplib.IncompleteRead:
                print('IncompleteRead')
    return article_list

#To trim off the query portion of a URL that starts after '?'
#And also the part that starts after '#'
def trim(s):
    q = s.find('?')
    if q != -1:
        s = s[0:q]
    q = s.find('#')
    if q != -1:
        s = s[0:q]
    return s

def clean(s):
    subs = s.split(' ')
    r = ''
    for t in subs:
        r = r+t.strip()+' '
    return r

