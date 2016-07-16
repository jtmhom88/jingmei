import re, urllib2, httplib, socket
from bs4 import BeautifulSoup
from cookielib import CookieJar

#Get article lines for given URL
def getarticlelines(sourceconfigs, url, source, cookieopeners):
    lines = []
    try:
        #For login sites, use provided cookie opener, if it exists
        copener = cookieopeners.get(source)
        o = urllib2.Request(url)
        if copener == None:
            cj = CookieJar()
            copener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        
        copener.addheaders = [('User-agent',
                                'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.5.0')]
        response = copener.open(o, timeout=5)
        soup = BeautifulSoup(response.read())

        tag = sourceconfigs[source]['article-text-tag']
        articlediv = soup.find_all(**tag)
        global clipped_lines
        clipped_lines = False
        
        if len(articlediv)==0:
            print "Couldn't find article text tag"
            return (20, ['Placeholder line'])
        else:
            for d in articlediv:
                maindiv = d
                if source != 'newsmax':
                #Look for <p> tags that are children of the main tag
                    for c in maindiv.descendants:
                        if c.name=='p':
                            articleline = ''
                            for s in c.contents:
                                #Sometimes article lines are broken up by <br> tags
                                #instead of <p> tags.
                                #The if statement deals w/ this
                                if s.name == None:
                                    articleline = articleline+s.strip()+" "
                                elif s.name == 'br':
                                    addToLines(articleline, lines)
                                    articleline = ''
                                else:
                                    for t in s.strings:
                                        articleline = articleline+t.strip()+" "
                               
                            addToLines(articleline, lines)
                else:
                    #Newsmax uses <p> tags very inconsistently
                    #Sometimes articles have no <p> tags,
                    #sometimes articles have text both outside and inside
                    #<p> tags.  No other sites seem to do this so we use a separate
                    #scraping routine
                    articleline = ''
                    for c in maindiv.contents:
                        if c.name==None:
                            articleline = articleline+c.strip()+" "
                        elif c.name=='br':
                            addToLines(articleline, lines)
                            articleline = ''
                        elif c.name=='p':
                            addToLines(articleline, lines)
                            articleline = ''
                            for s in c.contents:
                                #Sometimes article lines are broken up by <br> tags
                                #instead of <p> tags.
                                #The if statement deals w/ this
                                if s.name == None:
                                    articleline = articleline+s.strip()+" "
                                elif s.name == 'br':
                                    addToLines(articleline, lines)
                                    articleline = ''
                                else:
                                    for t in s.strings:
                                        articleline = articleline+t.strip()+" "
                               
                            addToLines(articleline, lines)
                            articleline = ''
                        else:
                            for t in c.strings:
                                articleline = articleline+t.strip()+" "
                    addToLines(articleline, lines)
                        
                        
        if len(lines)==0:
            return (3, ['Placeholder line'])
        else:
            if (clipped_lines == True):
                return (2, lines)
            if (clipped_lines == False):
                return (1, lines)
    except urllib2.HTTPError:
        print('HTTPError')
        return (12, lines)
    except urllib2.URLError:
        print('URLError')
        return (11, lines)
    except httplib.IncompleteRead:
        print('IncompleteRead')
        return (13, lines)
    except ValueError:
        print('ValueError (bad url?)')
        return(14, lines)
    except socket.timeout:
        print('timeout')
        return (10, lines)
    except socket.error:
        print('Socket error')
        return (15, lines)
    
def addToLines(articleline, lines):
    global clipped_lines
    strippedarticleline = articleline.strip()
    if strippedarticleline != '':
        lines.append(strippedarticleline)
        if len(strippedarticleline) > 10000:
            clipped_lines = True
