-- Schema for High-Volume Scheduling Records

CREATE TABLE IF NOT EXISTS rooms (
    room_id VARCHAR(50) PRIMARY KEY,
    building_name VARCHAR(100) NOT NULL,
    max_capacity INT NOT NULL
);

CREATE TABLE IF NOT EXISTS schedule_records (
    record_id SERIAL PRIMARY KEY,
    room_id VARCHAR(50) REFERENCES rooms(room_id),
    course_code VARCHAR(20) NOT NULL,
    enrollment_count INT NOT NULL,
    day_of_week INT, -- 1 (Monday) to 5 (Friday)
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    semester VARCHAR(10) NOT NULL
);

-- Crucial indexes to allow quick scanning over 100,000+ data rows
CREATE INDEX IF NOT EXISTS idx_schedule_room_semester ON schedule_records(room_id, semester);
CREATE INDEX IF NOT EXISTS idx_utilization_metrics ON schedule_records(day_of_week, start_time, enrollment_count);
