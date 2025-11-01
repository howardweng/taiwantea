# Docker Hub 部署指南

本文件說明如何使用 Docker Hub 部署 TAIWANTEA 到生產環境。

## 🏗️ 架構概覽

```
[本機開發] → [Docker Hub] → [生產伺服器]
     ↓             ↓                ↓
   建置映像      儲存映像         拉取並運行
```

**Docker Hub 映像**: `howardweng/taiwantea:latest`
**生產伺服器**: `128.199.112.130` (taiwantea.frrut.com)
**容器名稱**: `taiwantea-app`
**端口**: `7070`

---

## 🚀 快速開始

### 方法 1: 完整部署（建置 + 推送 + 部署）

當您有程式碼變更時使用：

```bash
./deploy-to-production.sh
```

這個腳本會：
1. ✅ 建置 Docker 映像
2. ✅ 推送到 Docker Hub
3. ✅ SSH 到生產伺服器
4. ✅ 拉取最新映像
5. ✅ 重啟容器
6. ✅ 驗證部署

### 方法 2: 快速部署（僅重啟容器）

當映像已經在 Docker Hub，只需要重啟：

```bash
./quick-deploy.sh
```

這個腳本會：
1. ✅ 在遠端伺服器拉取最新映像
2. ✅ 重啟容器

---

## 📋 部署前準備

### 1. Docker Hub 登入

確保已登入 Docker Hub：

```bash
docker login
```

輸入帳號密碼：
- Username: `howardweng`
- Password: [您的 Docker Hub 密碼]

### 2. SSH 連線測試

確保可以 SSH 到生產伺服器：

```bash
ssh databack "echo 'Connection successful'"
```

如果失敗，檢查 `~/.ssh/config` 中的 `databack` 配置。

### 3. 確認環境變數

檢查生產環境變數（已在腳本中配置）：

```bash
# MongoDB URL
MONGODB_URL=mongodb://datavanadmin:datavanabcbvf@172.17.0.1:2700/taiwantea?authSource=admin

# Allowed Origins
ALLOWED_ORIGINS=https://taiwantea.frrut.com,http://128.199.112.130:7070

# Secret Key (建議更換為更安全的值)
SECRET_KEY=taiwantea-prod-secret-key-change-this
```

---

## 📦 手動部署步驟

如果自動化腳本失敗，可以手動執行：

### 步驟 1: 本機建置並推送

```bash
# 建置映像
docker build -t howardweng/taiwantea:latest .

# 推送到 Docker Hub
docker push howardweng/taiwantea:latest
```

### 步驟 2: SSH 到生產伺服器

```bash
ssh databack
```

### 步驟 3: 更新容器

```bash
# 拉取最新映像
docker pull howardweng/taiwantea:latest

# 停止舊容器
docker stop taiwantea-app

# 刪除舊容器
docker rm taiwantea-app

# 啟動新容器
docker run -d \
    --name taiwantea-app \
    --restart unless-stopped \
    -p 7070:7070 \
    -v /root/taiwantea/uploads:/app/uploads \
    -v /root/taiwantea/logs:/app/logs \
    -e "MONGODB_URL=mongodb://datavanadmin:datavanabcbvf@172.17.0.1:2700/taiwantea?authSource=admin" \
    -e "DATABASE_NAME=taiwantea" \
    -e "SECRET_KEY=taiwantea-prod-secret-key-change-this" \
    -e "JWT_ALGORITHM=HS256" \
    -e "ACCESS_TOKEN_EXPIRE_MINUTES=15" \
    -e "ALLOWED_ORIGINS=https://taiwantea.frrut.com,http://128.199.112.130:7070" \
    -e "ENVIRONMENT=production" \
    howardweng/taiwantea:latest
```

### 步驟 4: 驗證部署

```bash
# 檢查容器狀態
docker ps | grep taiwantea-app

# 檢查日誌
docker logs --tail 50 taiwantea-app

# 測試健康檢查
curl http://localhost:7070/api/health
```

---

## 🔄 版本管理

### 使用語義化版本

您可以為特定版本打標籤：

```bash
# 部署特定版本
./deploy-to-production.sh v1.2.3
```

這會建立兩個標籤：
- `howardweng/taiwantea:v1.2.3`
- `howardweng/taiwantea:latest`

### 查看所有版本

