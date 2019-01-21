#!/usr/bin python
#-*-coding:utf-8 -*-
from bs4 import BeautifulSoup
import time
import re
import os
import requests
lyst_job=[]
dictJob={}
lystUrl=[]
class CountZeroError(Exception):
    def __init__(self,args):
        print args
def indexJob(job,pageNum):
    url="""https://www.zhipin.com/c101010100/y_6-e_106/?query={jobs}&period=5&ka=sel-scale-5&&page={num}""".format(jobs=job,num=pageNum)
    print url
    headers={
    "cookie": "",#fix-this line add cookie
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9"
}
    resp=requests.get(url,headers=headers)
    time.sleep(3)
    html=resp.content
    soup = BeautifulSoup(html,"html.parser")
    result = soup.find_all("div",class_="job-primary")
    if result:
        for singleJob in result:
            jobUrl = singleJob.find_all("a",class_="btn btn-startchat")[0]
            jobId = singleJob.find_all("h3",class_="name")[0].a["data-jobid"]
            dictJob[jobId]=jobUrl
    else:
        lystJobId = open("history_url","rb").readlines()
        for jobId_key,job_v in dictJob.items():
            print (jobId_key+"\n" not in lystJobId)
            if jobId_key+"\n" not in lystJobId:
                newJobUrl=parseDiv(dictJob[jobId_key])
                respJson=requests.get(newJobUrl,headers=headers)
            lystUrl.append(jobId_key)
        with open("history_url","w") as f:
            for jobId in lystUrl:
                f.write(jobId+"\n")
        raise CountZeroError("result count zero")
def parseDiv(div):
    indexUrl = """https://www.zhipin.com"""
    jobUrl = indexUrl+div.get("data-url")
    return jobUrl   
if __name__ == "__main__":
    if not os.path.exists("history_url"):
        s=file("history_url","w")
    for m in range(1,10): 
        indexJob("测试开发",m) #---fix this line job way
