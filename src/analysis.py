"""Steam game market EDA script.

This script uses the full local dataset when available. If the full dataset is
not present, it falls back to the tracked sample dataset for lightweight demo
outputs.
"""

from __future__ import annotations

import ast
import os
import re
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_TABLE_DIR = PROJECT_ROOT / "outputs" / "tables"
OUTPUT_FIGURE_DIR = PROJECT_ROOT / "outputs" / "figures"
MPL_CACHE_DIR = PROJECT_ROOT / ".matplotlib_cache"

FULL_DATA_PATH = DATA_DIR / "steam_full.csv"
SAMPLE_DATA_PATH = DATA_DIR / "sample_steam_games.csv"

MPL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE_DIR))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


WARNINGS: list[str] = []
PRICE_RANGE_ORDER = ["Free", "Low", "Mid", "High", "Premium", "Unknown"]


def warn(message: str) -> None:
    """Print and store a warning without stopping the EDA run."""
    WARNINGS.append(message)
    print(f"WARNING: {message}")


def ensure_output_dirs() -> None:
    OUTPUT_TABLE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FIGURE_DIR.mkdir(parents=True, exist_ok=True)


def load_dataset() -> tuple[pd.DataFrame, str, Path]:
    """Load full data first; fall back to the tracked sample data."""
    if FULL_DATA_PATH.exists():
        data_source = "full"
        data_path = FULL_DATA_PATH
    elif SAMPLE_DATA_PATH.exists():
        data_source = "sample"
        data_path = SAMPLE_DATA_PATH
    else:
        raise FileNotFoundError(
            "No Steam dataset found. Place the full dataset at "
            f"{FULL_DATA_PATH}, or keep a demo sample at {SAMPLE_DATA_PATH}."
        )

    print(f"Using {data_source} data: {data_path}")
    df = pd.read_csv(data_path, encoding="utf-8-sig", low_memory=False)
    df.columns = [str(col).strip() for col in df.columns]
    return df, data_source, data_path


def has_columns(df: pd.DataFrame, columns: Iterable[str]) -> bool:
    return all(column in df.columns for column in columns)


def to_numeric_series(df: pd.DataFrame, column: str) -> pd.Series:
    """Return a numeric column, or an all-NA series if the field is missing."""
    if column not in df.columns:
        warn(f"Missing field skipped: {column}")
        return pd.Series(np.nan, index=df.index, dtype="float64")
    return pd.to_numeric(df[column], errors="coerce")


def parse_list_like(value: object) -> list[str]:
    """Parse Steam list-style strings such as ['Action', 'Indie'] safely."""
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]

    if value is None:
        return []

    try:
        if pd.isna(value):
            return []
    except (TypeError, ValueError):
        return []

    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "[]"}:
        return []

    try:
        parsed = ast.literal_eval(text)
        if isinstance(parsed, list):
            return [str(item).strip() for item in parsed if str(item).strip()]
        if isinstance(parsed, tuple):
            return [str(item).strip() for item in parsed if str(item).strip()]
    except (SyntaxError, ValueError):
        pass

    parts = re.split(r"\s*[;,|]\s*", text)
    return [part.strip(" '\"[]") for part in parts if part.strip(" '\"[]")]


def first_label(value: object) -> str | None:
    labels = parse_list_like(value)
    return labels[0] if labels else None


def contains_label(value: object, target: str) -> bool:
    target_lower = target.lower()
    return any(target_lower == label.lower() for label in parse_list_like(value))


def parse_owner_midpoint(value: object) -> float:
    """Extract a midpoint from owner ranges such as '50,000 - 100,000'."""
    if value is None or pd.isna(value):
        return np.nan

    numbers = re.findall(r"\d[\d,]*", str(value))
    numeric_values = [float(number.replace(",", "")) for number in numbers]

    if len(numeric_values) >= 2:
        return float(np.mean(numeric_values[:2]))
    if len(numeric_values) == 1:
        return numeric_values[0]
    return np.nan


