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
INSERT INTO users
VALUES (1, 'szkript', 'Szanyi', 'Krisztián', '$2b$12$W/2xeeOXDf9EVoJemNANf.pFE0v8cG30Y6CX1f16V1hxvkP4Qwf6a', 'szkript@gmail.com');


INSERT INTO phases VALUES (0, 0, 1, NULL, NULL, '2019-05-09 22:46:00.652267', 1);
INSERT INTO phases VALUES (0, 0, NULL, 3, NULL, '2019-05-09 22:46:00.652268', 1);
INSERT INTO phases VALUES (0, 0, NULL, NULL, 2, '2019-05-09 22:46:00.652269', 1);
INSERT INTO phases VALUES (0, 0, 7, NULL, NULL, '2019-05-09 22:46:00.652270', 2);
INSERT INTO phases VALUES (0, 0, NULL, 9, NULL, '2019-05-09 22:46:00.652271', 2);
INSERT INTO phases VALUES (0, 0, NULL, NULL, 4, '2019-05-09 22:46:00.652272', 2);
INSERT INTO phases VALUES (0, 0, 3, NULL, NULL, '2019-05-09 22:46:00.652273', 3);
INSERT INTO phases VALUES (0, 0, NULL, 2, NULL, '2019-05-09 22:46:00.652273', 3);


ALTER TABLE ONLY users
  ADD CONSTRAINT pk_user_id PRIMARY KEY (id);

ALTER TABLE ONLY phases
  ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id) on delete cascade;