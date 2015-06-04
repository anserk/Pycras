# Pycras
Python scraper for Craigslist.

To start, update the file config.conf with your locations and categories.

Example of configuration file:

```python
	locations = ["losangeles", "newyork"]
	categories = ["eng", "sof", "sad", "tch", "web"]
```

The output is a very simple html file with the posts found. The name of the file is the timestamp of the time when you ran the program.

You need BeautifulSoup and python3.


