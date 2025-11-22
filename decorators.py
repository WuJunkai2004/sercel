import mimetypes
import json
import os
from functools import wraps

def auto_content_type(cls):
    """
    自动为API类的响应方法注入Content-Type头的装饰器
    """
    original_vercel_register = cls.vercel

    @wraps(original_vercel_register)
    def vercel_handler(**kwargs):
        if "response" in kwargs:
            original_send_file = kwargs["response"].send_file

            @wraps(original_send_file)
            def enhanced_send_file(self, filepath):
                # 自动检测并设置Content-Type
                content_type, _ = mimetypes.guess_type(filepath)
                if content_type:
                    self.send_header('Content-Type', content_type)
                return original_send_file(self, filepath)

            kwargs["response"].send_file = enhanced_send_file
        
        return original_vercel_register(**kwargs)
    cls.vercel = vercel_handler
    return cls


def hot_reload(cls):
    """
    为API类启用热重载功能的装饰器
    """
    cls.hot_reload = True
    return cls


class daemon:
    def __init__(self, func):
        self.func = func
        self.thread = None

    def __call__(self, *args, **kwargs):
        """Call to the function"""
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.func, args=args, kwargs=kwargs)
            self.thread.daemon = True
            self.thread.start()
        else:
            verlog.name('daemon')(f"Thread {self.thread.name} is already running.", level=logging.WARNING)
