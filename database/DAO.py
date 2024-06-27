from database.DB_connect import DBConnect
from model.product import Product


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def getColori():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct Product_color as c
                    from go_sales.go_products gp 
                    order by Product_color """

        cursor.execute(query, ())

        for row in cursor:
            result.append(row["c"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getProdotti(c):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct gp.Product_number number , gp.Product name
                    from go_sales.go_products gp 
                    where gp.Product_color = %s """

        cursor.execute(query, (c,))

        for row in cursor:
            result.append(Product(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(colore, anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select  g1.Product_number as p1, g2.Product_number as p2, count(distinct g2.`Date`) as count
                    from go_sales.go_daily_sales g1 , go_sales.go_daily_sales g2, go_sales.go_products gp , go_sales.go_products gp2
                    where g1.Product_number < g2.Product_number 
                    and g2.Retailer_code = g1.Retailer_code
                    and g2.`Date` = g1.`Date`
                    and year(g2.`Date`) = %s
                    and g1.Product_number = gp.Product_number
                    and gp.Product_color = %s
                    and g2.Product_number = gp2.Product_number
                    and gp2.Product_color = %s
                    group by  g1.Product_number, g2.Product_number """

        cursor.execute(query, (anno, colore, colore))

        for row in cursor:
            result.append([row["p1"], row["p2"], row["count"]])

        cursor.close()
        conn.close()
        return result

