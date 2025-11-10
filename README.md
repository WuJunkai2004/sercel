# Sercel - 一个轻量级的 Python Web 服务器

Sercel 是一个受 Vercel 启发、用于快速构建 Web 服务和 API 的轻量级 Python HTTP 服务器框架。它允许您通过简单的函数注册来创建 API 端点，并支持后台任务。

## 特性

-   **零配置**: 无需复杂配置，开箱即用。
-   **静态文件服务**: 自动托管静态文件（HTML, CSS, JS 等）。
-   **动态 API**: 使用 `@register` 装饰器轻松将 Python 函数转换为 API 端点。
-   **后台任务**: 使用 `@daemon` 装饰器运行常驻后台任务。
-   **数据解析**: 内置支持 JSON、表单数据和文件上传。
-   **热重载**: 修改 API 脚本后可自动重新加载，无需重启服务（如果启用了 `hot_reload`）。

## 如何使用

### 1. 启动服务器

项目已经包含一个入口文件 `__main__.py`，它会启动服务器。只需在项目根目录运行以下命令：

```bash
python .
```

服务器默认在 `15444` 端口上运行。

### 2. 创建 API 端点

要创建一个 API 端点，您只需要创建一个 Python 文件，并使用 `vercel.register` 装饰器来包装您的处理函数。

例如，在 `api` 目录下创建一个 `hello.py` 文件：

```python
# api/hello.py
import sercel.vercel as vercel

@vercel.register
def my_api_handler(response, data):
    """
    一个简单的 API 处理函数。
    - response: 用于向客户端发送响应。
    - data: 包含 URL 参数或 POST 请求体。
    """
    name = data.get('name', 'World')
    response.send_json({'message': f'Hello, {name}!'})

# 可选：开启热重载
# import sercel.decorators as dec
# @dec.hot_reload
```

当服务器运行时，您可以通过访问 `http://localhost:15444/api/hello?name=Guest` 来调用这个 API。

#### 可用参数

`@register` 装饰的函数可以根据需要选择以下参数：

-   `response`: 响应对象，用于发送数据回客户端（例如 `response.send_text(...)`, `response.send_json(...)`）。
-   `url`: 完整的请求路径。
-   `data`: 解析后的请求数据。对于 GET 请求，是 URL 查询参数字典；对于 POST 请求，是请求体（JSON、表单等）。
-   `headers`: 请求头字典。

### 3. 运行后台任务

如果您有需要在服务器启动时运行的后台任务（例如，定时任务、消息队列消费者），可以使用 `vercel.daemon` 装饰器。

创建一个 `tasks.py` 文件：

```python
# tasks.py
import time
from vercel import daemon, verlog

@daemon
def background_task():
    """
    这个函数将在一个独立的后台线程中运行。
    """
    count = 0
    while True:
        verlog.name('task')('后台任务正在运行... 次数: %d' % count)
        count += 1
        time.sleep(10)

# 确保在主入口文件中导入此模块以激活后台任务
```

然后，在 `__main__.py` 中导入这个文件，以确保后台任务被注册和启动：

```python
# __main__.py
import verapi
import tasks  # 导入以启动后台任务

if __name__ == '__main__':
    verapi.main()
```

当您启动服务器时，`background_task` 函数将自动在后台开始运行。

## 核心 API

### `vercel.register`

一个装饰器，用于将普通 Python 函数注册为 HTTP API 端点。被装饰的函数会自动成为一个包含 `vercel` 方法的处理程序实例。

### `vercel.daemon`

一个装饰器，用于将函数在一个新的后台守护线程中运行。非常适合执行需要在应用生命周期内持续运行的任务。
