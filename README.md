# Cloudia  challenge Solution.

Read more about the challenge here: [Cloudia Python](https://github.com/cloudiabot/cloudia_python)

### Running the production environment

```bash
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml run --rm web flask db upgrade
```

### Running the dev environment

```bash
docker-compose build
docker-compose up -d
docker-compose run --rm web flask db upgrade
```

### Running the tests

```bash
docker-compose run --rm web flask test
```

### Configute telegram webhook

```
https://api.telegram.org/bot<bot_token>/setWebhook?url=<your_domain>/api/telegram/update/
```

# Deploy on AWS

To deploy the application on AWS and automatically keep it updated with the latest version from GitHub, I will use DOKKU, a platform that helps create and manage the lifecycle of applications, from creation to scaling.
Note: I will not set up CD on this repository, but you can check out how to do it [here.](https://github.com/Mateus-Brito/deploying/blob/main/contents/dokku/django.md#continuous-integration-and-deploying-with-github-actions)

## RDS & EC2

Create an EC2 and RDS instance.

## Set up the EC2 instance

Start by creating a new user and adding them to the sudo and dokku groups so that we don't have to use sudo for every command.

```bash
sudo su
adduser dokku
sudo usermod -a -G sudo dokku
echo "%dokku ALL=(ALL:ALL) NOPASSWD:SETENV: /usr/bin/dokku" > /etc/sudoers.d/dokku-users
sudo usermod -a -G dokku dokku
su dokku
```

Now, install Dokku:
```bash
wget -qO- https://raw.githubusercontent.com/dokku/dokku/v0.29.3/bootstrap.sh | sudo dokku_TAG=v0.29.3 bash
```

Create an app on Dokku:
```bash
sudo dokku apps:create cloudia-challenge
```

Set the required environment variables:
"If you want to add Sentry, set the `SENTRY_DSN_URL` environment variable.
```bash
dokku config:set cloudia-challenge SECRET_KEY=? BOT_TOKEN=? DATABASE_URL=?
```

## SSH with default KEY from dokku user

Verify that the files and permissions are correct.
```
sudo su - dokku
mkdir ~/.ssh
chmod 700 ~/.ssh
touch ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

Retrieve the public key from the private key:
```
ssh-keygen -y -f file.pem
```

Update authorized keys on aws (put the retrieved public key):
```
sudo su - dokku
cat >> .ssh/authorized_keys
```

### SSH Key-Based Authentication from local key

If you already have an SSH key, skip the command below.
```
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Now send your local public key to the server to login to the remote host using public key authentication.
```
cat ~/.ssh/id_rsa.pub | sudo ssh -i file.pem dokku@server_ip "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

Set up a remote repository and push the project to the server.
```
git remote add dokku dokku@your_domain:cloudia-challenge
git push dokku main
```

Set up your domain on the app to configure the reverse proxy.
```
dokku domains:set cloudia-challenge your_domain
```

Enable SSL.
```
sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
dokku config:set --no-restart cloudia-challenge DOKKU_LETSENCRYPT_EMAIL=your@email.tld
sudo dokku letsencrypt:enable cloudia-challenge
```


Now, just set up your bot and have fun. :)
```
https://api.telegram.org/bot<bot_token>/setWebhook?url=<your_domain>/api/telegram/update/
```
