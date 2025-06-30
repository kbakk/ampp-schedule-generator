import typer
from ampp_schedule_generator import models


def generate_schedule(id: str, name: str) -> None:
    schedule = models.Schedule(id=id, name=name, items=[])
    print(schedule.model_dump_json())


if __name__ == "__main__":
    typer.run(generate_schedule)
