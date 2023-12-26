1. 主要作用:
   1. 从数据包中提取`"translate"`和`"fallback"`, 并且写入到专门的语言文件
   2. 使用`jsonfinder`来查找json字符串, 防止使用正则表达式产生的识别不到问题
2. 如何使用
   1. 安装`jsonfinder`库 (pip install jsonfinder)
   2. 调整
      ```python 
      directory = "data/" # 这个是需要遍历的目录
      output_file = "data/lang/zh_cn.json" # 这个是输出的语言文件地址
      ```
      这两个参数到你的实际情况
   3. 运行即可

注: 请严格遵守GPLv3!
