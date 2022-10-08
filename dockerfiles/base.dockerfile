# # Run from the main project directory (poetry-poems):
# docker build -t ubuntu-pyenv-poetry -f dockerfiles/base.dockerfile .
# docker run -it --rm --name ubuntu-pyenv-poetry ubuntu-pyenv-poetry

FROM ubuntu:18.04

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install make build-essential build-essential zlib1g-dev \
    libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget curl \
    python-setuptools python3 python3-dev python3-pip

ENV HOME="/root"
WORKDIR ${HOME}

# RUN git -c http.sslVerify=false clone https://github.com/pyenv/pyenv.git ~/.pyenv
COPY dockerfiles/pyenv-2.3.4.tar.gz $HOME
RUN mkdir $HOME/.pyenv && \
    tar -xzf pyenv-2.3.4.tar.gz -C $HOME/.pyenv --strip-components=1 && \
    rm pyenv-2.3.4.tar.gz

ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

# remember to run python3 instead of python
RUN pyenv install 3.9.1 & pyenv install 3.8.7 & pyenv install 3.7.9 & pyenv install 3.6.12; wait

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.1.15 python3 -
ENV PATH $HOME/.local/bin:$PATH

CMD ["bash"]
