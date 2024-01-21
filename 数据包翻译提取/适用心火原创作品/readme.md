# 翻译键提取 - 原创用

1. 主要作用:
   1. 针对老版本 "translate" 和 "fallback":
      1. 从数据包中提取`"translate"`和`"fallback"`, 并且写入到专门的语言文件
      2. 使用`jsonfinder`来查找 json 字符串, 防止使用正则表达式产生的识别不到问题
   2. 针对新版本 "trans_x" 和 "fallb_x":
      1. 从数据包中提取 "trans_x" 和 "fallb_x", 并且写入到专门的语言文件
      2. 使用`re`来查找 json 字符串, 因为新版本的 json 字符串是不规则的, 所以使用正则表达式查找

2. 如何使用

   1. 安装`jsonfinder`库 (`pip install jsonfinder`)
   2. 调整

      ```python
      directory = "data/" # 这个是需要遍历的目录
      output_file = "data/lang/zh_cn.json" # 这个是输出的语言文件地址
      ```

      这两个参数到你的实际情况

      - 注:
        - directory 是和你放置 py 文件目录同级的, 建议直接放置在 data/下
        - 请提前新建你需要的 output_file 文件

   3. 运行即可

注: 请严格遵守 GPLv3!
