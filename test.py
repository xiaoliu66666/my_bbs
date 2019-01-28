from flask import request
from utils import log


log("request的属性：", request.__dict__)