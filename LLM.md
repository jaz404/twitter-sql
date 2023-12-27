# More detail of any AI tool used, including the name, URL, all the input given and all the output received.  
To generate some intial data that could be inserted in the database, we used chatGPT:
chatGPT: https://chat.openai.com/
Prompt: 
-- Let's drop the tables in case they exist from previous runs
drop table if exists includes;
drop table if exists lists;
drop table if exists retweets;
drop table if exists mentions;
drop table if exists hashtags;
drop table if exists tweets;
drop table if exists follows;
drop table if exists users;

create table users (
  usr         int,
  pwd	      text,
  name        text,
  email       text,
  city        text,
  timezone    float,
  primary key (usr)
);
create table follows (
  flwer       int,
  flwee       int,
  start_date  date,
  primary key (flwer,flwee),
  foreign key (flwer) references users,
  foreign key (flwee) references users
);
create table tweets (
  tid	      int,
  writer      int,
  tdate       date,
  text        text,
  replyto     int,
  primary key (tid),
  foreign key (writer) references users,
  foreign key (replyto) references tweets
);
create table hashtags (
  term        text,
  primary key (term)
);
create table mentions (
  tid         int,
  term        text,
  primary key (tid,term),
  foreign key (tid) references tweets,
  foreign key (term) references hashtags
);
create table retweets (
  usr         int,
  tid         int,
  rdate       date,
  primary key (usr,tid),
  foreign key (usr) references users,
  foreign key (tid) references tweets
);
create table lists (
  lname        text,
  owner        int,
  primary key (lname),
  foreign key (owner) references users
);
create table includes (
  lname       text,
  member      int,
  primary key (lname,member),
  foreign key (lname) references lists,
  foreign key (member) references users
);

Here are some tables in a database, Generate a some inital values that i can insert in them

chatGPT response:
Certainly! Here's some starter data/values that you can insert into the tables you've created:

```sql
-- Users
INSERT INTO users (usr, pwd, name, email, city, timezone)
VALUES
(1, 'password1', 'User1', 'user1@example.com', 'City1', 5.5),
(2, 'password2', 'User2', 'user2@example.com', 'City2', 4.0),
(3, 'password3', 'User3', 'user3@example.com', 'City3', 6.5);

-- Follows
INSERT INTO follows (flwer, flwee, start_date)
VALUES
(1, 2, '2023-01-01'),
(1, 3, '2023-01-02'),
(2, 1, '2023-01-03'),
(3, 2, '2023-01-04');

-- Tweets
INSERT INTO tweets (tid, writer, tdate, text, replyto)
VALUES
(1, 1, '2023-01-01', 'This is the first tweet!', NULL),
(2, 2, '2023-01-02', 'Hello, Twitter!', NULL),
(3, 1, '2023-01-03', 'Replying to tweet 1.', 1),
(4, 3, '2023-01-04', 'Retweeting tweet 2.', NULL);

-- Hashtags
INSERT INTO hashtags (term)
VALUES
('#technology'),
('#programming'),
('#socialmedia');

-- Mentions
INSERT INTO mentions (tid, term)
VALUES
(1, '#technology'),
(2, '#socialmedia'),
(3, '#programming'),
(4, '#programming');

-- Retweets
INSERT INTO retweets (usr, tid, rdate)
VALUES
(2, 1, '2023-01-02'),
(3, 4, '2023-01-05');

-- Lists
INSERT INTO lists (lname, owner)
VALUES
('Tech Enthusiasts', 1),
('Favorite Writers', 2);

-- Includes
INSERT INTO includes (lname, member)
VALUES
('Tech Enthusiasts', 2),
('Favorite Writers', 1),
('Tech Enthusiasts', 3);
```

This code inserts some sample data into your tables, demonstrating how to populate them with values. You can adjust the data as needed for your specific use case.
