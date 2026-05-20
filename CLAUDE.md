# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Task Manager CLI — 用 Python 写的终端任务管理工具。用户在命令行输入指令，程序把任务保存到本地 JSON 文件。

## 学习目标

这是一个练习项目，目标是：
1. 补齐 Python 工程基础
2. 学会 Git 和 GitHub 工作流
3. 学会让 Claude Code 先规划、再实现、再测试

## MVP 命令

```
task add "买菜"              # 添加任务
task list                    # 列出所有任务
task done 1                  # 标记任务为完成
task remove 1                # 删除任务
task clear --yes             # 清空所有任务
```

## 文件结构

```
src/task_manager/
├── cli.py          # 入口，解析命令行参数（argparse）
├── models.py       # Task 数据结构
└── storage.py      # 读写 JSON 文件
tests/
└── test_storage.py # storage 模块的测试（已实现）
Makefile            # 常用开发命令快捷方式
compose.yaml        # Docker Compose 配置，简化容器命令
```

> `tests/test_cli.py` 尚未创建，计划后续补充 CLI 层的测试。

## 开发命令

```bash
# 安装（开发模式）
pip install -e .

# 运行
task list
task add "买菜"

# 测试
pytest

# 测试单个文件
pytest tests/test_storage.py

# 测试单个函数
pytest tests/test_storage.py::test_save_and_load

# Docker Compose（推荐，自动持久化数据到 volume）
docker compose run --rm task task add "买菜"
docker compose run --rm task task list
docker compose run --rm task pytest -q

# Makefile 快捷命令（优先使用）
make                      # 查看所有可用 target
make install              # 开发模式安装
make test                 # 运行全部测试
make compose-list         # Docker 内列出任务
make compose-add TITLE="买菜" # Docker 内添加任务
make compose-build        # Docker Compose 构建镜像
make docker-build         # Docker 构建镜像
make clean                # 清理缓存
```

## 技术栈

- Python 3.10+
- argparse（命令行解析）
- json（数据存储）
- pytest（测试）
- pathlib（文件路径）

## 协作规则

1. **先计划再动手** — 修改代码前必须先给出计划，说明要改什么、为什么改、涉及哪些文件。
2. **每次实现后告诉手动测试方法** — 完成改动后，必须提供用户可以手动执行的测试步骤。
3. **只用标准库和 pytest** — 第一版只使用 Python 标准库 + pytest，不引入第三方依赖。
4. **不要自动 commit** — 不要自动执行 `git commit`，由用户决定何时提交。
5. **不要引入复杂功能** — 不引入数据库、前端、AI 功能，保持项目简单。
6. **新增依赖前必须说明** — 如需新增第三方依赖，必须先说明原因，等用户确认后再加。
7. **每次修改后解释改动** — 每次改动后，说明修改了哪些文件、做了什么改动。
8. **提交前必须通过测试** — `make test` 必须全部通过，CI 会在每次 push 时自动运行测试。
