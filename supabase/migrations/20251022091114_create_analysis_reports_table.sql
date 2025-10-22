/*
  # Create Analysis Reports Table

  1. New Tables
    - `analysis_reports`
      - `id` (uuid, primary key)
      - `user_id` (uuid, optional - for future auth integration)
      - `age` (integer) - Predicted age
      - `gender` (text) - Predicted gender
      - `fatigue` (text) - Fatigue status
      - `emotion` (text) - Detected emotion
      - `symmetry_score` (real) - Facial asymmetry score
      - `symmetry_condition` (text) - Symmetry analysis result
      - `skin_condition` (text, nullable) - Detected skin condition
      - `health_index_score` (real) - Overall health index (0-100)
      - `health_index_rating` (text) - Health index rating (Excellent, Good, etc.)
      - `recommendations` (jsonb) - Array of recommendation strings
      - `confidence_scores` (jsonb) - Confidence scores for each analysis
      - `created_at` (timestamptz) - Report creation timestamp

  2. Security
    - Enable RLS on `analysis_reports` table
    - Add policy for anyone to insert reports (for now, before auth is added)
    - Add policy for users to read their own reports (prepared for future auth)
*/

CREATE TABLE IF NOT EXISTS analysis_reports (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid,
  age integer NOT NULL DEFAULT 0,
  gender text NOT NULL DEFAULT 'Unknown',
  fatigue text NOT NULL DEFAULT 'Unknown',
  emotion text NOT NULL DEFAULT 'Neutral',
  symmetry_score real NOT NULL DEFAULT 0.0,
  symmetry_condition text NOT NULL DEFAULT 'Unknown',
  skin_condition text,
  health_index_score real NOT NULL DEFAULT 0.0,
  health_index_rating text NOT NULL DEFAULT 'Fair',
  recommendations jsonb DEFAULT '[]'::jsonb,
  confidence_scores jsonb DEFAULT '{}'::jsonb,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE analysis_reports ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow anyone to insert reports"
  ON analysis_reports
  FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

CREATE POLICY "Users can read all reports for now"
  ON analysis_reports
  FOR SELECT
  TO anon, authenticated
  USING (true);

CREATE INDEX IF NOT EXISTS idx_analysis_reports_created_at 
  ON analysis_reports(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_analysis_reports_user_id 
  ON analysis_reports(user_id) 
  WHERE user_id IS NOT NULL;
