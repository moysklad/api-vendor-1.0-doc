FROM ruby:2.5.9
COPY . /usr/src/app
VOLUME /usr/src/app
EXPOSE 4567
WORKDIR /usr/src/app
RUN printf 'deb http://archive.debian.org/debian buster main\n' > /etc/apt/sources.list && \
    printf 'deb http://archive.debian.org/debian-security buster/updates main\n' >> /etc/apt/sources.list && \
    printf 'Acquire::Check-Valid-Until "false";\n' > /etc/apt/apt.conf.d/99archive && \
    apt-get update && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*
RUN bundle install
CMD ["bundle", "exec", "middleman", "server", "--watcher-force-polling"]


