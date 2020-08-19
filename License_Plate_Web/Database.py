import random
import shutil
import time
import datetime

import mysql.connector


class DataBase:

    def populate_database(self, items_cout=20):
        """
        For testing to fill the database with fake data
        :param items_cout: the number or records to add
        :return:
        """
        self.my_connect()
        mycursir = self.mydb.cursor()

        sql = "INSERT INTO licenses(license_number) VALUES (%s)"
        val = [(str(random.randint(1000000, 9999999)),) for i in range(items_cout)]

        mycursir.executemany(sql, val)

        self.mydb.commit()
        self.my_close()

    def add_number(self, license_number):
        """
        To add a number to the data base
        :param license_number: the number to add
        :return:
        """
        self.my_connect()
        mycursor = self.mydb.cursor()

        if self.search_for_car_number(license_number, mycursor):
            self.my_close()
            return False
        else:
            sql = "INSERT INTO licenses(license_number) VALUES (%s)"
            mycursor.execute(sql, [license_number])

            self.mydb.commit()
            self.my_close()

            return True

    def del_number(self, license_number):
        """
        To delete a number from the database
        :param license_number: the number to delete
        :return:
        """
        self.my_connect()
        mycursor = self.mydb.cursor()

        sql = "Delete From licenses where license_number = %s"
        mycursor.execute(sql, [license_number])

        self.mydb.commit()
        self.my_close()

    def edit_number(self, old_num, new_num):
        """
        to update a value of a number with a new value
        :param old_num: the number you want to update it's value
        :param new_num: the number you want to update the old value with
        :return:
        """
        self.my_connect()
        mycursor = self.mydb.cursor()

        if self.search_for_car_number(new_num, mycursor):
            self.my_close()
            return False
        else:
            sql = "UPDATE licenses SET license_number = %s WHERE license_number = %s"
            mycursor.execute(sql, [new_num, old_num])

            self.mydb.commit()
            self.my_close()

            return True

    def get_license_numbers(self):
        """
        To get all the car numbers from the licenses table in the database
        :return:
        """
        self.my_connect()
        mycursor = self.mydb.cursor()

        sql = "SELECT license_number FROM licenses"
        mycursor.execute(sql)
        values = mycursor.fetchall()

        self.my_close()

        return values

    def get_log(self):
        """
        to get all the records from the log table in the database
        :return:
        """
        self.my_connect()
        mycursor = self.mydb.cursor()

        sql = "SELECT * FROM log ORDER BY timestamp DESC;"
        mycursor.execute(sql)
        values = list(mycursor.fetchall())

        self.my_close()

        return values

    def get_image_index(self):
        """
        used to get the new number for the latest uploaded image to tag it with.
        :return:
        """
        self.my_connect()
        mycursor = self.mydb.cursor()

        sql = "SELECT MAX(image_id) from log;"

        mycursor.execute(sql)
        value = mycursor.fetchall()[0][0]

        self.my_close()

        return value+1 if value else 1;

    def add_log(self, gussed_num, uploaded_num):
        """
        used to add a new record to the log table
        :param gussed_num: the number the algorithm thinks it's on the given license plate
        :param uploaded_num: the number the user uploaded to be checked
        :return:
        """
        index = self.get_image_index()
        print(index)
        shutil.copy("file.png","mysite/static/img/"+str(index)+".png")
        shutil.copy("Cropped-Images-Text.png","mysite/static/img/"+str(index)+"C.png")

        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        self.my_connect()
        mycursor = self.mydb.cursor()

        sql = "INSERT INTO log(gussed_number, uploaded_number, timestamp) values(%s, %s, %s);"
        values = [gussed_num, uploaded_num, timestamp];

        mycursor.execute(sql, values)
        self.mydb.commit()
        self.my_close()


    def search_for_car_number(self, car_number: str, mycur=None):
        """
        used to search the licenses table for a record via a given car number
        :param car_number: the car number you want to check
        :param mycur: (optional)
        :return:
        """
        value = None
        if mycur is None:
            self.my_connect()
            mycursor = self.mydb.cursor()
        else:
            mycursor = mycur

        try:
            sql = f"SELECT license_number FROM licenses WHERE license_number={car_number}"
            mycursor.execute(sql)
            value = mycursor.fetchall()[0][0]

        except:
            pass

        finally:
            if mycur is None:
                self.my_close()

        return value is not None

    def my_close(self):
        """
        to close database connection
        :return:
        """
        self.mydb.close()

    def my_connect(self):
        """
        to connect to database on the cloud
        :return:
        """
        self.mydb = mysql.connector.connect(
            database='husseinAlshaikha$license_plates',
            host='husseinAlshaikhaaaaaa.mysql.pythonanywhere-services.com',
            user='husseinAlshaikha',
            password='KFpExZ53fuY@anM',
            use_pure= True,
        )

