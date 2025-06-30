from ampp_schedule_generator import models


def generate_schedule(id: str, name: str) -> models.Schedule:
    items = []
    # add items ...
    return models.Schedule(id=id, name=name, items=items)
