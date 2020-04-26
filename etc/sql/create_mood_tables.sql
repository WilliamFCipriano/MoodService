create table mood_values
(
	id interger not null
		constraint mood_values_pk
			primary key autoincrement,
	value string not null
);

create unique index mood_values_id_uindex
	on mood_values (id);

create unique index mood_values_value_uindex
	on mood_values (value);


create table mood_report
(
	id integer not null
		constraint mood_report_pk
			primary key autoincrement,
	mood_value_id integer not null,
	user_id integer not null,
	date integer not null
);

create unique index mood_report_id_uindex
	on mood_report (id);