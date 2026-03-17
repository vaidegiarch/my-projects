

import streamlit as st
import pandas as pd
import sqlite3
from streamlit_option_menu import option_menu

# DB connection
conn = sqlite3.connect("merged_data.db")

# Page config
st.set_page_config(layout='wide')

# Menu
selected = option_menu(
    menu_title=None,
    options=["Home", "Data Exploration", "SQL Query Runner", "Top 5 Crypto Analysis"],
    orientation="horizontal"
)

# Home Page
if selected == "Home":
    st.title("Cross-Market Analysis: Crypto, Oil & Stocks with python & SQL ")
import streamlit as st
import pandas as pd
import sqlite3
from streamlit_option_menu import option_menu

# MENU
selected = option_menu(
    menu_title=None,
    options=["Home", "Data Exploration", "SQL Query Runner", "Top 5 Crypto Analysis"],
    orientation="horizontal"
)

if selected == "Home":
    st.title("Cross Market Analysis")

elif selected == "Data Exploration":
    st.title("Cross Market Overview")

    # DB connection
    conn = sqlite3.connect("merged_data.db")

    # Load data
    df = pd.read_sql_query("SELECT * FROM merged_data", conn)

    # Convert date
    df['date'] = pd.to_datetime(df['date'])

    # DATE FILTER
    start_date = st.date_input("Start Date", df['date'].min(), key="start")
    end_date = st.date_input("End Date", df['date'].max(), key="end")

    # Filter data
    filtered_df = df[
        (df['date'] >= pd.to_datetime(start_date)) &
        (df['date'] <= pd.to_datetime(end_date))
    ]

    # SELECT BOX
    option = st.selectbox(
        "Select Analysis",
        [
            "Bitcoin Avg Price",
            "Oil Avg Price",
            "S&P 500 Avg",
            "NIFTY Avg"
        ],
        key="analysis"
    )

    # CALCULATIONS
    if option == "Bitcoin Avg Price":
        result = filtered_df[filtered_df['coin_id'] == 'bitcoin']['price_inr'].mean()
        st.metric("Bitcoin Average Price", round(result, 2))

    elif option == "Oil Avg Price":
        result = filtered_df['Price'].mean()
        st.metric("Oil Average Price", round(result, 2))

    elif option == "S&P 500 Avg":
        result = filtered_df['GSPC_Close'].mean()
        st.metric("S&P 500 Avg Close", round(result, 2))

    elif option == "NIFTY Avg":
        result = filtered_df['NSEI_Close'].mean()
        st.metric("NIFTY Avg Close", round(result, 2))

    # SHOW DATA
    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

# MENU
selected = option_menu(
    menu_title=None,
    options=["Home", "Data Exploration", "SQL Query Runner", "Top 5 Crypto Analysis"],
    orientation="horizontal"
)




if selected == "Home":
    st.title("Cross Market Analysis")

elif selected == "Data Exploration":
    st.title("Cross Market Overview")



