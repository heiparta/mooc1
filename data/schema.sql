drop table if exists users;
create table users (
  id integer primary key autoincrement,
  name text not null,
  password text not null
);
insert into users (id, name, password) values (1, "user1", "user1");
insert into users (id, name, password) values (2, "user2", "user2");

drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  content text not null,
  user integer,
  FOREIGN KEY(user) REFERENCES users(id)
);
insert into entries (user, title, content) values (1, "Entry for user1", "Text for entry one");
insert into entries (user, title, content) values (2, "Second entry, for user2", "Text for second entry");
