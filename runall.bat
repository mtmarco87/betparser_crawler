@echo off
echo Activating Scrapy Conda environment
CALL C:\DevTools\Anaconda3\condabin\conda.bat activate bet_parser_3.6
echo Launching Scrapy Spider for: Bet365, Bwin, William Hill and Sisal
cd C:/DevTools/Projects/betparser_crawler/
start "" scrapy crawl b365 
echo ^> logB365.txt
start "" scrapy crawl bwin 
echo ^> logBwin.txt
start "" scrapy crawl william 
echo ^> logWilliam.txt
start "" scrapy crawl sis 
echo cmd /c
echo ^> logSis.txt
