-- Remove calories column from activity table
ALTER TABLE public.activity DROP COLUMN IF EXISTS calories;
