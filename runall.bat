@echo off
echo Activating Scrapy Conda environment
CALL C:\DevTools\Anaconda3\condabin\conda.bat activate bet_parser_3.6
echo Launching Scrapy Spider for: Bet365, Bwin, William Hill and Sisal
cd C:/DevTools/Projects/bet_parser/
start "" cmd /c scrapy crawl b365 
echo ^> logB365.txt
start "" cmd /c scrapy crawl bwin 
echo ^> logBwin.txt
start "" cmd /c scrapy crawl william 
echo ^> logWilliam.txt
start "" cmd /c scrapy crawl sis 
echo ^> logSis.txt
