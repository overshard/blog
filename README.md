# Blog

A simple self-hostable blog built on Wagtail.


## Motivation

I was bored and felt like writing my own blog over the weekend.


## Requirements

You need docker + docker-compose installed for a quick production start or you
can figure out how we install and run things via the `Dockerfile` and set it up
yourself.

If you want to install things without docker then you'll need the following
dependencies:

- python
- pipenv
- node
- yarn
- chromium

You can also check the `Dockerfile` for an exact list of dependencies and adjust
package names for your desired platform.

This is a standard Django project. If you know how to run Django, or want to
look up any Django tutorial on how to run Django, you shouldn't have a problem
getting this project running on almost anything.


## Checking outdated dependencies

This can be done in both yarn and pipenv with the following two commands:

    pipenv update --outdated
    yarn outdated

You can then upgrade the outdated dependencies with the following two commands:

    pipenv update
    yarn upgrade

I recommend testing everything after this to make sure it's all working.


## Optimizing images with webp

My development system runs Ubuntu so I installed the official webp utils from
Google with `apt install webp`.

    cwebp -q 85 -m 6 -o /path/to/image.webp /path/to/image.png


## Using docker-compose

The easiest way to run this project is to run it using
`docker-compose up --build -d` if you have `docker-compose` and `docker`
installed. This will start the server and have you running at port 8000. The
first time you do this make sure you run migrations with
`docker-compose run web python manage.py migrate`. Make sure you setup the
`.env` file before running, you can copy the sample from
`samplefiles/env.sample` into the root of the project as `.env` and change the
variables.


## Default user

The default user is `admin` with the password `admin`.


## Backups

All data is stored in `/srv/data/blog/` and your repo is stored in
`/srv/git/blog.git/`. You can backup both of these folders and you'll have
a 100% backup of everything except changes you may have made to the `Caddyfile`
and the `.env` file which should be easy enough to recreate but you can back
those up too!


## Support

I won't be providing any user support for this project. I'm more than happy to
accept good pull requests and fix bugs but I don't have the time to help people
run or use this project. I appologize in advance for this. Maintaining
mutliple OSS projects has taught me that I need to step back from trying to
provide support to avoid burnout.


## Server guides

Here are a handful of guides on getting started on various distros, they are
very simplistic and you should probably add some extra security and automated
updates. Review your distro's documentation for more information on hardening
your server.

**IMPORTANT NOTE**: Change `blog.bythewood.me` to your domain name where
relevant in these instructions.

**TIP**: During the ufw portion to enable the firewall I recommend only allowing
your IP address or your ISP's IP address range which you can find on whois
lookups at the top. For example, replace `192.230.176.0/20` with your IP or your
ISP's IP range.

    ufw allow from 192.230.176.0/20 proto tcp to any port 22

I allow my local ISP's range because I have a DHCP lease from them and I get
tired of logging into my server from my hosting provider's UI to update it. It's
good enough security and much better than nothing!


### Server guide (Alpine Linux)

This quickstart requires that you have an Alpine Linux server running with a
domain name pointed to it. I'm currently using Linode as my host since they
support Alpine Linux nicely. If you don't want to use Linode or Alpine Linux
you can use these instructions and just change the apk commands at the start to
whatever Linux distro you're using.

Server:

    apk update && apk upgrade && apk add docker docker-compose caddy git iptables ip6tables ufw moreutils htop
    ufw allow 22/tcp && ufw allow 80/tcp && ufw allow 443/tcp && ufw --force enable
    echo -e "apk upgrade --update | ts '[%Y-%m-%d %H:%M:%S]' >> /var/log/apk-autoupgrade.log" > /etc/periodic/daily/apk-autoupgrade && chmod 700 /etc/periodic/daily/apk-autoupgrade
    rc-update add docker boot && service docker start
    mkdir -p /srv/git/blog.git && cd /srv/git/blog.git && git init --bare

Local:

    git clone git@github.com:overshard/blog.git && cd blog
    git remote remove origin && git remote add origin root@blog.bythewood.me:/srv/git/blog.git
    git push --set-upstream origin master

Server:

    mkdir -p /srv/docker && cd /srv/docker && git clone /srv/git/blog.git blog && cd /srv/docker/blog
    cp samplefiles/Caddyfile.sample /etc/caddy/Caddyfile && sed -i 's/blog.example.com/blog.bythewood.me/g' /etc/caddy/Caddyfile
    cp samplefiles/env.sample .env && sed -i 's/blog.example.com/blog.bythewood.me/g' .env
    cp samplefiles/post-receive.sample /srv/git/blog.git/hooks/post-receive
    mkdir -p /srv/data/blog && chown -R 1000:1000 /srv/data/blog
    docker-compose up --build --detach && docker-compose run web python3 manage.py migrate --noinput && docker-compose run web sqlite3 db.sqlite3 "PRAGMA journal_mode=WAL;" ".exit"
    rc-update add caddy boot && service caddy start


### Server guide (Ubuntu Linux)

Similar to the Alpine Linux guide this helps you get started with Ubuntu. Note
that Ubuntu doesn't seem to have Caddy in their default repositories so we
have to install it using their offical script.

Server:

    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/setup.deb.sh' | sudo -E bash
    apt update; apt upgrade -y; apt install -y docker-compose docker git ufw
    ufw allow 22/tcp && ufw allow 80/tcp && ufw allow 443/tcp && ufw --force enable
    mkdir -p /srv/git/blog.git; cd /srv/git/blog.git; git init --bare

Local:

    git clone git@github.com:overshard/blog.git && cd blog
    git remote add origin root@blog.bythewood.me:/srv/git/blog.git
    git push --set-upstream origin master

Remote:

    mkdir -p /srv/docker && cd /srv/docker && git clone /srv/git/blog.git blog && cd /srv/docker/blog
    cp samplefiles/Caddyfile.sample /etc/caddy/Caddyfile && sed -i 's/blog.example.com/blog.bythewood.me/g' /etc/caddy/Caddyfile
    cp samplefiles/env.sample .env && sed -i 's/blog.example.com/blog.bythewood.me/g' .env
    cp samplefiles/post-receive.sample /srv/git/blog.git/hooks/post-receive
    mkdir -p /srv/data/blog && chown -R 1000:1000 /srv/data/blog
    docker-compose up --build --detach && docker-compose run web python3 manage.py migrate --noinput && docker-compose run web sqlite3 db.sqlite3
    systemctl restart caddy
