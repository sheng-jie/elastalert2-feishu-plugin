# elastalert-feishu-plugin
## 安装
sudo apt install -y  python-pip python-dev libffi-dev libssl-dev

pip install elastalert
## 修改配置
### config.yaml:

``` 
es_host: elasticsearch 地址
es_port: elasticsearch 端口
```
### rules/example_frequency.yaml
``` 
alert:
- "elastalert_modules.feishu_alert.FeishuAlert"

# 飞书机器人接口地址
feishualert_url: "https://open.feishu.cn/open-apis/bot/v2/hook/"
# 飞书机器人id
feishualert_botid:
  "botid"
  
# 这个时间段内的匹配将不告警，适用于某些时间段请求低谷避免误报警
feishualert_skip:
  start: "01:00:00"
  end: "09:00:00"

alert_subject: "错误日志报警"
alert_text_type: alert_text_only
alert_text: |
 【告警主题】 错误日志报警
 【告警条件】 Error级别日志1分钟内>100
 【所属应用】 {}
 【错误日志】 {}
 【异常详情】 {}
 【错误数量】 {}
 【告警时间】 {}
alert_text_args:
 - kubernetes.container.name
 - message
 - exception
 - num_hits
 - "@timestamp"
```

## 运行
elastalert-create-index --config config.yaml

python -m elastalert.elastalert --verbose
