FROM python:3.7-alpine

# Set application directory
WORKDIR .

RUN apk add --no-cache gcc musl-dev libxslt-dev libmagic

ADD requirements.txt /web_crawler/requirements.txt
RUN pip3 install -r /web_crawler/requirements.txt

ADD . /web_crawler

ENTRYPOINT ["/web_crawler/pastebin/pastebin_crawling_executor.py"]

CMD ["-h"]
