# 快速开始指南

## 1. 环境准备

### 后端环境
```bash
# Python 3.11+
python --version

# 安装依赖
cd backend
pip install -r requirements.txt
# 或使用 uv
uv pip install -r requirements.txt
```

### 前端环境
```bash
# Node.js 18+
node --version

# pnpm
npm install -g pnpm

# 安装依赖
cd frontend
pnpm install
```

## 2. 配置

### 配置 Minimax API
```bash
cd backend
cp .env.example .env
# 编辑 .env 文件，填入你的 API Key
```

## 3. 启动项目

### 方式一：分别启动

**终端 1 - 启动后端：**
```bash
cd backend
python init_data.py  # 首次运行，初始化数据
python run.py        # 启动服务
```

**终端 2 - 启动前端：**
```bash
cd frontend
pnpm dev
```

### 方式二：使用启动脚本
```bash
chmod +x start.sh
./start.sh
```

## 4. 访问应用

- 前端页面：http://localhost:5173
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

## 5. 常见问题

### Q: 后端启动报错 ModuleNotFoundError?
A: 确保已安装所有依赖 `pip install -r requirements.txt`

### Q: 前端无法连接后端 API?
A: 检查后端是否已启动，且端口 8000 未被占用

### Q: AI 功能无法使用?
A: 需要在 `.env` 中配置有效的 Minimax API Key

### Q: 如何重置数据库?
A: 删除 `backend/guji.db` 文件，然后重新运行 `python init_data.py`

## 6. 项目结构速览

```
找到古籍/
├── backend/              # 后端代码
│   ├── app/
│   │   ├── models/      # 数据库模型
│   │   ├── routers/     # API 路由
│   │   ├── services/    # 业务逻辑
│   │   └── main.py      # 入口文件
│   ├── init_data.py     # 数据初始化
│   └── run.py           # 启动脚本
├── frontend/            # 前端代码
│   ├── src/
│   │   ├── components/  # 组件
│   │   ├── views/       # 页面
│   │   ├── api/         # API 封装
│   │   └── router/      # 路由配置
│   └── package.json
├── PLAN.md              # 开发计划
└── README.md            # 项目说明
```

## 7. 开发流程

1. 后端开发新 API → 测试 API → 更新前端 API 调用
2. 前端开发新页面 → 对接后端 → 联调测试
3. 发现问题 → 在 .agentstalk 中记录 → 协调修复

## 8. 核心功能模块

- **文章模块**：浏览、搜索、阅读古文
- **AI 模块**：智能推荐、翻译、解释
- **知识模块**：知识点生成、脑图展示
- **导出模块**：PDF 导出功能

---

祝开发顺利！🎉
