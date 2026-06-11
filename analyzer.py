import pandas as pd
import numpy as np
import sqlite3
import json
import sys

def compute_utilization_metrics(db_path):
    """
    Ingests scheduling rows, evaluates utilization metrics via Pandas,
    and returns a structured JSON string containing capacity insights.
    """
    # Establish connection with the analytical database
    conn = sqlite3.connect(db_path)
    
    # Read the 100,000+ records using highly optimized vector operations
    query = """
        SELECT r.room_id, r.building_name, r.max_capacity, 
               s.course_code, s.enrollment_count, s.day_of_week, s.start_time
        FROM schedule_records s
        JOIN rooms r ON s.room_id = r.room_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        return json.dumps({"error": "No data source records found."})

    # Metric 1: Calculate the exact seat fill ratio for every scheduled class
    df['seat_fill_ratio'] = (df['enrollment_count'] / df['max_capacity']) * 100

    # Metric 2: Isolate critical bottlenecks (Rooms overloaded beyond capacity bounds)
    overloaded_df = df[df['seat_fill_ratio'] > 100]
    total_overloaded = int(overloaded_df.shape[0])

    # Metric 3: Group by rooms to determine the overall worst/best spaces
    room_summary = df.groupby('room_id').agg(
        building=('building_name', 'first'),
        average_fill=('seat_fill_ratio', 'mean'),
        total_classes=('course_code', 'count')
    ).reset_index()

    # Metric 4: Pinpoint operational "dead zones" (under-utilized rooms with < 30% fill ratios)
    under_utilized = room_summary[room_summary['average_fill'] < 30.0]['room_id'].tolist()

    # Consolidate results into a production-ready payload
    insights = {
        "metadata": {
            "total_records_analyzed": len(df),
            "unique_rooms_tracked": len(room_summary)
        },
        "kpis": {
            "average_system_seat_fill_percentage": round(df['seat_fill_ratio'].mean(), 2),
            "total_overloaded_incidents": total_overloaded
        },
        "critical_alerts": {
            "under_utilized_room_ids": under_utilized,
            "top_3_congested_rooms": room_summary.nlargest(3, 'average_fill')['room_id'].tolist()
        }
    }
    
    return json.dumps(insights, indent=2)

if __name__ == "__main__":
    # Expecting the database path as a CLI argument for flexible system execution
    db_name = sys.argv[1] if len(sys.argv) > 1 else "scheduling.db"
    
    try:
        results_json = compute_utilization_metrics(db_name)
        print(results_json)
    except Exception as e:
        print(json.dumps({"status": "failed", "error": str(e)}))
