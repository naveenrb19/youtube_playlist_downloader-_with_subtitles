import selenium
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import urllib3
import re
from re import search
import time
import yaml
import os
from os import system,name
from pytube import YouTube
import numpy as np
import pandas as pd
import threading
from IPython.display import display
def clear():
  
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
options1 = webdriver.ChromeOptions()
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'
options1.add_argument('user-agent={0}'.format(user_agent))
options1.add_argument("--headless")
options1.add_argument("--start-maximized")
options1.add_argument("--window-size=1920,1080")
path=input('Enter video path(a new folder will be created, provide root path) Format:E:\Data\ : ')
purl=input('Enter playlist url: ')
while True:
        try:
            q=int(input('Enter video quality(number only): 144/240/360/480/720/1080/1440'))
            if q in [144,240,360,480,720,1080,1440,2160]:
                break
            else:
                print('Choose right quality')
        except:
            print('Enter numerical only')
driver=webdriver.Chrome(ChromeDriverManager().install())
driver.get(purl)
driver.implicitly_wait(5)
links=driver.find_elements_by_xpath('//div[@id="container"][@class="style-scope ytd-playlist-video-renderer"]/ytd-thumbnail/a')
li=[e.get_attribute('href') for e in links]
playlist=driver.find_element_by_xpath('//h1[@class="style-scope ytd-playlist-sidebar-primary-info-renderer"]').text
channel=driver.find_element_by_xpath('//div[@class="style-scope ytd-video-owner-renderer"]/ytd-channel-name/div/div/yt-formatted-string/a').text
folder=str(playlist+'-'+channel)
folder=re.sub('[^a-zA-Z0-9_-]', ' ',folder)
vid_path=path+folder
is_dir=isdir = os.path.isdir(vid_path)
if is_dir:
    print('Directory exists')
else:
    os.makedirs('{}\{}'.format(path,folder))
    print('Directory created')
print('Number of videos: {}'.format(len(li)))
print('Saving in: {}'.format(vid_path))
driver.quit()
def video(link,vid_path,q):
    os.chdir(vid_path)
#     quality=int(input('18: 360p/mp4 | 22: 720p/mp4 | 37: 1080p/mp4'))
    
    video=YouTube(link)
    video_streams = video.streams.filter(file_extension='mp4')
    a=[]
    a.clear()
    a=[]
    a.clear()
    for stream in video_streams:
        tag=stream.itag
        qual=stream.resolution
        try:
            qual=int(qual.replace('p',''))
        except:
            pass
        ty=stream.type
        aud=stream.includes_audio_track
        if aud and ty=='video':
            a.extend([[tag,qual]])
    x=np.array(a)
    x=np.sort(x,axis=1)
    
    idx=np.where(x==q)
    idx=idx[0]
    si=idx.size
    if si!=0:
        idx=int(idx)
        tag=x[idx][0]
        video_streams = video.streams.filter(file_extension='mp4').get_by_itag(tag)
        print(tag)
    elif q>int(max(x[:,1])):
            tag=x[-1,0]
            video_streams = video.streams.filter(file_extension='mp4').get_by_itag(tag)
            print(tag)
    elif q<int(min(x[:,1])):
            tag=x[0,0]
            video_streams = video.streams.filter(file_extension='mp4').get_by_itag(tag)
            print(tag)
            
        
    video_name=re.sub('[^a-zA-Z0-9]', ' ',video_streams.title)+'.mp4'
    print(video_name)
    video_streams.download(filename = video_name)
    print(f'Completed: {link}')

def subtitles(li,vid_path,p):
    missed=[]
    missed.clear()
    avail=str()
    d=dict()
    x=p
    try:
        os.chdir(vid_path)
    except:
        print('Directory error....always enter path ending with "\"')
    driver=webdriver.Chrome(ChromeDriverManager().install(),options=options1)
    driver.get('https://www.keepvid.to/1')
    search=driver.find_element_by_xpath('//div[@class="input-group"]/input')
    time.sleep(3)
    go=driver.find_element_by_xpath('//div[@class="input-group-append"]/button')
    time.sleep(3)
    search.clear()
    time.sleep(3)
    for j in range(len(li)):
        search.clear()
        time.sleep(3)
        search.send_keys(li[0])
        time.sleep(3)
        go.click()
        time.sleep(6)
        
        soup = BeautifulSoup(driver.page_source,"html5lib")
        subs=soup.find_all("div", {"class": "col-lg-6"})
        n=subs[1].find_all("strong")
        try:
            avail=str(n[0].text)
        except:
            print('empty')
        print(len(n))
        for i in range (len(n)):
            d[f'{i}']=n[i].text
        rows=0
        fr=np.empty([len(n),1], dtype=object)
        try:
            for i in range (len(n)):

                text=str(i)+':'+n[i].text+' '
                fr[i]=text
        except:
            pass
        r=len(n)%5
        print(r)
        try:
            for i in range(5-r):
                fr=np.append(fr,0)
                rows=int(len(fr)/5)
                fr=np.reshape(fr,(rows,5))

                df=pd.DataFrame(fr)
        except:
            pass
#         

        if bool(d)==True:
            if len(n)>1:

                    display(df)
                    if x==0:
                        lan=input('Enter number')
                        x=2
                    else:
                        pass
                    clear()
                #     if d[f'{lan}']==n[i].text:

                #             subl=driver.find_element_by_xpath(f'//div[@class="col-lg-6"][2]/table/tbody/tr[{i}]/td[3]/a')
                #             hre=subl.get_attribute('href')
                #             print(subl)
                #             subl.click()
                #             break


                    try:


                        video=YouTube(li[j])

                        vid=str(video.title)
                        subname=re.sub('[^a-zA-Z0-9]', ' ',vid)+'.srt'


                        time.sleep(8)

                        for i in range(0,len(n)):
                            if d[f'{lan}']==n[i].text:

                                subl=driver.find_element_by_xpath(f'//div[@class="downloadOptions"]/h6[2]/div/div[2]/table/tbody/tr[{i+1}]/td[3]/a')
                                hre=subl.get_attribute('href')
    #                             print(hre)
                                with requests.get(hre, stream=True) as r:
                                    r.raise_for_status()

                                    with open(subname, 'wb') as f:
                                        for chunk in r.iter_content(chunk_size=8192): 
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    #if chunk: 
                                            f.write(chunk)


                                break
                        print(f'Downloaded subtitle for: {li[j]}')
                         

                    except:
                        print(f'Missed or subtitle unavailable: {li[j]}')
                        missed.append(li[j])

            else:
                print(f'No subtitle available for: {li[j]}')
        else:
            print('Error occured when trying to download subtitle...Retrying')
            missed.append(li[j])
       
    print(len(missed))
    return missed,x
    driver.quit()

p=0
for x in range(0, len(li)):
    globals()['t%s' % x] =threading.Thread(target=video, args=(li[x],vid_path,q))
    globals()['t%s' % x].start()
clear()
mi,k=subtitles(li,vid_path,0)
while len(mi)>1:
    print('Retrying for missed subtitles')
    if p<10:
        mi=subtitles(mi,vid_path,k)
        p=p+1
for x in range(0, len(li)):
    globals()['t%s' % x].join()

