#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@pabloPerez
perico33723@gmail.com

"""

from pydantic import BaseModel


class CountPlatformResponse(BaseModel):
    count: int

class ProdPerCountyResponse(BaseModel):
    pais: str
    anio: int
    cantidad: int

class GetContentsResponse(BaseModel):
    rating: str
    content_count: int

class MostCommonActorResponse(BaseModel):
    most_common_actor: str
    count: int