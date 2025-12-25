# Hướng dẫn Setup Chi tiết

## Bước 1: Chuẩn bị môi trường

### 1.1 Kiểm tra Docker

```powershell
docker --version
docker-compose --version
```

Nếu chưa có, download Docker Desktop từ: https://www.docker.com/products/docker-desktop

### 1.2 Kiểm tra Git

```powershell
git --version
```

## Bước 2: Setup Jenkins

### 2.1 Khởi động Jenkins container

```powershell
cd d:\Nodejs\jenkins-cicd
docker-compose up -d
```

**Kiểm tra container đang chạy:**

```powershell
docker ps
```

Bạn sẽ thấy container `jenkins-cicd` đang chạy.

### 2.2 Lấy Initial Admin Password

```powershell
docker exec jenkins-cicd cat /var/jenkins_home/secrets/initialAdminPassword
```

Copy password này.

### 2.3 Truy cập Jenkins UI

1. Mở browser: `http://localhost:8080`
2. Paste initial admin password
3. Click **Continue**

### 2.4 Cài đặt Plugins

1. Chọn **Install suggested plugins**
2. Đợi plugins cài đặt (khoảng 5-10 phút)

### 2.5 Tạo Admin User

Điền thông tin:
- Username: `admin`
- Password: `<your-password>`
- Full name: `Admin`
- Email: `<your-email>`

Click **Save and Continue**

### 2.6 Jenkins URL

Giữ nguyên: `http://localhost:8080`

Click **Save and Finish** → **Start using Jenkins**

## Bước 3: Cài đặt Docker Plugin

### 3.1 Vào Plugin Manager

1. Click **Manage Jenkins** (sidebar)
2. Click **Manage Plugins**

### 3.2 Install Docker Pipeline Plugin

1. Tab **Available**
2. Tìm kiếm: `Docker Pipeline`
3. Check ✓ **Docker Pipeline**
4. Click **Install without restart**

### 3.3 Cài đặt Docker trong Jenkins container (nếu cần)

```powershell
# Vào container
docker exec -it -u root jenkins-cicd bash

# Cài đặt Docker CLI
apt-get update
apt-get install -y docker.io

# Kiểm tra
docker --version

# Exit
exit
```

## Bước 4: Tạo Jenkins Pipeline Job

### 4.1 Tạo Job mới

1. Click **New Item** (sidebar)
2. Enter name: `flask-cicd-pipeline`
3. Chọn **Pipeline**
4. Click **OK**

### 4.2 Configure Job

#### General Section

- ✓ Check **GitHub project**
- Project url: `https://github.com/<username>/<repo-name>/`

#### Build Triggers Section

- ✓ Check **GitHub hook trigger for GITScm polling**

#### Pipeline Section

- **Definition**: Chọn `Pipeline script from SCM`
- **SCM**: Chọn `Git`
- **Repository URL**: `https://github.com/<username>/<repo-name>.git`
- **Credentials**: 
  - Click **Add** → **Jenkins**
  - Kind: `Username with password`
  - Username: `<github-username>`
  - Password: `<github-personal-access-token>`
  - ID: `github-credentials`
  - Click **Add**
  - Chọn credentials vừa tạo
- **Branches to build**: `*/main` (hoặc `*/master`)
- **Script Path**: `Jenkinsfile`

Click **Save**

## Bước 5: Setup ngrok

### 5.1 Download ngrok

**Option 1: Download trực tiếp**
- Vào: https://ngrok.com/download
- Download Windows version
- Giải nén vào folder (ví dụ: `C:\ngrok`)

**Option 2: Dùng Chocolatey**

```powershell
choco install ngrok
```

### 5.2 Tạo ngrok account

1. Vào: https://dashboard.ngrok.com/signup
2. Sign up (free tier)
3. Vào Dashboard → **Your Authtoken**
4. Copy authtoken

### 5.3 Authenticate ngrok

```powershell
ngrok config add-authtoken <your-authtoken>
```

### 5.4 Khởi động ngrok tunnel

```powershell
ngrok http 8080
```

**Output sẽ như:**

```
Session Status                online
Account                       <your-email>
Version                       3.x.x
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://xxxx-xxxx-xxxx.ngrok-free.app -> http://localhost:8080

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**Copy URL**: `https://xxxx-xxxx-xxxx.ngrok-free.app`

⚠️ **LƯU Ý**: Giữ terminal này mở, đừng tắt!

### 5.5 Test ngrok

Mở browser: `https://xxxx-xxxx-xxxx.ngrok-free.app`

