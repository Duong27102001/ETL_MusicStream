import pandas as pd
import os

def process_song(path):
    song_data = pd.read_csv(path, delimiter="," , header=0 )
    #take artist_data
    stg_artist = song_data[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']]
    stg_artist = stg_artist.drop_duplicates()
    stg_artist = stg_artist.dropna()
    stg_artist_path = "./data/processed/stg_artist.csv"
    if os.path.exists(stg_artist_path): 
        os.remove(stg_artist_path)
    stg_artist.to_csv(stg_artist_path, index=False)
    
    #take song_data
    stg_song = song_data[['song_id', 'title', 'artist_id', 'year', 'duration']]    
    stg_song = stg_song.drop_duplicates()
    stg_song = stg_song.dropna()
    stg_song_path = "./data/processed/stg_song.csv"
    if os.path.exists(stg_song_path): 
        os.remove(stg_song_path)
    stg_song.to_csv(stg_song_path, index=False)

def process_log(path):
    log_data = pd.read_csv(path, delimiter="," , header=0 )
    log_data = log_data[log_data['page'] == 'NextSong'].astype({'ts': 'datetime64[ms]'})
    
    #take user_data
    stg_user = log_data[['userId','firstName','lastName','gender','level']]
    stg_user = stg_user.drop_duplicates()
    stg_user = stg_user.dropna()
    
    stg_user_path = "./data/processed/stg_user.csv"
    if os.path.exists(stg_user_path): 
        os.remove(stg_user_path)
    stg_user.to_csv(stg_user_path, index=False)
    
    #take stg_log
    log_data['day_key'] = log_data['ts'].dt.strftime('%Y%m%d%H')
    log_data = log_data[['day_key','userId','song', 'artist', 'userAgent', 'sessionId', 'length']]
    
    stg_log_path = "./data/processed/stg_log.csv"
    if os.path.exists(stg_log_path): 
        os.remove(stg_log_path)
    log_data.to_csv(stg_log_path, index=False)

def process_time():
    date_range = pd.date_range(start="2018-11-01", end="2018-12-01", freq='H')
    
    stg_time = pd.DataFrame({
        "day_key": date_range.strftime('%Y%m%d%H'),
        "start_time": date_range,
        "hour": date_range.hour,
        "day": date_range.day,
        "week": date_range.isocalendar().week,
        "month": date_range.month,
        "year": date_range.year,
        "weekdate": date_range.weekday
    })
    
    stg_time_path = "./data/processed/stg_time.csv"
    if os.path.exists(stg_time_path): 
        os.remove(stg_time_path)
    stg_time.to_csv(stg_time_path, index=False)