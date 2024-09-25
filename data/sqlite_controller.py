import sqlite3
import custom_filters.states as states

class SqliteTable():
    def __init__(self, table_path):
        self.con = sqlite3.connect(database=table_path)
        self.cur = self.con.cursor()
        
    #simplified state machine
    def set_user_state(self, user_id, user_name, state):
        if not self.is_user_exist(user_id):
            self.create_new_user(user_id, user_name, state=state)
        else:
            self.cur.execute(f"UPDATE users SET state='{state}' WHERE user_id={user_id}")
            self.con.commit()
        
    def is_user_exist(self, user_id) -> bool:
        res = self.cur.execute(f"SELECT user_id FROM users WHERE user_id={user_id}")
        if res.fetchone():
            return True
        else:
            return False
        
    def get_user_state(self, user_id, user_name) -> str:
        res = self.cur.execute(f"SELECT state FROM users WHERE user_id={user_id}")
        user_state = res.fetchone()
        if not user_state or len(user_state) == 0:
            self.create_new_user(user_id, user_name, state=states.BASE)
            return states.BASE
        return user_state[0]

    def create_new_user(self, user_id, user_name, state):
        self.cur.execute(f"INSERT INTO users (user_id, user_name, state) VALUES ({user_id}, '{user_name}', '{state}')")
        self.con.commit()
        
    def get_all_users(self):
        res = self.cur.execute("SELECT user_id, user_name, state FROM users")
        return res.fetchall()
        
    def get_product_data(self, article) -> dict:
        res = self.cur.execute("SELECT price, spp, spp_price, wallet_price FROM products WHERE article=?", (article,))
        product = res.fetchone()
        if product:
            data = {
                "article" : article,
                "seller" : "",
                "base-price" : product[0],
                "spp" : product[1],
                "spp-price" : product[2],
                "wallet_price" : product[3]
            }
            return data
        else: 
            return None

    def delete_products(self, articles: list):
        articles = [(article,) for article in articles]
        self.cur.executemany(f"DELETE FROM products WHERE article=?", articles)
        self.con.commit()
        
    def add_product(self, product_data: dict):
        article = product_data["article"]
        price = product_data["base-price"]
        spp = product_data["spp"]
        spp_price = product_data["spp-price"]
        wallet_price = product_data["wallet_price"]
        self.cur.execute(
            "INSERT INTO products (article, price, spp, spp_price, wallet_price) VALUES (?, ?, ?, ?, ?)", (article, price, spp, spp_price, wallet_price))
        self.con.commit()
        
    def update_product(self, product_data: dict):
        article = product_data["article"]
        price = product_data["base-price"]
        spp = product_data["spp"]
        spp_price = product_data["spp-price"]
        wallet_price = product_data["wallet_price"]
        self.cur.execute(
            "UPDATE products SET price=?, spp=?, spp_price=?, wallet_price=? WHERE article=?", (price, spp, spp_price, wallet_price, article)
        )
        self.con.commit()