Bạn sẽ thấy Jenkins UI.

## Bước 6: Setup GitHub Webhook

### 6.1 Tạo GitHub Personal Access Token (nếu chưa có)

1. GitHub → **Settings** → **Developer settings**
2. **Personal access tokens** → **Tokens (classic)**
3. **Generate new token (classic)**
4. Scopes:
   - ✓ `repo` (full control)
   - ✓ `admin:repo_hook`
5. Click **Generate token**
6. Copy token (lưu lại, chỉ hiện 1 lần)

### 6.2 Add Webhook

1. Vào repository → **Settings** → **Webhooks**
2. Click **Add webhook**
3. **Payload URL**: `https://xxxx-xxxx-xxxx.ngrok-free.app/github-webhook/`
   - ⚠️ **QUAN TRỌNG**: Phải có dấu `/` ở cuối!
4. **Content type**: `application/json`
5. **Secret**: Để trống (hoặc tạo secret nếu muốn)
6. **Which events would you like to trigger this webhook?**
   - Chọn: **Just the push event**
7. ✓ Check **Active**
8. Click **Add webhook**

### 6.3 Verify Webhook

1. Webhook vừa tạo sẽ có dấu ✓ màu xanh nếu thành công
2. Click vào webhook → Tab **Recent Deliveries**
3. Sẽ thấy ping event với status `200`

## Bước 7: Push Code lên GitHub

### 7.1 Initialize Git (nếu chưa có)

```powershell
cd d:\Nodejs\jenkins-cicd
git init
git add .
git commit -m "Initial commit: Flask CI/CD setup"
```

### 7.2 Add Remote và Push

```powershell
git remote add origin https://github.com/<username>/<repo-name>.git
git branch -M main
git push -u origin main
```

## Bước 8: Test CI/CD Pipeline

### 8.1 Test Manual Build

1. Vào Jenkins → Job `flask-cicd-pipeline`
2. Click **Build Now**
3. Xem progress trong **Build History**
4. Click vào build number → **Console Output**

**Kết quả mong đợi:**

```
✓ Pipeline completed successfully!
Application is running at: http://localhost:5000
Version: 1-20251225-144500
```

### 8.2 Test Webhook Trigger

1. Sửa file `app.py`:

```python
'message': 'Chào mừng đến với Flask CI/CD Demo - Updated!',
```

2. Commit và push:

```powershell
git add app.py
git commit -m "Update welcome message"
git push origin main
```

3. **Kiểm tra Jenkins**:
   - Vào Jenkins UI
   - Job sẽ tự động trigger (trong vài giây)
   - Xem Console Output

4. **Kiểm tra Application**:

```powershell
curl http://localhost:5000
```

Hoặc mở browser: `http://localhost:5000`

## Bước 9: Verify Deployment

### 9.1 Kiểm tra Container

```powershell
# List containers
docker ps

# Kiểm tra logs
docker logs flask-app

# Kiểm tra image
docker images flask-demo
```

### 9.2 Test API Endpoints

```powershell
# Health check
curl http://localhost:5000/health

# Info
curl http://localhost:5000/api/info

# Home
curl http://localhost:5000
```

## Troubleshooting

### Issue 1: Jenkins không build được Docker image

**Error**: `docker: command not found`

**Solution**:

```powershell
docker exec -it -u root jenkins-cicd bash
apt-get update && apt-get install -y docker.io
exit
```

### Issue 2: Permission denied khi build

**Error**: `Got permission denied while trying to connect to the Docker daemon socket`

**Solution**:

```powershell
docker exec -it -u root jenkins-cicd bash
chmod 666 /var/run/docker.sock
exit
```

### Issue 3: Webhook không trigger

**Kiểm tra**:

1. ngrok có đang chạy không?
2. GitHub webhook có status 200 không?
3. Jenkins job có enable "GitHub hook trigger" không?

**Debug**:

```powershell
# Xem ngrok requests
# Mở browser: http://localhost:4040
```

### Issue 4: Port 5000 đã được sử dụng

**Kiểm tra**:

```powershell
netstat -ano | findstr :5000
```

**Stop process**:

```powershell
# Lấy PID từ lệnh trên
taskkill /PID <PID> /F
```

## Hoàn thành! 🎉

Bây giờ bạn đã có một CI/CD pipeline hoàn chỉnh:

1. ✅ Push code → GitHub
2. ✅ Webhook → ngrok → Jenkins
3. ✅ Jenkins build Docker image
4. ✅ Deploy container tự động
5. ✅ Application running tại `http://localhost:5000`
