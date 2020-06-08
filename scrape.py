#!/usr/bin/env python3

import time # Needed for sleep function
import vlc # Play lound sounds
import mechanize # Needed for browser functionality
import http.cookiejar # Needed to save session cookies
import ssl # Needed to managed ssl
import html2text # Needed to parse html into something readable
import subprocess # Interact with system commands
from urllib.error import URLError, HTTPError # Error handling

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = http.cookiejar.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.set_header = [('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0')]

# Sound file location
p = vlc.MediaPlayer('file:///home/william/Music/Sounds/siren.mp3')

# May be useful if going through web browser's developer tools is too difficult for any reason.
# View available forms (in order to know which form index to select)
#for f in br.forms():
#    print(f)

# Misc stuff
j = 0
h = 0

def login():
    # Disable ssl cause I don't know how to set it up
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context
    # Session handling for website
    br.open('https://ec-lisboa.itamaraty.gov.br/login')
    # Select the index form for login
    br.select_form(nr=0)
    # User credentials
    # Form fileds may be named differently depending on website
    br.form['email'] = ''
    br.form['pass'] = ''
    # There may be a third form field that you need to send, it is usually invisible to the user, use your web browser's dev tools to find what it's called and what to fill in the field before submitting
    # Login
    br.submit()

def check():
    try:
        # What are we reading?
        content = str(br.open('https://ec-lisboa.itamaraty.gov.br/availability').read())
        parsedContent = str(html2text.html2text(content))
        noBreaksParsedContent = parsedContent.replace("\n", "")
        return noBreaksParsedContent
    # Adding the two following error exceptions fixes(hopefully) any problems that may arrise due to connectivity, be it server-side or client-side.
    except HTTPError as e:
        print('Server couldn\'t fulfill request.')
        print('Reason: ', e.reason, '. Restarting')
        main()
    except URLError as e:
        print('Failed to reach server.')
        print('Reason: ', e.reason, '. Restarting')
        main()

# Main function 
def main():
    global j
    global h
    i = 0
    login() # Seldom logs in, as session cookies are saved
    while h <= 10:
        toCheck = check()
        if toCheck.find("Passaporte para homens (entre 18 e 45 anos) - solteiro| Indi") < 0:
            h += 1
            print('Horário disponível!!!')
            subprocess.run(['telegram-send', 'Horário disponível, corre!'])
            break
        else:
            j += 1
            i += 1
            print('Number of attempts: ' + str(j))
            time.sleep(5)
            if i >= 400: # value may need to be changed, monitor the script to see what value makes sense.
                main()
    p.play()
    time.sleep(7)

main()


