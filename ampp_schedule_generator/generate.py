import dataclasses
import datetime
import enum
import random
import string
import uuid

from ampp_schedule_generator import models


class EnvEnum(enum.StrEnum):
    prod = "prod"
    stage = "stage"


@dataclasses.dataclass
class Network:
    name: str
    environment: EnvEnum
    id: str


networks = [
    # prod
    Network(
        name="TV4", environment=EnvEnum.prod, id="46ca4f11-d0c5-45fd-9ee4-c35304f9e88c"
    ),
    Network(
        name="TV5", environment=EnvEnum.prod, id="26a426cd-b7ec-48e8-b54e-81b03d20b57f"
    ),
    Network(
        name="TV6", environment=EnvEnum.prod, id="d9519ccb-dcbb-4e70-bd8d-8cad3782f8dc"
    ),
    Network(
        name="TV7", environment=EnvEnum.prod, id="59ec5330-38eb-47ca-a67e-82c705506c39"
    ),
    Network(
        name="NRK-Super",
        environment=EnvEnum.prod,
        id="a1d943c9-556c-44b5-9879-e466fdadf897",
    ),
    # stage
    Network(
        name="TV4", environment=EnvEnum.stage, id="64cdb08e-7dfc-4a28-8bd5-e5fff0c5b731"
    ),
    Network(
        name="TV6", environment=EnvEnum.stage, id="1fcd7ec5-5d4c-4dad-b3f5-3ac5c917dd34"
    ),
]


def get_network(name: str, environment: EnvEnum) -> Network:
    for network in networks:
        if network.name.lower() == name.lower() and network.environment == environment:
            return network
    available = ", ".join(f"{n.name} ({n.environment})" for n in networks)
    raise ValueError(
        f"Network {name} ({environment}) not found, available networks: {available}"
    )


def _get_rand_id() -> str:
    return str(uuid.uuid4())


