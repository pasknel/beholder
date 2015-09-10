# beholder
Pentest tool for OSINT in social networks

## Installation Steps

   1. Install python3 pip

      apt-get install python3-pip

   2. Install dependencies

      pip3 install -r requirements.txt

   3. Add API keys (settings.py)

      **Make sure you declare the 'REDIRECT URI' as "http://127.0.0.1:8000/finder" when creating the Instagram developer account !!**

      nano settings.py 

   4. Setup database (only before the first execution)

      python3.4 manage.py migrate

   5. Run web server

      python3.4 manage.py runserver 
