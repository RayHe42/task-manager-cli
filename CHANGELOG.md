# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [0.2.0] - 2026-05-21

### Added
- Input validation: reject empty or whitespace-only task titles
- Docker support with Dockerfile (python:3.12-slim)
- Docker Compose for simplified container commands
- Docker volume persistence for task data across container runs
- Makefile for common development commands (install, test, clean, docker)
- GitHub Actions CI workflow (Python 3.11 on Ubuntu)
- CONTRIBUTING.md with branching, PR, and commit conventions
- Developer setup documentation
- .gitignore for Python cache and build artifacts

## [0.1.0] - 2026-05-17

### Added
- Basic task manager CLI with add, list, done, remove, clear commands
- Task list filtering by status (`--todo` / `--done`)
- JSON file storage with auto-incrementing task IDs
- Input validation for empty task titles
- Installable `task` command via pyproject.toml
- Unit tests for storage module
- CLI integration tests
