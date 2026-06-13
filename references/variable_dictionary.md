# Variable Dictionary

This dictionary describes the main variables used in the Steam game market EDA project. Variables marked as derived are created or standardized by the analysis script.

## Main Variables

| Field | Source | Description |
| --- | --- | --- |
| `AppID` | Raw field | Unique Steam application ID. |
| `name` | Raw field | Game or application title. |
| `release_date` | Raw field | Release date of the Steam app. |
| `release_year` | Derived variable | Year extracted from `release_date` for release trend analysis. |
| `price` | Raw field, standardized as numeric | Listed price. Free games have a price of 0. |
| `price_range` | Derived variable | Price bucket used for business analysis. Current buckets are Free, Low, Mid, High, Premium, and Unknown. |
| `developers` | Raw field | Developer name or list of developer names. Used as the preferred entity for HHI concentration analysis. |
| `publishers` | Raw field | Publisher name or list of publisher names. Used as a fallback entity for HHI if developer data is unavailable. |
| `genres` | Raw field | Steam genre labels, such as Action, Adventure, Casual, Indie, RPG, Simulation, or Strategy. |
| `categories` | Raw field | Steam category labels, such as single-player, co-op, controller support, or in-app purchases. |
| `primary_genre` | Derived variable | Main genre used for grouped analysis. It is extracted from the first value in `genres`, with `analysis_category` used as a fallback when available. |
| `analysis_category` | Existing derived field from source data | Category label created in the previous course analysis and used as a fallback for `primary_genre`. |
| `is_indie` | Derived variable | Binary flag equal to 1 when Indie appears in `genres` or `categories`, otherwise 0. |
| `positive` | Raw field, standardized as numeric | Count of positive Steam reviews. |
| `negative` | Raw field, standardized as numeric | Count of negative Steam reviews. |
| `total_reviews` | Existing or derived variable | Total review count. If missing, it is calculated as `positive + negative`. |
| `positive_rate` | Existing derived field from source data | Positive review rate found in the source CSV. |
| `positive_review_rate` | Derived variable | Positive review rate used by the EDA script. It uses `positive_rate` when available, otherwise calculates `positive / (positive + negative)`. |
| `estimated_owners` | Raw field | Estimated owner range as text, such as `50,000 - 100,000`. This is not exact commercial performance data. |
| `median_estimated_owners` | Existing derived field from source data | Numeric owner estimate already included in the source CSV. |
| `estimated_owners_midpoint` | Derived variable | Numeric owner midpoint used for aggregation. It uses `median_estimated_owners` when available, otherwise parses the midpoint from `estimated_owners`. |
| `average_playtime_forever` | Raw field, standardized as numeric | Average lifetime playtime. |
| `median_playtime_forever` | Raw field, standardized as numeric | Median lifetime playtime. |
| `average_playtime_2weeks` | Raw field | Average playtime in the recent two-week window. |
| `median_playtime_2weeks` | Raw field | Median playtime in the recent two-week window. |
| `recommendations` | Raw field, standardized as numeric | Number of Steam recommendations. |
| `metacritic_score` | Raw field, standardized as numeric | Metacritic score when available. |
| `windows` | Raw field | Whether the app supports Windows. |
| `mac` | Raw field | Whether the app supports macOS. |
| `linux` | Raw field | Whether the app supports Linux. |
| `required_age` | Raw field | Minimum age requirement listed for the app. |
| `dlc_count` | Raw field | Number of DLC items associated with the app. |
| `achievements` | Raw field | Number of Steam achievements. |
| `supported_languages` | Raw field | Text field listing supported languages. |
| `peak_ccu` | Raw field | Peak concurrent users. |

## Encoded Field Groups

| Prefix | Source | Description |
| --- | --- | --- |
| `languages_` | Encoded raw/processed fields | One-hot encoded supported language indicators. |
| `categories_` | Encoded raw/processed fields | One-hot encoded Steam category indicators. |
| `genres_` | Encoded raw/processed fields | One-hot encoded Steam genre indicators. |

## Analysis Notes

- `estimated_owners_midpoint` is an approximation because Steam owner data is range-based.
- `positive_review_rate` is a descriptive review metric and should not be treated as a direct measure of commercial success.
- `price_range` is used to simplify pricing analysis for BI-style reporting.
- HHI in this project is calculated from developer or publisher game-count share within each `primary_genre`; it is not revenue-based concentration.
