from tqdm import tqdm
import pandas as pd

from config import PURCHASES_CSV_PATH


def insert_denorm_data_from_temp_table(target_model, value_list, database):
    with database as db:
        sql = f"""INSERT INTO {target_model._meta.table_name}({', '.join(target_model.fields_to_copy())})
                  VALUES {', '.join(map(str, value_list))}
                  ON CONFLICT DO NOTHING"""
        db.execute_sql(sql, commit=True)


def insert_denorm(models, database):
    for df in tqdm(pd.read_csv(PURCHASES_CSV_PATH, chunksize=100000)):
        for model in models:
            df_model_fields = df[model.get_fields()]
            tuples = [tuple(x) for x in df_model_fields.to_numpy()]
            insert_denorm_data_from_temp_table(model, tuples, database)


if __name__ == '__main__':
    from models import db, TransactionProduct, Transaction
    from peewee_migrate import Router

    router = Router(db)
    router.run('fill_initial_models')
    insert_denorm([Transaction, TransactionProduct], db)
