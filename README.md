## Setup
### 1. Create docker network
```bash
docker network create halcyon-external
```

### 2. Install black
```bash
pip install black
```

### 3. Set env variables
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
