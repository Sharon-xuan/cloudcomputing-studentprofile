import pymysql


class ProfileResource:

    def __int__(self):
        pass

    @staticmethod
    def get_connection():
        conn = pymysql.connect(
            # LOCAL
            host="localhost",
            port=3306,
            user="root",
            password="密码",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True

            # AWS
            # host="customerdb.cvjaygaiwg1r.us-east-1.rds.amazonaws.com",
            # port=3306,
            # user="admin",
            # password="dbuserdbuser",
            # cursorclass=pymysql.cursors.DictCursor,
            # autocommit=True
        )

        return conn

    @staticmethod
    def get_profile_by_uni(key):
        sql = "SELECT uni, name, interest, schedule, email FROM student_profile.student_info WHERE uni=%s"
        conn = ProfileResource.get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=key)
        result = cur.fetchone()

        return result

    # @staticmethod
    # def delete_account_by_emailID(key):
    #     sql = "DELETE FROM customerDB.account WHERE emailID=%s"
    #     conn = AccountResource.get_connection()
    #     cur = conn.cursor()
    #     res = cur.execute(sql, args=key)
    #     result = cur.fetchone()
    #
    #     return result
    #
    # @staticmethod
    # def create_account(account):
    #     placeholder = ", ".join(["%s"] * len(account))
    #     sql = "INSERT INTO customerDB.account({columns}) VALUES ({values})".format(columns=",".join(account.keys()),
    #                                                                                values=placeholder)
    #     conn = AccountResource.get_connection()
    #     cur = conn.cursor()
    #     res = cur.execute(sql, list(account.values()))
    #     result = cur.fetchone()
    #
    #     return result
    #
    @staticmethod
    def update_account(new_content):
        sql = "UPDATE student_profile.student_info SET interest=%s, schedule=%s where uni=%s"
        conn = ProfileResource.get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, (new_content[1], new_content[2], new_content[0]))
        result = cur.fetchone()
        return result
