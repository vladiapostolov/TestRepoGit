# VisualStudio Docker

This folder contains a multi-stage `Dockerfile` for a Python 3.12 application.

Quick build and debug commands

Run these from the project root (`/Users/vladimirapostolov/Desktop/VisualStudio`):

```bash
# show the Dockerfile being used
sed -n '1,200p' /Users/vladimirapostolov/Desktop/VisualStudio/Dockerfile

# check Docker version
docker --version

# build the image (explicit Dockerfile path + build context)
docker build -t myapp:latest -f /Users/vladimirapostolov/Desktop/VisualStudio/Dockerfile /Users/vladimirapostolov/Desktop/VisualStudio

# build without cache if you suspect stale state
docker build --no-cache -t myapp:latest -f /Users/vladimirapostolov/Desktop/VisualStudio/Dockerfile /Users/vladimirapostolov/Desktop/VisualStudio
```

Notes

- The Dockerfile defines a `base` stage (`FROM python:3.12-slim AS base`) so later stages referencing `base` won't be interpreted as a remote image named `base`.
- Ensure your build context contains an `app/` directory with `main.py` (or an ASGI app) and `requirements.txt` in the root.
- If you still see "pull access denied for base" then you are likely building a different Dockerfile or an older copy; pass `-f` to `docker build` to be explicit.