```bash
# 在 Docker Hub 查看
# https://hub.docker.com/r/howardweng/taiwantea/tags

# 或在伺服器上
ssh databack "docker images | grep taiwantea"
```

### 回滾到特定版本

```bash
ssh databack
docker stop taiwantea-app
docker rm taiwantea-app
docker run -d \
    --name taiwantea-app \
    --restart unless-stopped \
    -p 7070:7070 \
    -v /root/taiwantea/uploads:/app/uploads \
    -v /root/taiwantea/logs:/app/logs \
    -e "MONGODB_URL=mongodb://datavanadmin:datavanabcbvf@172.17.0.1:2700/taiwantea?authSource=admin" \
    -e "DATABASE_NAME=taiwantea" \
    -e "SECRET_KEY=taiwantea-prod-secret-key-change-this" \
    -e "JWT_ALGORITHM=HS256" \
    -e "ACCESS_TOKEN_EXPIRE_MINUTES=15" \
    -e "ALLOWED_ORIGINS=https://taiwantea.frrut.com,http://128.199.112.130:7070" \
    -e "ENVIRONMENT=production" \
    howardweng/taiwantea:v1.2.2  # 指定舊版本
```

---

## 🔧 常用管理命令

### 遠端操作

```bash
# 查看容器狀態
ssh databack "docker ps | grep taiwantea"

# 查看即時日誌
ssh databack "docker logs -f taiwantea-app"

# 查看最近 100 行日誌
ssh databack "docker logs --tail 100 taiwantea-app"

# 重啟容器
ssh databack "docker restart taiwantea-app"

# 停止容器
ssh databack "docker stop taiwantea-app"

# 進入容器 shell
ssh databack "docker exec -it taiwantea-app bash"

# 檢查容器資源使用
ssh databack "docker stats taiwantea-app --no-stream"
```

### 清理舊映像

```bash
# 在遠端伺服器清理未使用的映像
ssh databack "docker image prune -f"

# 查看所有映像
ssh databack "docker images"

# 刪除特定映像
ssh databack "docker rmi howardweng/taiwantea:old-version"
```

---

## 🐛 故障排除

### 問題 1: 無法推送到 Docker Hub

**錯誤訊息**: `denied: requested access to the resource is denied`

**解決方法**:
```bash
# 重新登入 Docker Hub
docker logout
docker login
```

### 問題 2: SSH 連線失敗

**錯誤訊息**: `Connection timeout` 或 `Permission denied`

**解決方法**:
```bash
# 檢查 SSH 配置
cat ~/.ssh/config | grep -A 3 databack

# 測試直接連線
ssh root@128.199.112.130

# 檢查 SSH 金鑰
ls -la ~/.ssh/
```

### 問題 3: 容器啟動失敗

**症狀**: 容器立即退出

**解決方法**:
```bash
# 查看錯誤日誌
ssh databack "docker logs taiwantea-app"

# 檢查 MongoDB 連線
ssh databack "docker exec taiwantea-app curl -f http://localhost:7070/api/health"

# 檢查環境變數
ssh databack "docker inspect taiwantea-app | grep -A 20 Env"
```

### 問題 4: 健康檢查失敗

**症狀**: 無法訪問 `/api/health`

**解決方法**:
```bash
# 檢查容器是否運行
ssh databack "docker ps | grep taiwantea"

# 檢查端口綁定
ssh databack "docker port taiwantea-app"

# 從伺服器內部測試
ssh databack "curl http://localhost:7070/api/health"

# 檢查 Nginx 代理設定（如果使用）
ssh databack "docker exec -it root-app-1 cat /etc/nginx/conf.d/*.conf | grep 7070"
```

### 問題 5: MongoDB 連線失敗

**錯誤訊息**: `Failed to connect to MongoDB`

**解決方法**:
```bash
# 檢查 MongoDB 容器狀態
ssh databack "docker ps | grep mongo"

# 測試 MongoDB 連線
ssh databack "docker exec -it mongo2700 mongosh --eval 'db.version()'"

# 檢查網路連通性
ssh databack "docker exec taiwantea-app ping -c 3 172.17.0.1"
```

---

## 📊 監控與日誌

### 即時監控

```bash
# 容器資源使用
ssh databack "docker stats taiwantea-app"

# 容器健康狀態
watch -n 5 'ssh databack "docker ps | grep taiwantea"'

# API 健康檢查
watch -n 10 'curl -s https://taiwantea.frrut.com/api/health | jq'
```

