@echo off
echo Activating Scrapy Conda environment
CALL C:\DevTools\Anaconda3\condabin\conda.bat activate bet_parser_3.6
echo Launching Scrapy Spider for: Bet365, Bwin, William Hill and Sisal
cd C:/DevTools/Projects/bet_parser/
start "" scrapy crawl b365
start "" scrapy crawl bwin
start "" scrapy crawl william
start "" scrapy crawl sis
