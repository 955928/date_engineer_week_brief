import pandas as pd
import sqlite3

connection = sqlite3.connect("olist.db")

df_reviews = pd.read_sql_query("SELECT * FROM Reviews",connection)


# Gestion valeurs manquantes
df_reviews = df_reviews.drop(["timestamp_field_7"],axis=1)

if df_reviews.shape[1]!= 7:
    raise ValueError("Le nombre de colonnes ne correspond pas")
else:
    print("Valeurs manquantes: OK")

# Gestion des doublons
df_reviews = df_reviews.drop_duplicates(['order_id','review_score','review_comment_title','review_comment_message','review_creation_date'])

if df_reviews.shape[0]!= 98371:
    raise ValueError("Le nombre de lignes ne correspond pas")
else:
    print("Dédoublonnage: OK")

# Changement des types
df_reviews.review_creation_date = pd.to_datetime(df_reviews['review_creation_date'], format= '%Y-%m-%d %H:%M:%S', errors="coerce")
df_reviews.review_answer_timestamp = pd.to_datetime(df_reviews['review_answer_timestamp'], format= '%Y-%m-%d %H:%M:%S', errors="coerce")

from numpy import dtype


if df_reviews.dtypes['review_creation_date'] != dtype('<M8[ns]') or df_reviews.dtypes['review_answer_timestamp'] != dtype('<M8[ns]'):
    raise ValueError("Les dates ne sont pas au bon format")
else:
    print("Gestion des dates: OK")

#Changement des valeurs types pour les dates
df_reviews = df_reviews.dropna(subset=['review_creation_date','review_answer_timestamp'])

if df_reviews.shape[0]!= 98344:    
    raise ValueError("Le nombre de lignes ne correspond pas")
else:
    print("Gestion des dates (valeurs manquantes): OK")


# Jointure avec la Table Orders
df_orders = pd.read_sql_query("SELECT * FROM Orders",connection)
df = df_reviews.merge(df_orders, how='left', on ='order_id')

if df.shape[0]!= 98344:    
    raise ValueError("Le nombre de lignes ne correspond pas")
else:
    print("Jointure avec Orders: OK")


# Gestion des types de data
df.order_purchase_timestamp = pd.to_datetime(df['order_purchase_timestamp'], 
                                            format= '%Y-%m-%d %H:%M:%S', 
                                            errors="coerce")

df.order_delivered_customer_date = pd.to_datetime(df['order_delivered_customer_date'], 
                                                  format= '%Y-%m-%d %H:%M:%S', 
                                                  errors="coerce")

df.order_estimated_delivery_date = pd.to_datetime(df['order_estimated_delivery_date'], 
                                                  format= '%Y-%m-%d %H:%M:%S', 
                                                  errors="coerce")


if df.dtypes['order_estimated_delivery_date'] != dtype('<M8[ns]') \
    or df.dtypes['order_delivered_customer_date'] != dtype('<M8[ns]')\
    or df.dtypes['order_estimated_delivery_date'] != dtype('<M8[ns]')    :
    raise ValueError("Les dates ne sont pas au bon format")
else:
    print("Gestion des dates (Orders): OK")

#Création de la table CleanDataset

df.to_sql('CleanDataset', connection, index=False, if_exists='replace')

print("Table CleanDataset mise à jour")

connection.close()