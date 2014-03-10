# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

import re
from collections import defaultdict


class PaperAnsys(object):
    def __init__(self,obj,ref,lib):
        self.obj = obj #查询目标
        self.ref = ref #所有引用
        self.lib = lib #作者提供
    #转换输入格式
    def fread(self,f):
        temp = open(f).readlines()
        return map(lambda t: ' '.join(t.split()), temp)
    def libread(self):
        return self.fread(self.lib)
    def objread(self):
        return self.fread(self.obj)
    def refread(self):
        heads = ['Record','Edited by:', 'eISSN:', 'Group Author(s):', 'ISBN:', 'ISSN:', 'Source:', 'Title:']
        def reffilter(s):
            for h in heads:
                if s == '' or s.startswith(h):
                    break
                    return False
            else:
                return True
        #筛选出Obj和Author
        temp = [f for f in self.fread(self.ref) if reffilter(f)]
        #ref存储
        refdic = defaultdict(list)
        for ref in temp:
            if not ref.startswith('Author'):
                refkey = ref if '.' not in ref.split()[-1] else ' '.join(ref.split()[:-1])
            else:
                refdic[refkey].append(ref)
        return refdic
            


obj = 'obj.txt'
ref = 'ref.txt'
lib = 'lib.txt'
pansys = PaperAnsys(obj,ref,lib)


objtable = pansys.objread()
sorted(objtable)


fref = pansys.refread()
sorted(fref.keys())


len(set(objtable) & set(fref.keys()))


lred = pansys.libread()
lred


text = lred
text


for idx,ptn in enumerate(objtable):
    print "obj %d: %s" % (idx+1, ptn)
    ptn = '.+?'.join(ptn.split()[-4:])
    print 'pattern:',ptn
    for t in text:
        if re.search(ptn,t,flags=re.I):
            print t
            continue


import urllib,urlparse
from bs4 import BeautifulSoup


def urldata(jurnobj):
    obj = urllib.quote(jurnobj.encode('utf8'))
    return 'http://epub.cnki.net/kns/oldnavi/n_list.aspx?NaviID=1&Field=cykm$%%22{0}%22&Value='+obj+'&selectIndex=0&NaviLink='+obj+'&ListSearchFlag=1&Flg=&DisplayMode=%E8%AF%A6%E7%BB%86%E6%96%B9%E5%BC%8F'


print urllib.unquote('%E5%8A%A8%E7%89%A9%E5%AD%A6%E6%8A%A5')
print urllib.unquote('%E8%AF%A6%E7%BB%86%E6%96%B9%E5%BC%8F')


urlparse.urlparse('http://epub.cnki.net/kns/oldnavi/n_list.aspx?NaviID=1&Field=cykm$%%22{0}%22&Value=%E5%8A%A8%E7%89%A9%E5%AD%A6%E6%8A%A5&selectIndex=0&NaviLink=%E6%A3%80%E7%B4%A2%3a%E5%8A%A8%E7%89%A9%E5%AD%A6%E6%8A%A5&ListSearchFlag=1&Flg=&DisplayMode=%E8%AF%A6%E7%BB%86%E6%96%B9%E5%BC%8F')


link = urldata(u'动物学报')
html_doc = urllib.urlopen(link)
soup = BeautifulSoup(html_doc)


soup.findAll('p',text=re.compile(u'中文名称'))

