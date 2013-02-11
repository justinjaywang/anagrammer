#!/usr/bin/env python

import cgitb, string, math, random, cgi, urllib
cgitb.enable()

# header and footer
header = 'Content-Type: text/html\n\n'

htmlHeader = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Anagrammer</title>
  <meta name="description" content="See the crazy phrases that result from your input.">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black">
  <link rel="stylesheet" href="styles/style.css">
</head>
<body>
  <div class="container">"""

htmlFooter = """  </div>
</body>
</html>"""

# url
urlStart = 'http://anagramgenius.com/server.php?source_text='
urlParams = '&emphasis=1&gender=2&vulgar=1&seen=true'

# functions
def main():
  """
  Receive input, and print HTML
  """
  # print header
  print header + htmlHeader

  # define placeholder and anagram text
  form = cgi.FieldStorage()
  if 'q' not in form: # no input
    sourceTextLong = 'William Shakespeare'
    anagramHTMLString = '<p class="result">I am a weakish speller.</p>'
  else: # form input exists
    sourceTextLong = form['q'].value
    sourceText = sourceTextLong.replace(' ','').replace('&','')
    if len(sourceText) < 7:
      anagramHTMLString = '<p class="result error">Input too short, try again.</p>'
    elif len(sourceText) > 30:
      anagramHTMLString = '<p class="result error">Input too long, try again.</p>'
    else:
      anagramString = findAnagram(sourceText)
      if not anagramString: # findAnagram returned false
        anagramHTMLString = '<p class="result error">None found, try again.</p>'
      else:
        anagramHTMLString = '<p class="result">' + anagramString + '</p>'

  # print input and anagram
  print '<form action=""><input type="text" name="q" class="source" autofocus="autofocus" placeholder="' + sourceTextLong + '" maxlength="36"></form>'
  print anagramHTMLString

  # print footer
  print htmlFooter

def findAnagram(sourceText):
  """
  Reads form input. Calls parseHTML(url) for specific query, returns anagram or false.
  """
  url = urllib.urlopen(urlStart + sourceText + urlParams)
  anagram = parseHTML(url)
  return anagram

def parseHTML(url):
  """
  Parses HTML string returned by URL. Returns string of interest (anagram).
  """
  html = url.read()
  # read important part of HTML
  startStr = '<br>anagrams to<br><span class="black-18">'
  stopStr = '<'
  indexStart = isSubstringIn(startStr, html)
  if not indexStart:
    url.close()
    return False
  else:
    indexEnd = indexStart + len(startStr) # index to start reading
    i = indexEnd
    returnString = '' # instantiate empty returnString
    # keep adding to returnString until stopStr is found
    while html[i] != stopStr:
      returnString += html[i]
      i += 1
    anagram = returnString[1:-1] # get rid of quotes
    url.close()
    return anagram

def isSubstringIn(subString, str):
  """
  Checks whether substring is in string. Returns index if True, or False.
  """
  try:
    i = str.index(subString)
    return i
  except ValueError:
    return False
              
if __name__ == '__main__':
  main()