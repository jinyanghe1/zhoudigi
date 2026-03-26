# 找到古籍 - AI时代的《古文观止》

> 让 AI 当你的古文老师，从浩如烟海的古籍中提取最相关的章节，既有高山仰止的名篇，也有被先人忽略的遗珠。

## 🌟 核心功能

- **📚 智能章节编排**：Agent 自动选取 300 篇古文，覆盖从先秦到晚清
- **🧠 脑图联系**：自动生成知识图谱，展示朝代、文人集团、风格分类
- **💡 知识点生成**：自动提取知识点，支持沉浸式翻译
- **🤖 AI 交互**：与 AI 对话，让它帮你选择想读的文章
- **📄 PDF 导出**：一键导出感兴趣的文章

## 🏗️ 技术架构

### 后端
- **FastAPI** - 高性能 Python Web 框架
- **SQLAlchemy** - ORM 数据库操作
- **Minimax API** - 大模型对话与推荐
- **维基文库 API** - 古籍检索

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **TypeScript** - 类型安全
- **Element Plus** - UI 组件库
- **ECharts** - 知识图谱可视化

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd 找到古籍
```

### 2. 配置环境

```bash
# 后端配置
cd backend
cp .env.example .env
# 编辑 .env 文件，填入你的 Minimax API Key
```

### 3. 启动后端

```bash
# 使用 uv 安装依赖（推荐）
uv pip install -r requirements.txt

# 或使用 pip
pip install -r requirements.txt

# 初始化数据
python init_data.py

# 启动服务
python run.py
```

后端服务将在 http://localhost:8000 启动

### 4. 启动前端

```bash
cd frontend

# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev
```

前端服务将在 http://localhost:5173 启动

## 📁 项目结构

```
找到古籍/
├── backend/                    # 后端
│   ├── app/
│   │   ├── models/            # 数据库模型
│   │   ├── schemas/           # Pydantic 模型
│   │   ├── routers/           # API 路由
│   │   ├── services/          # 业务逻辑
│   │   │   ├── minimax.py     # Minimax API
│   │   │   └── wikisource.py  # 维基文库
│   │   └── main.py            # FastAPI 入口
│   ├── init_data.py           # 数据初始化
│   └── requirements.txt
├── frontend/                   # 前端
│   ├── src/
│   │   ├── components/        # 组件
│   │   ├── views/             # 页面
│   │   ├── api/               # API 封装
│   │   └── router/            # 路由配置
│   └── package.json
└── README.md
```

## 🔧 配置说明

### Minimax API 配置

在 `backend/.env` 中配置：

```env
MINIMAX_API_KEY=your_minimax_api_key
MINIMAX_GROUP_ID=your_minimax_group_id
```

获取 API Key：[Minimax 开放平台](https://www.minimaxi.com/)

## 📝 API 文档

启动后端后，访问 http://localhost:8000/docs 查看 Swagger 文档

主要接口：
- `GET /api/articles` - 文章列表
- `GET /api/articles/{id}` - 文章详情
- `POST /api/ai/chat` - AI 对话
- `POST /api/ai/select-articles` - AI 推荐文章
- `POST /api/export/pdf` - 导出 PDF

## 🎨 界面预览

- **首页**：推荐文章流、分类浏览入口
- **书库**：按朝代/作者浏览文章
- **阅读页**：类似微信读书的沉浸式阅读体验
- **AI 助手**：与 AI 对话获取文章推荐
- **知识图谱**：可视化展示文学关系

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

MIT License
