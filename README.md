# Assignment

Django based server with all the requested API

---

## Overview

This server provides:

- Authentication API for both client and operation user
- Scripts to create new operation users
- API to allow operation user to upload new files
- API to allow clients to list uploaded files and get secure signed download links

It is built with:

- **Django** + **Python**
- **PostgreSQL** for database
- **Celery** for message queue
- **Redis** for message broker and caching content
- **Image Kit** for cloud storage of files

---

## Table of Contents

- [API Documentation](./docs/api.md)
- [Local Setup](./docs/setup.md)
- [Deployment](./docs/deployment.md)