def assign_price_range(price: object) -> str:
    """Bucket prices into portfolio-friendly market bands."""
    if pd.isna(price):
        return "Unknown"

    price_value = float(price)
    if price_value <= 0:
        return "Free"
    if price_value <= 5:
        return "Low"
    if price_value <= 15:
        return "Mid"
    if price_value <= 30:
        return "High"
    return "Premium"


def build_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Create the core EDA metrics used by tables and charts."""
    df = df.copy()

    # Normalize core numeric fields so aggregations are stable.
    df["price"] = to_numeric_series(df, "price")
    df["positive"] = to_numeric_series(df, "positive")
    df["negative"] = to_numeric_series(df, "negative")
    df["recommendations"] = to_numeric_series(df, "recommendations")
    df["average_playtime_forever"] = to_numeric_series(
        df, "average_playtime_forever"
    )
    df["median_playtime_forever"] = to_numeric_series(df, "median_playtime_forever")
    df["metacritic_score"] = to_numeric_series(df, "metacritic_score")

    # release_year supports trend analysis by launch timing.
    if "release_date" in df.columns:
        df["release_year"] = pd.to_datetime(
            df["release_date"], errors="coerce"
        ).dt.year
    else:
        df["release_year"] = np.nan
        warn("release_date missing; release year trend outputs may be skipped.")

    # total_reviews is reused as a reliability filter for review-rate metrics.
    if "total_reviews" in df.columns:
        df["total_reviews"] = pd.to_numeric(df["total_reviews"], errors="coerce")
    elif has_columns(df, ["positive", "negative"]):
        df["total_reviews"] = df["positive"] + df["negative"]
    else:
        df["total_reviews"] = np.nan
        warn("positive/negative missing; total_reviews could not be constructed.")

    # positive_review_rate is stored as a 0-100 percentage for readable outputs.
    if "positive_rate" in df.columns:
        df["positive_review_rate"] = pd.to_numeric(
            df["positive_rate"], errors="coerce"
        )
    elif has_columns(df, ["positive", "negative"]):
        denominator = df["positive"] + df["negative"]
        df["positive_review_rate"] = np.where(
            denominator > 0, df["positive"] / denominator * 100, np.nan
        )
    else:
        df["positive_review_rate"] = np.nan
        warn("positive_rate missing and cannot be derived from reviews.")

    # price_range turns raw price into business-friendly pricing tiers.
    df["price_range"] = df["price"].apply(assign_price_range)
    df["price_range"] = pd.Categorical(
        df["price_range"], categories=PRICE_RANGE_ORDER, ordered=True
    )

    # estimated_owners_midpoint uses a prepared median estimate when available;
    # otherwise it parses the midpoint from the owner range text.
    if "median_estimated_owners" in df.columns:
        df["estimated_owners_midpoint"] = pd.to_numeric(
            df["median_estimated_owners"], errors="coerce"
        )
    elif "estimated_owners" in df.columns:
        df["estimated_owners_midpoint"] = df["estimated_owners"].apply(
            parse_owner_midpoint
        )
    else:
        df["estimated_owners_midpoint"] = np.nan
        warn("Owner estimate fields missing; owner midpoint metrics are unavailable.")

    # is_indie flags games with Indie in genres or categories.
    if "genres" in df.columns or "categories" in df.columns:
        genre_indie = (
            df["genres"].apply(lambda value: contains_label(value, "Indie"))
            if "genres" in df.columns
            else False
        )
        category_indie = (
            df["categories"].apply(lambda value: contains_label(value, "Indie"))
            if "categories" in df.columns
            else False
        )
        df["is_indie"] = (genre_indie | category_indie).astype(int)
    else:
        df["is_indie"] = np.nan
        warn("genres/categories missing; is_indie could not be constructed.")

    # primary_genre is the first genre label; analysis_category fills blanks.
    if "genres" in df.columns:
        df["primary_genre"] = df["genres"].apply(first_label)
        if "analysis_category" in df.columns:
            fallback = df["analysis_category"].where(
                df["analysis_category"].astype(str).str.strip().ne("")
            )
            df["primary_genre"] = df["primary_genre"].fillna(fallback)
    elif "analysis_category" in df.columns:
        df["primary_genre"] = df["analysis_category"]
    else:
        df["primary_genre"] = "Unknown"
        warn("genres and analysis_category missing; primary_genre set to Unknown.")

    df["primary_genre"] = (
        df["primary_genre"].fillna("Unknown").astype(str).str.strip()
    )
    df.loc[df["primary_genre"].isin(["", "nan", "None"]), "primary_genre"] = "Unknown"

    return df


def missing_count(series: pd.Series) -> int:
    missing = series.isna()
    if series.dtype == "object":
        missing = missing | series.astype(str).str.strip().isin(["", "nan", "None"])
    return int(missing.sum())


def write_data_overview(df: pd.DataFrame, data_source: str) -> None:
    overview = pd.DataFrame(
        [
            {
                "number_of_games": len(df),
                "number_of_columns": len(df.columns),
                "data_source": data_source,
                "release_year_min": df["release_year"].min(skipna=True),
                "release_year_max": df["release_year"].max(skipna=True),
                "missing_price_count": missing_count(df["price"]),
                "missing_genre_count": (
                    missing_count(df["genres"]) if "genres" in df.columns else len(df)
                ),
            }
        ]
    )
    overview.to_csv(OUTPUT_TABLE_DIR / "data_overview.csv", index=False)


def write_missing_values_summary(df: pd.DataFrame) -> None:
    records = []
    for column in df.columns:
        count = missing_count(df[column])
        records.append(
            {
                "field": column,
                "missing_count": count,
                "missing_rate": count / len(df) if len(df) else np.nan,
            }
        )
    summary = pd.DataFrame(records).sort_values(
        ["missing_count", "field"], ascending=[False, True]
    )
    summary.to_csv(OUTPUT_TABLE_DIR / "missing_values_summary.csv", index=False)


def write_genre_distribution(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("primary_genre", dropna=False)
        .size()
        .reset_index(name="game_count")
        .sort_values("game_count", ascending=False)
    )
    summary["percentage"] = summary["game_count"] / len(df) if len(df) else np.nan
    summary.to_csv(OUTPUT_TABLE_DIR / "genre_distribution.csv", index=False)
    return summary


def write_price_range_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("price_range", observed=False)
        .agg(
            game_count=("name", "count") if "name" in df.columns else ("price", "size"),
            average_price=("price", "mean"),
            median_price=("price", "median"),
            average_positive_review_rate=("positive_review_rate", "mean"),
            median_estimated_owners_midpoint=("estimated_owners_midpoint", "median"),
        )
        .reset_index()
    )
    summary.to_csv(OUTPUT_TABLE_DIR / "price_range_summary.csv", index=False)
    return summary


def write_indie_summary(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["segment"] = np.where(df["is_indie"] == 1, "Indie", "Non-Indie")
    summary = (
        df.groupby("segment")
        .agg(
            game_count=("segment", "size"),
            average_price=("price", "mean"),
            median_price=("price", "median"),
            average_positive_review_rate=("positive_review_rate", "mean"),
            median_estimated_owners_midpoint=("estimated_owners_midpoint", "median"),
        )
        .reset_index()
        .sort_values("segment")
    )
    summary.to_csv(OUTPUT_TABLE_DIR / "indie_vs_non_indie_summary.csv", index=False)
    return summary


def write_genre_review_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("primary_genre", dropna=False)
        .agg(
            game_count=("primary_genre", "size"),
            average_positive_review_rate=("positive_review_rate", "mean"),
            average_price=("price", "mean"),
            median_estimated_owners_midpoint=("estimated_owners_midpoint", "median"),
        )
        .reset_index()
        .sort_values("game_count", ascending=False)
    )
    summary.to_csv(OUTPUT_TABLE_DIR / "genre_review_summary.csv", index=False)
    return summary


def write_genre_competition_hhi(df: pd.DataFrame) -> pd.DataFrame:
    if "developers" in df.columns:
        entity_column = "developers"
    elif "publishers" in df.columns:
        entity_column = "publishers"
    else:
        warn("developers/publishers missing; genre_competition_hhi.csv skipped.")
        return pd.DataFrame()

    competition_df = df[["primary_genre", entity_column]].copy()
    competition_df["entity"] = competition_df[entity_column].apply(first_label)
    competition_df = competition_df.dropna(subset=["entity"])
    competition_df["entity"] = competition_df["entity"].astype(str).str.strip()
    competition_df = competition_df[competition_df["entity"].ne("")]

    records = []
    for genre, group in competition_df.groupby("primary_genre", dropna=False):
        counts = group["entity"].value_counts()
        shares = counts / counts.sum()
        records.append(
            {
                "primary_genre": genre,
                "hhi": float((shares**2).sum()),
                "developer_or_publisher_count": int(counts.size),
                "game_count": int(counts.sum()),
            }
        )

    summary = pd.DataFrame(records).sort_values("hhi", ascending=False)
    summary.to_csv(OUTPUT_TABLE_DIR / "genre_competition_hhi.csv", index=False)
    return summary


def save_figure(filename: str) -> None:
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURE_DIR / filename, dpi=160, bbox_inches="tight")
    plt.close()


def plot_top_genres(genre_distribution: pd.DataFrame) -> None:
    if genre_distribution.empty:
        warn("top_genres_by_game_count.png skipped; no genre distribution data.")
        return

    top_genres = genre_distribution.head(12).sort_values("game_count")
    plt.figure(figsize=(9, 6))
    plt.barh(top_genres["primary_genre"], top_genres["game_count"], color="#4C78A8")
    plt.title("Top Genres by Game Count")
    plt.xlabel("Number of games")
    plt.ylabel("Primary genre")
    save_figure("top_genres_by_game_count.png")


def plot_price_distribution(df: pd.DataFrame) -> None:
    prices = df["price"].dropna()
    prices = prices[prices >= 0]
    if prices.empty:
        warn("price_distribution.png skipped; no valid price data.")
        return

    cap = prices.quantile(0.99)
    plot_prices = prices[prices <= cap]

    plt.figure(figsize=(9, 5))
    plt.hist(plot_prices, bins=30, color="#72B7B2", edgecolor="white")
    plt.title("Price Distribution")
    plt.xlabel("Price")
    plt.ylabel("Number of games")
    save_figure("price_distribution.png")


def plot_average_review_by_price_range(price_summary: pd.DataFrame) -> None:
    summary = price_summary.dropna(subset=["average_positive_review_rate"])
    summary = summary[summary["price_range"].astype(str).ne("Unknown")]
    if summary.empty:
        warn("average_review_by_price_range.png skipped; review data unavailable.")
        return

    plt.figure(figsize=(8, 5))
    plt.bar(
        summary["price_range"].astype(str),
        summary["average_positive_review_rate"],
        color="#F58518",
    )
    plt.title("Average Positive Review Rate by Price Range")
    plt.xlabel("Price range")
    plt.ylabel("Average positive review rate (%)")
    save_figure("average_review_by_price_range.png")


def plot_games_released_by_year(df: pd.DataFrame) -> None:
    years = df["release_year"].dropna().astype(int)
    if years.empty:
        warn("games_released_by_year.png skipped; release_year unavailable.")
        return

    yearly = years.value_counts().sort_index()
    plt.figure(figsize=(10, 5))
    plt.plot(yearly.index, yearly.values, marker="o", color="#54A24B")
    plt.title("Games Released by Year")
    plt.xlabel("Release year")
    plt.ylabel("Number of games")
    plt.grid(axis="y", alpha=0.25)
    save_figure("games_released_by_year.png")


def plot_indie_vs_non_indie(indie_summary: pd.DataFrame) -> None:
    if indie_summary.empty:
        warn("indie_vs_non_indie_comparison.png skipped; no indie summary data.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].bar(indie_summary["segment"], indie_summary["game_count"], color="#4C78A8")
    axes[0].set_title("Game Count")
    axes[0].set_xlabel("Segment")
    axes[0].set_ylabel("Number of games")

    axes[1].bar(
        indie_summary["segment"],
        indie_summary["average_positive_review_rate"],
        color="#E45756",
    )
    axes[1].set_title("Average Positive Review Rate")
    axes[1].set_xlabel("Segment")
    axes[1].set_ylabel("Positive review rate (%)")
    fig.suptitle("Indie vs Non-Indie Comparison")
    save_figure("indie_vs_non_indie_comparison.png")


def plot_genre_competition_hhi(hhi_summary: pd.DataFrame) -> None:
    if hhi_summary.empty:
        warn("genre_competition_hhi.png skipped; no HHI data.")
        return

    top_hhi = hhi_summary.sort_values("game_count", ascending=False).head(12)
    top_hhi = top_hhi.sort_values("hhi")

    plt.figure(figsize=(9, 6))
    plt.barh(top_hhi["primary_genre"], top_hhi["hhi"], color="#B279A2")
    plt.title("Genre Competition Concentration (HHI)")
    plt.xlabel("HHI by developer/publisher game-count share")
    plt.ylabel("Primary genre")
    save_figure("genre_competition_hhi.png")


def plot_review_vs_price_scatter(df: pd.DataFrame) -> None:
    plot_df = df[["price", "positive_review_rate", "total_reviews"]].dropna()
    plot_df = plot_df[(plot_df["price"] >= 0) & (plot_df["total_reviews"] > 0)]
    if plot_df.empty:
        warn("review_vs_price_scatter.png skipped; price/review data unavailable.")
        return

    if len(plot_df) > 10000:
        plot_df = plot_df.sample(10000, random_state=42)

    price_cap = plot_df["price"].quantile(0.99)
    plot_df = plot_df[plot_df["price"] <= price_cap]

    plt.figure(figsize=(9, 5))
    plt.scatter(
        plot_df["price"],
        plot_df["positive_review_rate"],
        s=14,
        alpha=0.35,
        color="#4C78A8",
        edgecolors="none",
    )
    plt.title("Positive Review Rate vs Price")
    plt.xlabel("Price")
    plt.ylabel("Positive review rate (%)")
    plt.grid(alpha=0.2)
    save_figure("review_vs_price_scatter.png")


def write_tables_and_figures(df: pd.DataFrame, data_source: str) -> None:
    ensure_output_dirs()

    write_data_overview(df, data_source)
    write_missing_values_summary(df)
    genre_distribution = write_genre_distribution(df)
    price_summary = write_price_range_summary(df)
    indie_summary = write_indie_summary(df)
    write_genre_review_summary(df)
    hhi_summary = write_genre_competition_hhi(df)

    plot_top_genres(genre_distribution)
    plot_price_distribution(df)
    plot_average_review_by_price_range(price_summary)
    plot_games_released_by_year(df)
    plot_indie_vs_non_indie(indie_summary)
    plot_genre_competition_hhi(hhi_summary)
    plot_review_vs_price_scatter(df)


def main() -> None:
    df, data_source, _ = load_dataset()
    print(f"Raw shape: {df.shape[0]:,} rows x {df.shape[1]:,} columns")

    df = build_indicators(df)
    write_tables_and_figures(df, data_source)

    print(f"Tables saved to: {OUTPUT_TABLE_DIR}")
    print(f"Figures saved to: {OUTPUT_FIGURE_DIR}")
    print(f"Warnings: {len(WARNINGS)}")


if __name__ == "__main__":
    main()
