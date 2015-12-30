import urllib2, httplib
from cookielib import CookieJar

def getwsjopener(path):
    try:
        f = open(path,'r')
    except IOError:
        return None
    cookiesdict = dict()
    for l in f:
        if l[0] != '#':
            strings = l.split()
            if len(strings)==7:
                val = strings[6]
            else:
                val = ''
            cookiesdict[strings[5]] = val

    #Build urllib2 request using the cookie dictionary
    o = urllib2.Request('http://www.wsj.com')
    o.add_header(
        'Cookie', "; ".join('%s=%s' % (k,v) for k,v in cookiesdict.items()))

    #Create a urllib2 opener with a cookie processor and cookie jar
    cj = CookieJar()
    newopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    #Next line will open wsj.com and store a 
    #new session cookie provided by wsj.com in the cookie jar
    try:
        response = newopener.open(o)
    except urllib2.HTTPError:
        print('HTTPError')
        return None
    except urllib2.URLError:
        print('URLError')
        return None
    except httplib.IncompleteRead:
        print('IncompleteRead' )
        return None

    return newopener
