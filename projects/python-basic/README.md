# Python Basic - Jupyter Environment

A Jupyter-based environment for learning Python fundamentals and data engineering basics.

## Quick Start

```bash
cd projects/python-basic
make up
```

Open [http://localhost:8888](http://localhost:8888) in your browser.

## Make Commands

| Command        | Description                    |
|----------------|--------------------------------|
| `make up`      | Start Jupyter container        |
| `make down`    | Stop Jupyter container         |
| `make build`   | Build Docker image             |
| `make restart` | Restart container              |
| `make logs`    | View container logs            |
| `make shell`   | Open bash shell in container   |
| `make clean`   | Remove container and image     |
| `make help`    | Show all available commands    |

## Directory Structure

```
python-basic/
├── Makefile             # Make commands
├── Dockerfile           # Python + Jupyter image
├── docker-compose.yml   # Container orchestration
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── notebooks/           # Jupyter notebooks (mounted volume)
    └── 01_getting_started.ipynb
```

## VSCode/Cursor Integration

You can also open `.ipynb` files directly in Cursor with the Jupyter extension.
