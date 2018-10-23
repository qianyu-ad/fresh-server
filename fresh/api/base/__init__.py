from flask_restful import Resource
from flask_restful.utils.cors import crossdomain
from fresh.mixins.rest import RestMixin

__all__ = (
    'router',
    'register_restful_api',
    'RestApi',
)

REST_API_RULE_MAPS = {}


def router(url):
    """ 通过装饰来绑定api的路由

        @router('/api/v1/test')
        class TestApi(RestApi):
            
            def get(self):
                return self.ok(msg='test')
    
    """
    def deco(cls):
        if cls not in REST_API_RULE_MAPS:
            REST_API_RULE_MAPS[cls] = url
        else:
            raise KeyError("Route key {} already exists.".format(cls.__name__))
        return cls

    return deco


def register_restful_api(api):
    """ 注册restful api的路由"""
    for cls, url in REST_API_RULE_MAPS.items():
        api.add_resource(
            cls, url,
        )


class RestApi(Resource, RestMixin):
    headers = [
        'content-type',
    ]
    
    decorators = [crossdomain(origin="*", headers=headers)]