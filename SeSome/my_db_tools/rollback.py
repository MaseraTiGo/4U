# -*- coding: utf-8 -*-
# @File    : rollback
# @Project : 4U
# @Time    : 2024/9/3 10:34
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
from pprint import pprint

import mysql.connector
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.event import *
from pymysqlreplication.row_event import *


def get_table_primary_key(connection, table_name):
    cursor = connection.cursor()
    query = f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table_name}'
        AND COLUMN_KEY = 'PRI'
        AND TABLE_SCHEMA = DATABASE();
    """
    cursor.execute(query)
    primary_keys = [row[0] for row in cursor.fetchall()]
    return primary_keys[0]


def get_table_columns(connection, table_name):
    cursor = connection.cursor()
    query = f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table_name}'
        AND TABLE_SCHEMA = DATABASE();
    """
    cursor.execute(query)
    columns = [row[0] for row in cursor.fetchall()]
    return columns


def connect_to_mysql():
    connection = mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        database=database
    )
    return connection


def get_binlog_stream(connection_settings):
    stream = BinLogStreamReader(
        connection_settings=connection_settings,
        server_id=100,  # Unique server ID for the connection
        log_file=log_file,
        log_pos=start_position,
        end_log_pos=stop_position,
        only_events=[WriteRowsEvent, UpdateRowsEvent, DeleteRowsEvent],
        resume_stream=True
    )
    return stream


def generate_rollback_sql(binlog_stream, table):
    rollback_statements = []
    columns = get_table_columns(connect_to_mysql(), table)
    primary_key = get_table_primary_key(connect_to_mysql(), table)
    for binlog_event in binlog_stream:
        if binlog_event.table != table:
            continue
        if isinstance(binlog_event, WriteRowsEvent):
            for row in binlog_event.rows:
                sql = generate_delete_statement(binlog_event, row, columns, primary_key)
                rollback_statements.append(sql)
        elif isinstance(binlog_event, UpdateRowsEvent):
            for row in binlog_event.rows:
                sql = generate_update_statement(binlog_event, row, columns, primary_key)
                rollback_statements.append(sql)
        elif isinstance(binlog_event, DeleteRowsEvent):
            for row in binlog_event.rows:
                sql = generate_insert_statement(binlog_event, row, columns, primary_key)
                rollback_statements.append(sql)

    rollback_statements.reverse()  # Reverse the order of statements for correct rollback

    pprint(rollback_statements)
    return rollback_statements


def _get_new_row(old_row, columns):
    new_row = {}
    i = 0
    for _, value in old_row.items():
        if value is None:
            value = ""
        new_row[columns[i]] = value
        i += 1
    return new_row


def generate_delete_statement(event, row, columns, primary_key):
    table = event.table
    where_clause = " AND ".join(
        f"`{k}`='{v}'" for k, v in _get_new_row(row['values'], columns).items())
    return f"DELETE FROM `{table}` WHERE {where_clause};"


def generate_update_statement(event, row, columns, primary_key):
    table = event.table

    old_row = _get_new_row(row['before_values'], columns)
    new_row = _get_new_row(row['after_values'], columns)

    alter_cols = []
    for k, v in old_row.items():
        if v != new_row[k]:
            alter_cols.append(k)

    set_clause = ", ".join(
        f"`{col}`='{old_row[col]}'" for col in alter_cols)
    if old_row[primary_key] != new_row[primary_key]:
        where_clause = " AND ".join(
            f"`{k}`='{v}'" for k, v in _get_new_row(row['after_values'], columns).items())
    else:
        where_clause = "`{}`='{}'".format(primary_key, old_row[primary_key])
    return f"UPDATE `{table}` SET {set_clause} WHERE {where_clause};"


def generate_insert_statement(event, row, columns, primary_key):
    table = event.table
    # columns = ", ".join(f"`{k}`" for k in row["values"].keys())
    values = ", ".join(f"'{v}'" for v in row["values"].values())
    return f"INSERT INTO `{table}` ({columns}) VALUES ({values});"


def execute_rollback(connection, rollback_statements):
    cursor = connection.cursor()
    for statement in rollback_statements:
        print(statement)
        cursor.execute(statement)
    connection.commit()


def rollback_database():

    connection_settings = {
        "host": host,
        "user": user,
        "passwd": password
    }

    binlog_stream = get_binlog_stream(connection_settings)
    rollback_statements = generate_rollback_sql(binlog_stream, table_to_rollback)
    connection = connect_to_mysql()
    execute_rollback(connection, rollback_statements)
    print("Rollback completed.")


if __name__ == "__main__":
    user = "root"
    password = "123918"
    host = "localhost"
    database = "data_leak"
    log_file = "binlog.000264"
    start_position = 5350886
    stop_position = 5352888
    table_to_rollback = 'b_user'
    rollback_database()
