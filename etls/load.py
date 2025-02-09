import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import psycopg2
from database.sql_queries import *
from config.config import DATABASE_CONFIG
    
def load_dim_Time(path):
    df = pd.read_csv(path, delimiter="," , header=0 )
    #connect to database
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    for _, row in df.iterrows():
        cur.execute(time_table_insert, (row.day_key, row.start_time, row.hour, row.day, row.week, row.month, row.year, row.weekdate))
        conn.commit()
    cur.close()
    conn.close()

def load_dim_Users(path):
    df = pd.read_csv(path, decimal=",", header=0)
    
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    
    for _, row in df.iterrows():
        #Check user_id exits
        cur.execute(user_select,(int(float(row.userId)),))
        existing_user = cur.fetchone()
        if existing_user:
            if (row.firstName, row.lastName, row.gender, row.level) == existing_user:
                continue
            else:
                cur.execute(update_user,(int(float(row.userId)),))
        cur.execute(user_table_insert, (int(float(row.userId)), row.firstName, row.lastName, row.gender, row.level))
        conn.commit()
    cur.close()
    conn.close()
    
def load_dim_artists(path):
    df = pd.read_csv(path, decimal=",", header=0)
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    
    for _, row in df.iterrows():
        cur.execute(artist_select, (row.artist_id,))
        existing_artist = cur.fetchone()
        if existing_artist:
            if (row.artist_id, row.artist_name, row.artist_location, row.artist_longitude, row.artist_latitude) == existing_artist:
                continue
            else:
                cur.execute(update_artist, (row.artist_id,))
        cur.execute(artist_table_insert, (row.artist_id, row.artist_name, row.artist_location, row.artist_longitude, row.artist_latitude))
        conn.commit()
    cur.close()
    conn.close()

def load_dim_songs(path):
    df = pd.read_csv(path, decimal=",", header=0)
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()    
    for _, row in df.iterrows():
        cur.execute(song_select, (row.artist_id,))
        existing_song = cur.fetchone()
        if existing_song:
            if (row.song_id, row.title, row.year, row.duration) == existing_song:
                continue
            else:
                cur.execute(update_song, (row.song_id))

        cur.execute(artists_key_select, (row.artist_id,))
        result = cur.fetchone()
        if result:
            artist_key = result
        else:
            artist_key = None
        cur.execute(songs_table_insert, (row.song_id, row.title, artist_key, row.year, row.duration))
        conn.commit()
    cur.close()
    conn.close()
    
def load_fact_songplays(path):
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    df = pd.read_csv(path, decimal=",", header=0)
    for _, row in df.iterrows():
        cur.execute(join_song_artist_dim, (row.song, row.artist, row.length))
        result = cur.fetchone()
        if result:
            song_key, artist_key = result
        else:
            song_key, artist_key = None, None
        
        cur.execute(user_key_select, (int(float(row.userId)),))
        result = cur.fetchone()
        if result:
            user_key = result
        else:
            user_key = None, None
        cur.execute(songplay_table_insert, (row.day_key, user_key, song_key, artist_key, row.sessionId, row.userAgent ))
        conn.commit()
    cur.close()
    conn.close()