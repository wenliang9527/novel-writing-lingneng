# novel-writing-lingneng

通用长篇小说写作技能，适用于任何小说项目。

## 功能

- **叙事指南**：视角纪律、滴水式世界构建、节奏控制、对白写作
- **章节类型模板**：日常章 / 研究探索章 / 战斗对抗章 / 过渡章 / 悬念收束章
- **AI 痕迹自查清单**：16 项常见 AI 写作模式及修正方案
- **字数统计工具**：`scripts/count_words.py`，按"汉字+字母+数字"标准统计

## 用法

作为 [opencode](https://opencode.ai) / Claude Code / Codex 技能加载：

```bash
# 在项目目录下
skill novel-writing-lingneng
```

字数统计：

```bash
python scripts/count_words.py                              # 全部
python scripts/count_words.py --volume "第一卷 卷名"       # 指定卷
python scripts/count_words.py --volume "第一卷 卷名" --chapter 1  # 指定章
python scripts/count_words.py --min-words 2500              # 自定义警告线
```

## 文件结构

```
novel-writing-lingneng/
├── SKILL.md                  # 技能主文件
├── scripts/
│   └── count_words.py        # 字数统计脚本
└── README.md
```

## 集成方式

将本仓库克隆或复制到项目下的 `.opencode/skills/novel-writing-lingneng/` 目录，加载 skill 后即可在写作时调用。
