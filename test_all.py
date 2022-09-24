from flask import Flask, request
import smtplib
import requests, json, os
from youtube_uploader_selenium import YouTubeUploader
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv('.env')

GMAIL_LOGIN=os.getenv('GMAIL_LOGIN') 
GMAIL_PASS=os.getenv('GMAIL_PASS')
GMAIL_USER_EMAIL = '' # email to which to send
video_path = '../output.mp4'
metadata_path = 'meta.json'


@app.route("/")
def hello_world():
    return "<p>This is just an example!</p>"

@app.route("/api/v1/upload")
def upload_youtube():

    uploader = YouTubeUploader(video_path, metadata_path)
    was_video_uploaded, video_id = uploader.upload()
    assert was_video_uploaded

    smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_object.ehlo()
    smtp_object.starttls()
    smtp_object.login(GMAIL_LOGIN, GMAIL_PASS)
    smtp_object.sendmail(GMAIL_LOGIN, 
                        GMAIL_USER_EMAIL, 
                        f'Subject:GG\nwww.youtube.com/watch?v={video_id}')
    smtp_object.quit()
    
    return "<p>This is just an example!</p>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4050)
