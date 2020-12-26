import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

#Staging Tables
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"

#Main Database
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time_table"

# CREATE TABLES
## DIST AND SORT KEYS ARE GIVEN TO OPTMIZIE THE QUERIES

staging_events_table_create= (""" CREATE TABLE staging_events(
                              eventId          BIGINT IDENTITY(0,1) NOT NULL distkey,
                              artist           VARCHAR,
                              auth             VARCHAR,
                              firstName        VARCHAR,
                              gender           VARCHAR,
                              itemInsession    SMALLINT,
                              lastName         VARCHAR,
                              length           FLOAT,
                              level            VARCHAR,
                              location         VARCHAR,
                              method           VARCHAR,
                              page             VARCHAR,
                              registration     VARCHAR,
                              sessionId        INTEGER,
                              song             VARCHAR,
                              status           INTEGER,
                              ts               BIGINT,
                              userAgent        VARCHAR,
                              userId           INTEGER);

""")
staging_songs_table_create = (""" CREATE TABLE staging_songs(
                                     num_songs          INTEGER,       
                                     artist_id          VARCHAR NOT NULL,
                                     artist_latitude    FLOAT,
                                     artist_longitude   FLOAT,
                                     artist_location    VARCHAR,
                                     artist_name        VARCHAR,
                                     song_id            VARCHAR NOT NULL distkey,
                                     title              VARCHAR,
                                     duration           FLOAT,
                                     year               INTEGER sortkey);
""")

songplay_table_create = (""" CREATE TABLE songplays(
                                    songplay_id        INTEGER IDENTITY(0,1) NOT NULL distkey sortkey, 
                                    start_time         TIMESTAMP, 
                                    user_id            INTEGER NOT NULL, 
                                    level              VARCHAR, 
                                    song_id            VARCHAR,
                                    artist_id          VARCHAR,
                                    session_id         INTEGER NOT NULL, 
                                    location           VARCHAR, 
                                    user_agent         VARCHAR
                                    );
                        """)

user_table_create = (""" CREATE TABLE users(
                                 user_id         INTEGER NOT NULL sortkey, 
                                 first_name      VARCHAR NOT NULL, 
                                 last_name       VARCHAR NOT NULL, 
                                 gender          VARCHAR, 
                                 level           VARCHAR NOT NULL
                                 );
                    """)
song_table_create = (""" CREATE TABLE songs(
                                song_id          VARCHAR NOT NULL sortkey, 
                                title            VARCHAR NOT NULL, 
                                artist_id        VARCHAR NOT NULL, 
                                year             INTEGER, 
                                duration         FLOAT(8)
                                );
                    """)

artist_table_create = (""" CREATE TABLE artists(
                                  artist_id      VARCHAR NOT NULL sortkey, 
                                  name           VARCHAR NOT NULL,
                                  location       VARCHAR, 
                                  latitude       FLOAT(8), 
                                  longitude      FLOAT(8)
                                  );
                      """)

time_table_create = (""" CREATE TABLE time_table(
                                start_time      TIMESTAMP NOT NULL sortkey, 
                                hour            INTEGER, 
                                day             INTEGER, 
                                week            INTEGER, 
                                month           INTEGER, 
                                year            INTEGER, 
                                weekday         INTEGER
                                );
                     """)

# STAGING TABLES

staging_events_copy = (""" COPY staging_events
                           FROM {}
                           CREDENTIALS 'aws_iam_role={}'
                           REGION 'us-west-2'
                           JSON AS {} ;
                       """).format(config.get("S3", "LOG_DATA"),config.get('IAM_ROLE','ARN'),config.get("S3", "LOG_JSONPATH"))

staging_songs_copy = (""" COPY staging_songs
                          FROM {}
                          CREDENTIALS 'aws_iam_role={}'
                          REGION 'us-west-2'
                          JSON AS 'auto' ;
                       """).format(config.get("S3", "SONG_DATA"),config.get("IAM_ROLE","ARN"))

# FINAL TABLES

songplay_table_insert = (""" INSERT INTO songplays(start_time, 
                                                   user_id, 
                                                   level, 
                                                   song_id, 
                                                   artist_id, 
                                                   session_id, 
                                                   location, 
                                                   user_agent)
                             SELECT timestamp 'epoch' + e.ts/1000 * interval '1 second' AS start_time,
                                    e.userId         AS user_id,             
                                    e.level          AS level, 
                                    s.song_id        AS song_id,            
                                    s.artist_id      AS artist_id,
                                    e.sessionId  AS session_id,          
                                    e.location   AS location,           
                                    e.userAgent  AS user_agent  
                             FROM staging_events e
                             LEFT JOIN staging_songs s 
                                  ON  e.song = s.title AND
                                      e.artist = s.artist_name AND
                                      e.length = s.duration
                             WHERE e.page='NextSong' ;
""")

##UNIQUE USER ## latest level

user_table_insert = (""" INSERT INTO users(user_id, first_name, last_name, gender, level)
                         SELECT DISTINCT s.userId    AS user_id,
                                s.firstName AS first_name,
                                s.lastName  AS last_name,
                                s.gender    AS gender,
                                s.level     AS level
                         FROM staging_events s
                         WHERE s.userId IS NOT NULL AND s.ts =(SELECT max(ts) from staging_events e where e.userId = s.userId
                         GROUP BY e.userId
                         ORDER BY e.userId) ;
                                                     
""")

## UNIQUE SONG

song_table_insert = ("""INSERT INTO songs(song_id, title, artist_id, year, duration)
                        SELECT DISTINCT song_id   AS song_id,
                               title     AS title,
                               artist_id AS artist_id,
                               year      AS year,
                               duration  AS duration
                        FROM staging_songs
                        WHERE song_id IS NOT NULL;
                                                             
""")

## UNIQUE ARTIST ## There are duplications of artist names for single_id in staging data ( which is sorted by year), 
#so Selecting last record of name, location, latitude & longitude)
artist_table_insert = ("""INSERT INTO artists(artist_id, name, location, latitude, longitude)
                          SELECT DISTINCT s.artist_id  AS artist_id,
                                 s.artist_name         AS name,
                                 s.artist_location     AS location,
                                 s.artist_latitude     AS latitude,
                                 s.artist_longitude    AS longitude
                          FROM staging_songs s
                          WHERE s.artist_id IS NOT NULL and s.year=(SELECT 
                          max(year) AS yr 
                          FROM staging_songs s2 where s2.artist_id = s.artist_id
                          GROUP BY s2.artist_id
                          ORDER BY yr DESC);
""")

## UNIQUE TIMSETAMP

time_table_insert = ("""INSERT INTO time_table(start_time, hour, day, week, month, year, weekday)
                        SELECT start_time                     AS start_time,
                               EXTRACT(HOUR FROM start_time)  AS hour,
                               EXTRACT(DAY FROM start_time)   AS day,
                               EXTRACT(WEEK FROM start_time)  AS week,
                               EXTRACT(MONTH FROM start_time) AS month,
                               EXTRACT(YEAR FROM start_time)  AS year,
                               EXTRACT(DOW FROM start_time)   AS weekday
                        FROM (SELECT distinct ts,'1970-01-01'::date + ts/1000 * interval '1 second' as start_time
                        FROM staging_events)
                        WHERE start_time IS NOT NULL;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
