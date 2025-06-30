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


class TransitionDetails(BaseModel):
    type: str


class LiveDetails(BaseModel):
    mediaStatus: str
    mediaStatusReason: str


class RecordDetail(BaseModel):
    sourceType: str
    name: str


class Recording(BaseModel):
    recordDetails: List[RecordDetail]


class Payload1(BaseModel):
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


class TimeDetails2(BaseModel):
    offset: Optional[str] = None
    timeMode: str
    startTime: Optional[str] = None
    duration: Optional[str] = None
    endTimeMode: Optional[str] = None
    fluidDuration: Optional[bool] = None
    inPoint: Optional[str] = None


class InTransitionDetails(BaseModel):
    type: str
    duration: str


class OutTransitionDetails(BaseModel):
    type: str
    duration: str


class TransitionDetails1(BaseModel):
    type: str


class LiveDetails1(BaseModel):
    mediaStatus: str
    mediaStatusReason: str


class AggregatedDetails(BaseModel):
    duration: str
    inPoint: str
    outPoint: str


class Payload2(BaseModel):
    type: str
    timeDetails: TimeDetails2
    materialId: str
    layer: Optional[int] = None
    inTransitionDetails: Optional[InTransitionDetails] = None
    outTransitionDetails: Optional[OutTransitionDetails] = None
    productcode: Optional[str] = None
    materialType: Optional[str] = None
    sourceType: Optional[str] = None
    transitionDetails: Optional[TransitionDetails1] = None
    liveDetails: Optional[LiveDetails1] = None
    mammediaid: Optional[str] = None
    carrierid: Optional[str] = None
    aggregatedDetails: Optional[AggregatedDetails] = None


class TimeDetails3(BaseModel):
    offset: str
    timeMode: str
    duration: Optional[str] = None


class InTransitionDetails1(BaseModel):
    type: str
    duration: str


class OutTransitionDetails1(BaseModel):
    type: str
    duration: str


class Payload3(BaseModel):
    type: str
    timeDetails: TimeDetails3
    materialId: str
    layer: int
    inTransitionDetails: InTransitionDetails1
    outTransitionDetails: OutTransitionDetails1


class ItemLevel3(BaseModel):
    id: str
    name: str
    payload: Payload3
    alternatives: List
    recorderStates: List
    version: int
    items: List


class ItemLevel2(BaseModel):
    id: str
    name: str
    payload: Payload2
    alternatives: List
    recorderStates: List
    version: int
    items: List[ItemLevel3]


class ItemLevel1(BaseModel):
    id: str
    name: str
    payload: Payload1
    alternatives: List
    recorderStates: List
    version: int
    items: List[ItemLevel2]


class Item(BaseModel):
    id: str
    name: str
    payload: Payload
    alternatives: List
    recorderStates: List
    version: int
    items: List[ItemLevel1]


class Model(BaseModel):
    id: str
    name: str
    items: List[Item]
