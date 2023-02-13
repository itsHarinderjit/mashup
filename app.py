import streamlit as st
import streamlit.components.v1 as components
import os
from pytube import YouTube

@st.cache_resource
def installff():
  os.system('sbase install geckodriver')

_ = installff()
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from pytube import YouTube
from moviepy.editor import *
import os
import re
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from zipfile import ZipFile
from zipfile import ZIP_BZIP2

def download_files(singerName,n) :
    check = n
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    browser = webdriver.Firefox(options=opts)

    print('opening browser')

    browser.get('https://www.youtube.com/results?search_query='+singerName)

    data.write('Fetching your songs....')
    time.sleep(15)
    check -= 20
    scroll = 0
    while check > 0 :
        browser.execute_script('window.scrollTo({}, {})'.format(8080*scroll,8080*(scroll+1)))
        time.sleep(15)
        check -= 20
        scroll += 1

    listings=browser.find_elements('xpath','//a[@id="thumbnail"]')
    links = []
    for l in listings:
        links.append(l.get_attribute("href"))
    
    i = 0
    for link in links :
        if n==0 :
            break
        if link == None :
            continue
        try :
            yt = YouTube(link)
            if(yt.length >= 120 and yt.length <= 360) :
                yt.streams.get_audio_only().download(filename='audio'+str(i)+'.mp3')
                n -= 1
                i += 1
                data.write('Currently downloading.... ' + yt.title)
        except :
            print('internal error')

def audio_merge(n,y) :
    data.write('Creating your mashup....')
    audio_list = []
    for i in range(n) :
        audio = AudioFileClip(r'audio'+str(i)+'.mp3')
        audio = audio.subclip(0,y)
        audio_list.append(audio)
    final_audio = concatenate_audioclips(audio_list)
    final_audio.write_audiofile('output.mp3')
    for lst in audio_list :
        lst.close()

    ## deleting audio files
    for i in range(n) :
        os.remove('audio'+str(i)+'.mp3')

    ## creating zip file
    with ZipFile(f'zipfile.zip','w',compression= ZIP_BZIP2 , allowZip64=True, compresslevel=9) as zip:
        zip.write('output.mp3')

    os.remove('output.mp3')
    data.empty()

def send_email(mailid) :
    data.write('Sending email....')
    fromaddr = "hsingh91218@gmail.com"
    toaddr = mailid
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Mashup"
    body = "Enjoy your mashup :) "
    msg.attach(MIMEText(body, 'plain'))
    attachment = open('zipfile.zip', "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
  
    encoders.encode_base64(p)
   
    p.add_header('Content-Disposition', "attachment; filename= %s" % "mashup.zip")
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(fromaddr, 'pgdyzgfabqypxctb')
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

    data.empty()
    st.info('process completed')

components.html(
    """
    <style>
        * {
            margin : 0px;
        }
        div {
            color : white;
            font-size : 8em;
            text-align : center;
            font-family: Arial, Helvetica, sans-serif;
            # font-weight : bold;
        }
    </style>
    <div>
        Mashup
    </div>
    """,
    height=150,
    width=600
)

st.write('Enter name of your favourite singer, number of songs, amount of song to trim and you will reveive a mashup through your email')

with st.form('input') :
    singername = st.text_input('Enter singer name')

    numSongs = st.text_input('Enter number of songs')

    y = st.text_input('Enter length of each song')

    email = st.text_input('Enter your email')

    submit_button = st.form_submit_button(label='Submit')

data = st.empty()

if submit_button :
    if singername != '' and numSongs != '' and y != '' and email != '' :
        singername = singername.split()[0]
        numSongs = numSongs.split()[0]
        y = y.split()[0]
        email = email.split()[0]
        regex = '[A-Za-z0-9_.]*@[A-Za-z]*\.[A-Za-z]*'
        match = re.findall(regex,email)
        if match[0] != email :
            st.error('Wrong email')
        else :
            try :
                download_files(singername,int(numSongs))
                audio_merge(int(numSongs),int(y))
            except :
                st.error('Wrong data in number of songs or length of each song')
            send_email(email)
    else :
        st.error('Please enter data in all fields')


