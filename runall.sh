#!/bin/bash

# This batch file is used to run all the Scrapy spiders for BetParser
# NOTE:
# 1) Make sure to add your Conda installation path to the PATH variable
# 2) Make sure to replace 'yourCondaEnv' with the name of your Conda environment

echo "Activating BetParser-Scrapy Conda environment"
conda activate yourCondaEnv

echo "Launching Scrapy Spider for: Bet365, Bwin, William Hill, and Sisal"
scrapy crawl b365 &
scrapy crawl bwin &
scrapy crawl william &
scrapy crawl sis