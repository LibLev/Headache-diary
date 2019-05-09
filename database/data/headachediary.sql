ALTER TABLE IF EXISTS ONLY public.user DROP CONSTRAINT IF EXISTS pk_user_id CASCADE;


DROP TABLE IF EXISTS public.user;
CREATE TABLE users (
  id serial NOT NULL,
  user_name varchar,
  first_name varchar,
  last_name varchar,
  hashed_password text,
  email_address varchar
);

DROP TABLE IF EXISTS public.phases;
CREATE TABLE phases (
  id serial NOT NULL,
  user_id integer,
  morning_scale integer,
  afternoon_scale integer,
  evening_scale integer,
  submission_time timestamp without time zone,
  num_of_day int
);

INSERT INTO users
VALUES (0, 'admin', 'admin', 'admin', '$2b$12$YFMZw7nZtVRiap51QSWj2uU5pUGPFvmOYadN89OtwAwbBnNG21/qO', 'headachediary.noreply@gmail.com');

ALTER TABLE ONLY users
  ADD CONSTRAINT pk_user_id PRIMARY KEY (id);

ALTER TABLE ONLY phases
  ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id) on delete cascade;