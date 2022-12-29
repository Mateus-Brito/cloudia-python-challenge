# Cloudia  challenge Solution.

Read more about the challenge here: [Cloudia Ppython](https://github.com/cloudiabot/cloudia_python)

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

```python
https://api.telegram.org/bot<bot_token>/setWebhook?url=<your_domain>/api/telegram/update/
```
