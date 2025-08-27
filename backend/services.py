from typing import List, Optional, Tuple
from urllib.parse import urlparse
import time
from .database import db
from .models import HistoryItem, HistoryFilters, StatsOverview

class HistoryService:
    top_sites_count: int = 6

    @staticmethod
    def parse_time_range(time_range: str) -> Tuple[Optional[int], Optional[int]]:
        """解析时间范围参数"""
        if not time_range or time_range == 'all':
            return None, None
        
        if '-' in time_range and time_range.count('-') == 1:
            # 自定义范围 "start_ts-end_ts"
            try:
                start_str, end_str = time_range.split('-')
                return int(start_str), int(end_str)
            except ValueError:
                return None, None
        
        # 预设范围
        current_time = int(time.time())
        if time_range == '1d':
            return current_time - 86400, current_time
        elif time_range == '7d':
            return current_time - 604800, current_time
        elif time_range == '30d':
            return current_time - 2592000, current_time
        elif time_range == '90d':
            return current_time - 7776000, current_time
        
        return None, None
    
    @staticmethod
    def build_where_clause(filters: HistoryFilters) -> Tuple[str, List]:
        """构建WHERE子句和参数"""
        conditions = []
        params = []
        
        # 关键词搜索
        if filters.keyword:
            conditions.append("(title LIKE ? OR url LIKE ?)")
            keyword_pattern = f"%{filters.keyword}%"
            params.extend([keyword_pattern, keyword_pattern])
        
        # 语言区域
        if filters.locale:
            conditions.append("locale = ?")
            params.append(filters.locale)
        
        # 时间范围
        if filters.time_range:
            start_time, end_time = HistoryService.parse_time_range(filters.time_range)
            if start_time is not None and end_time is not None:
                conditions.append("last_visited_time BETWEEN ? AND ?")
                params.extend([start_time, end_time])
        
        where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
        return where_clause, params
    
    @staticmethod
    def list_history(page: int, page_size: int, filters: HistoryFilters) -> dict:
        """获取历史记录列表"""
        # 构建WHERE子句
        where_clause, params = HistoryService.build_where_clause(filters)
        
        # 构建ORDER BY子句
        valid_sort_fields = ['title', 'last_visited_time', 'num_visits']
        sort_by = filters.sort_by if filters.sort_by in valid_sort_fields else 'last_visited_time'
        sort_order = 'DESC' if filters.sort_order == 'desc' else 'ASC'
        order_clause = f" ORDER BY {sort_by} {sort_order}"
        
        # 计算总数
        count_query = f"SELECT COUNT(*) as total FROM navigation_history{where_clause}"
        total_result = db.execute_query(count_query, tuple(params))
        total = total_result[0]['total'] if total_result else 0
        
        # 获取分页数据
        offset = (page - 1) * page_size
        data_query = f"""
            SELECT url, title, last_visited_time, num_visits, locale 
            FROM navigation_history
            {where_clause}
            {order_clause}
            LIMIT ? OFFSET ?
        """
        
        # 添加分页参数
        params.extend([page_size, offset])
        rows = db.execute_query(data_query, tuple(params))
        
        # 转换为模型
        items = [
            HistoryItem(
                url=row['url'],
                title=row['title'],
                last_visited_time=row['last_visited_time'],
                num_visits=row['num_visits'],
                locale=row['locale']
            )
            for row in rows
        ]
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'page_size': page_size
        }
    
    @staticmethod
    def extract_domain(url: str) -> str:
        """从URL提取域名"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            # 移除 www. 前缀
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        except Exception:
            return url
    
    @staticmethod
    def get_stats_overview(time_range: str = '7d') -> StatsOverview:
        """获取统计概览"""
        # 构建时间过滤器
        filters = HistoryFilters(time_range=time_range)
        where_clause, params = HistoryService.build_where_clause(filters)
        
        # 总访问次数
        total_visits_query = f"SELECT COALESCE(SUM(num_visits), 0) as total_visits FROM navigation_history{where_clause}"
        total_visits_result = db.execute_query(total_visits_query, tuple(params))
        total_visits = total_visits_result[0]['total_visits'] if total_visits_result else 0
        
        # 不同站点数
        distinct_sites_query = f"SELECT COUNT(DISTINCT url) as distinct_sites FROM navigation_history{where_clause}"
        distinct_sites_result = db.execute_query(distinct_sites_query, tuple(params))
        distinct_sites = distinct_sites_result[0]['distinct_sites'] if distinct_sites_result else 0
        
        # TOP站点 - 先提取域名聚合后再排序
        top_sites_query = f"""
            SELECT 
                CASE 
                    WHEN url LIKE 'http://%' THEN 
                        CASE 
                            WHEN instr(substr(url, 8), '/') > 0 
                            THEN substr(url, 8, instr(substr(url, 8), '/') - 1)
                            ELSE substr(url, 8)
                        END
                    WHEN url LIKE 'https://%' THEN 
                        CASE 
                            WHEN instr(substr(url, 9), '/') > 0 
                            THEN substr(url, 9, instr(substr(url, 9), '/') - 1)
                            ELSE substr(url, 9)
                        END
                    ELSE url
                END as site_name,
                SUM(num_visits) as total_visits 
            FROM navigation_history 
            {where_clause} 
            GROUP BY site_name 
            ORDER BY total_visits DESC 
            LIMIT {HistoryService.top_sites_count}
        """
        top_sites_result = db.execute_query(top_sites_query, tuple(params))
        
        # 提取站点名称列表
        top_entities = [row['site_name'] for row in top_sites_result]

        return StatsOverview(
            total_visits=total_visits,
            distinct_sites=distinct_sites,
            top_entities=top_entities
        )
