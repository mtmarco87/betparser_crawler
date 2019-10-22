FROM scrapinghub/scrapinghub-stack-scrapy:1.6-py3-latest
ENV TERM xterm
ENV SCRAPY_SETTINGS_MODULE bet_parser.settings
RUN mkdir -p /app
RUN mkdir /app/build
RUN mkdir /app/build/lib
RUN mkdir /app/build/lib/bet_parser
WORKDIR /app
COPY ./bet_parser/libs /app/build/lib/bet_parser/libs
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
RUN python setup.py install
