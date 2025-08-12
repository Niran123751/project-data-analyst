import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import io, base64

def scrape_wikipedia(question):
    url = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"
    html = requests.get(url).text
    dfs = pd.read_html(html)

    df = dfs[0]  # Main table
    df["Worldwide gross"] = df["Worldwide gross"].replace('[\$,]', '', regex=True).astype(float)
    
    # Example answers
    ans1 = df[(df["Worldwide gross"] >= 2_000_000_000) & (df["Year"] < 2000)].shape[0]
    ans2 = df[df["Worldwide gross"] > 1_500_000_000].sort_values("Year").iloc[0]["Title"]

    corr = df["Rank"].corr(df["Peak"])

    # Scatter plot
    plt.scatter(df["Rank"], df["Peak"])
    m, b = pd.Series(df["Peak"]).corr(df["Rank"]), 0
    plt.plot(df["Rank"], m*df["Rank"] + b, 'r--')
    plt.xlabel("Rank")
    plt.ylabel("Peak")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plot_b64 = "data:image/png;base64," + base64.b64encode(buf.read()).decode()

    return [ans1, ans2, round(corr, 6), plot_b64]
