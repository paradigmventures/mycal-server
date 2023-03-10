## Integrated Dev Environment Setup

Assumes Mac/Linux environment, adjust commands for Windows if needed.

### Project domain

Pick a local domain to host from (I use `my-cal.local` in this example).

### Project folder

I use a folder convention where the project root folder is named as the domain, and code repos are contained within.  Example:
```
project root: /PATH/TO/my-cal.local/
mycal-server: /PATH/TO/my-cal.local/mycal-server
mycal-client: /PATH/TO/my-cal.local/mycal-client
```

### Local dns entry

Edit hosts:
```
$ vim /etc/hosts
```

Add the following line

```
127.0.0.1       my-cal.local
```

### Setup nginx

Nginx is used to combine both projects on a single domain, and uses a location alias for the client dist assets so they're available where the client project assumes they'll be.

My nginx config folder is located in `/usr/local/etc/nginx/` and contains a subfolder called `servers/` for additional virtualhost config files.

Within `/usr/local/etc/nginx/servers/` I create a file called `my-cal.local`

Contents of the file are:
```
server {
        listen       80;
        server_name  my-cal.local;

        location /assets/ {
                alias /PATH/TO/my-cal.local/mycal-client/dist/assets/;
        }

        location / {
                proxy_pass              http://127.0.0.1:8000;
                proxy_set_header        Host            $host;
                proxy_set_header        X-Real-IP       $remote_addr;
        }
}
```

NOTE: the `mycal-server` python/django dev server will be running on port 8000

To reload nginx configs:
```
$ sudo nginx -s reload
```

### Setup mysql db

In the examples below, substitute out `MYSQL-DB-HERE`, `MYSQL-USER-HERE`, and `MYSQL-PASSWORD-HERE` for real values.

Create a database: 
```
mysql> CREATE DATABASE `MYSQL-DB-HERE`;
```

Create a user and set password:
```
mysql> CREATE USER `MYSQL-USER-HERE`@`%` IDENTIFIED BY 'MYSQL-PASSWORD-HERE';
```

Assign privileges to the user:
```
mysql> GRANT ALL PRIVILEGES ON `MYSQL-DB-HERE`.* TO `MYSQL-USER-HERE`@`%`;
```

If needed, specify encoding for database (prior to populating data):
```
mysql> ALTER DATABASE `MYSQL-DB-HERE` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

NOTES:
- use backticks to enclose db & user strings, and single quotes to enclose password string.
- mysql password policy requires special characters in pw, not just alphanumeric characters.

### Setup python virtualenv

To create a new python3 virtualenv:
```
$ cd /PATH/TO/my-cal.local
$ python3 -m venv env3
```

To activate the virtualenv (from `/PATH/TO/my-cal.local`):
```
$ source env3/bin/activate
```

With the virtualenv activated, the command line then looks like:
```
(env3) $
```

### Setup mycal-server project

```
(env3) $ cd /PATH/TO/my-cal.local
(env3) $ git clone https://github.com/paradigmventures/mycal-server.git
(env3) $ cd mycal-server
(env3) $ pip install -r requirements.txt
```

NOTE: if you run into an error building the `mysqlclient` package from `requirements.txt`, it is because `mysql` isn't in the available PATH.  Run this command below, then run the `pip install` command again:

```
(env3) $ export PATH=$PATH:/usr/local/mysql/bin
```

### Configure your local django settings file

Within the `mycal-server` project (located at `/PATH/TO/my-cal.local/mycal-server`) is another folder called `mycal/` which contains a `settings.py` file. The `settings.py` file will import additional settings from a `settings_local.py` file within the same folder, which does not exist locally yet.

Within the `mycal/` directory, create a `settings_local.py` with the following settings:

```
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-SECRETKEYSECRETKEYSECRETKEYSECRETKEY'

DEBUG = True

# NOTE: my-cal.local for accessing the server behind nginx (with client dist assets integration), 
#       127.0.0.1 for accessing the server directly

