--liquibase formatted sql

--changeset damian@swistowski.org:002.0
CREATE TABLE country
(
    id   serial primary key,
    name text not null

)
--rollback drop table country