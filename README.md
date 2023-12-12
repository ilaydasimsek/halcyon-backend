## Setup
### 1. Create docker network
```bash
docker network create halcyon-external
```

### 2. Set env variables
```bash
cp .env.example .env
```

## Development

### How to update packages
```bash
pip-compile requirements.in && pip-compile requirements-dev.in
```

### Setup pre-commit
```bash
pip install pre-commit
pre-commit install
```

### Run tests
```bash
# Run in the docker container
./manage.py test
```

### Populate test data
```bash
# Run in the docker container
./manage.py populate_test_data
```

### How to deploy
https://fly.io/docs/hands-on/install-flyctl/
```bash
flyctl deploy --dockerfile deployment/Dockerfile
```
