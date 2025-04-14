# BetParser Crawler

BetParser Crawler is a Python application designed to parse and extract betting odds from websites. It leverages the Scrapy framework, Firebase, custom Selenium integrations, and SciPy for efficient data extraction and processing.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Environment Setup](#environment-setup)
   - [Clone the Repository](#1-clone-the-repository)
   - [Install Anaconda3](#2-install-anaconda3)
   - [Configure an Environment](#3-configure-an-environment)
   - [Install Libraries](#4-install-libraries)
3. [Selenium Middleware Configuration](#selenium-middleware-configuration)
4. [Firebase Configuration](#firebase-configuration)
5. [Run/Debug](#rundebug)
6. [Development with Scrapy Framework](#development-with-scrapy-framework)
7. [Machine Learning Mapper - Word Similarity Algorithms](#machine-learning-mapper---word-similarity-algorithms)
8. [Optional Configurations](#optional-configurations)
   - [Splash Middleware](#splash-middleware-configuration)
   - [Tor and Custom Proxy Middlewares](#tor-and-custom-proxy-middlewares)
   - [Google Translator Mapper](#google-translator-mapper)
9. [License](#license)

## Project Overview

BetParser Crawler simplifies the process of extracting betting odds from web pages. It supports parsing complex JavaScript-powered pages using Selenium and includes machine learning algorithms to standardize team names. The project is highly configurable and integrates with Firebase for real-time database updates.

## Environment Setup

### 1) Clone the Repository

Clone this repository to your local machine using:

```bash
git clone https://github.com/mtmarco87/betparser_crawler.git
```

### 2) Install Anaconda3

Download and install Anaconda3 with Python 3 from the [Anaconda Download Page](https://www.anaconda.com/distribution/#download-section).

### 3) Configure an Environment

1. Open the Anaconda prompt.
2. Create a new environment with Python 3.6:
   ```bash
   conda create -n <env_name> python=3.6
   ```
3. Activate the environment:
   ```bash
   conda activate <env_name>
   ```
4. Manage environments with the following commands:
   - `conda deactivate` - Deactivate the current environment.
   - `conda env list` - List all environments.
   - `conda remove <env_name>` - Remove an environment.

### 4) Install Libraries

1. Activate your environment:
   ```bash
   conda activate <env_name>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Alternatively, install libraries individually:
   ```bash
   pip install scrapy scrapy-useragents shadow-useragent scrapy-splash selenium pyrebase numpy nltk unidecode googletrans stem torrequest urllib3 requests pytz
   ```
4. If issues arise, install specific versions:
   ```bash
   pip install scrapy==1.7.3 scrapy-useragents=0.0.1 shadow-useragent=0.0.17 scrapy-splash=0.7.2 selenium==3.141.0 pyrebase=3.0.27 numpy==1.17.2 nltk=3.4.5 unidecode=1.1.1 googletrans=2.4.0 stem=1.7.1 torrequest=0.1.0 urllib3=1.25.6 requests=2.11.1 pytz=2019.2
   ```

## Selenium Middleware Configuration

Selenium is a powerful tool for interacting with JavaScript-heavy pages. It allows automated web testing and renders pages as they would appear in a browser. BetParser includes a custom Scrapy-Selenium middleware for handling complex, JS/Angular-powered pages.

### Steps to Configure Selenium Middleware:

1. **Install Chrome and ChromeDriver**:

   - Download and install Chrome if not already installed.
   - Download the appropriate [Chrome WebDriver](https://chromedriver.chromium.org/downloads) for your OS.
   - Place the driver in the project folder: `bet_parser/libs/selenium_drivers`.

2. **Create a Chrome Profile**:

   - Open Chrome and create a new user profile.
   - Locate the profile folder on your system (search online for instructions specific to your OS).
   - Copy the profile folder to: `bet_parser/libs/selenium_drivers/chrome_profiles`.

3. **Update Settings**:

   - Edit `bet_parser/settings.py` in the "Selenium config" section. Update the following:
     - `SELENIUM_CHROME_DRIVER`: Path to the ChromeDriver binary.
     - `SELENIUM_CHROME_USER_DATA_DIR`: Path to the Chrome profile folder.
   - Other parameters can be adjusted for fine-tuning but are pre-configured for most use cases.

4. **Handle Protected Pages**:

   - Some websites allow pages to be displayed only after user interactions. Use the Chrome profile to manually visit these pages and accept any banners or prompts to generate valid cookies.
   - Selenium will use this profile to access these pages during scraping.

5. **Middleware Features**:
   - The middleware creates a temporary copy of the Chrome profile to avoid bloating the folder.
   - `SeleniumMiddleware` / `SeleniumRequest` parameters include:
     - `driver`: Can be `'chrome'` or `'firefox'`.
     - `render_js`: Set to `true` to extract the fully rendered DOM using JavaScript execution; set to `false` for standard HTML extraction with Selenium.
     - `wait_time` and `wait_until`: Define wait conditions for page rendering.
     - `headless`: Run in headless mode (no browser window).
     - `script`: Execute custom JavaScript before extraction.

By following these steps, the Selenium middleware will be ready to handle complex pages effectively.

## Firebase Configuration

1. Create a Firebase account and database named `parsed_bets`.
2. Enable a Firebase app and configure its credentials in `bet_parser/settings.py`.

## Run/Debug

### PyCharm IDE Configuration

1. Open PyCharm and configure the project interpreter to use the environment created earlier.
2. Add a Python Run/Debug Configuration for each spider:
   - Script path: `<env_path>/Lib/site-packages/scrapy/cmdline.py`
   - Parameters: `crawl <spider_name>`
   - Working directory: `<project_directory>`
   - Under Execution check Run with Python Console (else the Debug will work, but the Run will be broken)

## Development with Scrapy Framework

1. Create a project:
   ```bash
   scrapy startproject betparser
   ```
2. Add a spider:
   ```bash
   scrapy genspider <spider_name>
   ```
3. Run a spider:
   ```bash
   scrapy crawl <spider_name>
   ```

## Machine Learning Mapper - Word Similarity Algorithms

After extracting betting odds, team names often appear in different formats or languages, making it difficult to identify unique matches. To address this, BetParser includes a machine learning-based mapper that standardizes team names using word similarity algorithms.

### How It Works:

1. **Team Name Standardization**:

   - The mapper checks each team name against a pre-defined dataset (`team_names.csv`).
   - If a match is found, the standardized name is used.

2. **Handling Unknown Names**:

   - If no match is found, the name is logged in `to_validate.txt` for manual review.
   - This ensures new names are added to the dataset for future use.

3. **Manual Validation**:

   - Open `to_validate.txt` and compare each name with entries in `team_names.csv`.
   - If a name exists in another form or language, add the new form to `team_names.csv` and map it to the standardized name.
   - For completely new names, add them to `team_names.csv` with a standardized English version and any known variations.

4. **Improving Accuracy**:
   - Regularly update `team_names.csv` to reduce the size of `to_validate.txt`.
   - Add as many variations of team names as possible to avoid repeated manual validation.

### Configuration:

- The mapper's behavior can be fine-tuned in the "Machine Learning config" section of `bet_parser/settings.py`.
- The current configuration is optimized for most scenarios but can be adjusted as needed.

This process ensures accurate and consistent team name mapping, which is critical for the crawler's functionality.

## Optional Configurations

### Splash Middleware Configuration

Use Splash for alternative JavaScript rendering:

1. Install Docker and run Splash:
   ```bash
   docker pull scrapinghub/splash
   docker run -p 8050:8050 scrapinghub/splash
   ```
2. Update `bet_parser/settings.py` to configure Splash.

### Tor and Custom Proxy Middlewares

Enable Tor or proxy rotation to avoid bans when requesting and parsing pages at high frequency. These features are experimental and require refinement.

### Google Translator Mapper

A Google Translator-based mapper is available but less effective. It can be enabled if needed.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
