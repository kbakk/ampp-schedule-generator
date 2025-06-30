import typer
from ampp_schedule_generator import generate


def generate_and_output_schedule(id: str, name: str) -> None:
    schedule = generate.generate_schedule(id, name)
    print(schedule.model_dump_json())


if __name__ == "__main__":
    typer.run(generate_and_output_schedule)
