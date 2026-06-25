from database.DB_connect import DBConnect
from model.pilota import Pilota


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getPiloti(data1, data2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct d.*
                    from drivers d, results r, races g
                    where d.driverId = r.driverId and r.raceId = g.raceId 
                    and g.`date` BETWEEN %s and %s
                    and r.`position` is not NULL """

        cursor.execute(query, (data1, data2, ))

        for row in cursor:
            results.append(Pilota(**row))

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getEdges(data1, data2, mappa):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.driverId as d1, t2.driverId as d2, count(*) as peso
                    from (select r.*
                    from results r, races g
                    where r.raceId = g.raceId 
                    and g.`date` BETWEEN %s and %s
                    and r.`position` is not NULL ) t1,
                    (select r.*
                    from results r, races g
                    where r.raceId = g.raceId 
                    and g.`date` BETWEEN %s and %s
                    and r.`position` is not NULL ) t2
                    where t1.constructorId = t2.constructorId 
                    and t1.raceId = t2.raceId
                    and t1.driverId < t2.driverId 
                    group by t1.driverId, t2.driverId, t1.constructorId, t2.constructorId   """

        cursor.execute(query, (data1, data2, data1, data2, ))

        for row in cursor:
            p1 = mappa[row["d1"]]
            p2 = mappa[row["d2"]]
            results.append((p1, p2, row["peso"]))

        cursor.close()
        conn.close()
        return results


