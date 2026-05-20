.DEFAULT_GOAL := help

TITLE ?= 学习 Makefile

.PHONY: install test help docker-build compose-build compose-help compose-list compose-add compose-down compose-down-volumes clean

install:                        ## 开发模式安装项目
	pip install -e .

test:                           ## 运行全部测试
	pytest

clean:                          ## 清理 __pycache__ 和 .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

docker-build:                   ## 构建 Docker 镜像
	docker build -t task-manager .

compose-build:                  ## 使用 Docker Compose 构建镜像
	docker compose build

compose-help:                   ## Docker Compose 内显示 task 帮助
	docker compose run --rm task task --help

compose-list:                   ## Docker Compose 内列出所有任务
	docker compose run --rm task task list

compose-add:                    ## Docker Compose 内添加任务，例如: make compose-add TITLE="买菜"
	docker compose run --rm task task add "$(TITLE)"

compose-down:                   ## 停止并移除容器（保留数据）
	docker compose down

compose-down-volumes:           ## 停止容器并删除数据卷（会丢失所有任务数据！）
	docker compose down -v

help:                           ## 显示所有可用命令
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'
