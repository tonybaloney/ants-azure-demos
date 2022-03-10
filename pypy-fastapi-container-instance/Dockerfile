FROM pypy:3.9-slim-buster
COPY . /api
WORKDIR /api
ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get -y update && apt-get clean -y && rm -rf /var/lib/apt/lists/*
COPY ./api/requirements.txt /code/requirements.txt
RUN pypy -m pip install -U pip && pypy -m pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./api /code/app
CMD ["pypy", "-m", "uvicorn", "--host", "0.0.0.0", "--port", "80", "--proxy-headers", "api.main:app"]