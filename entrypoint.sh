#!/bin/bash

alembic upgrade head

uvicorn src.server:app --host 0.0.0.0 --port 81
