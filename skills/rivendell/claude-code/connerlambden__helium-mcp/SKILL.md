# Helium MCP — News, Markets & AI Intelligence

Use this skill when users ask about news, media bias, stock markets, options trading, crypto, market analysis, balanced perspectives, or trending memes.

## Prerequisites

Helium MCP must be configured. Add to your MCP settings:

```json
{
  "mcpServers": {
    "helium": {
      "url": "https://heliumtrades.com/mcp"
    }
  }
}
```

## Available Tools

### News & Bias Analysis
- **search_news** — Search 3.2M+ articles from 5,000+ sources with bias scores across 15+ dimensions
- **search_balanced_news** — Get AI-synthesized balanced articles aggregating left/right/center perspectives
- **get_trending_topics** — Get currently trending news topics across all sources
- **get_source_bias** — Get detailed bias profile for any news source (e.g., CNN, Fox News, Reuters)
- **get_article_bias** — Get full multi-dimensional bias analysis for a specific article

### Market Data & Analysis
- **get_ticker** — Live stock/ETF/crypto price data with AI-generated bull/bear cases and price forecasts
- **get_option_price** — ML-predicted fair value and probability ITM for any option contract
- **get_top_trading_strategies** — Top-ranked options strategies with risk/reward analysis

### Other
- **search_memes** — Semantic search across trending memes

## Usage Patterns

- Compare media coverage: `search_news` with different sources, then highlight bias differences
- Get balanced views: `search_balanced_news` for multi-perspective synthesis on any topic
- Stock research: `get_ticker` for price + AI analysis, then `get_option_price` for derivatives
- Discover trading ideas: `get_top_trading_strategies` for AI-ranked setups

## Notes

- Free tier: 50 queries, no signup needed
- All tools are read-only
- More info: https://heliumtrades.com/mcp-page/
