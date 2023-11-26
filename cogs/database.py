from nextcord.ext import commands
import psycopg2
from psycopg2 import sql

class DatabaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_url = self.bot.db_url

    async def cog_load(self):
        self.bot.loop.run_in_executor(None, self.setup_database)

    def setup_database(self):
        conn = psycopg2.connect(self.db_url)
        cur = conn.cursor()

        # Define SQL for table creation
        commands = [
            sql.SQL("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    date_joined DATE NOT NULL,
                    holder_role BIGINT,
                    holder_role_2 BIGINT,
                    holder_role_3 BIGINT,
                    monthly_token_allocation INT,
                    token_balance INT,
                    current_month_usage INT
                )
            """),
            sql.SQL("""
                CREATE TABLE IF NOT EXISTS threads (
                    user_id BIGINT REFERENCES users(user_id),
                    assistant_id TEXT,
                    thread_id TEXT
                )
            """),
            sql.SQL("""
                CREATE TABLE IF NOT EXISTS transactions (
                    user_id BIGINT REFERENCES users(user_id),
                    date DATE,
                    transaction_tx TEXT,
                    number_of_tokens INT
                )
            """)
        ]

        try:
            # Execute each command to ensure all tables are set up
            for command in commands:
                cur.execute(command)
            conn.commit()
        except Exception as e:
            print(f"An error occurred while setting up the database: {e}")
        finally:
            # Close communication with the database
            cur.close()
            conn.close()

def setup(bot):
    bot.add_cog(DatabaseCog(bot))