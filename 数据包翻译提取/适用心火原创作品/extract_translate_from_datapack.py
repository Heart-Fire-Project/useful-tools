# -*- coding: UTF-8 -*-
"""
Minecraft Datapack Translation Key Extractor
从 Minecraft 数据包中提取翻译键，生成语言文件
支持 JSON 和 SNBT 两种格式，兼容 Minecraft 1.21+
"""
import os
import json
import re

directory = "data/"
output_file = "data/lang/zh_cn.json"
result = {}


def is_macro_placeholder(text):
    """检查是否为 Minecraft 宏占位符 $(...)"""
    return text.startswith("$(") or "$(" in text


def extract_from_snbt(text):
    """
    从 SNBT 格式文本中提取翻译键
    SNBT 格式: translate:"key",fallback:"value" (键无引号)
    """
    extracted = {}

    # 匹配 SNBT 格式的 translate 和 fallback 对
    # 支持中间有其他字段的情况
    pattern = r'(?<!["\w])translate\s*:\s*"([^"]+)"[^}]*?fallback\s*:\s*"([^"]+)"'
    matches = re.findall(pattern, text)
    for key, value in matches:
        # 跳过宏占位符
        if is_macro_placeholder(key) or is_macro_placeholder(value):
            continue
        if key not in extracted:
            extracted[key] = value

    return extracted


def extract_from_json_obj(json_obj, res_dict):
    """
    递归从 JSON 对象中提取翻译键
    JSON 格式: "translate": "key", "fallback": "value"
    """
    if isinstance(json_obj, dict):
        translate = json_obj.get("translate")
        fallback = json_obj.get("fallback")
        # 跳过宏占位符
        if translate and fallback and translate not in res_dict:
            if not is_macro_placeholder(translate) and not is_macro_placeholder(fallback):
                res_dict[translate] = fallback
        # 递归处理嵌套结构
        for value in json_obj.values():
            if isinstance(value, (dict, list)):
                extract_from_json_obj(value, res_dict)
            elif isinstance(value, str):
                # 字符串值可能包含 SNBT 格式的翻译
                snbt_extracted = extract_from_snbt(value)
                for k, v in snbt_extracted.items():
                    if k not in res_dict:
                        res_dict[k] = v
    elif isinstance(json_obj, list):
        for item in json_obj:
            if isinstance(item, (dict, list)):
                extract_from_json_obj(item, res_dict)
            elif isinstance(item, str):
                snbt_extracted = extract_from_snbt(item)
                for k, v in snbt_extracted.items():
                    if k not in res_dict:
                        res_dict[k] = v


def extract_from_json_text(text):
    """
    从 JSON 格式文本中提取翻译键
    支持多行 JSON 和字段间有其他内容的情况
    """
    extracted = {}

    # 匹配 JSON 格式的 translate 和 fallback 对
    pattern = r'"translate"\s*:\s*"([^"]+)"[^}]*?"fallback"\s*:\s*"([^"]+)"'
    matches = re.findall(pattern, text)
    for key, value in matches:
        # 跳过宏占位符
        if is_macro_placeholder(key) or is_macro_placeholder(value):
            continue
        if key not in extracted:
            extracted[key] = value

    return extracted


def process_mcfunction_file(filepath):
    """处理 .mcfunction 文件"""
    extracted = {}
    try:
        with open(filepath, "r", encoding="UTF-8") as f:
            content = f.read()

            # 提取 SNBT 格式
            snbt_extracted = extract_from_snbt(content)
            extracted.update(snbt_extracted)

            # 提取 JSON 格式（有些 mcfunction 文件中可能有 JSON 格式）
            json_extracted = extract_from_json_text(content)
            for k, v in json_extracted.items():
                if k not in extracted:
                    extracted[k] = v

    except Exception as e:
        print(f"处理文件 {filepath} 时出错: {e}")

    return extracted


def process_json_file(filepath):
    """处理 .json 文件"""
    extracted = {}
    try:
        with open(filepath, "r", encoding="UTF-8") as f:
            content = f.read()

            # 先尝试解析为 JSON 对象
            try:
                json_obj = json.loads(content)
                extract_from_json_obj(json_obj, extracted)
            except json.JSONDecodeError:
                pass

            # 同时用正则直接从文本提取（处理嵌套字符串中的翻译）
            json_extracted = extract_from_json_text(content)
            for k, v in json_extracted.items():
                if k not in extracted:
                    extracted[k] = v

            # 也检查 SNBT 格式（某些 JSON 文件中可能嵌入 SNBT）
            snbt_extracted = extract_from_snbt(content)
            for k, v in snbt_extracted.items():
                if k not in extracted:
                    extracted[k] = v

    except Exception as e:
        print(f"处理文件 {filepath} 时出错: {e}")

    return extracted


def main():
    global result

    # 确保输出目录存在
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)

            if file.endswith(".mcfunction"):
                print(f"正在处理 {filepath}")
                extracted = process_mcfunction_file(filepath)
                result.update(extracted)

            elif file.endswith(".json"):
                print(f"正在处理 {filepath}")
                extracted = process_json_file(filepath)
                result.update(extracted)

            elif file.endswith(".mcmeta"):
                print(f"正在处理 {filepath}")
                extracted = process_json_file(filepath)
                result.update(extracted)

    # 清理结果（如果有列表值，取第一个）
    for key in result.keys():
        if isinstance(result[key], list):
            result[key] = result[key][0] if result[key] else ""

    # 按键名排序
    sorted_result = dict(sorted(result.items()))

    # 输出统计信息
    print(f"\n提取完成！")
    print(f"总翻译键数: {len(sorted_result)}")

    # 保存到文件
    with open(output_file, "w", encoding="UTF-8") as f:
        json.dump(sorted_result, f, ensure_ascii=False, indent=4)

    print(f"已保存到: {output_file}")


if __name__ == "__main__":
    main()
