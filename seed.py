"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User, Rating, Movie, connect_to_db, db 
import datetime

from server import app


def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()


    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    Movie.query.delete()
    

    print "Movies"

    for row in open("seed_data/u.item"):
        row = row.rstrip()
        split_row = row.split("|")
        new_row = split_row[0:-19]

        movie_id, title, release_at, _empty, imdb_url = new_row

        # The date is in the file as daynum-month_abbreviation-year;
        # we need to convert it to an actual datetime object.
        if release_at:
            release_at = datetime.datetime.strptime(release_at, "%d-%b-%Y")
        else:
            release_at = None

        #_empty is throw away var not to be used
        title = title[0:-7]       # " (YEAR)" == 7
        
        # movie_id = new_row[0] 
        # title = new_row[1]
        # title = title[0:-7]
        # release_at = new_row[2] 
        # imdb_url = new_row[4]

        movie = Movie(movie_id=movie_id, title=title, 
                        release_at=release_at, imdb_url=imdb_url) 

         # Adding each item as we are running for loop
        db.session.add(movie)
   

    # committing the batch
    db.session.commit()



def load_ratings():
    """Load ratings from u.data into database."""

    Rating.query.delete()
    

    print "Ratings"

    for row in open("seed_data/u.data"):
        row = row.rstrip()
        split_row = row.split("\t")        

        user_id = split_row[0]
        movie_id = split_row[1]
        score = split_row[2]

        rating = Rating(user_id=user_id, movie_id=movie_id, 
                            score=score)

        db.session.add(rating)

    db.session.commit()



def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    #max is a method on func, func is a class imported from sqlalchemy
    #.one() purpose is to fetch records
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
