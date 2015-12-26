#Data source config format:

#"urls": list of dictionaries that each represent a URL to scan for links.
#In each dictionary, "url" is the actual URL to scan.  Then we scan each <a> tag in the HTML to 
#see if the href matches any of the regexes in "patterns".  If it does, append 
#"baseurl" to get a full article URL.

#"code": name we use for the data source

#"need-cookies": indicates whether the URL needs cookies to open.  (Just the front page URL, not the actual articles)
#So far, only Barron's needs cookies

datasources = {
    "www" : { 
            "urls" : [
         {"url" : "http://www.www.com", 
         "patterns" : [{'regex': '.*\/articles\/.*', 'baseurl' : ''}]},
         {"url" : "http://www.www.com/news/markets",
         "patterns" : [{'regex' : '.*\/articles\/.*', 'baseurl' : ''}]},
             {"url" : "http://blogs.www.com/moneybeat/",
         #actual article links have a date string in them, so should have 4 consecutive digits
             #We also don't want any comment links
         "patterns" : [{'regex' : '^(?!.*comments).*[0123456789][0123456789][0123456789][0123456789]', 'baseurl' : ''}]}
         ],
            "code" : "www",
        "need-cookies" : "no"
    },
    "yyy" : { 
            "urls" : [
         {"url" : "http://finance.yyy.com", 
         "patterns" : [{'regex': '\/news\/.*', 'baseurl' : 'http://finance.yyy.com'}]}
         ],
            "code" : "yyy",
        "need-cookies" : "no"
    }
}
