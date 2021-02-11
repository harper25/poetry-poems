# # Run from the main project directory (poetry-poems):
# docker build -t ubuntu-pyenv-poetry -f dockerfiles/base.dockerfile .
# docker run -it --rm --name ubuntu-pyenv-poetry ubuntu-pyenv-poetry

FROM ubuntu:18.04

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install git make build-essential build-essential zlib1g-dev \
    libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget curl \
    python-setuptools python3 python3-dev python3-pip

# pyenv
RUN git clone git://github.com/yyuu/pyenv.git .pyenv
RUN git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
ENV HOME  /
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

# remember to run python3 instead of python
RUN pyenv install 3.9.1
RUN pyenv install 3.8.7
RUN pyenv install 3.7.9
RUN pyenv install 3.6.12

# poetry
ENV POETRY_VERSION=1.1.4
ADD https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py /tmp
RUN python3 tmp/get-poetry.py
ENV PATH $HOME/.poetry/bin:$PATH

CMD ["bash"]
