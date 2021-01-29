# encoding:utf8
import MySQLdb as my
from time import sleep


def generate_data(sql_begin, start_i):
    sql = sql_begin
    for i in range(1000000):
        if i == 999999:
            tmp_sql = "(name = 'ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss" + str(
                i) + "' and name1 = 'ttttttttttttttttttttttttttttttttttttttttt" + str(i) + "' );"
        else:
            tmp_sql = "(name = 'ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss" + str(
                i) + "' and name1 = 'ttttttttttttttttttttttttttttttttttttttttt" + str(i) + "' ) or "
        sql += tmp_sql
    return sql


def main():
    sql_begin = "delete from test1 where "
    i = 0
    sql = generate_data(sql_begin, i)
    myconn = my.connect(host='127.0.0.1', port=3306, db='testdb', user='root', passwd='root', charset='utf8mb4')
    cur_myconn = myconn.cursor()
    for i in range(10000):
        print
        "sql_len: ", len(sql), "execute sql", sql[0:200], "\n"
        try:
            cur_myconn.execute(sql)
            myconn.commit()
        except Exception, e:
            print
            e
        print
        "sql executed, but does't close the connection \n"
        sleep(100);
    cur_myconn.close()
    myconn.close()


if __name__ == '__main__':
    main()
