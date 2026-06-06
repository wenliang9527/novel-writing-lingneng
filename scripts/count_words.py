# -*- coding: utf-8 -*-
"""
字数统计工具

字数计算标准（与 novel-writing-lingneng skill 一致）：
汉字+字母+数字，不包含任何标点符号和空白。

用法：
  python count_words.py                          # 统计所有卷
  python count_words.py --volume 第四卷          # 统计指定卷
  python count_words.py --volume 第四卷 --chapter 1   # 统计指定章
  python count_words.py --min-words 2500         # 设定警告线
"""

import os, re, sys, argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

TEXT_DIR = None
for candidate in [
    os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '0001', '正文')),
    os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..', '正文')),
]:
    if os.path.isdir(candidate):
        TEXT_DIR = candidate
        break

if TEXT_DIR is None:
    print('错误：找不到正文目录', file=sys.stderr)
    sys.exit(1)

def strip_punctuation(text):
    return re.sub(r'[\u3000-\u303f\uff00-\uffef\uff0c\u3001\u3002\uff1f\uff01\uff1b\uff1a\u201c\u201d\u2018\u2019\uff08\uff09\u3010\u3011\u300a\u300b\u2014\u2026\u00b7\uff0d\,\!\.\?\;\:"\(\)\[\]\{\}\-\#\*\n\r\t \u3000]', '', text).replace('#', '')

def count_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return len(strip_punctuation(text))

def scan_volume(vol_name, min_words):
    vol_path = os.path.join(TEXT_DIR, vol_name)
    if not os.path.isdir(vol_path):
        return [], 0
    results = []
    total = 0
    for d in sorted(os.listdir(vol_path)):
        dirpath = os.path.join(vol_path, d)
        if not os.path.isdir(dirpath):
            continue
        for f in os.listdir(dirpath):
            if f.endswith('.md'):
                fp = os.path.join(dirpath, f)
                count = count_file(fp)
                status = 'OK' if count >= min_words else 'SHORT'
                results.append((d, count, status))
                total += count
    return results, total

def main():
    parser = argparse.ArgumentParser(description='统计小说正文字数')
    parser.add_argument('--volume', '-v', help='指定卷名（如 "第四卷 异界之潮"），不指定则统计所有卷')
    parser.add_argument('--chapter', '-c', type=int, help='指定章号（需同时指定 --volume）')
    parser.add_argument('--min-words', '-m', type=int, default=3000, help='字数警告线（默认 3000）')
    args = parser.parse_args()

    if args.chapter and not args.volume:
        print('错误：指定 --chapter 时必须同时指定 --volume')
        sys.exit(1)

    if args.volume:
        volumes = [args.volume]
    else:
        volumes = sorted(os.listdir(TEXT_DIR)) if os.path.isdir(TEXT_DIR) else []

    if not volumes:
        print(f'未找到正文目录: {TEXT_DIR}')
        sys.exit(1)

    grand_total = 0
    for vol in volumes:
        results, vol_total = scan_volume(vol, args.min_words)
        if not results:
            continue
        print(f'\n=== {vol} ===')
        for name, count, status in results:
            if args.chapter:
                tag = f'第{args.chapter}章'
                if tag in name:
                    print(f'  {name}: {count}字 [{status}]')
                    grand_total += count
            else:
                print(f'  {name}: {count}字 [{status}]')
                grand_total += count
        if not args.chapter:
            total_status = 'OK' if vol_total >= args.min_words * len(results) else 'SHORT'
            print(f'  卷合计: {vol_total}字 [{total_status}]')

    if args.chapter:
        print(f'\n总计: {grand_total}字')
    else:
        print(f'\n全书总计: {grand_total}字')

if __name__ == '__main__':
    main()
