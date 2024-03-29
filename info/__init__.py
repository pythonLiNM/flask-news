import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis
from config import config

# 先初始化扩展对象,然后在调用init_app初始化
db = SQLAlchemy()
redis_store = None  # type:StrictRedis


# redis_store:StrictRedis=None


def setup_log(config_name):
    # 设置日志的记录等级
    logging.basicConfig(level=config[config_name].DEBUG)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("/home/lilinming-pc/Desktop/flask/Flask_Projects/flask-news/logs/log",
                                           maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):
    setup_log(config_name)  # 配置文件
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)  # 初始化
    global redis_store
    redis_store = StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT)

    # 开启csrf 保护
    CSRFProtect(app)
    # session保存配置
    Session(app)

    # 注册蓝图
    from info.modules import index_blu
    app.register_blueprint(index_blu)
    return app
