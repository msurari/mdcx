import json

p = json.load(open("/opt/data/profiles/movie/cache/scratch/py_classified.json", encoding="utf-8"))
byval = {e["value"]: e for e in p["strings"]}
for v in ["直播盒子", "最新情报", "注册免费送", "，", "不跳过小文件", "翻译服务", "媒体路径", "开始", "选择目录",
          "演员名", "有码", "无码", "素人", "国产", "欧美", "动漫", "里番", "中文字幕", "标签", "系列",
          "4K", "未知演员", "保存", "确认", "警告", "失败", "成功"]:
    e = byval.get(v)
    if not e:
        print(f"{v!r}: NOT FOUND")
        continue
    loc = e["locations"][0]
    print(f"{v!r}: {e['category']} ui={e['in_ui_context']} data={e['in_data_context']} cats={e['cats']} "
          f"@ {loc['file']}:{loc['line']} call={loc['call']}")
