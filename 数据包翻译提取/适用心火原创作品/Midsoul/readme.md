# 翻译键提取器 - Midsoul 用

## Translation Key Extractor

1. 主要作用
   1. 从 Minecraft 数据包中提取所有翻译键（translate）及其回退值（fallback）
   2. 支持 JSON 格式（`"translate": "key"`）, SNBT 格式（`translate:"key"`）和宏函数格式（`merge_sign`, `trans_N` 与 `fallb_N`）
   3. 生成终端表格预览
   4. 生成 Excel 报告（`translation_report.xlsx`）
   5. 统计翻译键总数及重复键数量

2. 如何使用
   1. 安装依赖：`pip install prettytable openpyxl`
   2. 运行脚本：`python temp_main.py`
   3. 输入数据包目录路径（如 `Midsoul-plus`）

3. 输出说明
   | 列名 | 说明 |
   |------|------|
   | 翻译键 | translate 的值 |
   | 键值 | fallback 的值 |
   | 文件名 | 来源文件路径 |
   | 是否重复 | 该键是否在多个文件中出现 |

4. 兼容性
   - Minecraft 1.21+ 数据包格式
   - `.json`、`.mcfunction`、`.mcmeta` 文件

注: 请严格遵守 GPLv3