FROM grahamdumpleton/mod-wsgi-docker:python-3.4-onbuild

RUN mkdir /code

COPY requirements/base.txt /code/requirements./base.txt

WORKDIR /code
COPY . /code/

ENV PYTHONUNBUFFERED 1

EXPOSE 80 3500

RUN python3 -m pip install -r requirements/base.txt

CMD [ "--working-directory", ".", \
      "--url-alias", "/static", "/static", \
      "--application-type", "module", "config.wsgi" ]



