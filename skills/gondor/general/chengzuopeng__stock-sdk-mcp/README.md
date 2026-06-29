# Stock SDK MCP Skills

本目录包含基于 `stock-sdk-mcp` 构建的 **AI Skills（技能）**。

Skills 是对底层原子工具（Tools）的**二次逻辑封装**。它们不仅仅是调用接口，而是通过一套"思维链（CoT）"告诉 AI 应该如何步步深入地分析市场。

---

## 📁 预置技能深度解析

| Skill | 核心逻辑 | 适用场景 |
|-------|----------|----------|
| **[stock-analyst](./stock-analyst/SKILL.md)** | **深度技术分析**。利用多周期 K 线和指标交叉验证趋势。 | 个股诊断、买卖点评估、MACD/KDJ 形态识别 |
| **[stock-screener](./stock-screener/SKILL.md)** | **量化筛选器**。支持全市场 A/港/美 2万+ 标的的条件过滤。 | 寻找涨停板、低估值蓝筹寻找、板块龙头挖掘 |
| **[market-overview](./market-overview/SKILL.md)** | **全景扫描仪**。汇总指数、行业、概念、情绪等多个维度。 | 开盘点评、复盘报告、热点跟踪 |
| **[realtime-monitor](./realtime-monitor/SKILL.md)** | **智能管家**。实时跟踪自选股异动并动态计算盈亏。 | 组合盯盘、价格预警、投后管理 |

---

## 💡 核心方法应用：`get_kline_with_indicators`

在本项目的 Skills 架构中，最重要的底层能力是工具 `get_kline_with_indicators`。

### 为什么它对 AI 至关重要？
普通的股票 API 通常只返回原始的 OHLC 数据，AI 很难直接通过数字计算出 MACD 或 RSI（计算开销大且易出错）。
我们的这个方法**在 MCP 服务端直接完成了指标计算**，返回给 AI 的是：
- 每一天的 `ma5`, `ma20` 数值
- 每一天的 `macd_dif`, `macd_dea` 柱状图数据
- 每一天的 `rsi`, `kdj` 等实时状态

### 在 Skills 中的实际应用示例
在 [stock-analyst](./stock-analyst/SKILL.md) 技能中，AI 被指令执行如下操作：
1. **获取数据**：调用 `get_kline_with_indicators(symbol="600519", indicators={"ma": true, "macd": true})`。
2. **逻辑对比**：AI 直接对比 `close` 与 `ma20` 的关系，判断是否突破压力位。
3. **信号捕捉**：AI 观察 `macd_macd`（柱状图）从负转正的过程，识别"水下金叉"。

---

## 🔧 AI 服务平台安装说明

### 重点：OpenClaw 集成

OpenClaw 是本项目的**第一优先级支持方案**，它能完美解析 Skill 文件夹。

1. **指向配置**：
   在 `~/.clawdbot/config.yaml` 中添加：
   ```yaml
   skills:
     directories:
       - /你的本地路径/stock-sdk-mcp/skills
   ```
2. **动态加载**：
   OpenClaw 会将 `SKILL.md` 顶部的 YAML Frontmatter 自动转为 Agent 的 Metadata。
3. **HTTP 自动化**：
   你可以直接通过 REST API 触发技能，实现自动化交易提醒逻辑。

### IDE 全局配置（Cursor / Antigravity）

如果你希望 AI 永远记住这些技能，建议操作：
- **Cursor**：将 Skills 的内容分别保存到 `.cursor/rules/stock-analyst.md` 类似的规则文件中。
- **自定义指令**：在设置中添加："当提到股票时，参考当前项目 `skills/` 目录下的逻辑规范进行分析。"

---

## 🚀 进阶：编写通用的 Skills

为了让你的 Skill 兼容所有平台，请遵循本项目定义的 **Skill 编写规范**：

1. **自包含说明**：Skill 必须包含明确的身份设定（如"你是一个分析师"）。
2. **多模态友好**：输出应包含 Markdown 表格或简单的 ASCII 图表。
3. **错误优雅处理**：明确告诉 AI 如果 `get_quotes_by_query` 没查到结果，应该提示用户修正名称，而不是编造。

---

## 📄 License

ISC © [chengzuopeng](https://github.com/chengzuopeng/stock-sdk-mcp)
