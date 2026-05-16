# Task Manager CLI

用 Python 写的终端任务管理工具。

## 功能

```
task add "买菜"              # 添加任务
task list                    # 列出所有任务
task done 1                  # 标记任务为完成
task remove 1                # 删除任务
```

## 安装

```bash
pip install -e .
```

## 使用

```bash
task add "学习 Python"
task list
task done 1
```

## 运行测试

```bash
pytest
```
