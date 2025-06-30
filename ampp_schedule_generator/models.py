from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Payload(BaseModel):
    type: str
    timeDetails: TimeDetailsNotional


class TimeDetailsSimple(BaseModel):
    duration: Optional[str] = None
    timeMode: str
    endTimeMode: Optional[str] = None
    externalTriggerWindow: Optional[Dict[str, Any]] = None
    startTime: Optional[str] = None


class TimeDetailsNotional(BaseModel):
    duration: str
    timeMode: str
    externalTriggerWindow: Optional[Dict[str, Any]] = None
    notionalStartTime: Optional[str] = None
    startTime: Optional[str] = None


class TimeDetailsWithOffset(BaseModel):
    offset: Optional[str] = None
    timeMode: str
    startTime: Optional[str] = None
    duration: Optional[str] = None
    endTimeMode: Optional[str] = None
    fluidDuration: Optional[bool] = None
    inPoint: Optional[str] = None


class TimeDetailsOffsetRequired(BaseModel):
    offset: str
    timeMode: str
    duration: Optional[str] = None


class TransitionDetails(BaseModel):
    type: str


class InTransitionDetails(BaseModel):
    type: str
    duration: str


class OutTransitionDetails(BaseModel):
    type: str
    duration: str


class LiveDetails(BaseModel):
    mediaStatus: str
    mediaStatusReason: str


class RecordDetail(BaseModel):
    sourceType: str
    name: str


class Recording(BaseModel):
    recordDetails: List[RecordDetail]


class AggregatedDetails(BaseModel):
    duration: str
    inPoint: str
    outPoint: str


class Level1Payload(BaseModel):
    type: str
    productcode: Optional[str] = None
    materialId: Optional[str] = None
    timeDetails: Optional[TimeDetailsSimple] = None
    materialType: Optional[str] = None
    sourceType: Optional[str] = None
    transitionDetails: Optional[TransitionDetails] = None
    liveDetails: Optional[LiveDetails] = None
    recording: Optional[Recording] = None
    notes: Optional[str] = None


class Level2Payload(BaseModel):
    type: str
    timeDetails: TimeDetailsWithOffset
    materialId: str
    layer: Optional[int] = None
    inTransitionDetails: Optional[InTransitionDetails] = None
    outTransitionDetails: Optional[OutTransitionDetails] = None
    productcode: Optional[str] = None
    materialType: Optional[str] = None
    sourceType: Optional[str] = None
    transitionDetails: Optional[TransitionDetails] = None
    liveDetails: Optional[LiveDetails] = None
    mammediaid: Optional[str] = None
    carrierid: Optional[str] = None
    aggregatedDetails: Optional[AggregatedDetails] = None


class Level3Payload(BaseModel):
    type: str
    timeDetails: TimeDetailsOffsetRequired
    materialId: str
    layer: int
    inTransitionDetails: InTransitionDetails
    outTransitionDetails: OutTransitionDetails


class ItemLevel3(BaseModel):
    id: str
    name: str
    payload: Level3Payload
    alternatives: List
    recorderStates: List
    version: int
    items: List


class ItemLevel2(BaseModel):
    id: str
    name: str
    payload: Level2Payload
    alternatives: List
    recorderStates: List
    version: int
    items: List[ItemLevel3]


class ItemLevel1(BaseModel):
    id: str
    name: str
    payload: Level1Payload
    alternatives: List
    recorderStates: List
    version: int
    items: List[ItemLevel2]


class GenericContainer(BaseModel):
    id: str
    name: str
    payload: Payload
    alternatives: List
    recorderStates: List
    version: int
    items: List[ItemLevel1]


class Schedule(BaseModel):
    id: str
    name: str
    items: List[GenericContainer]
