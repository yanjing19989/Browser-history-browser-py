from pydantic import BaseModel
from typing import Optional, List

class HistoryItem(BaseModel):
    url: str
    title: Optional[str] = None
    last_visited_time: int
    num_visits: int = 0
    locale: Optional[str] = None

class HistoryFilters(BaseModel):
    keyword: Optional[str] = None
    locale: Optional[str] = None
    time_range: Optional[str] = None
    sort_by: Optional[str] = "last_visited_time"
    sort_order: Optional[str] = "desc"

class HistoryResponse(BaseModel):
    items: List[HistoryItem]
    total: int
    page: int
    page_size: int

class StatsOverview(BaseModel):
    total_visits: int
    distinct_sites: int
    top_entities: List[str]

class ConfigModel(BaseModel):
    db_path: Optional[str] = None
    top_sites_count: Optional[int] = 6
    browser_db_path: Optional[str] = None
