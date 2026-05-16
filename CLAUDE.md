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
```

## 文件结构

```
src/task_manager/
├── cli.py          # 入口，解析命令行参数（argparse）
├── storage.py      # 读写 JSON 文件
└── models.py       # Task 数据结构
tests/
├── test_cli.py
└── test_storage.py
```

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
pytest tests/test_storage.py::test_add_task
```

## 技术栈

- Python 3.10+
- argparse（命令行解析）
- json（数据存储）
- pytest（测试）
- pathlib（文件路径）
