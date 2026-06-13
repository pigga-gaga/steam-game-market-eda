# Project Summary

## English Project Summary

This project is an exploratory data analysis of the Steam game market. It analyzes recent Steam game records from 2020 to 2025, focusing on genre distribution, pricing structure, review performance, indie versus non-indie differences, and genre-level competition concentration. The project uses business-friendly derived metrics such as price range, positive review rate, estimated owner midpoint, indie flag, primary genre, and developer-level HHI. The goal is to translate descriptive data patterns into publishing strategy insights without making causal claims or future performance forecasts.

## Chinese Project Summary

这个项目是一个 Steam 游戏市场探索性数据分析项目，分析 2020 到 2025 年的 Steam 游戏数据，重点关注游戏类型分布、价格结构、用户口碑、独立游戏与非独立游戏差异，以及不同类型内部的竞争集中度。项目构造了价格区间、好评率、所有者中点估计、是否独立游戏、主类型和 HHI 等业务指标，并把描述性数据模式转化为发行策略洞察。项目不做未来商业表现预测，也不把相关性解释为因果关系。

## English Resume Bullets

- Conducted EDA on 86K+ Steam game records, analyzing genre distribution, pricing bands, review performance, ownership estimates, and platform-related game attributes.
- Engineered business metrics including positive review rate, price range, estimated owner midpoint, indie flag, primary genre, and genre-level HHI to support market and publishing strategy analysis.
- Built reproducible Python outputs with pandas and matplotlib, generating summary tables and visualizations that translate Steam market patterns into portfolio-ready BI insights.

## Chinese Resume Bullets

- 基于 8.6 万余条 Steam 游戏数据完成探索性数据分析，分析类型分布、价格区间、好评表现、所有者估计和平台相关字段。
- 构造好评率、价格区间、所有者中点估计、是否独立游戏、主类型和类型 HHI 等业务指标，用于支持市场结构和发行策略分析。
- 使用 pandas 和 matplotlib 生成可复现的汇总表与可视化结果，将 Steam 市场数据模式转化为适合作品集展示的 BI 洞察。

## 1-Minute Chinese Interview Script

这个项目是一个 Steam 游戏市场 EDA 项目。我主要想解决的问题是：从平台游戏数据中，如何理解市场结构、价格分布、玩家口碑和竞争程度。

我先整理了原始课程项目，把它重构成 clean 的作品集项目。分析部分使用 pandas 和 matplotlib，读取完整 Steam 数据后构造了几个业务指标，包括发行年份、价格区间、好评率、所有者中点估计、是否独立游戏、主类型和 HHI。

从结果看，Action、Adventure 和 Casual 是数量占比最高的三个类型；低价和中价游戏占多数；独立游戏数量很多，平均价格更低，好评率略高；大类型的 HHI 很低，说明竞争非常分散。这个项目的价值在于，它不只是画图，而是把图表转化成发行策略层面的解释，比如热门大类虽然市场大，但也更拥挤，需要更明确的差异化定位。

## 2-Minute Chinese Interview Script

这个项目是我把一个课程项目整理成作品集后的 Steam 游戏市场探索性分析项目。项目目标不是做未来商业表现预测，而是站在数据分析和 BI 的角度，回答几个业务问题：Steam 最近几年的游戏主要集中在哪些类型，不同价格区间的表现有什么差异，独立游戏和非独立游戏有什么不同，以及不同类型内部的竞争是否分散。

数据方面，我保留了完整数据的本地运行逻辑，同时在 GitHub 项目中只保留 sample 数据，避免上传大文件。代码会优先读取 `data/steam_full.csv`，如果没有完整数据，就读取 sample。分析中我构造了几个关键指标：`release_year` 用来看发行趋势，`price_range` 用来看定价结构，`positive_review_rate` 用来衡量玩家口碑，`estimated_owners_midpoint` 用来近似衡量用户规模，`is_indie` 用来区分独立游戏，`primary_genre` 用来做类型汇总。另外我还用 HHI 来衡量每个类型内部开发者或发行商的集中度。

完整数据结果显示，Action、Adventure 和 Casual 是数量占比最高的类型，三者合计占比超过九成，说明这些大类供给非常密集。价格上，低价和中价游戏数量最多；从平均好评率看，免费和高价区间表现较高，但这只是描述性关系，不能解释为价格导致好评。独立游戏数量明显多于非独立游戏，平均价格更低，平均好评率略高。HHI 结果显示 Action、Adventure、Casual 这类大市场非常分散，意味着竞争激烈，新产品进入时需要更清晰的定位。

这个项目最能体现的是我把原始数据转成业务指标、汇总表和可视化结果的能力，也体现了我在解释数据时会区分相关性和因果，不夸大结论。
