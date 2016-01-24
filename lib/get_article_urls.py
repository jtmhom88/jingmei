import re, urllib2, httplib, socket
from bs4 import BeautifulSoup
from urlparse import urljoin
from cookielib import CookieJar

#Return full article list from the datasource config data
def getarticlelist(sourceconfigs):
    #Article list we return will be a dictionary with keys = article urls
    #and value the tuple (datasource, title)
    article_list = dict()
    for s, sdata in sourceconfigs.iteritems():
        print 'Getting article URLs for '+sdata['code']
        for u in sdata['urls']:
            urlstring = u['url']
            o = urllib2.Request(urlstring)

            #Build opener with a cookie processor (required for some sites)
            cj = CookieJar()
            newopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            newopener.addheaders = [('User-agent',
                                  'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.5.0')]
            try:
                response = newopener.open(o, timeout=5)
                soup = BeautifulSoup(response.read())

                #Get all <a> tags
                links = soup.find_all(name='a',href=True)
            
                #Compile the regexes in the list of patterns
                patterns = []
                patternlist = u['patterns']
                for p in patternlist:
                    r = re.compile(p)
                    patterns.append(r)

                #Find all links that match one of the patterns in the config
                #Add them to article list if they match
                #Text contents of the <a> tag is added as article title
                for a in links:
                    for p in patterns:
                        if p.match(a['href']):
                            trimmedurl = urljoin(u['url'],trim(a['href']))
                            article_list[trimmedurl] = (sdata['code'],clean(a.get_text()))
                            
            except urllib2.HTTPError:
                print('HTTPError')
            except urllib2.URLError:
                print('URLError')
            except httplib.IncompleteRead:
                print('IncompleteRead')
            except ValueError:
                print ('ValueError (bad URL?)')
            except socket.timeout:
                print('timeout')
            except socket.error:
                print('Socket error')
    print "Got "+str(len(article_list))+" articles"
    return article_list

#To trim off the query portion of a URL that starts after '?'
#And also the part that starts after '#', and the "/" at
#the end of the URL, if there is one.
#This prevents duplicate urls that link to the same page but
#have different query strings, etc.
def trim(s):
    q = s.find('?')
    if q != -1:
        s = s[0:q]
    q = s.find('#')
    if q != -1:
        s = s[0:q]
    if len(s) > 0:
        if s[-1]=="/":
            s = s[0:-1]
    return s

def clean(s):
    subs = s.split(' ')
    r = ''
    for t in subs:
        r = r+t.strip()+' '
    return r.strip()

