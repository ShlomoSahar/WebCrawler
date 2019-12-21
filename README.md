# WebCrawler

Web crawler with dedicated example of pastbin.com

## Usage

### pastbin.com example:
### python pastebin/pastebin_crawling_executor.py

### general crawler:
### python general/main.py -u url -d depth
#### for example: python general/main.py -u https://bbc.com -d 1

#### Prerequisites

- [Python](https://www.python.org/) 3.7 (with pip) or greater
coloredlogs==10.0
requests==2.20.1
requests-html==0.10.0
python-magic>=0.4.15
urllib3==1.22
tinydb==3.13.0
argparse

#### Commands

``` shell
cd web_crawler
pip install -r requirements.txt
./general/main.py -d <DEPTH> -u <URL>
```

### Option 2 - Docker

#### Prerequisites

- [Docker](https://www.python.org/)
- [docker-compose](https://docs.docker.com/compose/install/)

#### Commands

``` shell
DEPTH=<DEPTH> URL=<URL> docker-compose up -d
docker-compose logs -f
```

## Outputs

All pages downloaded reside in local directory called `<URL_BASE_NAME>`.
For example: `news.bbc.com/`
