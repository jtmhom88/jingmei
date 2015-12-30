import re, urllib2, httplib
from bs4 import BeautifulSoup
from cookielib import CookieJar

#Get article lines for given URL
def getarticlelines(sourceconfigs, url, source, cookieopeners):
    #If source is wsj or seekingalpha, need to log in
    #Need to figure out how to throw out comments on zerohedge
    lines = []
    if source == 'zerohedge' or source == 'seekingalpha':
        return lines
    else:
        try:
            #For login sites, use provided cookie opener, if it exists
            copener = cookieopeners.get(source)
            o = urllib2.Request(url)
            if copener == None:
                cj = CookieJar()
                copener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

            response = copener.open(o)
            soup = BeautifulSoup(response.read())

            tag = sourceconfigs[source]['article-text-tag']
            articlediv = soup.find_all(**tag)
            
            if len(articlediv)==0:
                print "Couldn't find article text tag"
            else:
                maindiv = articlediv[0]
                #Look for <p> tags that are children of the main tag
                for c in maindiv.descendants:
                    if c.name=='p':
                        articleline = ''
                        for s in c.contents:
                            #Sometimes article lines are broken up by <br> tags
                            #instead of <p> tags.  The if statement deals w/ this
                            if s.name == None:
                                articleline = articleline+s.strip()+" "
                            elif s.name == 'br':
                                if articleline.strip() != '':
                                    lines.append(articleline)
                                    if len(articleline) > 10000:
                                        raise Exception
                                articleline = ''
                            else:
                                for t in s.strings:
                                    articleline = articleline+t.strip()+" "
                               
                        if articleline.strip() != '':
                            lines.append(articleline)
                            if len(articleline) > 10000:
                                raise Exception
            return lines
        except urllib2.HTTPError:
            print('HTTPError')
            return lines
        except urllib2.URLError:
            print('URLError')
            return lines
        except httplib.IncompleteRead:
            print('IncompleteRead')
            return lines
    
        
