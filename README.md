# 地面降水质控子系统

## 一、配置控制系统

### 1.1 模型设计

#### 1.1.1 配置表

| 配置名(config_name) | 配置码(config_code) | 配置体(config_body) | 备注(remarks) |
| ------------------- | ------------------- | ------------------- | ------------- |
| string              | integer             | text                | string        |
| unique              | unique              |                     |               |

请求体设置:

```json
{
    "config_name": "test",
    "config_code": "1",
    "config_body": {},
    "remarks": ""
}
```

配置体设置：

```json
{
    0: {
        "algorithm_name": "name1",
        "algorithm_code": 2,
        "params": {
            "param1": "1",
            "param2": "2",
        }
    },
}
```

核心代码：

```python
class ConfigModel(BaseModel):
    """配置表
     - 用于存储用户设定的算法运行配置
     - 涵盖了算法执行顺序、算法运行参数
    """

    config_name = models.CharField("配置名", max_length=128, unique=True, help_text="配置名")
    config_code = models.IntegerField("配置码", unique=True, help_text="配置码")
    config_body = models.TextField("配置体", help_text="配置体")

    def __str__(self):
        return f"<{self.config_code}:{self.config_name}>"

    class Meta:
        db_table = "configuration"
        ordering = ["id"]
        verbose_name = "配置表"
        verbose_name_plural = verbose_name
```

#### 1.1.2 算法表

| 算法名(algorithm_name) | 算法码(algorithm_code) | 质控码(qc_code) | 是否停用(is_stop) | 备注(remarks) |
| ---------------------- | ---------------------- | --------------- | ----------------- | ------------- |
| string                 | integer                | integer         | integer           |               |
| max_length=128         | unique                 | unique          | default=False     |               |
| unique                 |                        |                 |                   |               |

核心代码:

```python
class AlgorithmModel(BaseModel):
    """算法表"""

    algorithm_name = models.CharField("算法名", max_length=128, unique=True, help_text="算法名")
    algorithm_code = models.IntegerField("算法码", unique=True, help_text="算法码")
    qc_code = models.IntegerField("质控码", unique=True, help_text="质控码")
    is_stop = models.BooleanField("是否停用", default=False, help_text="是否停用")

    def __str__(self):
        return f"<{self.algorithm_code}: {self.algorithm_name}>"

    class Meta:
        db_table = "algorithm"
        ordering = ["id"]
        verbose_name = "算法表"
        verbose_name_plural = verbose_name
```

#### 1.2 接口设计

术语统一：

| 术语      | 含义                                                         |
| --------- | ------------------------------------------------------------ |
| ${host}   | 指接口所在主机的域名或 ip，包含协议信息如 http、https，以及服务端口号 |
| :xx       | xx，为某个参数，使用 : 符号标记其后的 xx 为路径参数，如 :id，意味着应填入 id，:pk，意味着需要填入主键 |
| text/json | 意味着这是一个 json 格式的字符串                             |

##### 1.2.1 配置表查询接口

接口地址：${host}/api/configuration/

返回格式：json

请求方式：get

请求示例： ${host}/api/configuration/

接口备注： 该接口属于配置表功能，用于查询配置表信息，默认返回所有信息，支持参数过滤，请使用表内字段查询。

------

过滤参数说明：

| 名称        | 必须性 | 类型      | 描述                                                      |
| ----------- | ------ | --------- | --------------------------------------------------------- |
| config_name | 否     | string    | 配置名                                                    |
| config_code | 否     | integer   | 配置码                                                    |
| config_body | 否     | text/json | json 格式的长字符串，支持过滤，但不建议使用该参数进行过滤 |

返回参数说明：

| 名称        | 类型   | 说明                         |
| ----------- | ------ | ---------------------------- |
| result_code | string | 返回状态码                   |
| message     | string | 状态码对应信息，或自定义信息 |
| data        | list   | 具体的查询数据列表           |

返回参数示例：

```json
# 默认返回
{
    result_code: "200",
    message: "成功",
    data: [
        {
            id: 2, 
            config_name: "test2", 
            config_code: 2, 
            config_body: {
                0: {
                    algorithm_name: "name1",
                    algorithm_code: 2,
                    params: {
                        param1: "param1",
                        param2: "param2"
                    }
                },
                1: {
                    algorithm_name: "name2",
                    algorithm_code: 1,
                    params: {
                        param1: "param1",
                        param2: "param2"
                    }
                }
            },
            remarks: "",
        },
        {
            id: 5,
            config_name: "test3",
            config_code: 3,
            config_body: {
                0: {
                    algorithm_name: "name1",
                    algorithm_code: 2,
                    params: {
                        param1: "param1",
                        param2: "param2",
                    }
                }
            },
            remarks: "",
        }
    ]
}
```

##### 1.2.2 配置表增加接口

接口地址：${host}/api/configuration/

