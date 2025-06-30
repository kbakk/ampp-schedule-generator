from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


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


class TransitionDetails(BaseModel):
    type: str
    duration: Optional[str] = None


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


# Flexible payload that can handle any payload type with any combination of fields
class FlexiblePayload(BaseModel):
    type: str
    # Container fields
    timeDetails: Optional[
        Union[TimeDetailsNotional, TimeDetailsSimple, TimeDetailsWithOffset]
    ] = None
    # Live/Media fields
    productcode: Optional[str] = None
    materialId: Optional[str] = None
    materialType: Optional[str] = None
    sourceType: Optional[str] = None
    transitionDetails: Optional[TransitionDetails] = None
    liveDetails: Optional[LiveDetails] = None
    recording: Optional[Recording] = None
    notes: Optional[str] = None
    # Layer fields
    layer: Optional[int] = None
    inTransitionDetails: Optional[TransitionDetails] = None
    outTransitionDetails: Optional[TransitionDetails] = None
    mammediaid: Optional[str] = None
    carrierid: Optional[str] = None
    aggregatedDetails: Optional[AggregatedDetails] = None
    # Offset fields
    offset: Optional[str] = None
    endTimeMode: Optional[str] = None
    fluidDuration: Optional[bool] = None
    inPoint: Optional[str] = None
    startTime: Optional[str] = None
    duration: Optional[str] = None
    externalTriggerWindow: Optional[Dict[str, Any]] = None
    notionalStartTime: Optional[str] = None


# Single flexible item that can contain any other items
class FlexibleItem(BaseModel):
    id: str
    name: str
    payload: FlexiblePayload
    alternatives: List
    recorderStates: List
    version: int
    items: List["FlexibleItem"]


class Schedule(BaseModel):
    id: str
    name: str
    items: List[FlexibleItem]
