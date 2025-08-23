#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除Markdown文件中的 "jsCopy to Clipboard" 字符串
支持单个文件和批量处理
"""

import os
import glob
import argparse
from pathlib import Path


def clean_markdown_file(file_path, target_string="jsCopy to Clipboard", backup=True):
    """
    清理单个markdown文件
    
    Args:
        file_path: 文件路径
        target_string: 要删除的目标字符串
        backup: 是否创建备份文件
    
    Returns:
        tuple: (是否成功, 删除的字符串数量)
    """
    try:
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 统计要删除的字符串数量
        count = content.count(target_string)
        
        if count == 0:
            print(f"✓ {file_path}: 未找到目标字符串")
            return True, 0
        
        # 创建备份（如果需要）
        if backup:
            backup_path = file_path + '.bak'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"📄 已创建备份: {backup_path}")
        
        # 删除目标字符串
        cleaned_content = content.replace(target_string, '')
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        print(f"✓ {file_path}: 已删除 {count} 个目标字符串")
        return True, count
        
    except Exception as e:
        print(f"✗ {file_path}: 处理失败 - {str(e)}")
        return False, 0


def find_markdown_files(directory, recursive=True):
    """
    查找目录中的markdown文件
    
    Args:
        directory: 目录路径
        recursive: 是否递归搜索子目录
    
    Returns:
        list: markdown文件路径列表
    """
    if recursive:
        pattern = os.path.join(directory, '**', '*.md')
        return glob.glob(pattern, recursive=True)
    else:
        pattern = os.path.join(directory, '*.md')
        return glob.glob(pattern)


def main():
    parser = argparse.ArgumentParser(description='删除Markdown文件中的指定字符串')
    parser.add_argument('path', help='文件或目录路径')
    parser.add_argument('-s', '--string', default='jsCopy to Clipboard', 
                       help='要删除的字符串 (默认: "jsCopy to Clipboard")')
    parser.add_argument('-r', '--recursive', action='store_true', 
                       help='递归处理子目录')
    parser.add_argument('--no-backup', action='store_true', 
                       help='不创建备份文件')
    parser.add_argument('--dry-run', action='store_true', 
                       help='仅预览，不实际修改文件')
    
    args = parser.parse_args()
    
    # 检查路径是否存在
    if not os.path.exists(args.path):
        print(f"错误: 路径不存在 - {args.path}")
        return
    
    # 获取要处理的文件列表
    if os.path.isfile(args.path):
        if args.path.endswith('.md'):
            files = [args.path]
        else:
            print("错误: 指定的文件不是markdown文件")
            return
    else:
        files = find_markdown_files(args.path, args.recursive)
    
    if not files:
        print("未找到任何markdown文件")
        return
    
    print(f"找到 {len(files)} 个markdown文件")
    print(f"目标字符串: '{args.string}'")
    print("-" * 50)
    
    total_processed = 0
    total_deleted = 0
    success_count = 0
    
    for file_path in files:
        if args.dry_run:
            # 预览模式
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                count = content.count(args.string)
                print(f"[预览] {file_path}: 将删除 {count} 个目标字符串")
                total_deleted += count
            except Exception as e:
                print(f"[预览] {file_path}: 读取失败 - {str(e)}")
        else:
            # 实际处理
            success, count = clean_markdown_file(
                file_path, 
                args.string, 
                backup=not args.no_backup
            )
            if success:
                success_count += 1
                total_deleted += count
        
        total_processed += 1
    
    print("-" * 50)
    if args.dry_run:
        print(f"预览完成: 共检查 {total_processed} 个文件，将删除 {total_deleted} 个目标字符串")
    else:
        print(f"处理完成: {success_count}/{total_processed} 个文件成功，共删除 {total_deleted} 个目标字符串")


if __name__ == "__main__":
    main()


# 简化版本的使用示例
def simple_clean(file_or_directory, target_string="jsCopy to Clipboard"):
    """
    简化版本：清理文件或目录中的目标字符串
    
    使用示例:
    simple_clean("example.md")  # 处理单个文件
    simple_clean("./docs")      # 处理目录中的所有md文件
    """
    if os.path.isfile(file_or_directory):
        clean_markdown_file(file_or_directory, target_string)
    else:
        files = find_markdown_files(file_or_directory)
        for file_path in files:
            clean_markdown_file(file_path, target_string)


# 使用示例
if __name__ == "__main__":
    # 如果不想使用命令行参数，可以直接调用
    # simple_clean("./docs")  # 处理docs目录下的所有md文件
    # simple_clean("README.md")  # 处理单个文件
    main()