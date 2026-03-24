CREATE TABLE public.activity (
    id BIGINT PRIMARY KEY,          -- Strava activity ID
    user_id UUID NOT NULL,          -- FK to your user table
    name TEXT NOT NULL,
    type TEXT NOT NULL,             -- e.g., Run, Ride
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    duration_seconds DOUBLE PRECISION NOT NULL, -- moving time
    distance_meters DOUBLE PRECISION NOT NULL,
    average_speed DOUBLE PRECISION, -- meters/second
    max_speed DOUBLE PRECISION,     -- meters/second
    elevation_gain_meters DOUBLE PRECISION,
    average_heart_rate DOUBLE PRECISION,
    max_heart_rate DOUBLE PRECISION,
    calories DOUBLE PRECISION,
    gps_polyline TEXT,              -- optional, store as encoded polyline or GeoJSON
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users (id)
) TABLESPACE pg_default;

-- Optional: index on user_id for faster queries per user
CREATE INDEX idx_activity_user_id ON activity(user_id);

-- Optional: index on start_date for querying by time ranges
CREATE INDEX idx_activity_start_date ON activity(start_date);

GRANT ALL ON public.activity TO authenticated, service_role;

CREATE TABLE public.kudos (
    id BIGSERIAL PRIMARY KEY,          -- internal unique ID
    activity_id BIGINT NOT NULL,       -- FK to activity table
    giver_id BIGINT NOT NULL,          -- Strava user ID of the person giving kudos
    giver_name TEXT,                   -- Optional: cache their name at time of sync
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(), -- when the kudos was given

    -- Foreign key constraint
    CONSTRAINT fk_activity FOREIGN KEY(activity_id) REFERENCES activity(id)
) TABLESPACE pg_default;

-- Index for querying all kudos on a specific activity
CREATE INDEX idx_kudos_activity_id ON kudos(activity_id);

-- Index for querying kudos given by a specific person
CREATE INDEX idx_kudos_giver_id ON kudos(giver_id);

GRANT ALL ON public.kudos TO authenticated, service_role;

ALTER TABLE public.users
ADD COLUMN last_synced TIMESTAMP WITH TIME ZONE DEFAULT NULL;