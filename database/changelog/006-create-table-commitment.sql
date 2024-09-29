--liquibase formatted sql

--changeset damian@swistowski.org:006.0
CREATE TABLE commitment
(
    id              serial primary key,
    investor_id     integer references investor    not null,
    currency_symbol text references currency       not null,
    class_id        integer references asset_class not null,
    amount          bigint                         not null
)
--rollback drop table commitment
