# BetParser Crawler

BetParser Crawler is a Python application able to parse and extract betting odds from the web, making use of the Scrapy framework, FireBase, a custom Selenium integrations and SciPy.

## Environment Setup

The following guide is specific to Windows machines for the Anaconda env configuration. In case you're using Linux, you'll have to use the same commands but you'll need to adapt some of them to your OS.

### 1) Clone this repo

Just use `git clone` to clone this repository to your local machine.

### 2) Install Anaconda3

Install Anaconda3 with Python 3 from here, choosing the correct version for your OS: [Anaconda Download Page](https://www.anaconda.com/distribution/#download-section).
This will be the tool that allow us to create our Python environment

### 3) Configure an environment

3.1) Open Anaconda prompt (you can use the shortcut: `C:\Users\{username}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Anaconda3 (64-bit)`, where {username} is your Windows username)

3.2) Create a new Anaconda env with Python 3.6: `conda create -n {env_name} python=3.6`

{env_name} is the name you want to give to the Python env that will hold your BetParser Crawler

3.3) You can check that Anaconda has created for you a new env at this location: `C:\{anaconda_install_dir}\envs`. 

3.4) At the end of the installation we have 4 commands available to handle the environments:

	- conda activate {env_name}			# to activate an env
	- conda deactivate {env_name}		# to deactivate an env
	- conda env list					# to list all your env (a `*` indicates the current active one)
	- conda remove {env_name}			# to remove an env

### 4) Install libraries

4.1) With the Anaconda prompt open, activate your new environment: `conda activate {env_name}`

4.2) Run the following command to install all of the needed libraries:
	`pip install -r requirements.txt`

4.3) Or install them one by one manually:

- pip install scrapy
- pip install scrapy-useragents
- pip install shadow-useragent
- pip install scrapy-splash
- pip install selenium
- pip install pyrebase
- pip install numpy
- pip install nltk
- pip install unidecode
- pip install googletrans
- pip install stem
- pip install torrequest
- pip install urllib3
- pip install requests
- pip install pytz

4.4) If you're experiencing problems with some of the libraries, try to force the following specific versions:

- scrapy                    1.7.3
- scrapy-useragents         0.0.1
- shadow-useragent          0.0.17
- scrapy-splash             0.7.2
- selenium                  3.141.0
- pyrebase                  3.0.27
- numpy                     1.17.2
- nltk                      3.4.5
- unidecode                 1.1.1
- googletrans               2.4.0
- stem                      1.7.1
- torrequest                0.1.0
- urllib3                   1.25.6
- requests                  2.11.1
- pytz                      2019.2

## 5) Run/Debug

5.1) PyCharm IDE Configuration

* Open PyCharm and configure the IDE to use the existing environment created at the point 3.2 of the Environment Setup section.

* Open the settings menu with `CTRL + ALT + S` and search for `Project Interpreter` and then add a new interpreter (go to settings in the top-right corner and press on add)

* Then choose 'Existing environment' and put the location of your env python interpreter `C:\{anaconda_dir}\envs\{env_name}\python.exe`


5.2) Run/Debug

To setup debugging in PyCharm we must create a single debugging configuration for each Spider created. The steps are the following:
	
* Add a new Python Run/Debug Configuration (top-right button edit configurations, then + button)

* Set the Script path to: `C:\{anaconda_dir}\envs\{env_name}\Lib\site-packages\scrapy\cmdline.py`

* Set the Parameters to: `crawl {spidername}`

* Select the correct project Python interpreter

* Set the Working directory to: `C:\{betparser_project_dir}`

* Under Execution check Run with Python Console (else the Debug will work, but the Run will be broken)

* Now you can debug!

## Selenium middleware Configuration

Selenium it's a powerful tool that allows automated web testing. With the usage of Selenium is possible to perform potentially every interaction on a web page, and to render the same page exactly like it'd happen on a normal Chrome or Firefox browser. A powerful custom implementation of a Scrapy-Selenium middleware has been created in BetParser.
This middleware is the most indicated solution to use to parse complex, JS/Angular powered pages.


To enable Selenium middleware in BetParser:

1) Install Chrome browser in your machine, if you don't have it yet

2) Download a Selenium Chrome driver: [Chromium - Chrome WebDriver download](https://chromedriver.chromium.org/downloads)

Choose the correct one according to your OS

3) Place the downloaded Chrome driver in the project folder in the path: `bet_parser/libs/selenium_drivers`

4) Another needed step is to create a Chrome profile folder, and to copy it manually in the path: `bet_parser/libs/selenium_drivers/chrome_profiles`

To generate a new Chrome profile, it's enough to open Chrome browser, use the menu to create and use a new user profile. After it's necessary to search in your system for the Chrome data folder to find the newly created profile folder. You can search on google for detailed instructions. (in case of problems you can ask to some of the devs)

5) IMPORTANT: Some websites protect their pages from robotic access, generating some cookies only after the human user perform some actions. To enable Selenium to use the generated Chrome profile to correctly access these pages (as some of those visited by the BetParser spiders), in the previous step you need to visit these web pages and manually confirm some of the welcome banners to get your cookies generated.
The generated cookies validity is normally very long.

6) Last step: edit the file `bet_parser/settings.py`, and in the 'Selenium config' section, change only the `SELENIUM_CHROME_DRIVER` and the `SELENIUM_CHROME_USER_DATA_DIR` respectively to your specific Chrome Driver binary, and to your custom Chrome user profile. 
The other parameter could be used to fine tune some global behaviour of the middleware, and to add in case a Firefox Driver. We suggest to leave them untouched.

