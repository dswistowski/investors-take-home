import typing as t
import os
import csv
from datetime import date, datetime
from decimal import Decimal

from typing_extensions import NamedTuple
from psycopg import connect


def with_id[T](element: t.Iterable[T]) -> t.Mapping[T, int]:
    return {e: i for i, e in enumerate(sorted(element))}  # type: ignore[type-var]


class Investor(NamedTuple):
    name: str
    type_id: int
    country_id: int
    date_added: date
    last_updated: date

class Commitment(NamedTuple):
    investor_id: int
    currency_symbol: str
    class_id: int
    amount: Decimal


def parse_date(str_date: str) -> date:
    return datetime.strptime(str_date, "%Y-%m-%d").date()

CSVFormat = t.TypedDict('CSVFormat', {
'Investor Name': str, 'Investory Type': str, 'Investor Country': str, 'Investor Date Added': str, 'Investor Last Updated': str, 'Commitment Asset Class': str, 'Commitment Amount': str, 'Commitment Currency': str
})

def seed(db_url: str, file_path: str):
    with open(file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        data = t.cast(list[CSVFormat], list(reader))

    investory_types = with_id({r["Investory Type"] for r in data})

    db_connection = connect(db_url, autocommit=True)
    with db_connection.cursor() as cursor:
        cursor.executemany("""INSERT INTO investory_type (name, id) VALUES (%s, %s) ON CONFLICT DO NOTHING """, list(investory_types.items()))

    countries = with_id({r["Investor Country"] for r in data})
    with db_connection.cursor() as cursor:
        cursor.executemany("""INSERT INTO country (name, id) VALUES (%s, %s) ON CONFLICT DO NOTHING """, list(countries.items()))

    asset_classes = with_id({r["Commitment Asset Class"] for r in data})
    with db_connection.cursor() as cursor:
        cursor.executemany("""INSERT INTO asset_class (name, id) VALUES (%s, %s) ON CONFLICT DO NOTHING """, list(asset_classes.items()))

    investors = with_id(
        {
            Investor(
                r["Investor Name"],
                investory_types[r["Investory Type"]],
                countries[r["Investor Country"]],
                parse_date(r["Investor Date Added"]),
                parse_date(r["Investor Last Updated"]),
            )
            for r in data
        }
    )
    with db_connection.cursor() as cursor:
        cursor.executemany(
            """INSERT INTO investor (id, name, type_id, country_id, date_added, last_updated) 
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING""",
            [
                (
                    id,
                    investor.name,
                    investor.type_id,
                    investor.country_id,
                    investor.date_added,
                    investor.last_updated,
                )
                for investor, id in investors.items()
            ],
        )

    investor_id_by_name = {investor.name: id for investor, id in investors.items()}
    currencies = {r['Commitment Currency'] for r in data}
    with db_connection.cursor() as cursor:
        cursor.executemany(
            """INSERT INTO currency (symbol) VALUES (%s) ON CONFLICT DO NOTHING""", [(c,) for c in currencies]
        )

    commitments = with_id({
        Commitment(
            investor_id=investor_id_by_name[r['Investor Name']],
            currency_symbol=r['Commitment Currency'],
            class_id=asset_classes[r['Commitment Asset Class']],
            amount=Decimal(r['Commitment Amount']),
        )
        for r in data
    })
    with db_connection.cursor() as cursor:
        cursor.executemany("""INSERT INTO commitment (id, investor_id, currency_symbol, class_id, amount) 
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING """, [(
            id,
            commitment.investor_id,
            commitment.currency_symbol,
            commitment.class_id,
            commitment.amount
        )
        for commitment, id in commitments.items()])


if __name__ == "__main__":
    try:
        db_url = os.environ["DB_URL"]
    except KeyError:
        raise RuntimeError("DB_URL env variable is not set") from None

    try:
        file = os.environ["SEED_FILE"]
    except KeyError:
        raise RuntimeError("SEED_FILE env variable is not set") from None

    seed(db_url, file)
