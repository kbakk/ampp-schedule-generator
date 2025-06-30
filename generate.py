import typer
from ampp_schedule_generator import models


def generate_schedule(id: str, name: str) -> models.Schedule:
    items = []
    # add items ...
    return models.Schedule(id=id, name=name, items=items)


def generate_and_output_schedule(id: str, name: str) -> None:
    schedule = generate_schedule(id, name)
    print(schedule.model_dump_json())


if __name__ == "__main__":
    typer.run(generate_and_output_schedule)
