@echo off

REM This batch file is used to run all the Scrapy spiders for BetParser
REM NOTE:
REM 1) Make sur to add your Conda installation path to the PATH variable
REM 2) Make sure to replace 'yourCondaEnv' with the name of your Conda environment

echo Activating BetParser-Scrapy Conda environment
conda activate yourCondaEnv

echo Launching Scrapy Spider for: Bet365, Bwin, William Hill and Sisal
start "" scrapy crawl b365 
start "" scrapy crawl bwin
start "" scrapy crawl william
start "" scrapy crawl sis 