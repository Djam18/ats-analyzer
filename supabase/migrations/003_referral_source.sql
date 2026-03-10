-- Add referral source tracking to profiles
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS referral_source text;

-- Allowed values: 'word_of_mouth', 'linkedin', 'google', 'youtube_blog', 'twitter', 'other'
-- NULL means not yet answered
