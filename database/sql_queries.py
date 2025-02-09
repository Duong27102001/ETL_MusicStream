# DROP TABLES
songplay_table_drop = "DROP TABLE IF EXISTS fact_songplays"
user_table_drop = "DROP TABLE IF EXISTS dim_users"
song_table_drop = "DROP TABLE IF EXISTS dim_songs"
artist_table_drop = "DROP TABLE IF EXISTS dim_artists"
time_table_drop = "DROP TABLE IF EXISTS dim_time"

#DELETE RECORDS
songplay_table_delete = "DELETE FROM fact_songplays"
user_table_delete = "DELETE FROM dim_users"
song_table_delete = "DELETE FROM dim_songs"
artist_table_delete = "DELETE FROM dim_artists"
time_table_delete = "DELETE FROM dim_time"

#CREATE DIM_TABLES
user_table_create = ("""CREATE TABLE IF NOT EXISTS dim_users(
    user_key SERIAL CONSTRAINT users_pk PRIMARY KEY,
    user_id INT NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    gender CHAR(1),
    level VARCHAR(10) NOT NULL,
    rowIsCurrent BOOLEAN DEFAULT TRUE, 
    rowStartDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    rowEndDate TIMESTAMP DEFAULT '1999-12-31' NOT NULL,
    rowChangeReason VARCHAR NULL
    
)""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS dim_artists(
    artist_key SERIAL CONSTRAINT artists_pk PRIMARY KEY,
    artist_id VARCHAR(100) NOT NULL,
    name VARCHAR(100),
    location VARCHAR(255),
    latitude DECIMAL(9,6),
    longtitude DECIMAL(9,6),
    rowIsCurrent BOOLEAN DEFAULT TRUE,  
    rowStartDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    rowEndDate TIMESTAMP DEFAULT '1999-12-31' NOT NULL,
    rowChangeReason VARCHAR NULL
)""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS dim_songs(
    song_key SERIAL CONSTRAINT songs_pk PRIMARY KEY,
    song_id VARCHAR NOT NULL,
    title VARCHAR,
    artist_key INT REFERENCES dim_artists(artist_key),
    year INT CHECK(year >= 0),
    duration FLOAT,
    rowIsCurrent BOOLEAN DEFAULT TRUE, 
    rowStartDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    rowEndDate TIMESTAMP DEFAULT '1999-12-31' NOT NULL,
    rowChangeReason VARCHAR NULL
)""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS dim_time(
    day_key INT CONSTRAINT time_pk PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    hour INT NOT NULL CHECK (hour >= 0),
    day INT NOT NULL CHECK (day >= 0),
    week INT NOT NULL CHECK (week >= 0),
    month INT NOT NULL CHECK (month >= 0),
    year INT NOT NULL CHECK (year >= 0),
    weekday INT NOT NULL
)
                   """)

#CREATE FACT TABLE
songplay_table_create = (""" CREATE TABLE IF NOT EXISTS fact_songplays(
    songplay_id SERIAL CONSTRAINT songplay_pk PRIMARY KEY,
    day_key INT REFERENCES dim_time(day_key),
    user_key INT REFERENCES dim_users(user_key),
    song_key INT REFERENCES dim_songs(song_key),
    artist_key INT REFERENCES dim_artists(artist_key),
    session_key INT NOT NULL,
    user_agent TEXT
)                     
    """)

#INSERT RECORDS 
songplay_table_insert = "INSERT INTO fact_songplays VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)"

#Apply SCD type 2 to the dim_users, dim_songs, dim_artists
user_table_insert = "INSERT INTO dim_users(user_id, first_name, last_name, gender, level) VALUES(%s, %s, %s, %s, %s)"
songs_table_insert = "INSERT INTO dim_songs(song_id, title, artist_key, year, duration) VALUES(%s, %s, %s, %s, %s)"
artist_table_insert = "INSERT INTO dim_artists(artist_id, name, location, latitude, longtitude) VALUES(%s, %s, %s, %s, %s)"

#Apply CSD type 1 to the dim_time
#If the new data matches the existing data (conflict on day_key), do nothing 
time_table_insert = "INSERT INTO dim_time VALUES(%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (day_key) DO NOTHING"


#Check if user_id exists in the dim_users table
user_select = "SELECT first_name, last_name, gender, level FROM dim_users WHERE user_id = %s AND rowiscurrent = TRUE"
artist_select = "SELECT artist_id, name, location, longtitude, latitude FROM dim_artists WHERE artist_id = %s AND rowiscurrent = TRUE"
song_select = "SELECT song_id, title, year, duration FROM dim_songs WHERE song_id = %s AND rowiscurrent = TRUE"

join_song_artist_dim = ("""SELECT dim_songs.song_key, dim_artists.artist_key
    FROM dim_songs JOIN dim_artists ON dim_songs.artist_key = dim_artists.artist_key
    WHERE dim_songs.title = %s
    AND dim_artists.name = %s
    AND dim_songs.duration = %s
""")
user_key_select = "SELECT user_key FROM dim_users WHERE user_id = %s AND rowiscurrent = TRUE"
#SELECT RECORD WITH CONDITION
artists_key_select = """SELECT artist_key FROM dim_artists WHERE artist_id = %s AND rowiscurrent = TRUE"""
#FUCNTION UPDATE

#Update the old record in the dim_users to mark it as no longer effective
update_user = "UPDATE dim_users SET rowiscurrent = FALSE, rowenddate = now() WHERE user_id = %s and rowiscurrent = TRUE"
update_artist = "UPDATE dim_artists SET rowiscurrent = FALSE, rowenddate = now() WHERE artist_id = %s and rowiscurrent = TRUE"
update_song = "UPDATE dim_songs SET rowiscurrent = FALSE, rowenddate = now() WHERE song_id = %s and rowiscurrent = TRUE"
#QUERY LIST
create_table_queries = [user_table_create, artist_table_create, song_table_create, time_table_create, 
                        songplay_table_create]
drop_table_queries = [songplay_table_drop, song_table_drop, user_table_drop, artist_table_drop, time_table_drop]

delete_records = [songplay_table_delete, song_table_delete, user_table_delete, artist_table_delete, time_table_delete]