请求格式：json， 请使用 json 的格式发出请求

返回格式：json

请求方式：post

请求示例： ${host}/api/configuration/

接口备注： 该接口属于配置表功能，用于增加配置表信息、新建配置表条目。

------

请求参数说明：

| 名称        | 必须性 | 类型      | 描述                |
| ----------- | ------ | --------- | ------------------- |
| config_name | 是     | string    | 配置名              |
| config_code | 是     | integer   | 配置码              |
| config_body | 是     | text/json | json 格式的长字符串 |

返回参数说明：

| 名称        | 类型   | 说明                         |
| ----------- | ------ | ---------------------------- |
| result_code | string | 返回状态码                   |
| message     | string | 状态码对应信息，或自定义信息 |

返回参数示例：

```json
# 默认返回
{
    result_code: "200",
    message: "成功",
}
```

##### 1.2.3 配置表修改接口

接口地址：${host}/api/configuration/

请求格式：json， 请使用 json 的格式发出请求

返回格式：json

请求方式：put

请求示例： ${host}/api/configuration/:id/

接口备注： 该接口属于配置表功能，用于修改对应 id 的配置表条目信息。

------

请求参数说明：

| 名称        | 必须性 | 类型      | 描述                    |
| ----------- | ------ | --------- | ----------------------- |
| config_name | 否     | string    | 配置名                  |
| config_code | 否     | integer   | 配置码                  |
| config_body | 否     | text/json | json 格式的长字符串     |
| id          | 是     | integer   | 需要修改的配置表条目 id |

返回参数说明：

| 名称        | 类型   | 说明                         |
| ----------- | ------ | ---------------------------- |
| result_code | string | 返回状态码                   |
| message     | string | 状态码对应信息，或自定义信息 |

返回参数示例：

```json
# 默认返回
{
    result_code: "200",
    message: "成功",
}
```

##### 1.2.4 配置表删除接口

接口地址：${host}/api/configuration/

返回格式：json

请求方式：delete

请求示例： ${host}/api/configuration/:id/

接口备注： 该接口属于配置表功能，用于删除对应 id 的配置表条目信息。

------

请求参数说明：

| 名称 | 必须性 | 类型    | 描述                    |
| ---- | ------ | ------- | ----------------------- |
| id   | 是     | integer | 需要删除的配置表条目 id |

返回参数说明：

| 名称        | 类型   | 说明                         |
| ----------- | ------ | ---------------------------- |
| result_code | string | 返回状态码                   |
| message     | string | 状态码对应信息，或自定义信息 |

返回参数示例：

```json
# 默认返回
{
    result_code: "200",
    message: "成功",
}
```

##### 1.2.5 算法表查询接口

接口地址：${host}/api/algorithm/

返回格式：json

请求方式：get

请求示例： ${host}/api/algorithm/

接口备注： 该接口属于配置表功能，用于删除对应 id 的配置表条目信息。

<hr>

过滤参数说明：

| 名称           | 必须性 | 类型    | 描述                   |
| -------------- | ------ | ------- | ---------------------- |
| algorithm_name | 是     | string  | 算法名                 |
| algorithm_code | 是     | integer | 算法码                 |
| qc_code        | 是     | integer | 质控码                 |
| is_stop        | 否     | boolean | 是否停用，默认为 False |

返回参数说明：

| 名称        | 类型   | 说明                         |
| ----------- | ------ | ---------------------------- |
| result_code | string | 返回状态码                   |
| message     | string | 状态码对应信息，或自定义信息 |
| data        | list   | 具体的查询数据条目列表       |

返回参数示例：

```json
# 默认返回
{
    "result_code": "200", 
    "message": "成功", 
    "data": [
        ...
    ]
}
```

##### 1.2.6 算法表增加接口

接口地址：${host}/api/algorithm/

请求格式：json， 请使用 json 的格式发出请求

返回格式：json

请求方式：post

请求示例： ${host}/api/algorithm/

接口备注： 该接口属于配置表功能，用于删除对应 id 的配置表条目信息。

<hr>

请求参数说明：

| 名称           | 必须性 | 类型    | 描述     |
| -------------- | ------ | ------- | -------- |
| algorithm_name | 是     | string  | 算法名   |
| algorithm_code | 是     | integer | 算法码   |
| qc_code        | 是     | integer | 质控码   |
| is_stop        | 否     | boolean | 是否停用 |

返回参数说明：

| 名称        | 类型   | 说明                         |
| ----------- | ------ | ---------------------------- |
| result_code | string | 返回状态码                   |
| message     | string | 状态码对应信息，或自定义信息 |

返回参数示例：

```json
# 默认返回
{
    result_code: "200",
    message: "成功",
}
```



##### 1.2.7 算法表修改接口

接口地址：${host}/api/algorithm/

请求格式：json， 请使用 json 的格式发出请求

返回格式：json

请求方式：put

请求示例： ${host}/api/algorithm/:id/

