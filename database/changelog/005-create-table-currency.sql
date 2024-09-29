--liquibase formatted sql

--changeset damian@swistowski.org:005.0
CREATE TABLE currency
(
    symbol text primary key
)
--rollback drop table currency