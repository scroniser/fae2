# Functional Accessibility Evaluator, version 2.0.0

Development is primarily supported by the [University of Illinois at Urbana-Champaign](http://illinois.edu).  The development is lead by [Accessible IT Group](http://disability.illinois.edu/academic-support/aitg) which is a unit of [Disability Resources and Educational Servcies](http://www.disability.illinois.edu) which is part fo the [College of Applied Health Sciences](http://www.ahs.illinois.edu).  Additional contributions for the [HTMLUnit](http://htmlunit.sourceforge.net/) based web site analysis engine are provided by [Administrative Information Technology Services (ATIS)](https://www.aits.uillinois.edu/) of University Administration.



## What is Functional Accessibility Evaluator (FAE)?
* FAE analyzes a website based on the requirements of the W3C Web Content Accessibility Guidelines 2.0 Single A and AA Success Criteria.
* Every rule used in FAE 2.0 references at primary WCAG 2.0 Success Criterion requirement it is based on.
* The rules support not only accessibility, but also usable web design for people with disabilities.
* The rules support accessible and usable design by enforcing the accessible coding practices and techniques of the Accessible Rich Internet Application (ARIA) 1.0 and W3C HTML5 specifications.  

## Apache 2.0 License
FAE may be used and distributed based on the terms and conditions of the [Apache License Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). 

## Server requirements for Linux

* Apache2 Web Server
* Python 2.7.x
* Java 1.8
* Python development package (`python-dev` in Debian/Ubuntu)
* postgresql-devel (`libpq-dev` in Debian/Ubuntu)
* `psycopg2` package for python to talk to postgres

### Python modules

Here is the [requirements.txt] file to use with pip

```
Django==1.9
django-password-reset==0.9
django-registration==2.0.4
django-timezone-field==1.3
psycopg2
future==0.15.2
Markdown==2.6.5
pytz==2015.7
requests==2.10.0
```

### Creating a <code>secrets.json</code> file

The "secretes.json" file must be created and provides:
* Security information for Django
* Information for Django to access and manage the database
* Information on on e-mail commmunications for registration and announcements.
* Place this file in the <code><em>[absolute path]</em>/fae2/fae2</code> directory

```
{
  "FILENAME": "secrets.json",
  "PROCESSING_THREADS": 4, 
  "SITE_URL": "[your site URL]",
  "SITE_NAME": "FAE 2.0 for [your organization]",
  "SECRET_KEY": "[random string of 40-50 characters used by django]",
  "SELF_REGISTRATION_ENABLED": true,
  "ANONYMOUS_ENABLED": true,
  "DEBUG": false,
  "LOGGER_LEVEL": "INFO",
  "DATABASE_HOST": "[ip address or localhost if database on same server]",
  "DATABASE_PORT": "[port, typicall 5432]",
  "DATABASE_NAME": "[DB name]",
  "DATABASE_USER": "[DB username]",
  "DATABASE_PASSWORD": "[DB password]",
  "ALLOWED_HOSTS": ["[your site URL]"],
  "EMAIL_HOST": "[mailserver]",
  "EMAIL_PORT": 25,
  "EMAIL_USE_TLS": true,
  "EMAIL_HOST_USER": "[email used for sending registration information and announcements]",
  "EMAIL_HOST_USER_PASSWORD": "[email password]",
  "ACCOUNT_ACTIVATION_DAYS" : 3,
  "CONTACT_EMAIL" : "[email notification when a contact form is submitted]",
  "ADMIN_USER_NAME" : "[username of admin user]",
  "ADMIN_FIRST_NAME" : "[first name of admin]",
  "ADMIN_LAST_NAME" : "[last name of admin]",
  "ADMIN_PASSWORD": "[password for admin]",
  "ADMIN_EMAIL": "[email for admin]",
  "ANONYMOUS_PASSWORD" : "[anonymous password, use random characters]",
  "DEFAULT_ACCOUNT_TYPE" : 2
}
```

### Apache 2.0 configuration notes

* MOD_WSGI must be installed and support Python 2.7

#### Sample Apache configuration gile

```
<VirtualHost *:80 >

  Servername  [fae.somedomain.org]
  ServerAlias [fae.somedomain.org]

  Alias /static /var/www/fae2/fae2/fae2/fae2/static/

  <Directory /var/www/fae2/fae2/fae2/fae2/static>
    Require all granted
  </Directory>

  <Directory /var/www/fae2/fae2/fae2>
    <Files wsgi.py>
     Require all granted
    </Files>
  </Directory>

  WSGIDaemonProcess fae2 python-path=/var/www/fae2/fae2/fae2:/var/www/fae2/fae2env/lib/python2.7/site-packages
  WSGIProcessGroup  fae2

  WSGIScriptAlias / /var/www/fae2/fae2/fae2/fae2/wsgi.py process-group=fae2

</VirtualHost>
```

### Setting up fae directories for read/write access
* Need to create `data` directory with write permissions for `apache` user and group `root` user
* Need to create `logs` direcotry with write permissions for `apache` user and group `root` user


### Multiple Django Apps and mod_wsgi 
* [Configuring wsgi.py for multiple Django apps](https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/modwsgi/)

### Initialize database tables
* You will need to run <code>python manage.py migrate</code> to create the tables in the database
* After the tables in the database are created, go to the "populate" directory
* In the populate directory run <code>python pop_all.py</code> to initialize the tables

### fae-util configuration and testing
* Purpose of fae-util
  * fae-util is a server based browser emulator based on HTMLUnit
  * It monitors the database waiting for evaluation requests
  * When it identifes a request it will then load web pages and analyze them using the OpenAjax Evaluation Library
  * Each page evaluation results in a JSON file being crerated with the results
  * After all pages are analyzed the information in the JSON files is moved to the database
* Testing fae-util
  * Go to the "fae-util" directory
  * Use <code>./run -c test.properties</code> to test if the utility is properly installed and configured
  * It will output URL processing information to the console
  * It will create a directory called "test" that contains *.json files of evaluaiton results
  * NOTE: You must delete the "test" directory to rerun this test (e.g. directory exists error will occur)
* Creating a service to run evaluation requests
  * IMPORTANT: Must run <code>fae-util/python process_evaluation_requests.py</code> to process website evaluations in the background
  * There are a number of ways to make this program run in parallel with django application depending on your operating system
    * Linux: How to write a System V init script to start, stop, and restart my own application or service(http://www.cyberciti.biz/tips/linux-write-sys-v-init-script-to-start-stop-service.html)


### Utility to clean up reports and update summary statistics
* IMPORTANT: Must run <code>fae-util/process_achive_reports.py</code> to process remove reports and update summary statistics
* Create cron job to run a shell script once a day
* The shell script contains the following command lines:
<pre>
#!/usr/bin/env bash
<path to virtual environment>/python <path to fae-util>/fae-util/process_achive_reports.py
</pre>

## InCommon (Shibboleth) Configuration

To enable shibboleth support through [InCommon](https://www.incommon.org) for your institution or organization you need your service manager to enable the following attributes to the entityID identifying the installation of FAE with Shibboleth Support (e.g. "https://fae.illinois.edu/shibboleth" for the University of Illinois campus):
* eppn
* giveName
* sn
* mail

Enityt IDs: [https://www.incommon.org/federation/info/all-entities.html#IdPs]

## Testing e-mail on localhost development
* Use a python utitlity to simulate an SMTP server: <code>python -m smtpd -n -c DebuggingServer localhost:1025</code>
* Configure e-mail in "secretes.json" with the following values:
```
    ....
    "EMAIL_HOST": "localhost",
    "EMAIL_PORT": 1025,
    "EMAIL_USE_TLS": false,
    "EMAIL_HOST_USER": "None",
    "EMAIL_HOST_USER_PASSWORD": "None",
    ....

```

## Development Resources

### Django Shibboleth Resources
* [How to (not) use Shibboleth with the Django web framework](https://5chub3r7.wordpress.com/2014/12/05/how-to-not-use-shibboleth-with-the-django-web-framework/)

### Incommon Resources (Multi-Institution Shibboleth)
* [InCommon: Embedded Discovery Service](https://wiki.shibboleth.net/confluence/display/EDS10/Embedded+Discovery+Service)
* [Technology Services: Shibboleth, Multi-university configuration](https://answers.uillinois.edu/illinois/48456)
* [InCommon: Federation Entities](https://www.incommon.org/federation/info/all-entities.html)
