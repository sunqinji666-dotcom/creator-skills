# 阿里云智能语音交互（ISI）- 语音识别技能

## 功能说明
将音频/视频文件自动转换为文字，支持：
- 多种音频格式（mp3/wav/m4a/flac/mp4/mov 等）
- 输出格式：纯文本 / SRT 字幕
- 自动音频预处理（采样率转换/单声道）

## 快速开始

### 1. 配置阿里云 AccessKey

```bash
# 复制配置模板
cp ~/.my_skills/voice/ali-isi-config.example.sh ~/.my_skills/voice/ali-isi-config.sh

# 编辑配置文件，填入你的阿里云密钥
nano ~/.my_skills/voice/ali-isi-config.sh
```

**获取密钥步骤：**
1. 登录 [阿里云控制台](https://homenew.console.aliyun.com/)
2. 进入 [智能语音交互控制台](https://nls-portal.console.aliyun.com/)
3. 创建项目，获取 `AppKey`
4. 在 [AccessKey 管理](https://ram.console.aliyun.com/manage/ak) 获取 `AccessKey ID` 和 `AccessKey Secret`

### 2. 使用命令

```bash
# 基础用法（输出 .txt）
ali-isi-transcribe.sh 会议录音.mp4

# 指定语言（英文）
ali-isi-transcribe.sh interview.mp3 -l en

# 输出 SRT 字幕文件
ali-isi-transcribe.sh video.mp4 -f srt

# 指定输出路径
ali-isi-transcribe.sh audio.wav -o /path/to/output.txt

# 查看帮助
ali-isi-transcribe.sh -h
```

## 输出示例

```
🔑 正在获取 Access Token...
🔄 正在转换音频格式...
🎙️ 正在识别语音...
✅ 已生成文本: 会议录音.txt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 识别完成！
📄 输出文件: 会议录音.txt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 与现有工具对比

| 特性 | whisper (本地) | 阿里云 ISI |
|------|---------------|-----------|
| 依赖 | 本地 GPU/CPU | 云端 API |
| 成本 | 免费 | 按量付费 |
| 速度 | 取决于硬件 | 快速（云端） |
| 语言支持 | 多语言 | 中文优化好 |
| 适用场景 | 离线/大批量 | 快速/集成阿里云生态 |

## 故障排查

### Q: 提示 "获取 Token 失败"
- 检查 `ali-isi-config.sh` 中的 `ALI_AK` 和 `ALI_SK` 是否正确
- 确认 AccessKey 状态为"启用"

### Q: 提示 "缺少依赖命令"
```bash
brew install ffmpeg curl jq
```

### Q: 识别结果不准确
- 尝试指定正确的语言代码：`-l cn`（中文）或 `-l en`（英文）
- 确保音频质量清晰，无过多背景噪音

## 计费说明
- 一句话识别：按调用次数计费
- 详细价格请查看 [产品定价页](https://www.aliyun.com/price/product#/nls/detail)

## 文件位置
- 主脚本：由使用者自行安装并加入 `PATH`
- 配置模板：由使用者自行维护本地示例文件
- 用户配置：仅保留在本机，勿提交
