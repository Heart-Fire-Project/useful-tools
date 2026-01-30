# 翻译键提取 - 原创用

## Extract translate from datapack

1. 主要作用:
   1. 针对 JSON 格式 `"translate"` 和 `"fallback"`:
      1. 从数据包中提取 `"translate": "key"` 和 `"fallback": "value"`
      2. 递归解析 JSON 对象，支持嵌套结构
   2. 针对 SNBT 格式 `translate:` 和 `fallback:`:
      1. 从数据包中提取 `translate:"key"` 和 `fallback:"value"`（键无引号）
      2. 使用正则表达式匹配，支持字段间有其他内容的情况
   3. 针对宏函数调用:
      1. 对自定义宏函数（如 `merge_sign`）参数的提取支持
      2. 识别并配对参数块中的 `trans_N` 与 `fallb_N`（如 `trans_2` 与 `fallb_2`）
   3. 自动过滤 Minecraft 宏占位符 `$(...)`
   4. 兼容 Minecraft 1.21+ 数据包格式
   5. 无需 `jsonfinder` 依赖，使用纯标准库

2. 如何使用

   1. 调整

      ```python
      directory = "data/" # 这个是需要遍历的目录
      output_file = "data/lang/zh_cn.json" # 这个是输出的语言文件地址
      ```

      这两个参数到你的实际情况

      - 注:
         - directory 是和你放置 py 文件目录同级的，建议直接放置在 data/ 下
         - 输出目录会自动创建，无需手动新建

   2. 运行即可

3. 支持的文件类型
   - `.json` - 数据包 JSON 文件
   - `.mcfunction` - 函数文件
   - `.mcmeta` - 元数据文件

## Extract_value_from_paratranz

1. 主要作用:
   1. 从 paratranz 的导出文件中提取翻译键，并且写入到专门的语言文件

2. 如何使用
   1. 运行即可

注: 请严格遵守 GPLv3!