接口备注： 该接口属于配置表功能，用于修改对应 id 的配置表条目信息。

------

请求参数说明：

| 名称        | 必须性 | 类型      | 描述                    |
| ----------- | ------ | --------- | ----------------------- |
| algorithm   | 否     | string    | 配置名                  |
| config_code | 否     | integer   | 配置码                  |
| config_body | 否     | text/json | json 格式的长字符串     |
| id          | 是     | integer   | 需要修改的配置表条目 id |

返回参数说明：

| 名称        | 类型   | 说明                         |
| ----------- | ------ | ---------------------------- |
| result_code | string | 返回状态码                   |
| message     | string | 状态码对应信息，或自定义信息 |

返回参数示例：

```json
# 默认返回
{
    result_code: "200",
    message: "成功",
}
```



##### 1.2.8 算法表删除接口

接口地址：${host}/api/algorithm/

返回格式：json

请求方式：delete

请求示例： ${host}/api/algorithm/:id/

接口备注： 该接口属于算法表功能，用于删除对应 id 的算法表条目信息。

------

请求参数说明：

| 名称 | 必须性 | 类型    | 描述                    |
| ---- | ------ | ------- | ----------------------- |
| id   | 是     | integer | 需要删除的算法表条目 id |

返回参数说明：

| 名称        | 类型   | 说明                         |
| ----------- | ------ | ---------------------------- |
| result_code | string | 返回状态码                   |
| message     | string | 状态码对应信息，或自定义信息 |

##### 1.2.9 配置表详情接口

接口地址：${host}/api/configuration/

返回格式：json

请求方式：get

请求示例： ${host}/api/configuration/:id/

接口备注： 该接口属于配置表功能，用于查询配置表某个条目信息，使用 id 来指定这个条目，可以使用表字段进行过滤。

------

过滤参数说明：

| 名称        | 必须性 | 类型      | 描述                                                      |
| ----------- | ------ | --------- | --------------------------------------------------------- |
| config_name | 否     | string    | 配置名                                                    |
| config_code | 否     | integer   | 配置码                                                    |
| config_body | 否     | text/json | json 格式的长字符串，支持过滤，但不建议使用该参数进行过滤 |

返回参数说明：

| 名称        | 类型   | 说明                         |
| ----------- | ------ | ---------------------------- |
| result_code | string | 返回状态码                   |
| message     | string | 状态码对应信息，或自定义信息 |
| data        | list   | 具体的查询数据列表           |

返回参数示例：

```json
{
    result_code: "200",
    message: "成功",
    data: [
        {
            id: 2, 
            config_name: "test2", 
            config_code: 2, 
            config_body: {
                0: {
                    algorithm_name: "name1",
                    algorithm_code: 2,
                    params: {
                        param1: "param1",
                        param2: "param2"
                    }
                },
                1: {
                    algorithm_name: "name2",
                    algorithm_code: 1,
                    params: {
                        param1: "param1",
                        param2: "param2"
                    }
                }
            },
            remarks: "",
        }
    ]
}
```

##### 1.2.10 算法表详情接口

接口地址：${host}/api/algorithm/

返回格式：json

请求方式：get

请求示例： ${host}/api/algorithm/:id

接口备注： 该接口属于算发表查询功能，用于查询算法表某个条目信息，使用 id 来指定这个条目，可以使用表字段进行过滤。

------

过滤参数说明：

| 名称           | 必须性 | 类型    | 描述                   |
| -------------- | ------ | ------- | ---------------------- |
| algorithm_name | 是     | string  | 算法名                 |
| algorithm_code | 是     | integer | 算法码                 |
| qc_code        | 是     | integer | 质控码                 |
| is_stop        | 否     | boolean | 是否停用，默认为 False |

返回参数说明：

| 名称        | 类型   | 说明                         |
| ----------- | ------ | ---------------------------- |
| result_code | string | 返回状态码                   |
| message     | string | 状态码对应信息，或自定义信息 |
| data        | list   | 具体的查询数据列表           |

返回参数示例：

```json
{
    result_code: "200",
    message: "成功",
    data: [
		...
    ]
}
```

##### 

## 二、Quick Start

### 2.1 How to run

1. 下载本项目。

2. 安装对应版本 python 库。 `pip install -r requirements.txt`

3. 配置 mysql

   - 创建数据库 surface_rainfall_sys `create database surface_rainfall_sys  `。

   - 添加账号 sl。`create user 'sl'@'host' `
   - 将对应数据库权限赋予 sl。`grant all privileges on surface_rainfall_sys.* to 'sl'@'%' identified by 'sl@123'`

3. 数据库迁移
   - 制作迁移 `python manage.py makemigrations`
   - 执行迁移 `python manage.py migrate`
   - 注意：在上传代码的时候，不允许将 migrations 上传
4. 运行
   - `python manage.py runserver 0:8000`

