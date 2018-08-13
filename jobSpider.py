from urllib import request,error
import re
import threading
from tkinter import *
import tkinter.messagebox

count=0
def run_spider(cin):
    header=('User-Agent',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')
    opener=request.build_opener()
    opener.addheaders=[header]
    request.install_opener(opener)
    f=open('和%s有关的职位.docx'%cin,'a')
    allurls=['https://www.nowcoder.com/recommend-intern/167?jobId=%s'%i for i in range(1700,1801)]

    def reaminHanzi(x):
        s=re.sub('<(.*?)>','',x)
        s=re.sub('&nbsp','',s)
        return s

    class threadOne(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
        def run(self):
            for i in range(1,len(allurls),2):
                try:
                    pattern_name = '<h2>(.+?)</h2>'
                    # pattern_company='<h3 class="teacher-name">(.+?)</h3>'
                    pattern_require='<dt>岗位要求</dt>(.+?)</dl>'
                    res = request.urlopen(allurls[i], timeout=2).read().decode('utf-8')
                    job_name = re.compile(pattern_name).findall(res)
                    # company_name=re.compile(pattern_company).findall(res)
                    job_require=re.compile(pattern_require,flags=re.S).findall(res)
                    # print(job_require[0])
                    if re.findall(cin, job_require[0], flags=re.I) and not re.findall('硕士', job_require[0], flags=re.I):
                        print('%s位置爬取成功！'%i)
                        # print(company_name)
                        require=reaminHanzi(job_require[0])
                        f.write(job_name[0] + '\n' + allurls[i] + '\n' +require+'\n'+'--------------------------' + '\n')
                    global count
                    count+=i
                    if count==2500:
                        tkinter.messagebox.showinfo(title='提示',message='爬取完毕！')

                except error.URLError as e:
                    print('爬取失败！')
                    if hasattr(e, 'code'):
                        print(e.code)
                    if hasattr(e, 'reason'):
                        print(e.reason)
    class threadTwo(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
        def run(self):
            for i in range(0,len(allurls),2):
                try:
                    pattern_name = '<h2>(.+?)</h2>'
                    # pattern_company='<h3 class="teacher-name">(.+?)</h3>'
                    pattern_require = '<dt>岗位要求</dt>(.+?)</dl>'
                    res = request.urlopen(allurls[i], timeout=2).read().decode('utf-8')
                    job_name = re.compile(pattern_name).findall(res)
                    # company_name=re.compile(pattern_company).findall(res)
                    job_require = re.compile(pattern_require, flags=re.S).findall(res)
                    # print(job_require[0])
                    if re.findall(cin, job_require[0], flags=re.I) and not re.findall('硕士', job_require[0], flags=re.I):
                        print('%s位置爬取成功！' % i)
                        # print(company_name)
                        require = reaminHanzi(job_require[0])
                        f.write(
                            job_name[0] + '\n' + allurls[i] + '\n' + require + '\n' + '--------------------------' + '\n')

                except error.URLError as e:
                    print('爬取失败！')
                    if hasattr(e, 'code'):
                        print(e.code)
                    if hasattr(e, 'reason'):
                        print(e.reason)

    one=threadOne()
    two=threadTwo()
    one.start()
    two.start()
    # if not one.is_alive() and not two.is_alive():
    #     tkinter.messagebox.showinfo(title='提示',message='爬取完成')

tk=Tk()
tk.title('求职通')
e=Entry(tk)
b=Button(tk,text='搜索',command=lambda :run_spider(cin=e.get()))
b.pack(side=RIGHT)
e.pack(side=LEFT)
tk.mainloop()
