0)clone this repo

1)Install anaconda wit python 3.7 from here: 
	https://www.anaconda.com/distribution/#download-section
  This will be the tool that allow us to create our python environment
  1.1) Go in C:\Users\efricano\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Anaconda3 (64-bit) and open Anaconda prompt
  1.2) Run in the cmd conda create -n test_env_ema3 python
  1.3) You will see in the prompt that anaconda created for you a new env at this location 
       C:\Users\efricano\AppData\Local\Continuum\anaconda3\envs , where it installed python and other packages
  1.4) At the end of the installation we have 4 command suggested for us:
       - conda activate test_env_ema3     #to activate an env
       - conda deactivate test_env_ema3   #to deactivate an env
       - conda env list  		  #to list all your env, a * indicates the current active one
       - conda remove test_env_ema3       #to remove an env

2)Install scrapy in your new env with 'pip install scrapy'. This is the tool that will help us to do the request and collect the
  data from the page with the possibility to create a really well designed program structure that will allow our code to be simple.

3)Install scrapy-splash with 'pip install scrapy-splash'. This will allow scrapy to comunicate with splash a browser that will
  execute some js pages and will give us the final html and the possibility to send for instance some cookie in the request.
  Basically is an extension that add powerfull to scrapy. 

4)Run then in docker (that you should install for your os if you don' t have yet) 
  4.1) 'docker pull scrapinghub/splash' 
  4.2) 'docker run -p 8050:8050 scrapinghub/splash'.
  So we have the instance of our 'splash browser' running for us at the port 8050 in our os.

5)This project was created with 'scrapy startproject betparser'. Now try to run scrapy crawl example to run our first spider.
  Open pycharm and configure the ide to use the existing environment created at the point 1 (use test_env_3)
  5.1) open the menu with 'ctrl + alt + s' and search for 'Project Interpreter' and then add a new interpreter ( go to settings in the 
       up-rigth corner and press on add
  5.2) then choose existing env and put the location of your env 'C:\Users\efricano\AppData\Local\Continuum\anaconda3\envs\test_env_ema3\python.exe'
  5.3) in the anaconda prompt go to the main folder of our project and run 'scrapy crawl example', where example is the name of the spider you want to run :)
       Let's start :)

6)To add a new spider from the main folder in the anaconda prompt run 'scrapy genspider diretta', and we can start to code :)