import streamlit as st
import os, sys
from pytube import YouTube

@st.cache_resource
def installff():
  os.system('sbase install geckodriver')

_ = installff()
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from pytube import YouTube
from moviepy.editor import *
import sys
import os
import re
import shutil
import time

# opts = FirefoxOptions()
# opts.add_argument("--headless")
# browser = webdriver.Firefox(options=opts)

# browser.get('https://www.youtube.com/results?search_query=')

# listings=browser.find_elements('xpath','//a[@id="thumbnail"]')
# links = []
# for l in listings:
#     links.append(l.get_attribute("href"))
# st.write('Links aquired')
# st.write(len(links))
# link = links[2]
# st.write(link)

# yt = YouTube(link)
# st.write('Object created')

def download_files(singerName,n) :
    st.write('inside download files')
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    browser = webdriver.Firefox(options=opts)

    print('opening browser')

    browser.get('https://www.youtube.com/results?search_query='+singerName)

    time.sleep(10)

    listings=browser.find_elements('xpath','//a[@id="thumbnail"]')
    links = []
    for l in listings:
        links.append(l.get_attribute("href"))
    
    i = 0
    st.write('middle of download files')
    st.write(links)
    # st.write('Currently downloading ...')
    for link in links :
        st.write(i)
        if n==0 :
            break
        if link == None :
            continue
        try :
            yt = YouTube(link)
            st.write(yt.length)  ## remove later
            if(yt.length >= 120 and yt.length <= 360) :
                yt.streams.get_audio_only().download(filename='audio'+str(i)+'.mp3')
                n -= 1
                i += 1
                data.write('Currently downloading.... ' + yt.title)
        except :
            print('internal error')

def audio_merge(n,y) :
    st.write('inside audio merge')
    final_audio = AudioFileClip(r'audio1.mp3')
    final_audio = final_audio.cutout(0,y)
    data.write('Creating your mashup .... ')
    for i in range(1,n) :
        audiofile = AudioFileClip(r'audio' + str(i) + '.mp3')
        audiofile = audiofile.cutout(0,y)
        final_audio = concatenate_audioclips([final_audio,audiofile])

    final_audio.write_audiofile('output'+'.mp3')

    for i in range(n) :
        os.remove('audio'+str(i)+'.mp3')
    data.empty()

    archive = shutil.make_archive('send.mp3','zip','output.mp3')

    st.info('process completed')

st.title('Mashup')

st.write('Enter name of your favourite singer, number of songs, amount of song to trim and you will reveive a mashup through your email')

with st.form('input') :
    singername = st.text_input('Enter singer name')

    numSongs = st.text_input('Enter number of songs')

    time = st.text_input('Enter time')

    email = st.text_input('Enter your email')

    submit_button = st.form_submit_button(label='Submit')

data = st.empty()

if submit_button :
    if singername != '' and numSongs != '' and time != '' and email != '' :
        regex = '[A-Za-z0-9_]*@[A-Za-z]*\.[A-Za-z]*'
        match = re.findall(regex,email)
        if match[0] != email :
            st.write(match)
            st.error('Wrong email')
        else :
            st.write('inside submit button')
            download_files(singername,int(numSongs))
            st.write('after download_files')
            audio_merge(int(numSongs),int(time))
            st.write('after audio merge')
    else :
        st.error('Please enter data in all fields')


