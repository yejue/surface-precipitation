from django.db import models

from libs.models import BaseModel
# Create your models here.


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
