--liquibase formatted sql

--changeset damian@swistowski.org:001.0
CREATE TABLE investory_type
(
    id   serial primary key,
    name text not null

)
--rollback drop table investory_type