### 日誌管理

```bash
# 查看特定時間範圍的日誌
ssh databack "docker logs --since 1h taiwantea-app"

# 過濾錯誤日誌
ssh databack "docker logs taiwantea-app 2>&1 | grep -i error"

# 導出日誌
ssh databack "docker logs taiwantea-app > /tmp/taiwantea.log 2>&1"
scp databack:/tmp/taiwantea.log ./logs/
```

### 持久化日誌位置

伺服器上的日誌檔案位置：
- 應用日誌: `/root/taiwantea/logs/`
- 容器日誌: `docker logs taiwantea-app`

---

## 🔒 安全建議

### 1. 更新 SECRET_KEY

目前的 SECRET_KEY 應該更換為更安全的值：

```bash
# 生成新的 secret key
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# 更新 deploy-to-production.sh 中的 SECRET_KEY 變數
```

### 2. 環境變數管理

考慮使用環境變數檔案而不是直接在腳本中：

```bash
# 建立 .env.production 檔案（不要提交到 git）
echo "SECRET_KEY=your-secret-here" > .env.production
echo "MONGODB_URL=..." >> .env.production

# 修改腳本讀取 .env.production
```

### 3. 最小權限原則

考慮建立專用的部署使用者而不是使用 root：

```bash
# 在伺服器上建立部署使用者
ssh databack "useradd -m -s /bin/bash deployer"
ssh databack "usermod -aG docker deployer"
```

### 4. 啟用 HTTPS

確保只透過 HTTPS 訪問生產環境：
- ✅ 已配置: `https://taiwantea.frrut.com`
- ⚠️ HTTP 端口 7070 僅用於內部

---

## 📝 部署檢查清單

在每次部署前檢查：

- [ ] 所有測試通過 (`pytest` 和 `npm test`)
- [ ] 已登入 Docker Hub (`docker login`)
- [ ] 可以 SSH 到生產伺服器 (`ssh databack`)
- [ ] 已備份重要資料（如有需要）
- [ ] 通知團隊成員即將部署
- [ ] 準備好回滾計劃

部署後驗證：

- [ ] 容器狀態正常 (`docker ps`)
- [ ] 健康檢查通過 (`curl /api/health`)
- [ ] 前端可以訪問
- [ ] 管理後台可以登入
- [ ] 產品圖片正常顯示
- [ ] 檢查錯誤日誌 (`docker logs`)

---

## 🎯 最佳實踐

### 1. 使用語義化版本

```bash
# 主要版本變更（Breaking changes）
./deploy-to-production.sh v2.0.0

# 次要版本變更（New features）
./deploy-to-production.sh v1.1.0

# 修訂版本變更（Bug fixes）
./deploy-to-production.sh v1.0.1
```

### 2. 在測試環境先測試

在部署到生產前，先在本機或測試環境驗證：

```bash
# 本機測試
docker run -d -p 7070:7070 \
    -e "MONGODB_URL=..." \
    howardweng/taiwantea:latest

# 訪問測試
curl http://localhost:7070/api/health
```

### 3. 保留映像歷史

保留最近 5 個版本的映像，以便快速回滾：

```bash
# 列出所有版本
ssh databack "docker images | grep taiwantea"

# 只刪除很舊的版本
ssh databack "docker image prune -a --filter 'until=720h'"
```

### 4. 建立部署記錄

在 `docs/DEPLOYMENT_LOG.md` 記錄每次部署：

```markdown
## 2025-11-01

- **版本**: v1.2.0
- **部署者**: datavan
- **變更內容**: 新增 SEO 優化功能
- **狀態**: 成功
- **注意事項**: sitemap.xml 已更新
```

---

## 🔗 相關文件

- [DEPLOYMENT.md](../DEPLOYMENT.md) - 原始部署指南（直接在伺服器建置）
- [README.md](../README.md) - 專案概覽
- [TESTING.md](TESTING.md) - 測試指南
- [docker-compose.production.yml](../docker-compose.production.yml) - Docker Compose 配置

---

## 🆘 獲取協助

遇到問題？

1. 查看本文件的「故障排除」章節
2. 檢查容器日誌: `ssh databack "docker logs taiwantea-app"`
3. 查看 [GitHub Issues](https://github.com/howardweng/taiwantea/issues)
4. 聯繫團隊成員

---

**最後更新**: 2025-11-01
**維護者**: datavan