elif selected == "SQL Query Runner":
    st.title("SQL Query Runner")

    conn = sqlite3.connect("Cryptocurrencies.db")



    queries = {

    # ------------------ CRYPTOCURRENCIES ------------------
    "Top 3 Cryptos by Market Cap": {
        "query": """SELECT * FROM Cryptocurrencies
                    ORDER BY market_cap_rank ASC
                    LIMIT 3""",
        "db": "Cryptocurrencies.db"
    },

    "Circulating Supply > 90%": {
        "query": """SELECT id,symbol,name,circulating_supply,total_supply
                    FROM Cryptocurrencies
                    WHERE circulating_supply > 0.9 * total_supply""",
        "db": "Cryptocurrencies.db"
    },

    "Coins Near ATH": {
        "query": """SELECT name,symbol,current_price,ath
                    FROM Cryptocurrencies
                    WHERE current_price >= 0.9 * ath""",
        "db": "Cryptocurrencies.db"
    },

    "Avg Market Rank (>1B Volume)": {
        "query": """SELECT AVG(market_cap_rank)
                    FROM Cryptocurrencies
                    WHERE total_volume > 1000000000""",
        "db": "Cryptocurrencies.db"
    },

    "Most Recent Coin": {
        "query": """SELECT name,symbol,date
                    FROM Cryptocurrencies
                    ORDER BY date DESC
                    LIMIT 1""",
        "db": "Cryptocurrencies.db"
    },

    # ------------------ CRYPTO PRICES ------------------
    "Bitcoin Max Price": {
        "query": """SELECT coin_id,date,MAX(price_inr)
                    FROM Crypto_prices
                    WHERE coin_id='bitcoin'""",
        "db": "Crypto_prices.db"
    },

    "Bitcoin Feb 2025 Prices": {
        "query": """SELECT coin_id,date,price_inr
                    FROM Crypto_prices
                    WHERE coin_id='bitcoin'
                    AND date BETWEEN '2025-02-01' AND '2025-02-28'""",
        "db": "Crypto_prices.db"
    },

    "Highest Avg Price Coin": {
        "query": """SELECT coin_id,AVG(price_inr)
                    FROM Crypto_prices
                    GROUP BY coin_id
                    ORDER BY AVG(price_inr) DESC
                    LIMIT 1""",
        "db": "Crypto_prices.db"
    },

    "Bitcoin Avg Feb 2025": {
        "query": """SELECT AVG(price_inr)
                    FROM Crypto_prices
                    WHERE coin_id='bitcoin'
                    AND date LIKE '2025-02-%'""",
        "db": "Crypto_prices.db"
    },

    "Bitcoin Avg Feb 2026": {
        "query": """SELECT AVG(price_inr)
                    FROM Crypto_prices
                    WHERE coin_id='bitcoin'
                    AND date LIKE '2026-02-%'""",
        "db": "Crypto_prices.db"
    },

    # ------------------ OIL ------------------
    "Highest Oil Price (5Y)": {
        "query": """SELECT date,price_inr
                    FROM Oil_prices
                    WHERE date >= date('now','-5 years')
                    ORDER BY price_inr DESC
                    LIMIT 1""",
        "db": "Oil_prices.db"
    },

    "Oil Avg Per Year": {
        "query": """SELECT substr(date,1,4) AS year,AVG(price_inr)
                    FROM Oil_prices
                    GROUP BY year""",
        "db": "Oil_prices.db"
    },

    "Oil COVID Crash": {
        "query": """SELECT date,price_inr
                    FROM Oil_prices
                    WHERE date BETWEEN '2020-03-01' AND '2020-04-30'""",
        "db": "Oil_prices.db"
    },

    "Lowest Oil (10Y)": {
        "query": """SELECT MIN(price_inr)
                    FROM Oil_prices
                    WHERE date >= date('now','-10 years')""",
        "db": "Oil_prices.db"
    },

    "Oil Volatility": {
        "query": """SELECT strftime('%Y',date) AS year,
                           MAX(price_inr)-MIN(price_inr) AS volatility
                    FROM Oil_prices
                    GROUP BY year""",
        "db": "Oil_prices.db"
    },

    # ------------------ STOCKS ------------------
    "NSEI Stock Data": {
        "query": """SELECT date,open,high,low,close,volume
                    FROM stocks
                    WHERE ticker='^NSEI'""",
        "db": "stocks.db"
    },

    "NASDAQ Highest Close": {
        "query": """SELECT date,ticker,close
                    FROM stocks
                    WHERE ticker='^IXIC'
                    ORDER BY close DESC
                    LIMIT 1""",
        "db": "stocks.db"
    },

    "S&P500 Volatility Days": {
        "query": """SELECT date,high,low,(high-low) AS diff
                    FROM stocks
                    WHERE ticker='^GSPC'
                    ORDER BY diff DESC
                    LIMIT 5""",
        "db": "stocks.db"
    },

    "Monthly Avg Stocks": {
        "query": """SELECT ticker,strftime('%Y-%m',date) AS month,
                           AVG(close)
                    FROM stocks
                    GROUP BY ticker,month""",
        "db": "stocks.db"
    },

    "NSEI Volume 2024": {
        "query": """SELECT AVG(volume)
                    FROM stocks
                    WHERE ticker='^NSEI'
                    AND date BETWEEN '2024-01-01' AND '2024-12-31'""",
        "db": "stocks.db"
    },

    # ------------------ MERGED DATA ------------------
    "Bitcoin vs Oil 2026": {
        "query": """SELECT 'Bitcoin' AS asset,AVG(price_inr)
                    FROM merged_data
                    WHERE coin_id='bitcoin'
                    UNION ALL
                    SELECT 'Oil',AVG(price)
                    FROM merged_data""",
        "db": "merged_data.db"
    },

    "Bitcoin vs S&P500": {
        "query": """SELECT date,price_inr,GSPC_Close
                    FROM merged_data
                    WHERE coin_id='bitcoin'""",
        "db": "merged_data.db"
    },

    "Ethereum vs NASDAQ": {
        "query": """SELECT date,price_inr,IXIC_Close
                    FROM merged_data
                    WHERE coin_id='ethereum'""",
        "db": "merged_data.db"
    },

    "Bitcoin Oil Correlation Data": {
        "query": """SELECT date,price_inr AS bitcoin_price,Price AS oil_price
                    FROM merged_data
                    WHERE coin_id='bitcoin'""",
        "db": "merged_data.db"
    },

    "Top 3 Coins vs Market": {
        "query": """SELECT date,coin_id,price_inr,GSPC_Close,IXIC_Close
                    FROM merged_data
                    WHERE coin_id IN ('bitcoin','ethereum','tether')
                    LIMIT 10""",
        "db": "merged_data.db"
    },

    "Stock vs Oil": {
        "query": """SELECT date,GSPC_Close,Price
                    FROM merged_data
                    LIMIT 10""",
        "db": "merged_data.db"
    },

    "Bitcoin Full Market View": {
        "query": """SELECT date,price_inr,GSPC_Close,IXIC_Close,Price
                    FROM merged_data
                    WHERE coin_id='bitcoin'
                    LIMIT 10""",
        "db": "merged_data.db"
    }
}

    #  ALL QUERIES
    selected_query = st.selectbox("Select SQL Query", list(queries.keys()))

    st.code(queries[selected_query]["query"], language="sql")

    if st.button("Run Query"):
      query = queries[selected_query]["query"]
      db = queries[selected_query]["db"]

      conn = sqlite3.connect(db)

      result = pd.read_sql_query(query, conn)
      st.dataframe(result)

