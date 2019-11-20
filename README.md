# BetParser Crawler

BetParser Crawler is a Python application able to parse and extract betting odds from the web, making use of the Scrapy framework, SciPy and custom Selenium integrations.

## Environment Setup

The following guide is partially specific to Windows machines. In case you're using Linux, you'll have to use the same commands but you'll need to adapt some of them to your OS.

### 1) Clone this repo

Just use `git clone` to clone this repository to your local machine.

### 2) Install Anaconda3

Install Anaconda3 with Python 3 from here, choosing the correct version for your OS: [Anaconda3 Download Page](https://www.anaconda.com/distribution/#download-section).
This will be the tool that allow us to create our Python environment

### 3) Configure an environment

3.1) Open Anaconda prompt (you can use the shortcut: `C:\Users\{username}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Anaconda3 (64-bit)`, where {username} is your Windows username);

3.2) Create an Anaconda environment with Python 3.7, running in the terminal: `conda create -n {env_name} python=3.7`. 
{env_name} is the name you want to give to the Python env that will hold your BetParser Crawler;

3.3) You can verify that Anaconda has created for you a new env at this location: `C:\{anaconda_install_dir}\envs`. Python and some base packages have been put there by Anaconda;

3.4) At the end of the installation we have 4 commands available to handle the environments:

	- `conda activate {env_name}`		# to activate an env
	- `conda deactivate {env_name}`		# to deactivate an env
	- `conda env list`					# to list all your env (a `*` indicates the current active one)
	- `conda remove {env_name}`			#to remove an env

### 4) Install libraries
2) Install scrapy in your new env with 'pip install scrapy'. This is the tool that will help us to do the request and collect the
   data from the page with the possibility to create a really well designed program structure that will allow our code to be simple.

3) Install firebase and extra needed libraries: 
   pip install pyrebase
   pip install Scipy googletrans Nltk selenium
   pip install unidecode

4) Install scrapy-splash with 'pip install scrapy-splash'. This will allow scrapy to comunicate with splash a browser that will
   execute some js pages and will give us the final html and the possibility to send for instance some cookie in the request.
   Basically is an extension that add powerfull to scrapy. 

5) Run then in docker (that you should install for your os if you don' t have yet) 
   5.1) 'docker pull scrapinghub/splash' 
   5.2) 'docker run -p 8050:8050 scrapinghub/splash'.
   So we have the instance of our 'splash browser' running for us at the port 8050 in our os.

6) This project was created with 'scrapy startproject betparser'. Now try to run scrapy crawl example to run our first spider.
   Open pycharm and configure the ide to use the existing environment created at the point 1 (use {envname})
   6.1) open the menu with 'ctrl + alt + s' and search for 'Project Interpreter' and then add a new interpreter ( go to settings in the 
        up-right corner and press on add )
   6.2) then choose existing env and put the location of your env 'C:\Users\{username}\AppData\Local\Continuum\anaconda3\envs\{envname}\python.exe'
   6.3) in the anaconda prompt go to the main folder of our project and run 'scrapy crawl {spidername}', where {spidername} is the name of the spider you want to run :)
        Let's start :)

7) To add a new spider from the main folder in the anaconda prompt run 'scrapy genspider {spidername}', and we can start to code :)

8) add under selenium_drivers/chrome_profiles your profile (ask to some dev in the team if you don t have)