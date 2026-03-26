#!/bin/bash

# 找到古籍 - 启动脚本

echo "🚀 启动 找到古籍 项目..."

# 启动后端
echo "📦 启动后端服务..."
cd backend
python init_data.py 2>/dev/null || echo "数据已初始化"
python run.py &
BACKEND_PID=$!
cd ..

# 等待后端启动
sleep 2

# 启动前端
echo "🎨 启动前端服务..."
cd frontend
pnpm dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ 服务已启动！"
echo "📚 后端 API: http://localhost:8000"
echo "🌐 前端页面: http://localhost:5173"
echo ""
echo "按 Ctrl+C 停止服务"

# 捕获中断信号
 trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT

# 等待
wait
