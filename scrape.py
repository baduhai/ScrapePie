#!/usr/bin/env python3

import time # Needed for sleep function
import mechanize # Needed for browser functionality
import http.cookiejar # Needed to save session cookies
import ssl # Needed to managed ssl
import html2text # Needed to parse html into something readable
import subprocess # Interact with system commands

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
br.set_header = [('User-Agent', '<put a sane user-agent here>')]

# View available forms (in order to know which form index to select)
#for f in br.forms():
#    print(f)

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
    br.open('login page address')
    # Select the index form for login
    br.select_form(nr=0)
    # User credentials
    br.form['email'] = '<example@email.com>' # This field may be named differently depending on website
    br.form['pass'] = '<password>' # This field may be named differently depending on website
    # There may be a third field for authentication token that you have to find manually
    # Login
    br.submit()

# Main function 
def check():
    # What are we reading?
    content = str(br.open('page address for where info will be').read())
    parsedContent = str(html2text.html2text(content))
    conca = parsedContent.splitlines()[77] + parsedContent.splitlines()[78] # Specific lines where you'll find changes
    return conca    

login() # Log ins only once, as session cookies are saved
i = 0
while True:
    if len(check()) != 101: # Number of characters the relevant line of data has when there are no changes
        subprocess.run(['telegram-send', 'Data changed! ']) # Send message via telegram (telegram-send must be installed and configured!)
        break
    else:
        i += 1
        print('Number of attempts: ' + str(i)) # Prints how many times it's attempted to find new info.
        time.sleep(5) # Delay unti trying again
