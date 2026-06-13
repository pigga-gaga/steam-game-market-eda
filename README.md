# Steam Game Market EDA and Strategy Analysis

## 1. Project Title

**Steam Game Market EDA and Strategy Analysis**

An exploratory data analysis project on the Steam game market, focusing on market trends, pricing, genre competition, review performance, and publishing strategy insights.

## 2. Background

Steam is one of the largest PC game distribution platforms, with a wide mix of indie titles, premium releases, free-to-play games, and niche genres. For game publishers, developers, and market analysts, it is useful to understand how games are distributed across genres, price bands, review performance, and competitive concentration.

This project cleans and restructures a course project into a portfolio-ready EDA project for data analysis, BI, business analysis, and data operations roles.

## 3. Business Questions

- Which genres dominate the recent Steam game market by game count?
- How are games distributed across price ranges?
- Do different price ranges show different review performance and owner estimates?
- How do indie games differ from non-indie games in price and review performance?
- Which genres appear more fragmented or concentrated by developer-level HHI?
- What publishing strategy signals can be drawn from these market patterns?

## 4. Dataset

The full local dataset contains Steam game records from 2020 to 2025.

- Full dataset used for current outputs: `data/steam_full.csv`
- Raw full-data shape from the analysis run: 86,696 rows x 206 columns
- EDA output shape after derived variables: 86,696 rows x 212 columns
- Full data is not tracked by git
- Demo sample included in the repository: `data/sample_steam_games.csv`

Main fields include game title, release date, price, genres, categories, developers, publishers, review counts, estimated owners, recommendations, playtime, platform support, and Metacritic score.

## 5. Methodology

The analysis script performs lightweight EDA without machine learning models.

Core steps:

- Load `data/steam_full.csv` if available, otherwise fall back to `data/sample_steam_games.csv`
- Standardize numeric fields such as price, reviews, recommendations, playtime, and Metacritic score
- Create derived variables:
  - `release_year`
  - `total_reviews`
  - `positive_review_rate`
  - `price_range`
  - `estimated_owners_midpoint`
  - `is_indie`
  - `primary_genre`
- Generate summary tables under `outputs/tables/`
- Generate matplotlib charts under `outputs/figures/`
- Calculate developer-level HHI by primary genre to describe competitive concentration

## 6. Key Findings

These findings are based on the full-data outputs, not the sample dataset.

1. **The market is heavily concentrated by game count in a few broad genres.**  
   Action has 37,452 games, accounting for 43.2% of the dataset. Adventure has 22,864 games, or 26.4%. Casual has 18,229 games, or 21.0%. Together, these three primary genres represent about 90.6% of all games in the full dataset.

2. **Most games are in low and mid price bands.**  
   Low-price games account for 39,735 titles, while mid-price games account for 31,711 titles. High-price games account for 10,212 titles, free games for 2,956 titles, and premium games for 2,082 titles. This suggests that Steam's recent catalog is strongly weighted toward accessible pricing tiers.

3. **Review performance differs by price range, but this is descriptive rather than causal.**  
   Free games have the highest average positive review rate at 69.3%, followed by high-price games at 66.6%. Low-price games have a lower average positive review rate at 55.6%, while mid and premium games are both around 60.5%. This pattern may reflect differences in product positioning, audience expectations, and game quality signals, but it does not prove that price causes review outcomes.

4. **Indie games form the majority of the analyzed catalog.**  
   The analysis identifies 63,288 indie games and 23,408 non-indie games. Indie games have a lower average price, 7.65 versus 11.76 for non-indie games, and a higher average positive review rate, 61.1% versus 54.5%. This supports a portfolio insight that indie titles are a major supply-side force in the recent Steam market.

5. **Some smaller genres show strong review performance, but sample size matters.**  
   Free to Play has the highest average positive review rate among primary genres at 70.4%, but it only has 129 games. Strategy has an average positive review rate of 64.1%, Indie has 63.9%, and Action has 61.4%. Small categories such as Sports and Violent should be interpreted carefully because their game counts are limited.

6. **Large genres are highly fragmented by developer-level HHI.**  
   Action has an HHI of 0.00019 across 16,546 developers or publishers, Adventure has 0.00055 across 8,267, and Casual has 0.00045 across 7,787. These very low HHI values indicate that major genres are highly fragmented and competitive by game-count share.

7. **Niche categories may appear more concentrated, but small game counts affect interpretation.**  
   Sports has an HHI of 0.1006 with 13 games, and Massively Multiplayer has an HHI of 0.0449 with 32 games. These higher HHI values suggest more concentration, but the small number of games means the result should be treated as a directional signal rather than a definitive market conclusion.

## 7. How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the EDA script:

```bash
python src/analysis.py
```

Expected behavior:

- If `data/steam_full.csv` exists, the script uses the full local dataset
- If full data is missing, the script uses `data/sample_steam_games.csv`
- Tables are saved to `outputs/tables/`
- Figures are saved to `outputs/figures/`

The full dataset is intentionally ignored by git.

## 8. Project Structure

```text
steam-game-market-eda-clean/
|-- README.md
|-- requirements.txt
|-- data/
|   |-- README.md
|   `-- sample_steam_games.csv
|-- docs/
|   |-- interview_notes.md
|   `-- project_summary.md
|-- outputs/
|   |-- figures/
|   `-- tables/
|-- references/
|   |-- original_data_preprocessing.py
|   `-- variable_dictionary.md
`-- src/
    `-- analysis.py
```

## 9. Limitations

- This is an exploratory analysis, not a causal study.
- The project does not estimate future commercial outcomes.
- Steam owner estimates are range-based and approximate.
- Review performance may be affected by genre norms, player expectations, marketing, game quality, and community effects.
- HHI is calculated by developer or publisher game-count share, not by revenue or active users.
- Small genres can produce unstable averages and concentration metrics.
- The dataset should not be interpreted as official Steam market research.

## 10. What I Learned

- How to restructure a messy course project into a clean portfolio project
- How to design reproducible EDA outputs for BI-style reporting
- How to engineer business-friendly metrics such as price range, positive review rate, indie flag, owner midpoint, and genre-level HHI
- How to translate descriptive patterns into cautious publishing strategy insights
- How to separate exploratory evidence from causal claims
