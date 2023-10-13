import urllib.request
import xml.etree.ElementTree as ET
url = "http://py4e-data.dr-chuck.net/comments_1910356.xml"
html = urllib.request.urlopen(url).read()
total = 0
count = 0
tree = ET.fromstring(html)
lst = tree.findall ('comments/comment')
for item in lst:
    count += 1
    t = item.find ('count').text
    total = total + float (t)
print ('Count:', count)
print ('Sum:' , total)