import streamlit as st
import pandas as pd
import sqlite3
from streamlit_option_menu import option_menu

# MENU
selected = option_menu(
    menu_title=None,
    options=["Home", "Data Exploration", "SQL Query Runner", "Top 5 Crypto Analysis"],
    orientation="horizontal"
)

if selected == "Home":
    st.title("Cross Market Analysis")

elif selected == "Data Exploration":
    st.title("Cross Market Overview")

elif selected == "SQL Query Runner":
    st.title("SQL Query Runner")

elif selected == "Top 5 Crypto Analysis":
    st.title("Top 5 Crypto Analysis")

    import sqlite3
    import pandas as pd

    conn = sqlite3.connect("Crypto_prices.db")

    # ---- Get Top 3 coins ----
    top_crypto_query = """
        SELECT DISTINCT coin_id
        FROM Crypto_prices
        LIMIT 3
    """
    top_crypto_df = pd.read_sql_query(top_crypto_query, conn)

    crypto_list = top_crypto_df["coin_id"].tolist()

    # ---- Select Crypto ----
    selected_crypto = st.selectbox("Select Cryptocurrency", crypto_list)

    # ---- Load Data for selected crypto ----
    query = f"""
        SELECT date, price_inr
        FROM Crypto_prices
        WHERE coin_id = '{selected_crypto}'
    """
    df = pd.read_sql_query(query, conn)

    # ---- Convert Date ----
    df["date"] = pd.to_datetime(df["date"])

    # ---- Date Filter ----
    start_date = st.date_input("Start Date", df["date"].min())
    end_date = st.date_input("End Date", df["date"].max())

    filtered_df = df[(df["date"] >= pd.to_datetime(start_date)) &
                     (df["date"] <= pd.to_datetime(end_date))]

    # ---- Line Chart (Optional) ----
    st.subheader("Daily Price Trend")
    st.line_chart(filtered_df.set_index("date")["price_inr"])

    # ---- Table ----
    st.subheader("Daily Price Data")
    st.dataframe(filtered_df)

    conn.close()


!streamlit run /content/project.py &>/content/logs.txt &
!grep -o 'https://.*\.trycloudflare.com' nohup.out | head -n 1 | xargs -I {} echo "Your tunnel url {}"















