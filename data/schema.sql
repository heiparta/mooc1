drop table if exists users;
create table users (
  id integer primary key autoincrement,
  name text not null
);
insert into users (id, name) values (1, "Foo");
insert into users (id, name) values (2, "Bar");

drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  user integer,
  FOREIGN KEY(user) REFERENCES users(id)
);
insert into entries (user, title) values (1, "First entry");
insert into entries (user, title) values (2, "Second entry");
