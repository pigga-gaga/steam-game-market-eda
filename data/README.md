# Data

The full Steam dataset should be placed locally at:

```text
data/steam_full.csv
```

The full dataset is not tracked by git. A small sample dataset is included at:

```text
data/sample_steam_games.csv
```

The sample is intended for demo, testing, and lightweight development only. It may not reproduce full analysis results exactly.

## Full Dataset Reference

The original full Steam file found during cleanup was:

```text
../steam_full_副本.csv
```

It has about 86,696 data rows and is about 56 MB, so it is kept outside the clean GitHub project.

## Main Fields Found

Key fields found in the Steam data include:

- `AppID`: Steam application ID.
- `name`: Game title.
- `release_date`: Release date.
- `required_age`: Minimum age requirement.
- `price`: Listed price.
- `dlc_count`: Number of DLC items.
- `windows`, `mac`, `linux`: Platform availability flags.
- `metacritic_score`: Metacritic score.
- `achievements`: Number of achievements.
- `recommendations`: Recommendation count.
- `supported_languages`: Supported language text field.
- `developers`: Developer names.
- `publishers`: Publisher names.
- `categories`: Steam category labels.
- `genres`: Steam genre labels.
- `positive`, `negative`: Review counts.
- `estimated_owners`: Owner range text.
- `average_playtime_forever`, `median_playtime_forever`: Lifetime playtime metrics.
- `average_playtime_2weeks`, `median_playtime_2weeks`: Recent playtime metrics.
- `peak_ccu`: Peak concurrent users.
- `total_reviews`, `positive_rate`, `negative_rate`: Derived review metrics.
- `median_estimated_owners`: Derived numeric owner estimate.
- `analysis_category`: Derived category used in prior analysis.

The dataset also contains many one-hot encoded columns with prefixes such as `languages_`, `categories_`, and `genres_`.

