## 基于flask和selenium的接口
接受POST请求里的动态id字段，返回动态截图的图床链接
```
import requests
url = 'http://127.0.0.1:5000/api/bili_dyn_scnshot'
data = {'dynid' : '681572603811332104' }
r = requests.post(url,data)
```
注:截图样式受设备影响，比例需自行调整
