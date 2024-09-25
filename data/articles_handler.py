import pandas as pd
from loader import BOT_DIR

articles_table_path = f"{BOT_DIR}/data/articles.xlsx"


def get_all_articles():
    df = pd.read_excel(articles_table_path, sheet_name="Лист1")
    articles = df["Артикулы"].tolist()
    return articles

def append_new_articles(new_articles):
    df = pd.read_excel(articles_table_path, sheet_name="Лист1")
    for new_article in new_articles:
        data = {"Артикулы" : new_article}
        df.loc[len(df)] = data
    df.to_excel(articles_table_path, sheet_name="Лист1", index=False)
    
def save_articles(all_articles):
    data = pd.Series(all_articles)
    df = pd.read_excel(articles_table_path, sheet_name="Лист1")
    df["Артикулы"] = data
    df.to_excel(articles_table_path, sheet_name="Лист1", index=False)
    
