@echo off
echo Activating Scrapy Conda environment
CALL C:\yourcondadir\Anaconda3\condabin\conda.bat activate yourcondaenv
echo Launching Scrapy Spider for: Bet365, Bwin, William Hill and Sisal
cd C:/your_betparser_crawler_dir/betparser_crawler/
start "" scrapy crawl b365 
start "" scrapy crawl bwin
start "" scrapy crawl william
start "" scrapy crawl sis 
