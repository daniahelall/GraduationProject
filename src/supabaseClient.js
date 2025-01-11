// src/supabaseClient.js
import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = 'https://nugmsadjxlyswwkstglm.supabase.co'; // Replace with your Supabase project URL
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51Z21zYWRqeGx5c3d3a3N0Z2xtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI3OTg0MzMsImV4cCI6MjA0ODM3NDQzM30.SHsTETPKSceVgp8_9eI4psOnKqym-uVULa1HEvY2N8M'; // Replace with your anon key

export const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);
