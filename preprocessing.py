def make_headers(id : str, secret : str):
    return {
        "Content-Type": "application/x-www-form-urlencoded",
        "charset": "UTF-8",
        "X-Naver-Client-Id": id,
        "X-Naver-Client-Secret": secret
    }