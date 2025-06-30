import typer
from ampp_schedule_generator import generate


def generate_and_output_schedule(
    network_name: str, environment: generate.EnvEnum
) -> None:
    schedule = generate.ScheduleGenerator(network_name, environment).generate_schedule()
    print(schedule.model_dump_json(exclude_unset=True))


if __name__ == "__main__":
    typer.run(generate_and_output_schedule)
