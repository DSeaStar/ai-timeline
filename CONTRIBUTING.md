# AI Timeline 数据贡献指南

## 数据格式

每个事件是一个 YAML 对象，包含以下字段：

```yaml
- date: "YYYY-MM-DD"          # 必填，日期
  title: "事件标题"            # 必填，简短标题
  category: "llm"             # 必填，分类
  description: "详细描述"      # 必填，中文描述
  links:                      # 可选，相关链接
    - text: "链接文字"
      url: "https://..."
  tags: ["标签1", "标签2"]     # 可选，标签
```

## 分类说明

| 分类值 | 说明 | 适用场景 |
|--------|------|----------|
| `llm` | 大语言模型 | GPT、Claude、Gemini、LLaMA 等 |
| `image` | 文生图 | DALL·E、Midjourney、Stable Diffusion 等 |
| `video` | 文生视频 | Sora、Runway、Pika、可灵等 |
| `speech` | 语音/音频 | TTS、ASR、音乐生成 |
| `research` | 研究突破 | 重要论文、开源模型、新架构 |
| `policy` | 政策监管 | AI 治理、法规、伦理 |
| `business` | 商业动态 | 融资、并购、产品发布 |

## 提交规范

1. 确保日期准确（尽量精确到日，若不确定可用月初/月末）
2. 描述使用中文，客观简洁
3. 提供可靠来源链接（官方博客、arXiv、权威媒体）
4. 标签使用 2-4 个，包含公司和产品名
5. 按时间顺序添加到 YAML 文件中

## 更新后操作

```bash
pip install -r requirements.txt
python scripts/generate_timeline.py
```

提交时包含 `data/` 和 `timeline/` 的变更。
