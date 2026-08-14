/**
 * Hand-written Supabase schema types — mirrors supabase/migrations/0001_init.sql
 * exactly. If you change the SQL, change this file in the same commit.
 */

export type ContactStatus =
  | 'pending'
  | 'calling'
  | 'called'
  | 'booked'
  | 'declined'
  | 'opted_out'
  | 'suppressed'
  | 'invalid'
  | 'no_answer'
  | 'failed';

export type CallOutcome =
  | 'dialing'
  | 'answered'
  | 'booked'
  | 'declined'
  | 'no_answer'
  | 'voicemail'
  | 'busy'
  | 'failed'
  | 'opted_out';

export type Vertical = 'salon' | 'medspa';

/** trialing | active | past_due | canceled — kept as string: Stripe adds states. */
export type StripeStatus = string;

/** opt_out | dnc | complaint | invalid | manual */
export type SuppressionReason = string;

export type Database = {
  public: {
    Tables: {
      clients: {
        Row: {
          id: string;
          name: string;
          contact_name: string | null;
          contact_email: string;
          contact_phone: string | null;
          offer_text: string;
          timezone: string;
          vertical: Vertical;
          avg_ticket_cents: number;
          stripe_status: StripeStatus;
          stripe_customer_id: string | null;
          booking_phone: string | null;
          active: boolean;
          created_at: string;
        };
        Insert: {
          id?: string;
          name: string;
          contact_name?: string | null;
          contact_email: string;
          contact_phone?: string | null;
          offer_text: string;
          timezone?: string;
          vertical?: Vertical;
          avg_ticket_cents?: number;
          stripe_status?: StripeStatus;
          stripe_customer_id?: string | null;
          booking_phone?: string | null;
          active?: boolean;
          created_at?: string;
        };
        Update: {
          id?: string;
          name?: string;
          contact_name?: string | null;
          contact_email?: string;
          contact_phone?: string | null;
          offer_text?: string;
          timezone?: string;
          vertical?: Vertical;
          avg_ticket_cents?: number;
          stripe_status?: StripeStatus;
          stripe_customer_id?: string | null;
          booking_phone?: string | null;
          active?: boolean;
          created_at?: string;
        };
        Relationships: [];
      };
      contacts: {
        Row: {
          id: string;
          client_id: string;
          campaign: string;
          name: string | null;
          first_name: string | null;
          phone: string | null;
          phone_raw: string | null;
          email: string | null;
          consent: boolean;
          last_visit: string | null;
          lifetime_value_cents: number | null;
          status: ContactStatus;
          scrub_reason: string | null;
          attempts: number;
          claimed_at: string | null;
          created_at: string;
        };
        Insert: {
          id?: string;
          client_id: string;
          campaign?: string;
          name?: string | null;
          first_name?: string | null;
          phone?: string | null;
          phone_raw?: string | null;
          email?: string | null;
          consent?: boolean;
          last_visit?: string | null;
          lifetime_value_cents?: number | null;
          status?: ContactStatus;
          scrub_reason?: string | null;
          attempts?: number;
          claimed_at?: string | null;
          created_at?: string;
        };
        Update: {
          id?: string;
          client_id?: string;
          campaign?: string;
          name?: string | null;
          first_name?: string | null;
          phone?: string | null;
          phone_raw?: string | null;
          email?: string | null;
          consent?: boolean;
          last_visit?: string | null;
          lifetime_value_cents?: number | null;
          status?: ContactStatus;
          scrub_reason?: string | null;
          attempts?: number;
          claimed_at?: string | null;
          created_at?: string;
        };
        Relationships: [
          {
            foreignKeyName: 'contacts_client_id_fkey';
            columns: ['client_id'];
            isOneToOne: false;
            referencedRelation: 'clients';
            referencedColumns: ['id'];
          },
        ];
      };
      calls: {
        Row: {
          id: string;
          contact_id: string | null;
          client_id: string | null;
          vapi_call_id: string | null;
          outcome: CallOutcome;
          duration_seconds: number | null;
          cost_usd: number | null;
          transcript_url: string | null;
          recording_url: string | null;
          summary: string | null;
          ended_reason: string | null;
          started_at: string | null;
          ended_at: string | null;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          contact_id?: string | null;
          client_id?: string | null;
          vapi_call_id?: string | null;
          outcome?: CallOutcome;
          duration_seconds?: number | null;
          cost_usd?: number | null;
          transcript_url?: string | null;
          recording_url?: string | null;
          summary?: string | null;
          ended_reason?: string | null;
          started_at?: string | null;
          ended_at?: string | null;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          contact_id?: string | null;
          client_id?: string | null;
          vapi_call_id?: string | null;
          outcome?: CallOutcome;
          duration_seconds?: number | null;
          cost_usd?: number | null;
          transcript_url?: string | null;
          recording_url?: string | null;
          summary?: string | null;
          ended_reason?: string | null;
          started_at?: string | null;
          ended_at?: string | null;
          created_at?: string;
          updated_at?: string;
        };
        Relationships: [
          {
            foreignKeyName: 'calls_contact_id_fkey';
            columns: ['contact_id'];
            isOneToOne: false;
            referencedRelation: 'contacts';
            referencedColumns: ['id'];
          },
          {
            foreignKeyName: 'calls_client_id_fkey';
            columns: ['client_id'];
            isOneToOne: false;
            referencedRelation: 'clients';
            referencedColumns: ['id'];
          },
        ];
      };
      suppression: {
        Row: {
          id: string;
          phone: string;
          reason: SuppressionReason;
          source_contact_id: string | null;
          created_at: string;
        };
        Insert: {
          id?: string;
          phone: string;
          reason: SuppressionReason;
          source_contact_id?: string | null;
          created_at?: string;
        };
        Update: {
          id?: string;
          phone?: string;
          reason?: SuppressionReason;
          source_contact_id?: string | null;
          created_at?: string;
        };
        Relationships: [];
      };
      bookings: {
        Row: {
          id: string;
          contact_id: string | null;
          client_id: string | null;
          call_id: string | null;
          slot_text: string;
          confirmed: boolean;
          notified_at: string | null;
          estimated_value_cents: number | null;
          created_at: string;
        };
        Insert: {
          id?: string;
          contact_id?: string | null;
          client_id?: string | null;
          call_id?: string | null;
          slot_text: string;
          confirmed?: boolean;
          notified_at?: string | null;
          estimated_value_cents?: number | null;
          created_at?: string;
        };
        Update: {
          id?: string;
          contact_id?: string | null;
          client_id?: string | null;
          call_id?: string | null;
          slot_text?: string;
          confirmed?: boolean;
          notified_at?: string | null;
          estimated_value_cents?: number | null;
          created_at?: string;
        };
        Relationships: [
          {
            foreignKeyName: 'bookings_contact_id_fkey';
            columns: ['contact_id'];
            isOneToOne: false;
            referencedRelation: 'contacts';
            referencedColumns: ['id'];
          },
          {
            foreignKeyName: 'bookings_client_id_fkey';
            columns: ['client_id'];
            isOneToOne: false;
            referencedRelation: 'clients';
            referencedColumns: ['id'];
          },
          {
            foreignKeyName: 'bookings_call_id_fkey';
            columns: ['call_id'];
            isOneToOne: false;
            referencedRelation: 'calls';
            referencedColumns: ['id'];
          },
        ];
      };
    };
    Views: { [_ in never]: never };
    Functions: {
      /** The claim query. Returns the rows it just moved to status='calling'. */
      claim_contacts_for_dialing: {
        Args: { p_limit: number; p_window_start: string; p_window_end: string };
        Returns: Database['public']['Tables']['contacts']['Row'][];
      };
      /**
       * Sweeps contacts stranded in 'calling' and calls stranded in 'dialing' to
       * 'failed'. Returns the total rows swept (contacts + calls).
       */
      expire_stuck_calling: {
        Args: { p_older_than_minutes: number };
        Returns: number;
      };
    };
    Enums: { [_ in never]: never };
    CompositeTypes: { [_ in never]: never };
  };
};

export type Client = Database['public']['Tables']['clients']['Row'];
export type ClientInsert = Database['public']['Tables']['clients']['Insert'];
export type ClientUpdate = Database['public']['Tables']['clients']['Update'];

export type Contact = Database['public']['Tables']['contacts']['Row'];
export type ContactInsert = Database['public']['Tables']['contacts']['Insert'];
export type ContactUpdate = Database['public']['Tables']['contacts']['Update'];

export type Call = Database['public']['Tables']['calls']['Row'];
export type CallInsert = Database['public']['Tables']['calls']['Insert'];
export type CallUpdate = Database['public']['Tables']['calls']['Update'];

export type Suppression = Database['public']['Tables']['suppression']['Row'];
export type SuppressionInsert = Database['public']['Tables']['suppression']['Insert'];

export type Booking = Database['public']['Tables']['bookings']['Row'];
export type BookingInsert = Database['public']['Tables']['bookings']['Insert'];
export type BookingUpdate = Database['public']['Tables']['bookings']['Update'];
