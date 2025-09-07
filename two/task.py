from celery import Celery

# 使用带密码的 Redis
app = Celery(
    "my_tasks",
    broker="redis://:mjlsport@8.133.199.221:6379/0",
    backend="redis://:mjlsport@8.133.199.221:6379/1"  # 推荐单独用一个db存储结果
)

@app.task
def add(x, y):
    return x + y
