import os
import urllib

def getData(url):
        filename = url[url.rfind("/")+1:]
        path = '/tmp/' + filename
        if not os.path.exists(path):
            f = urllib.urlopen(url)
            with open(path, 'w') as fc:
                fc.write(f.read())
        
        return open(path, 'r')
