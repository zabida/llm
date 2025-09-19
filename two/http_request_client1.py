import time
import requests

url = "https://httpbin.org/status/500"

for i in range(3):
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        print("成功:", resp.text)
        break
    except requests.exceptions.RequestException as e:
        print(f"第 {i+1} 次失败: {e}")
        if i < 2:
            time.sleep(2 ** i)  # 指数退避
else:
    print("重试 3 次后仍失败")
