from django.http import JsonResponse

from libs.res_code import Code, error_map


def json_response(result_code=Code.OK, message=error_map[Code.OK], data=None, **kwargs):
    """json 序列化"""

    js_dict = {
        "result_code": result_code,
        "message": message,
        "data": data
    }
    js_dict.update(**kwargs)

    return JsonResponse(js_dict, charset="utf8")
