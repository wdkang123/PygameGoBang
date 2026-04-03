# 部署指南

## 目录

- [环境要求](#环境要求)
- [本地开发部署](#本地开发部署)
- [桌面应用部署](#桌面应用部署)
- [API 服务部署](#api-服务部署)
- [CI/CD 部署](#cicd-部署)
- [生产环境注意事项](#生产环境注意事项)

---

## 环境要求

| 依赖 | 版本要求 |
|------|----------|
| Python | >= 3.10 |
| pip | >= 21.0 |
| 操作系统 | macOS / Linux / Windows |

---

## 本地开发部署

### 1. 克隆项目

```bash
git clone https://github.com/wdkang123/PygameGoBang.git
cd PygameGoBang
```

### 2. 创建虚拟环境（推荐）

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows
```

### 3. 安装依赖

```bash
# 仅运行时依赖
pip install -e .

# 开发依赖（含测试、lint 工具）
pip install -e ".[dev]"
```

### 4. 验证安装

```bash
make test    # 运行测试
make check   # format + lint + test
```

---

## 桌面应用部署

### 快速启动

```bash
# 人机对战（人类执黑先行）
python -m pygobang.app.main --opponent heuristic

# 人机对战（人类执黑 vs Minimax 深度4）
python -m pygobang.app.main --opponent minimax --depth 4

# 双人同机对战
python -m pygambang.app.main
```

### 桌面应用构建说明

当前为源码运行模式，无独立可执行文件。如需构建：

**macOS/Linux 打包为可执行文件：**

```bash
pip install pyinstaller
pyinstaller --onefile --name PygameGoBang \
  --add-data "configs:configs" \
  src/pygobang/app/main.py
```

生成的 `dist/PygameGoBang` 即为可执行文件。

**Windows 打包：**

```bash
pyinstaller --onefile --name PygameGoBang ^
  --add-data "configs;configs" ^
  src\pygobang\app\main.py
```

---

## API 服务部署

### 本地启动

```bash
# 方式一：使用 Makefile
make api

# 方式二：直接运行
python scripts/run_api.py

# 方式三：uvicorn 模块方式
uvicorn pygobang.api.app:app --host 0.0.0.0 --port 8000
```

启动后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Docker 部署

#### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY scripts/ scripts/
COPY configs/ configs/

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["python", "scripts/run_api.py"]
```

#### 构建与运行

```bash
docker build -t pygobang-api .
docker run -d -p 8000:8000 --name pygobang-api pygobang-api
```

#### Docker Compose（推荐）

```yaml
version: "3.8"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

```bash
docker-compose up -d
docker-compose logs -f api
```

### 生产环境反向代理

**Nginx 配置：**

```nginx
upstream pygobang_api {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://pygobang_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket 支持（未来扩展）
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # API 文档（可选限制）
    location /docs {
        proxy_pass http://pygobang_api;
    }
}
```

**启用 HTTPS（Let's Encrypt）：**

```bash
certbot --nginx -d your-domain.com
```

---

## CI/CD 部署

### GitHub Actions

CI 配置已存在于 `.github/workflows/ci.yml`，包含：

1. 代码格式化检查（black）
2. Lint 检查（ruff + mypy）
3. 单元测试（pytest）
4. Smoke 测试

**添加部署任务到 CI：**

在 `.github/workflows/` 下创建 `deploy.yml`：

```yaml
name: Deploy

on:
  push:
    branches: [master]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install -e .
          pip install -e ".[dev]"

      - name: Run tests
        run: make test

      - name: Build Docker image
        run: |
          docker build -t pygobang-api:${{ github.sha }} .
          docker tag pygobang-api:${{ github.sha }} pygobang-api:latest

      - name: Deploy to server
        env:
          SSH_KEY: ${{ secrets.SSH_KEY }}
          SERVER_HOST: ${{ secrets.SERVER_HOST }}
        run: |
          echo "$SSH_KEY" | tr -d '\r' > deploy_key
          chmod 600 deploy_key
          scp -i deploy_key -o StrictHostKeyChecking=no Dockerfile docker-compose.yml user@$SERVER_HOST:/app/
          ssh -i deploy_key -o StrictHostKeyChecking=no user@$SERVER_HOST "cd /app && docker-compose up -d"
```

### 添加 GitHub Secrets

在 GitHub 仓库 Settings → Secrets 中添加：

| Secret 名称 | 说明 |
|------------|------|
| `SSH_KEY` | 服务器 SSH 私钥 |
| `SERVER_HOST` | 服务器地址（IP 或域名） |

---

## 生产环境注意事项

### 1. 安全

- [ ] 所有网络端口仅对必要地址开放
- [ ] API 使用 HTTPS（TLS 终止于 Nginx）
- [ ] 定期更新依赖：`pip install -U -r requirements.txt`
- [ ] 不在代码中硬编码密钥，使用环境变量或 Secret 管理

### 2. 性能

- [ ] API 服务使用 `uvicorn --workers 4` 多进程
- [ ] 静态文件由 Nginx 直接服务
- [ ] 定期清理 `/tmp` 下的临时 replay 文件

### 3. 监控

```bash
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f api

# 查看资源使用
docker stats
```

### 4. 备份

```bash
# 备份 replay 数据（如果有持久化存储）
tar -czf replays_backup_$(date +%Y%m%d).tar.gz replays/
```

### 5. 更新

```bash
git pull origin master
pip install -U -e .
docker-compose down && docker-compose up -d --build
make test
```

---

## 快速命令参考

```bash
# 安装
pip install -e .

# 开发
make check       # format + lint + test
make test        # 仅测试
make benchmark   # AI 性能基准

# 运行
python -m pygobang.app.main --opponent heuristic   # 桌面 UI
make api                                           # API 服务

# Docker
docker build -t pygobang-api .
docker run -d -p 8000:8000 pygobang-api
```
