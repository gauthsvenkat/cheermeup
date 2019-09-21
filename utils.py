from urllib.request import urlopen
import re
import cv2

def playVideo(url, name=None):
    assert url.endswith('.webm') or url.endswith('.mp4')
        
    clip = cv2.VideoCapture(url)

    rval, frame = clip.read()

    if not rval:
        return False

    while(rval):
       cv2.imshow(name if name is not None else 'clip', frame)

       if cv2.waitKey(40)&0xFF == ord('q'):
           break

       rval, frame = clip.read()

    cv2.destroyAllWindows()

    return True

def parseLink(url):

    if 'gfycat.com' in url:
        
        page = urlopen(url).read().decode('utf8')
        regex = "https:\/\/thumbs\.gfycat\.com\/[\w-]+\.(mp4|webm)"
        match = re.search(regex, page)
        url = match.group(0)

    url = url.replace('.gifv', '.mp4') if url.endswith('.gifv') else url
    url = url.replace('https:', 'http:') if url.startswith('https:') else url
    
    return url
