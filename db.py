"""
A module which has the implementation of executing the SQL queries on database
"""
import pymysql
from error_codes import ERROR_CONFIG
from config import DATA_BASE


class DBConnection:
    """
    DBConnection
    """

    def __init__(self):
        self._conn = None

    @property
    def conn(self):
        """
        Make Database connection
        """
        return self._conn or self._initiate_db_connection()

    @staticmethod
    def custom_error_response(sql_err):
        """
        Getting a custom sql error message from
        modules.config.mysql_error.ERROR_CONFIG and provide to request
        response

        :param str sql_err: Custom sql error msg for request response
        """
        custom_err = ERROR_CONFIG.get(sql_err[0]) \
            if ERROR_CONFIG.get(sql_err[0]) else ERROR_CONFIG.get(
                'generic')
        client_error_code = custom_err.get('status_code')

        raise Exception(custom_err, client_error_code)

    def _initiate_db_connection(self):
        """
        Create a new connection on Database
        """
        try:
            self._conn = pymysql.connect(
                DATA_BASE['host'],
                user=DATA_BASE['user'],
                passwd=DATA_BASE['password'],
                db=DATA_BASE['db_name'],
                connect_timeout=15, port=DATA_BASE['port'])
        except pymysql.Error as err:
            self.custom_error_response(err.args)
        return self._conn

    def close_connection(self):
        """
        Closing a database connection
        """
        self.conn.close()

    def commit_and_close(self):
        """
        Commit the connection and close
        """
        if self.conn and not self.conn._closed:
            self.conn.commit()
            self.close_connection()

    def rollback_and_close(self):
        """
        Rolling back the connection and close
        """
        if self.conn and not self.conn._closed:
            self.conn.rollback()
            self.close_connection()

    def execute_conditional_format_query(self, query, values):
        """
        Executing insert/update query on the database table.

        :param str query: Insert or update query to be executed on the
          data table.
        :param tupe values: Collection of values to be replaced with %s
          place holder
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, values)
                cur.close()
        except pymysql.Error as err:
            self.custom_error_response(err.args)

    def run_query(self, query, req_data=False):
        """
        Execute a query on the database
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(query)
                cur.close()
                if req_data:
                    # Extract row headers
                    row_headers = [row[0] for row in cur.description]
                    row_values = cur.fetchall()
                    json_data = []
                    for value in row_values:
                        json_data.append(dict(zip(row_headers, value)))
                    return json_data
        except pymysql.Error as err:
            self.custom_error_response(err.args)

    def insert_many(self, insert_query, records_to_insert):
        """
        This function insert many rows to the table
        """
        try:
            with self.conn.cursor() as cur:
                cur.executemany(insert_query, records_to_insert)
                cur.close()
        except pymysql.Error as err:
            self.custom_error_response(err.args)

    def execute_procedure(self, procedure_name, params=[]):
        """This function executes mysql procedures."""
        try:
            with self.conn.cursor() as cur:
                cur.callproc(procedure_name, params)
                cur.close()
        except pymysql.Error as err:
            self.custom_error_response(err.args)