7) From now on if everything has been correctly configured the Selenium middleware should execute requests correctly and should be able to create as needed a temporary copy of the custom user profile to avoid folder bloating

8) To understand the usage of the middleware in the code check out the SeleniumRequest/SeleniumMiddleware class.
Most important SeleniumRequest parameters:

- driver ==> 'chrome' or 'firefox', specify which web driver you want to use with selenium (and so which browser)

- render_js ==> true: execute a js script to extract the rendered DOM for the response; false: just ask selenium to extract html content of the page

- wait_time ==> alone: sets a waiting time for selenium to render the page; together with wait_until: sets a deadline until which to wait for the wait_until condition

- wait_until ==> works only together with wait_time, and represent a Selenium expectation that has to happen before the page is fetched

- headless ==> true: no browser window opened, operate in ghost mode; false: use a browser window

- window_size ==> size of the above window

- script ==> pass a custom js script to execute (before the extraction)

## Machine Learning mapper - Word Similarity Algorithms

After the betting odds are parsed from the web pages with Selenium, there is often a common issue: the Sport Matches are not always unique, because the Team Names can be expressed in different form or in different languages.

To overcome this big problem, a small Machine Learning class have been implemented using some Word Similarity Algorithms.

This ML class processes the Team Names of every single parsed Match, and check their existance in a big key-value pairs file already provided in the repo (with a continuously improved list of Team Names): `bet_parser/libs/ml_data/team_names.csv`
If a Team Name is found in this file the corresponding standardized version is taken.
Else if this Team Name isn't similar to any of the available ones, it means that is a completely new match and its value is appended in a validation file: `bet_parser/libs/ml_data/to_validate.txt`

IMPORTANT:
This is a very crucial step to make BetParser Crawler working correctly. 
Sometimes after running many times the Spiders, the to_validate.txt grows a lot in size with several new unknown Team Names.
In this moment it's really important to manually open the 'to_validate.txt' and the 'team_names.csv' to try to verify if each one of the team names in the to_validate is:
1) already existing in different forms or languages in the team_names.csv;
2) not existing at all in that file;

In the first case it's just worth copying this new form/language in the team_names.csv, together with a mapping to the already existing standardized name.
In the second case it's extremely important and worth to copy the unknown team name in the team_names.csv, and to map it to a standardized, possibly English version of the Team Name. And also it's really worth starting from now to add every possible other language and found form on the web of this Team Name, to avoid in the future to see it back in the to_validate.txt, but in another form.


*EXTRA:
In BetParser Crawler everything is configurable, and also the ML it is. In particular we can fine tune its behaviour in the 'Machine Learning config' section of the `bet_parser/settings.py`.
Though the current configuration is convenient in many scenarios.

## FireBase Configuration

The very last step in the crwaling process is the write process to the DataBase.
In BetParser Crawler we've choosen to implement FireBase DB connection, to use a real time and flexible data feed.

To enable FireBase you need to:

1) Create a FireBase account if you don't have one yet

2) Create a FireBase database named `parsed_bets`

3) Enabe a FireBase App from the account settings

4) Configure BetParser Crawler to use the FireBase App key/secrets, editing the FireBase section in the `bet_parser/settings.py`

## Extra Information

### Development with Scrapy framework

BetParser Crawler is built on top of the Scrapy framework. Scrapy is the tool that will help us to do the request and collect the data from the page with the possibility to create a well designed program structure that will allow our code to be simple.

The Scrapy framework can be used to easily initialize projects and spiders skeletons:

1) Create Projects - run: `scrapy startproject betparser`, in the Anaconda prompt, in a choosen folder 

2) Create Spiders - to add a new spider, from the project folder in the Anaconda prompt run: `scrapy genspider {spidername}`, and you can start to code :)

3) Run Spiders - to run a spider, from the project folder in the Anaconda prompt run: `scrapy crawl {spidername}`, to run your first spider

## Splash middleware Configuration (OPTIONAL)

Scrapy-Splash is a third party middleware that allows Scrapy to comunicate with Splash, an headless browser that can execute some JavaScript powered pages (Angular included) and will give us the final html extracted from the DOM and the possibility to send, for instance, some cookies in the request. It's an extension that adds lot of power to Scrapy, and is Dockerizable. 

To use a docker image of Splash (you should install docker for your os first, if you don't have it yet): 
	- `docker pull scrapinghub/splash`
	- `docker run -p 8050:8050 scrapinghub/splash`
Using the commands above, we have an instance of our Splash browser running on the port 8050 of our localhost.

The final step is to configure the `bet_parser/settings.py` in the Splash section, to ensure that the host and the port of the Splash browser are correct, and in the downloader and spider middleware sections to enable the scrapy-splash downloader and all the needed spider middleware.

## Tor and Custom Proxy middlewares (OPTIONAL)

In BetParser Crawler have been implemented other 2 custom downloaders:

1) Tor to try to avoid ban when requesting and parsing pages at high frequency from some web sites; this technique needs to be refined;

2) Same story for Custom Proxy, that tries to use a Free Proxy rotation to obtain the same result;

## Google Translator mapper (OPTIONAL)

A google translator based mapper has also been implemented to use the famous translation engine to try to align the Team Names. This solution has revealed itself to not being very effective. But it's still available.
