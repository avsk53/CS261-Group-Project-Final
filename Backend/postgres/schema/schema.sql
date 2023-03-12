DROP TABLE IF EXISTS project_assignments CASCADE;
DROP TABLE IF EXISTS metric CASCADE;
DROP TABLE IF EXISTS metric_assignment CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS project CASCADE;
DROP TABLE IF EXISTS improvement_metrics CASCADE;
DROP TABLE IF EXISTS passwords CASCADE;
DROP TABLE IF EXISTS teams CASCADE;
DROP TABLE IF EXISTS project_evaluation CASCADE;

CREATE EXTENSION IF NOT EXISTS tablefunc;

CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(32),
    user_role INTEGER,
    role_desc VARCHAR(32),
    email VARCHAR(128) UNIQUE,
    last_logged_in TIMESTAMP
);

CREATE TABLE passwords(
    user_id INTEGER REFERENCES users(user_id),
    password_hash VARCHAR(300),
    PRIMARY KEY(user_id)
);

CREATE TABLE project(
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(64),
    project_start TIMESTAMP,
    project_end TIMESTAMP,
    number_of_people INTEGER,
    github_link VARCHAR(1000),
    project_manager_id INTEGER
);

CREATE TABLE project_evaluation(
    evaluation_id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES project(project_id),
    evaluation_date TIMESTAMP,
    evaluation_type INTEGER,
    evaluation_label VARCHAR(100),
    evaluation_percent FLOAT(16)
);

CREATE TABLE project_assignments(
    user_id INTEGER REFERENCES users(user_id),
    project_id INTEGER REFERENCES project(project_id), 
    PRIMARY KEY(user_id, project_id)    
);

CREATE TABLE metric(
    metric_id SERIAL PRIMARY KEY,
    metric_type INTEGER,
    metric_desc VARCHAR(64)
);

CREATE TABLE metric_assignment(
    metric_id INTEGER REFERENCES metric(metric_id), 
    project_id INTEGER REFERENCES project(project_id),
    metric_value FLOAT(16),
    PRIMARY KEY(metric_id, project_id)
);

--direction will be 1 if it's an increase in metric value, -1 if it's a decrease, 0 if no change.
--This comment is just for PR, delete when you read.
CREATE TABLE improvement_metrics(
    metric_id INTEGER REFERENCES metric(metric_id), 
    evaluation_id INTEGER REFERENCES project_evaluation(evaluation_id),
    direction INTEGER,
    improvement_value FLOAT(16),
    PRIMARY KEY(metric_id, evaluation_id)
);


CREATE TABLE teams(
    supervisor_id INTEGER REFERENCES users(user_id),
    project_manager_id INTEGER REFERENCES users(user_id),
    PRIMARY KEY(supervisor_id, project_manager_id)
);

ALTER SEQUENCE users_user_id_seq RESTART WITH 10000000;
ALTER SEQUENCE project_evaluation_evaluation_id_seq RESTART WITH 1000000;
ALTER SEQUENCE project_project_id_seq RESTART WITH 1000000;