ALLOWED_HOSTS = [
    'my-cal.local',
    '127.0.0.1',
]

# NOTE: '/PATH/TO/my-cal.local/mycal-server/static/dist' is so that 'index.html' can be recognized as a template at /app

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            '/PATH/TO/my-cal.local/mycal-server/static/dist',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# NOTE: substitute MYSQL-DB-HERE, MYSQL-USER-HERE, and MYSQL-PASSWORD-HERE values below

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'MYSQL-DB-HERE',
        'USER': 'MYSQL-USER-HERE',
        'PASSWORD': 'MYSQL-PASSWORD-HERE',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    },
}

### Static files ###

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / "static"

# NOTE: this setting will enable copying dist files from '/PATH/TO/my-cal.local/mycal-client/dist' to '/PATH/TO/my-cal.local/mycal-server/static/dist'
#       the actual command to copy static files is:
#       $ ./manage.py collectstatic --no-input

STATICFILES_DIRS = [
    ('dist', '/PATH/TO/my-cal.local/mycal-client/dist'),
]


# NOTE: this loosens cookie transport security, so that cookie data can be sent over http (which dev server runs)

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False


# NOTE: 'IsAuthenticatedOrReadOnly' loosens the data access permissions, 
#       so that mysql-client running on localhost:5173 can do GETs and populate calendar without user auth
#       (POSTs, PUTs, and DELETEs still require user auth, which is available when served from 'my-cal.local')

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ]
}


# NOTE: this sets CORS headers, allowing these domains to use javascript to access API data from a different domain

CORS_ALLOWED_ORIGINS = [
    "http://my-cal.local",
    "http://localhost:5173",
]
```

Lines starting with `# NOTE:` are comments describing the various settings.

**Make sure to replace the various `/PATH/TO/` placeholders with real path info, as well as with real mysql credentials.**

### Populate mysql database with tables
```
(env3) $ cd /PATH/TO/my-cal.local/mycal-server
(env3) $ ./manage.py migrate
```

### Create django admin user
```
(env3) $ ./manage.py createsuperuser
```

### Run dev server
```
(env3) $ ./manage.py runserver
```

### Setup mycal-client project

```
$ cd /PATH/TO/my-cal.local
$ git clone https://github.com/paradigmventures/mycal-client.git
$ cd mycal-client
$ npm install
```

Or, wherever your original `mycal-client` project location is, make sure to set `STATICFILES_DIRS` in `settings_local.py` to that directory.  So that the dist files can be copied over from the `mycal-client` project into the `mycal-server` project `static/` folder for hosting.

Create a file named `.env.local` with the following line (or update original `.env.local` with the new local django server):
```
VITE_API_DOMAIN=http://my-cal.local
```

Then to create build files:
```
$ npm run build
```

### Copy dist assets from client to server

```
(env3) $ cd /PATH/TO/my-cal.local/mycal-server
(env3) $ ./manage.py collectstatic --no-input
```

### Test the hosting

With the django server running (`$ ./manage.py runserver`), you should be able to open a browser and go to http://my-cal.local, where you should see a log in screen.  Use the credentials created for the django admin user.  Once logged in, you should be directed to the calendar app.

To help manage calendar and event data (when the client-side code isn't working), the django admin panel is available at: 
- http://my-cal.local/djadmin

### Process to build, integrate, and serve client files

To review the iterative process of syncing files between client and server projects.

Create `mycal-client` build files: 
```
$ cd /PATH/TO/my-cal.local/mycal-client
$ npm run build
```

Copy build files to `mycal-server` project:
```
(env3) $ cd /PATH/TO/my-cal.local/mycal-server
(env3) $ ./manage.py collectstatic --no-input
```

Cancel and re-run the dev server to serve up new files:
```
(env3) $ ./manage.py runserver
```

Also, accessing the client project directly from `http://localhost:5173` should be fine for quick development styling the UI with Vue hot reloading, but for code changes that involve data access/changes between client and server, the above process is required.