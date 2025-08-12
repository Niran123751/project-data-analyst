import duckdb
import pandas as pd
import io, base64
import matplotlib.pyplot as plt

def analyze_court_data(question, attachments):
    # Connect DuckDB in-memory
    con = duckdb.connect()

    # Install extensions
    con.execute("INSTALL httpfs; LOAD httpfs;")
    con.execute("INSTALL parquet; LOAD parquet;")

    # Path to S3 parquet files
    base_path = "s3://indian-high-court-judgments/metadata/parquet/year=*/court=*/bench=*/metadata.parquet?s3_region=ap-south-1"

    # 1. Most disposals 2019–2022
    df = con.execute(f"""
        SELECT court, COUNT(*) as count
        FROM read_parquet('{base_path}')
        WHERE year BETWEEN 2019 AND 2022
        GROUP BY court
        ORDER BY count DESC
        LIMIT 1
    """).df()
    most_disposals = df.iloc[0]["court"]

    # 2. Regression slope for delay in court=33_10
    df_delay = con.execute(f"""
        SELECT year, date_of_registration, decision_date
        FROM read_parquet('{base_path}')
        WHERE court='33_10'
    """).df()

    df_delay["date_of_registration"] = pd.to_datetime(df_delay["date_of_registration"], errors="coerce")
    df_delay["decision_date"] = pd.to_datetime(df_delay["decision_date"], errors="coerce")
    df_delay["delay_days"] = (df_delay["decision_date"] - df_delay["date_of_registration"]).dt.days

    # Regression slope per year
    slope = df_delay.groupby("year").apply(
        lambda g: pd.Series({"slope": g["delay_days"].mean()})
    ).mean()["slope"]

    # 3. Scatterplot of year vs delay_days
    plt.scatter(df_delay["year"], df_delay["delay_days"], alpha=0.5)
    plt.plot(df_delay["year"], [slope]*len(df_delay), 'r--')
    plt.xlabel("Year")
    plt.ylabel("Delay (days)")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plot_b64 = "data:image/png;base64," + base64.b64encode(buf.read()).decode()

    return {
        "Which high court disposed the most cases from 2019 - 2022?": most_disposals,
        "What's the regression slope of the date_of_registration - decision_date by year in the court=33_10?": slope,
        "Plot the year and # of days of delay from the above question as a scatterplot with a regression line. Encode as a base64 data URI under 100,000 characters": plot_b64
    }
