import requests
r = requests.get('https://github.com/eojo459/404-course-not-found/blob/master/lab01/script.py')
open('script_downloaded.py', 'wb').write(r.content)