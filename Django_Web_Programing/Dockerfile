FROM python:3.12.1-alpine3.19

# ensures that the python output
# i.e. the stdout and stderr streams are sent straight to terminal
ENV PYTHONUNBUFFERED 1

ARG DEV=false

COPY requirements.txt /mysite/
COPY requirements.dev.txt /mysite/
COPY mysite /mysite/

WORKDIR /mysite
RUN pip install Django

# install this only if it is dev mode
RUN if [ $DEV = true ]; then pip install -r requirements.dev.txt; fi

EXPOSE 8000