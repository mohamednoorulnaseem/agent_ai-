"""
Analytics engine for tracking and analyzing agent performance.
Provides insights and metrics for optimization.
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
from collections import defaultdict
import statistics


class Analytics:
    """Tracks and analyzes agent performance metrics."""
    
    def __init__(self, db_manager=None):
        self.db = db_manager
        self.metrics = defaultdict(list)
    
    def record_execution(self, task_id: int, duration: float, success: bool, result_length: int = 0):
        """Record task execution metrics."""
        self.metrics[f"task_{task_id}"].append({
            "timestamp": datetime.now().isoformat(),
            "duration": duration,
            "success": success,
            "result_length": result_length
        })
    
    def get_execution_stats(self, task_id: int) -> Dict[str, Any]:
        """Get statistics for a specific task."""
        executions = self.metrics.get(f"task_{task_id}", [])
        
        if not executions:
            return {"error": "No executions found"}
        
        durations = [e["duration"] for e in executions]
        successes = sum(1 for e in executions if e["success"])
        
        return {
            "total_executions": len(executions),
            "successful": successes,
            "failed": len(executions) - successes,
            "success_rate": (successes / len(executions)) * 100,
            "avg_duration": statistics.mean(durations),
            "min_duration": min(durations),
            "max_duration": max(durations),
            "std_dev": statistics.stdev(durations) if len(durations) > 1 else 0
        }
    
    def get_plan_analytics(self, plan_id: int) -> Dict[str, Any]:
        """Get analytics for a complete plan."""
        if not self.db:
            return {"error": "Database not available"}
        
        plan = self.db.get_plan(plan_id)
        if not plan:
            return {"error": "Plan not found"}
        
        tasks = self.db.get_plan_tasks(plan_id)
        stats = self.db.get_plan_statistics(plan_id)
        
        total_tasks = len(tasks)
        completed_tasks = sum(1 for t in tasks if t["completed"])
        
        durations = []
        for task in tasks:
            if task.get("result"):
                # Estimate from result
                durations.append(len(task.get("result", "")) / 100)  # Rough estimate
        
        return {
            "plan_id": plan_id,
            "goal": plan.get("goal"),
            "created_at": plan.get("created_at"),
            "status": plan.get("status"),
            "progress": {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "completion_percentage": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            },
            "execution": {
                "total_executions": stats.get("total_executions", 0),
                "avg_execution_time": statistics.mean(durations) if durations else 0
            }
        }
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get overall system metrics."""
        return {
            "timestamp": datetime.now().isoformat(),
            "total_metrics_tracked": len(self.metrics),
            "active_sessions": self._count_active_sessions()
        }
    
    def _count_active_sessions(self) -> int:
        """Count active sessions."""
        # This would typically query from database or session manager
        return 0
    
    def get_trending_tasks(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get trending tasks based on execution count."""
        task_counts = defaultdict(int)
        
        for metric_key, executions in self.metrics.items():
            if metric_key.startswith("task_"):
                task_id = metric_key.replace("task_", "")
                task_counts[task_id] = len(executions)
        
        trending = sorted(task_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
        return [
            {"task_id": int(task_id), "execution_count": count}
            for task_id, count in trending
        ]
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate a comprehensive performance report."""
        total_metrics = len(self.metrics)
        
        if total_metrics == 0:
            return {"status": "No data available"}
        
        all_durations = []
        total_successes = 0
        total_executions = 0
        
        for executions in self.metrics.values():
            for execution in executions:
                all_durations.append(execution["duration"])
                if execution["success"]:
                    total_successes += 1
                total_executions += 1
        
        return {
            "summary": {
                "total_tasks_tracked": total_metrics,
                "total_executions": total_executions,
                "successful_executions": total_successes,
                "failed_executions": total_executions - total_successes,
                "success_rate": (total_successes / total_executions * 100) if total_executions > 0 else 0
            },
            "performance": {
                "avg_execution_time": statistics.mean(all_durations) if all_durations else 0,
                "min_execution_time": min(all_durations) if all_durations else 0,
                "max_execution_time": max(all_durations) if all_durations else 0,
                "std_dev": statistics.stdev(all_durations) if len(all_durations) > 1 else 0
            },
            "generated_at": datetime.now().isoformat()
        }


class MetricsCollector:
    """Collects and aggregates metrics over time."""
    
    def __init__(self):
        self.hourly_metrics = defaultdict(dict)
        self.daily_metrics = defaultdict(dict)
    
    def record_hourly_metric(self, metric_name: str, value: float):
        """Record an hourly metric."""
        now = datetime.now()
        hour_key = now.strftime("%Y-%m-%d %H:00")
        
        if metric_name not in self.hourly_metrics[hour_key]:
            self.hourly_metrics[hour_key][metric_name] = []
        
        self.hourly_metrics[hour_key][metric_name].append(value)
    
    def record_daily_metric(self, metric_name: str, value: float):
        """Record a daily metric."""
        now = datetime.now()
        day_key = now.strftime("%Y-%m-%d")
        
        if metric_name not in self.daily_metrics[day_key]:
            self.daily_metrics[day_key][metric_name] = []
        
        self.daily_metrics[day_key][metric_name].append(value)
    
    def get_hourly_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get hourly metrics summary for the last N hours."""
        summary = {}
        now = datetime.now()
        
        for i in range(hours):
            hour = now - timedelta(hours=i)
            hour_key = hour.strftime("%Y-%m-%d %H:00")
            
            if hour_key in self.hourly_metrics:
                summary[hour_key] = {}
                for metric, values in self.hourly_metrics[hour_key].items():
                    summary[hour_key][metric] = {
                        "avg": statistics.mean(values),
                        "min": min(values),
                        "max": max(values),
                        "count": len(values)
                    }
        
        return summary
    
    def get_daily_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get daily metrics summary for the last N days."""
        summary = {}
        now = datetime.now()
        
        for i in range(days):
            day = now - timedelta(days=i)
            day_key = day.strftime("%Y-%m-%d")
            
            if day_key in self.daily_metrics:
                summary[day_key] = {}
                for metric, values in self.daily_metrics[day_key].items():
                    summary[day_key][metric] = {
                        "avg": statistics.mean(values),
                        "min": min(values),
                        "max": max(values),
                        "count": len(values)
                    }
        
        return summary


# Global analytics instance
analytics = Analytics()
metrics_collector = MetricsCollector()