class ScheduleGenerator:
    def __init__(self, network_name: str, environment: EnvEnum):
        self.network = get_network(network_name, environment)
        curr_date = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
        self._schedule_name = f"{self.network.name}_{curr_date}"
        self._rec_prefix = f"zz-{self.network.name}-{curr_date}"

    def get_recording_name(self, part) -> str:
        rand_str = "".join(random.choices(string.ascii_lowercase, k=3))
        return f"{self._rec_prefix}-{part}-{rand_str}"

    def generate_schedule(self) -> models.Schedule:
        day_container = self._build_complete_container(
            name=self._schedule_name,
            container_items=[
                self._plakat_with_logo("GFX Fullscreen 1"),
                self._plakat_with_logo("GFX Fullscreen 2"),
                models.FlexibleItem(
                    id=_get_rand_id(),
                    name="SDI Input",
                    payload=models.FlexiblePayload(
                        type="Live",
                        materialType="Live",
                        materialId="NRK1ABIT",
                        sourceType="SDI",
                        timeDetails=models.TimeDetailsSimple(
                            duration="00:00:20.0000000",
                            timeMode="Auto",
                            endTimeMode="Manual",
                        ),
                        transitionDetails=models.TransitionDetails(type="Cut"),
                        liveDetails=models.LiveDetails(
                            mediaStatus="Invalid", mediaStatusReason="WaitingToResolve"
                        ),
                    ),
                    alternatives=[],
                    recorderStates=[],
                    version=1,
                    items=[],
                ),
                self._plakat_with_logo("GFX Fullscreen 2"),
            ],
        )

        return models.Schedule(
            id=self.network.id, name=self._schedule_name, items=[day_container]
        )

    @staticmethod
    def _build_complete_container(
        name: str, container_items: list[models.FlexibleItem]
    ) -> models.FlexibleItem:
        """Build the complete first container with all nested items."""
        return models.FlexibleItem(
            id=_get_rand_id(),
            name=name,
            payload=models.FlexiblePayload(
                type="Show",
                timeDetails=models.TimeDetailsNotional(
                    duration="24:00:00.0000000",
                    timeMode="Auto",
                    externalTriggerWindow={},
                    # notionalStartTime="2025-06-30T08:25:36.0000000Z",
                ),
            ),
            alternatives=[],
            recorderStates=[],
            version=8,
            items=container_items,
        )

    def _plakat_with_logo(self, name: str) -> models.FlexibleItem:
        logo_item = models.FlexibleItem(
            id=_get_rand_id(),
            name="NRKTV",
            payload=models.FlexiblePayload(
                type="Logo",
                timeDetails=models.TimeDetailsWithOffset(
                    offset="00:00:00.0000000", timeMode="ParentDuration"
                ),
                materialId="LG8ONE",
                layer=6,
                inTransitionDetails=models.TransitionDetails(
                    type="Fade", duration="00:00:00.2600000"
                ),
                outTransitionDetails=models.TransitionDetails(
                    type="Fade", duration="00:00:00.2600000"
                ),
            ),
            alternatives=[],
            recorderStates=[],
            version=1,
            items=[],
        )

        return models.FlexibleItem(
            id=_get_rand_id(),
            name=name,
            payload=models.FlexiblePayload(
                type="Live",
                productcode="ChyronQ7AA",
                materialId=f"{self.network.name}-PLAKAT",
                timeDetails=models.TimeDetailsSimple(
                    duration="00:01:00.0000000", timeMode="Auto", endTimeMode="Manual"
                ),
                materialType="Live",
                sourceType="Fabric",
                transitionDetails=models.TransitionDetails(type="Cut"),
                liveDetails=models.LiveDetails(
                    mediaStatus="Invalid", mediaStatusReason="WaitingToResolve"
                ),
            ),
            alternatives=[],
            recorderStates=[],
            version=1,
            items=[],
        )

    def _build_show_wrapper(
        self, name: str, record_part: str, items: list[models.FlexibleItem]
    ) -> models.FlexibleItem:
        return models.FlexibleItem(
            id=_get_rand_id(),
            name=name,
            payload=models.FlexiblePayload(
                type="Show",
                timeDetails=models.TimeDetailsSimple(
                    duration="00:01:00.0000000",
                    timeMode="Auto",
                    externalTriggerWindow={},
                ),
                recording=models.Recording(
                    recordDetails=[
                        models.RecordDetail(
                            sourceType="Clean feed",
                            name=self.get_recording_name(record_part),
                        )
                    ]
                ),
            ),
            alternatives=[],
            recorderStates=[],
            version=2,
            items=items,
        )

    def _build_testserie_show(self, record_part: str) -> models.FlexibleItem:
        return models.FlexibleItem(
            id=_get_rand_id(),
            name="Testserie AMPP: Fotball",
            payload=models.FlexiblePayload(
                type="Show",
                recording=models.Recording(
                    recordDetails=[
                        models.RecordDetail(
                            sourceType="Clean feed",
                            name=self.get_recording_name(record_part),
                        )
                    ]
                ),
                productcode="MSPO000027/24",
            ),
            alternatives=[],
            recorderStates=[],
            version=4,
            items=[
                models.FlexibleItem(
                    id=_get_rand_id(),
                    name=f"{i['name']} ({i['MaterialId']})",
                    payload=models.FlexiblePayload(
                        type=i["Type"],
                        materialType="Live",
                        materialId=i["MaterialId"],
                        sourceType="Fabric",
                        timeDetails=models.TimeDetailsSimple(
                            duration="00:00:20.0000000",
                            timeMode="Auto",
                            endTimeMode="Manual",
                        ),
                        transitionDetails=models.TransitionDetails(type="Cut"),
                        liveDetails=models.LiveDetails(
                            mediaStatus="Invalid", mediaStatusReason="WaitingToResolve"
                        ),
                    ),
                    alternatives=[],
                    recorderStates=[],
                    version=1,
                    items=[],
                )
                for i in [
                    {
                        "name": "Sub-item 1",
                        "Type": "Live",
                        "MaterialId": f"{self.network.name}-A",
                    },
                    {
                        "name": "Sub-item 2",
                        "Type": "Live",
                        "MaterialId": f"{self.network.name}-B",
                    },
                    {
                        "name": "Sub-item 3",
                        "Type": "Live",
                        "MaterialId": f"{self.network.name}-A",
                    },
                ]
            ],
        )

    @staticmethod
    def _build_sync_note() -> models.FlexibleItem:
        """Build the SYNC NOTE item."""
        return models.FlexibleItem(
            id="sync-note-id-new",
            name="SYNC NOTE",
            payload=models.FlexiblePayload(
                type="Note",
                materialId="SYNC NOTE",
                notes="🔽 Alt nedenfor synkroniseres fra PRF / alt ovenfor (180 minutter) kan endres 🔼",
                timeDetails=models.TimeDetailsSimple(timeMode="Auto"),
                transitionDetails=models.TransitionDetails(type="Cut"),
            ),
            alternatives=[],
            recorderStates=[],
            version=1,
            items=[],
        )
