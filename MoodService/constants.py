database_location = 'moodService.db'


create_user_table = ["""
create table users
(
  int_id        integer not null
    constraint users_pk
      primary key autoincrement,
  user_id       string  not null,
  password_hash integer not null
);
""","""
create unique index users_int_id_uindex
  on users (int_id);
""","""
create unique index users_user_id_uindex
  on users (user_id);
"""]