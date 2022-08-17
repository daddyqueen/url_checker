# Command line URL checker

This program will test a url or group of urls and return its connection status or response code. There are additional options that allow the user to scrape url information from the page, as well as the ability to perform the checks synchronously or asynchronously, and output errors to a file.

## Installation

1. Create a Python virtual environment

```sh
$ python3 -m venv ./venv
$ source venv/bin/activate
(venv) $
```

2. Install the requirements

```
(venv) $ python3 -m pip install -r requirements.txt
```

## Options

This url checker has the following options:

* `-u` or `--urls` input one or more URLs and checks if they're online. (will add prefix http:// to url if missing from input)
* `-f` or `--input-file` input a file containing a list of URLs to check.
* `-a` or `--asynchronous` runs the check asynchronously. (Do not use this option with -r or -s, those options will still run syncronously to avoid time out issues)
* `-s` or `--scrape` scrapes all url data from input url(s) (only runs synchronously)
* `-r` or `--request` requests status code of all urls (only runs synchronously)
* `-o` or `--output-file` outputs & appends to text file for all url errors that occur during program execution (default name is 'urlcheck_errors.txt')

## Sample Usage & Output

```sh
(venv) % python3 -m urlcheck -u github.com      
🟢 Online ~~ "http://github.com/"

(venv) % python3 -m urlcheck -u bad-url.com  
❌ Unavailable
	Error: "[Errno 8] nodename nor servname provided, or not known" "http://bad-url.com/"

(venv) % python3 -m urlcheck -u https://books.toscrape.com/ -s
🟢 Online ~~ "https://books.toscrape.com/index.html"
🟢 Online ~~ "https://books.toscrape.com/catalogue/category/books_1/index.html"
🟢 Online ~~ "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
...

(venv) % python3 -m urlcheck -u https://books.toscrape.com/ -r
🟢 Status 200 ~~ "https://books.toscrape.com/"

(venv) % python3 -m urlcheck -u github.com daddyqueen.com -r
🟢 Status 200 ~~ "http://github.com/"
❌ Unavailable 
	Error: "404" "http://daddyqueen.com/"
	
(venv) % python3 -m urlcheck -f sample_links.txt -a           
❌ Unavailable
	Error: "Cannot connect to host superbadurl.com-help.u:80 ssl:default [nodename nor servname provided, or not known]" "http://superbadurl.com-help.u/"
🟢 Online ~~ "http://target.com/"
🟢 Online ~~ "http://python.org/"
🟢 Online ~~ "http://github.com/"
🟢 Online ~~ "http://githug.com/"
🟢 Online ~~ "http://jup.ag/"

(venv) % python3 -m urlcheck -u jup.ag -s -r       
🟢 Status 200 ~~ "http://jup.ag/"
🟢 Status 200 ~~ "http://jup.ag/"
🟢 Status 200 ~~ "http://jup.ag/infra"
🟢 Status 200 ~~ "https://docs.jup.ag/"
🟢 Status 200 ~~ "http://jup.ag/stats"
🟢 Status 200 ~~ "http://jup.ag/infra"
```



## Inspiration

This project idea originally came from https://realpython.com/site-connectivity-checker-python/.

Added additional functionality for scraping, making requests, and documenting errors.