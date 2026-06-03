# AI Timeline

记录文生图、文生视频、大语言模型等 AI 相关技术在发展过程中的重要时间点。

## 项目说明

这是一个中文的 AI 技术发展时间线仓库，追踪人工智能领域的关键里程碑事件，包括：

- **大语言模型 (LLM)** — GPT、Claude、Gemini、LLaMA 等
- **文生图 (Text-to-Image)** — DALL·E、Midjourney、Stable Diffusion 等
- **文生视频 (Text-to-Video)** — Sora、Runway、Pika 等
- **语音/音频 (Speech/Audio)** — Whisper、VALL-E、Suno 等
- **研究突破 (Research)** — 重要论文、开源模型、基准测试
- **政策与监管 (Policy)** — AI 治理、法规、行业动态

## 参考来源

- [mrrhq/ai-timeline](https://github.com/mrrhq/ai-timeline) — 综合 AI 时间线
- [hollobit/GenAI_LLM_timeline](https://github.com/hollobit/GenAI_LLM_timeline) — ChatGPT、Generative AI 和 LLM 时间线
- [NHLOCAL/AiTimeline](https://github.com/NHLOCAL/AiTimeline) — 2022 年起现代 AI 爆发期时间线
- [jam3scampbell/AI-timeline](https://github.com/jam3scampbell/AI-timeline) — 交互式 AGI 时间线
- [Epoch AI Data](https://epoch.ai/data/ai-models) — AI 模型数据库（1950 年至今）
- [steven2358/awesome-generative-ai](https://github.com/steven2358/awesome-generative-ai) — 生成式 AI 里程碑
- [AlonzoLeeeooo/awesome-text-to-image-studies](https://github.com/AlonzoLeeeooo/awesome-text-to-image-studies) — 文生图论文时间线

## 数据结构

所有事件以 YAML 格式存储在 `data/` 目录，按年份组织。每个事件包含以下字段：

```yaml
- date: "YYYY-MM-DD"          # 日期（尽可能精确）
  title: "事件标题"            # 事件名称
  category: "llm"             # 分类：llm | image | video | speech | research | policy | business
  description: "详细描述"      # 事件描述（中文）
  links:                      # 相关链接
    - text: "论文"
      url: "https://arxiv.org/..."
    - text: "博客"
      url: "https://openai.com/..."
  tags: ["OpenAI", "GPT"]     # 标签
```

## 使用方式

### 查看时间线

- 按年份浏览：`timeline/` 目录下的 Markdown 文件
- 完整数据：`data/` 目录下的 YAML 文件
- 在线版本：计划部署为静态网站

### 贡献数据

1. 编辑 `data/YYYY.yml` 文件添加新事件
2. 运行 `scripts/generate_timeline.py` 重新生成 Markdown
3. 提交 Pull Request

### 本地运行

```bash
# 克隆仓库
git clone https://github.com/yourusername/ai-timeline.git
cd ai-timeline

# 生成时间线（需要 Python 3.8+）
pip install -r requirements.txt
python scripts/generate_timeline.py

# 启动预览服务器
python -m http.server 8000
# 访问 http://localhost:8000/timeline/
```

## 时间线概览

| 年份 | 文件 | 事件数 |
|------|------|--------|
| 2026 | [2026.md](timeline/2026.md) | 持续更新 |
| 2025 | [2025.md](timeline/2025.md) | 持续更新 |
| 2024 | [2024.md](timeline/2024.md) | 整理中 |
| 2023 | [2023.md](timeline/2023.md) | 整理中 |
| 2022 | [2022.md](timeline/2022.md) | 整理中 |

## 分类说明

| 分类 | 标识 | 说明 |
|------|------|------|
| 大语言模型 | `llm` | GPT、Claude、Gemini、LLaMA 等对话/推理模型 |
| 文生图 | `image` | DALL·E、Midjourney、Stable Diffusion 等 |
| 文生视频 | `video` | Sora、Runway、Pika、可灵等 |
| 语音/音频 | `speech` | TTS、ASR、音乐生成、语音克隆 |
| 研究突破 | `research` | 重要论文、开源模型、新架构、基准测试 |
| 政策监管 | `policy` | AI 治理、法规、伦理、安全 |
| 商业动态 | `business` | 融资、并购、产品发布、合作 |

## 许可证

MIT License — 欢迎自由使用、修改和分发。

---

*记录 AI 历史，见证智能未来。*
