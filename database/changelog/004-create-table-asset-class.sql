--liquibase formatted sql

--changeset damian@swistowski.org:004.0
CREATE TABLE asset_class
(
    id   serial primary key,
    name text not null
)
--rollback drop table asset_class