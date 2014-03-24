# -*- coding: utf-8 -*-
import re
class PaperAnsys(object):
    def __init__(self,obj,ref,lib):
        self.obj = obj #查询目标
        self.ref = ref #所有引用
        self.lib = lib #作者提供
    #转换输入格式
    def fread(self,f):
        result = list()
        for line in open(f).readlines():            #依次读取每行
            line = line.strip()                      #去掉每行头尾空白
            if not len(line):                        #判断是否是空行
                continue                             #是的话，跳过不处理
            result.append(line)  
        return result
    def libread(self):
        return self.fread(self.lib)
    def objread(self):
        return self.fread(self.obj)
    def refread(self):
        f = self.fread(self.ref)
        # 筛选出Obj
        objtemp = [f[idx-1] for idx,li in enumerate(f) if li.startswith('Record 1 of')]
        obj = map(lambda s : ' '.join(s.split()[:-1]) if '/' in s.split()[-1] else s.strip(), objtemp)
        with open('refobj.txt','w') as fobj:
            for idx,li in enumerate(obj):
                fobj.write(li + '\n') #生成被引论文列表
                print idx+1,li
        # 筛选Record|Title:|Author\(s\):|Source:|ISSN:|ISBN:
        contents = []
        ptn = r'^(Record|Title:|Author\(s\):|Source:|ISSN:|ISBN:)'
        for li in f:
            if re.search(ptn,li):
                contents.append(li.strip())
        
        #ref存储
        refdic = {}
        idx = 0
        for ref in contents:
            if ref.startswith('Record 1 of'):
                refkey =  '%s. %s' % (str(idx+1), obj[idx])
                refdic[refkey] = [ref]
                idx += 1
            else:
                refdic[refkey].append(ref)
        return refdic

def main():
    obj = 'obj.txt'
    ref = 'ref.txt'
    lib = 'lib.txt'
    pansys = PaperAnsys(obj,ref,lib)
    # 输出
    fref = pansys.refread()
    with open('refclear.txt','w') as f:
        for k,v in sorted(fref.iteritems(),key=lambda (k,v): int(k.split('.')[0]),reverse=False):
            f.write(k + '\n')
            for li in v:
                f.write(li + '\n')
    for k,v in fref.items():
        fname = '%s.txt' % str(k)
        with open(fname,'w') as f:
            for idx,author in enumerate(v):
                if author.startswith('Author(s):'):
                    f.write(author[11:] + '\n')

if __name__ == '__main__':
    main()