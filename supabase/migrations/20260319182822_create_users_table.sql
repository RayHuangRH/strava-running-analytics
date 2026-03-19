create table public.users (
  id uuid not null default gen_random_uuid (),
  name character varying null,
  strava_id bigint not null,
  created_at timestamp with time zone not null default now(),
  profile_url character varying null,
  constraint users_pkey primary key (id),
  constraint users_strava_id_key unique (strava_id)
) TABLESPACE pg_default;

create table public.strava_tokens (
  user_id uuid not null default gen_random_uuid (),
  created_at timestamp with time zone not null default now(),
  access_token character varying null,
  refresh_token character varying null,
  expires_at timestamp with time zone null,
  constraint strava_tokens_pkey primary key (user_id),
  constraint strava_tokens_user_id_fkey foreign KEY (user_id) references users (id)
) TABLESPACE pg_default;