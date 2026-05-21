# Contributing to Task Manager CLI

感谢你对这个项目的兴趣！这是一个学习项目，目标是练习 Python 工程基础和 GitHub 工作流。欢迎任何形式的贡献。

## 项目简介

Task Manager CLI 是一个用 Python 写的终端任务管理工具。用户在命令行输入指令，程序把任务保存到本地 JSON 文件。项目只使用 Python 标准库 + pytest，不引入第三方依赖。

## 本地开发环境设置

### 方式一：本地 Python（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/<your-username>/task-manager-cli.git
cd task-manager-cli

# 2. 创建虚拟环境（推荐）
python3 -m venv .venv
source .venv/bin/activate

# 3. 安装（开发模式）
pip install -e .

# 4. 运行测试，确认环境正常
make test
```

### 方式二：Docker（不需要本地 Python）

```bash
git clone https://github.com/<your-username>/task-manager-cli.git
cd task-manager-cli
docker compose build
docker compose run --rm task pytest -q
```

## 常用 Makefile 命令

```bash
make                      # 查看所有可用命令
make install              # 开发模式安装
make test                 # 运行全部测试
make clean                # 清理 __pycache__ 和 .pytest_cache
make docker-build         # 构建 Docker 镜像
make compose-build        # Docker Compose 构建镜像
make compose-list         # Docker 内列出任务
make compose-add TITLE="买菜"  # Docker 内添加任务
```

## Git 分支命名规则

从 `main` 分支创建新分支，分支名应体现用途：

| 类型 | 命名格式 | 示例 |
|------|----------|------|
| 新功能 | `feat/简短描述` | `feat/search-command` |
| 修复 Bug | `fix/简短描述` | `fix/empty-title-crash` |
| 文档 | `docs/简短描述` | `docs/add-contributing` |
| 测试 | `test/简短描述` | `test/cli-edge-cases` |
| 重构 | `refactor/简短描述` | `refactor/storage-module` |

## Pull Request 流程

1. **从 `main` 创建分支**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feat/你的功能名
   ```

2. **开发并测试**
   ```bash
   # 写代码……
   make test  # 确保测试通过
   ```

3. **提交代码**
   ```bash
   git add <修改的文件>
   git commit -m "feat: 添加搜索功能"
   ```

4. **推送到 GitHub 并创建 PR**
   ```bash
   git push origin feat/你的功能名
   ```
   然后在 GitHub 上创建 Pull Request。

### PR 描述应包含

- **做了什么**：简要说明改动内容
- **为什么**：解释动机或解决的问题
- **改了哪些文件**：列出主要变更文件
- **手动验证**：如何测试这个改动

### Commit Message 格式

```
类型: 简短描述
```

类型包括：
- `feat` — 新功能
- `fix` — 修复 Bug
- `docs` — 文档变更
- `test` — 测试相关
- `refactor` — 重构（不改变行为）
- `chore` — 构建、依赖等杂项

示例：
```
feat: 添加 task search 命令
fix: 修复空标题导致的崩溃
docs: 新增 CONTRIBUTING.md
```

## 提交前检查清单

在创建 PR 之前，请确认以下事项：

- [ ] `make test` 全部通过
- [ ] 没有引入第三方依赖（只用标准库 + pytest）
- [ ] 新增代码有类型注解
- [ ] 新增功能有对应测试
- [ ] commit message 符合格式规范
- [ ] 没有提交不该提交的文件（见下方）

## 不应该提交的文件

以下是不该出现在 Git 仓库中的文件：

| 文件/目录 | 原因 |
|-----------|------|
| `tasks.json` | 本地数据文件，每人不同 |
| `__pycache__/` | Python 编译缓存 |
| `.pytest_cache/` | pytest 缓存 |
| `*.egg-info/` | pip 安装生成的元数据 |
| `.venv/` | 虚拟环境 |
| `.env` | 环境变量（如果有） |

这些文件已经在 `.gitignore` 中，正常情况下不会被提交。如果你发现某个文件应该被忽略但没有，请提 Issue。

## CI 必须通过

每次 push 和 Pull Request 都会触发 GitHub Actions，自动运行：

1. 设置 Python 3.11 环境
2. 安装依赖
3. 运行 `make test`

**CI 不通过的 PR 不会被合并。** 请在本地先跑 `make test` 确认通过再推送。

## 有问题？

- **Bug 报告**：在 GitHub Issues 中提交，描述复现步骤
- **功能建议**：在 GitHub Issues 中提交，说明你的想法
- **不确定怎么开始**：先在 Issues 中讨论，再动手写代码

感谢你的贡献！
