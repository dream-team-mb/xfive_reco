from peewee import *

from config import CLIENTS_CSV_PATH, PRODUCTS_CSV_PATH

db = PostgresqlDatabase('xfive_reco', user='postgres', password='secret', host='localhost', port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = TextField(unique=True, primary_key=True)
    first_issue_date = DateTimeField()
    first_redeem_date = DateTimeField(null=True)
    age = IntegerField()
    gender = CharField(max_length=1, choices=('U', 'F', 'M'))

    class Meta:
        table_name = 'users'
        csv_path = CLIENTS_CSV_PATH

    @classmethod
    def fields_to_copy(cls):
        return [field.name for field in cls._meta.fields.values()]


class Transaction(BaseModel):
    id = TextField(unique=True, primary_key=True, db_column='transaction_id')
    user = ForeignKeyField(User, backref='transactions')
    transaction_datetime = DateTimeField()
    regular_points_received = FloatField()
    express_points_received = FloatField()
    regular_points_spent = FloatField()
    express_points_spent = FloatField()
    purchase_sum = FloatField()
    store_id = TextField()

    class Meta:
        table_name = 'transactions'
        csv_path = CLIENTS_CSV_PATH

    @classmethod
    def fields_to_copy(cls):
        return ['user_id', 'transaction_id', 'transaction_datetime', 'regular_points_received',
                'express_points_received', 'regular_points_spent', 'express_points_spent', 
                'purchase_sum', 'store_id']

    @classmethod
    def get_fields(cls):
        return ['client_id', 'transaction_id', 'transaction_datetime', 'regular_points_received',
                'express_points_received', 'regular_points_spent',
                'express_points_spent', 'purchase_sum', 'store_id']


class Product(BaseModel):
    id = TextField(unique=True, primary_key=True)
    level1 = TextField(null=True)
    level2 = TextField(null=True)
    level3 = TextField(null=True)
    level4 = TextField(null=True)
    segment_id = TextField(null=True)
    brand_id = TextField(null=True)
    vendor_id = TextField(null=True)
    netto = FloatField(null=True)
    is_own_trademark = BooleanField()
    is_alcohol = BooleanField()

    class Meta:
        table_name = 'products'
        csv_path = PRODUCTS_CSV_PATH

    @classmethod
    def fields_to_copy(cls):
        return [field.name for field in cls._meta.fields.values()]


class TransactionProduct(BaseModel):
    id = AutoField()
    transaction_id = ForeignKeyField(Transaction, backref='products_for_transaction')
    product_id = ForeignKeyField(Product, backref='transactionproducts')
    product_quantity = FloatField()
    trn_sum_from_iss = FloatField()

    @classmethod
    def fields_to_copy(cls):
        return tuple(field.column_name for field in cls._meta.fields.values() if field.name != 'id')

    @classmethod
    def get_fields(cls):
        return [field.name for field in cls._meta.fields.values()
                if field.name in ['transaction_id', 'product_id',
                                  'product_quantity', 'trn_sum_from_iss']]

    class Meta:
        table_name = 'transaction_products'
