## Setup
### 1. Create docker network
```bash
docker network create halcyon-external
```

### 2. Install black
```bash
pip install black
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