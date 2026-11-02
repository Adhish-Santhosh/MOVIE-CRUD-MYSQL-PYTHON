
from mysql import connector


# DATABASE CONNECTION

class DbConnect:

    def get_connection(self):

        try:
            self.connection = connector.connect(
                host="localhost",
                user="root",
                password="Adhish@123",
                database="movie_db"
            )

            return self.connection

        except Exception as e:
            print(e)
            return None


# MOVIE MANAGEMENT

class MovieManager(DbConnect):

    # DISPLAY ALL MOVIES

    def get(self):

        try:
            self.connect = super().get_connection()

            if not self.connect:
                return

            self.cursor = self.connect.cursor()

            query = "SELECT * FROM movie"

            self.cursor.execute(query)

            records = self.cursor.fetchall()

            for rec in records:
                print(rec)

        except Exception as e:
            print(e)

        finally:
            if self.connect and self.connect.is_connected():
                self.cursor.close()
                self.connect.close()


    # ADD NEW MOVIE

    def post(self, **kwargs):

        try:
            self.connect = super().get_connection()

            if not self.connect:
                return

            self.cursor = self.connect.cursor()

            query = """
            INSERT INTO movie
            (name,director,language,genre,rating,release_year)
            VALUES(%s,%s,%s,%s,%s,%s)
            """

            values = [
                kwargs["name"],
                kwargs["director"],
                kwargs["language"],
                kwargs["genre"],
                kwargs["rating"],
                kwargs["release_year"]
            ]

            self.cursor.execute(query, values)

            self.connect.commit()

            print("New Movie Added Successfully!")

        except Exception as e:
            print(e)

        finally:
            if self.connect and self.connect.is_connected():
                self.cursor.close()
                self.connect.close()


    # GET MOVIE OBJECT

    def get_object(self, id=None):

        try:
            self.connect = super().get_connection()

            if not self.connect:
                return None

            self.cursor = self.connect.cursor()

            query = "SELECT * FROM movie WHERE id=%s"

            values = (id,)

            self.cursor.execute(query, values)

            record = self.cursor.fetchone()

            return record

        except Exception as e:
            print(e)
            return None

        finally:
            if self.connect and self.connect.is_connected():
                self.cursor.close()
                self.connect.close()


    # RETRIEVE PARTICULAR MOVIE

    def retrieve(self, id=None):

        try:
            record = self.get_object(id=id)

            if record is None:
                print("Movie Not Found!")
            else:
                print(record)

        except Exception as e:
            print(e)


    # DELETE MOVIE

    def delete(self, id=None):

        try:
            record = self.get_object(id=id)

            if record is not None:

                self.connect = super().get_connection()

                if not self.connect:
                    return

                self.cursor = self.connect.cursor()

                query = "DELETE FROM movie WHERE id=%s"

                values = (id,)

                self.cursor.execute(query, values)

                self.connect.commit()

                print("Movie Deleted Successfully!")

            else:
                print("Movie Not Found!")

        except Exception as e:
            print(e)

        finally:
            if hasattr(self, "connect") and self.connect and self.connect.is_connected():
                self.cursor.close()
                self.connect.close()


    # UPDATE MOVIE

    def put(self, id=None, **kwargs):

        try:

            allowed_fields = {
                "name",
                "director",
                "language",
                "genre",
                "rating",
                "release_year"
            }

            if not kwargs or not set(kwargs).issubset(allowed_fields):
                print("Invalid update fields!")
                return

            record = self.get_object(id=id)

            if record is not None:

                self.connect = super().get_connection()

                if not self.connect:
                    return

                self.cursor = self.connect.cursor()

                placeholder = ""

                for k in kwargs.keys():
                    placeholder += k + "=%s,"

                placeholder = placeholder.rstrip(",")

                query = f"UPDATE movie SET {placeholder} WHERE id=%s"

                values = list(kwargs.values())

                values.append(id)

                self.cursor.execute(query, values)

                self.connect.commit()

                print("Movie Updated Successfully!")

            else:
                print("Movie Not Found!")

        except Exception as e:
            print(e)

        finally:
            if hasattr(self, "connect") and self.connect and self.connect.is_connected():
                self.cursor.close()
                self.connect.close()


# OBJECT CREATION

movie_instance = MovieManager()


# ADD MOVIES

# movie_instance.post(
#     name="Interstellar",
#     director="Christopher Nolan",
#     language="English",
#     genre="Sci-Fi",
#     rating=8.7,
#     release_year=2014
# )
#
# movie_instance.post(
#     name="Inception",
#     director="Christopher Nolan",
#     language="English",
#     genre="Thriller",
#     rating=8.8,
#     release_year=2010
# )
#
# movie_instance.post(
#     name="Drishyam",
#     director="Jeethu Joseph",
#     language="Malayalam",
#     genre="Thriller",
#     rating=8.5,
#     release_year=2013
# )


# DISPLAY ALL MOVIES

movie_instance.get()

print("--------------------------------")


# RETRIEVE MOVIE

movie_instance.retrieve(1)

print("--------------------------------")


# DELETE MOVIE

# movie_instance.delete(1)

# print("After Deletion")

# movie_instance.get()


# UPDATE MOVIE

# movie_instance.put(2, rating=9.0)

# movie_instance.retrieve(2)
