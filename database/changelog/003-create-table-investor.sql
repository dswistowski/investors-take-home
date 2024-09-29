--liquibase formatted sql

--changeset damian@swistowski.org:003.0
CREATE TABLE investor
(
    id           serial primary key,
    name         text                              not null unique,
    type_id      integer references investory_type not null,
    country_id   integer references country        not null,
    date_added   date                              not null default now(),
    last_updated date                              not null default now()
)
--rollback drop table investor