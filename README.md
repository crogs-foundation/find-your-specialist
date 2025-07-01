# Find Your Specialist (FYS)

![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![Ruff](https://img.shields.io/badge/style-ruff-%23cc66cc.svg?logo=ruff&logoColor=white)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen.svg)

---

## Table of Contents

- [Requirements](#requirements)
- [Before You Start](#before-you-start)
- [Quick Start](#quick-start)
  - [Setup](#setup)
  - [Production](#production)
  - [Development](#development)
- [Repository Structure](#repository-structure)

---

## Requirements

- Tested on **Fedora Linux 42**
- Requires **Python 3.13**
- All dependencies are listed in [`pyproject.toml`](./pyproject.toml)

---

## Before You Start

Install all dependencies using [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Enable pre-commit hooks for auto-formatting/linting:

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

---

## Quick Start

### Setup

> \[!IMPORTANT]
> Make sure that you have installed all the python dependencies (check [Before You Start](#before-you-start) for details)

Setup project using script:

- **Windows**:

  ```powershell
  ./setup.bat
  ```

- **Linux**:

  ```bash
  bash ./setup.sh
  ```

Or run corresponding python script:

```bash
uv run ./src/setup.py
```

> \[!WARNING]
> When setting up using script, you can not pass any flags. For flag description run: `uv run ./src/setup.py -h`

### Production

Start everything together:

- **Windows**:

  ```powershell
  ./run_prod.bat
  ```

- **Linux**:

  ```bash
  bash ./run_prod.sh
  ```

Or start frontend/backend separately:

- **Backend**:

  ```bash
  uv run fastapi run
  ```

- **Frontend**:

  ```bash
  cd frontend
  yarn build
  yarn start
  ```

---

### Development

Start everything together:

- **Windows**:

  ```powershell
  ./run_dev.bat
  ```

- **Linux**:

  ```bash
  bash ./run_dev.sh
  ```

Or start frontend/backend separately:

- **Backend**:

  ```bash
  uv run fastapi dev
  ```

- **Frontend**:

  ```bash
  cd frontend
  yarn dev
  ```

---

## Repository Structure

```text
.
├── frontend/                  # Next.js frontend application
│
├── src/                       # Main source code
│   ├── notebooks/             # Jupyter notebooks
│   │   ├── *.ipynb
│   │
│   ├── pipeline.py             # Complete pipelines
│   ├── rag_local.py            # RAG with local models
│   ├── rag.py                  # RAG with API
│   ├── setup.py                # Main setup file
│   └── utils.py
│
├── .env                       # Environment variables
├── .env.example               # Example environment template
├── .gitignore
├── .pre-commit-config.yaml    # Pre-commit hooks config
├── .python-version
├── main.py                    # FastAPI backend application
├── presentation.pdf           # Project presentation
├── pyproject.toml             # Dependency and tool config
├── uv.lock
└── README.md                  # Project documentation (this file)
```
