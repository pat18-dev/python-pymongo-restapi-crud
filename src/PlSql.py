import json
import sys

from psycopg2 import OperationalError, connect, errors
from psycopg2.extensions import SQL_IN


class ErrorPlSql(Exception):
    def __init__(self, message, attr):
        self.message = message
        self.attr = attr

    def __str__(self):
        return self.message


class PlSql:
    def __init__(self, dsn: str, iscommited: bool = True, reference_fileStore=None):
        self.dsn = dsn
        self.iscommited = iscommited
        self.ReferenceFileStore = reference_fileStore
        self.state = "SUCCESS"
        self.error = None
        self.rowcount = 0
        self.description = None
        self.data = None
        # self.test_connection(self.dsn)

    @staticmethod
    def getquoted(lst: list) -> str:
        txt = SQL_IN(lst)
        return txt.getquoted()

    @staticmethod
    def test_connection(dsn: str):
        try:
            print("---INIT TEST SQL")
            print(dsn)
            connect(dsn)
            print("---SQL TEST INSTANCE CREATED")
        except (OperationalError, AttributeError) as conn_err:
            raise ErrorPlSql(str(conn_err), dsn)

    def connect(self):
        try:
            print("---INIT SQL")
            print(self.dsn)
            self.connection = connect(self.dsn)
            print("---SQL INSTANCE CREATED")
        except (OperationalError, AttributeError):
            raise ErrorPlSql("DSN connection NOT VALID", self.dsn)

    def exec(self, query: str):
        self.connect()
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query)
                self.rowcount = cursor.rowcount
                self.description = cursor.description
                if cursor.description is not None:
                    self.data = cursor.fetchall()
                if self.iscommited:
                    self.connection.commit()
                else:
                    self.state = "INFO"
                    self.connection.rollback()
                cursor.close()
            except errors.DatabaseError as pg_err:
                self.state = "ERROR"
                self.connection.rollback()
                self.error = self.get_psycopg2_exception(pg_err)
                raise ErrorPlSql(self.error, query)
            finally:
                if cursor is not None:
                    cursor.close()
                    del cursor
                self.connection.close()
                if self.ReferenceFileStore is not None:
                    self.ReferenceFileStore.publish_msg(
                        json.dumps(
                            {
                                "state": self.state,
                                "iscommited": self.iscommited,
                                "query": query,
                                "data": self.data,
                                "error": self.error,
                            }
                        )
                    )

    def get_psycopg2_exception(self, err):
        # get details about the exception
        err_type, err_obj, traceback = sys.exc_info()

        # get the line number when exception occured
        line_num = traceback.tb_lineno
        # print the connect() error
        error = f"\npsycopg2 ERROR: {err}, on line number: {line_num} \npsycopg2 traceback: {traceback} -- type: {err_type}"

        # psycopg2 extensions.Diagnostics object attribute
        error += f"\nextensions.Diagnostics: {err.diag}"

        # print the pgcode and pgerror exceptions
        error += f"\npgerror:{err.pgerror}\npgcode: {err.pgcode}\n"
        return error
