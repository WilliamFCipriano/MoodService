create table users
(
  int_id        integer not null
    constraint users_pk
      primary key autoincrement,
  user_name       string  not null,
  password_hash integer not null,
  last_submission date,
  streak_days integer
);

create unique index users_int_id_uindex
  on users (int_id);

create unique index users_user_id_uindex
  on users (user_id);
