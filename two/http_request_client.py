import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def requests_with_retry(
    method: str,
    url: str,
    retries: int = 3,
    backoff_factor: float = 1,
    status_forcelist=(500, 502, 503, 504),
    timeout: int = 5,
    **kwargs
) -> requests.Response:
    """
    通用请求方法，支持失败自动重试

    :param method: 请求方法 (GET/POST/PUT/DELETE...)
    :param url: 请求地址
    :param retries: 最大重试次数
    :param backoff_factor: 重试退避因子 (1 -> 1s, 2s, 4s)
    :param status_forcelist: 需要重试的状态码
    :param timeout: 请求超时时间
    :param kwargs: 其他 requests 支持的参数，如 headers, params, data, json
    :return: requests.Response 对象
    """
    session = requests.Session()
    retry_strategy = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    response = session.request(method=method, url=url, timeout=timeout, **kwargs)
    return response

if __name__ == "__main__":
    try:
        # GET 请求
        resp = requests_with_retry("GET", "https://httpbin.org/status/500")
        print(resp.status_code, resp.text)

        # POST 请求
        resp = requests_with_retry(
            "POST",
            "https://httpbin.org/post",
            json={"name": "wuzun", "age": 30}
        )
        print(resp.status_code, resp.json())

    except requests.exceptions.RequestException as e:
        print("最终请求失败:", e)
