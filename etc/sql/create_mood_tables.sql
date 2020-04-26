create table mood_value
(
	id interger not null
		constraint mood_value_pk
			primary key autoincrement,
	value string not null
);

create unique index mood_value_id_uindex
	on mood_value (id);

create unique index mood_value_value_uindex
	on mood_value (value);


create table mood_report
(
	id integer not null
		constraint mood_report_pk
			primary key autoincrement,
	mood_value_id integer not null,
	user_id integer not null,
	date date not null
);

create unique index mood_report_id_uindex
	on mood_report (id);

create table mood_percentiles
(
	percentile float not null
		constraint mood_percentiles_pk
			primary key,
	streak_days integer not null
);