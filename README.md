# ATS Analyzer

AI-powered CV scoring tool for job seekers. Upload your CV, paste a job offer, and get an ATS compatibility score with missing keywords, section analysis, and rewrite suggestions.

## Features

- **ATS Score** — 0–100 compatibility score between your CV and a job offer
- **Keyword Analysis** — matched and missing keywords ranked by importance
- **Section Breakdown** — scores for experience, skills, education, and formatting
- **Rewrite Suggestions** — before/after sentence improvements
- **Seniority Match** — checks if your experience level fits the role
- **Quota System** — 3 free lifetime analyses, Pro (50/month), Expert (unlimited)
- **i18n** — French and English, auto-detected from browser
- **Auth** — email/password via Supabase, email confirmation

## Stack

| Layer | Tool |
|---|---|
| Framework | Nuxt 4 + TypeScript |
| UI | Nuxt UI v4 (Radix Vue + Tailwind CSS) |
| Auth & DB | Supabase (PostgreSQL + RLS) |
| Storage | Supabase Storage |
| AI | HuggingFace Inference API (Mistral-7B) |
| Payments | Stripe Checkout + Webhooks |
| Emails | Resend |
| i18n | @nuxtjs/i18n v9 |

## Project Structure

```
ats-analyzer/
├── app/
│   ├── components/
│   │   ├── analysis/       # Score display, keywords, section cards
│   │   ├── cv/             # CV uploader, CV card, CV list
│   │   ├── layout/         # AppSidebar, AppHeader
│   │   └── onboarding/     # Onboarding wizard steps
│   ├── composables/
│   │   ├── useAnalysis.ts  # Analysis CRUD + polling
│   │   ├── useCV.ts        # CV upload + management
│   │   └── useQuota.ts     # Quota display
│   ├── middleware/
│   │   ├── auth.ts         # Redirect unauthenticated users
│   │   ├── onboarding.ts   # Redirect to onboarding if not completed
│   │   └── admin.ts        # Restrict admin routes
│   ├── pages/
│   │   ├── index.vue       # Landing page
│   │   ├── login.vue
│   │   ├── register.vue
│   │   ├── confirm.vue     # Email confirmation + welcome email
│   │   ├── onboarding.vue
│   │   ├── dashboard.vue
│   │   ├── cvs/index.vue
│   │   ├── analyses/
│   │   │   ├── index.vue   # Analysis history
│   │   │   ├── new.vue     # New analysis form
│   │   │   └── [id].vue    # Analysis result
│   │   ├── pricing.vue
│   │   ├── settings/
│   │   │   ├── index.vue   # Profile settings
│   │   │   └── billing.vue
│   │   └── admin/
│   │       └── stats.vue   # Acquisition & growth stats
│   └── layouts/
│       └── default.vue     # Sidebar + header layout
├── server/
│   ├── api/
│   │   ├── analysis/       # create, [id].get
│   │   ├── cv/             # upload, list, [id].delete, [id].patch
│   │   ├── user/           # quota.get
│   │   ├── auth/           # send-welcome, delete-account
│   │   ├── stripe/         # create-checkout, webhook, portal
│   │   └── admin/          # stats.get, check.get
│   ├── middleware/
│   │   └── rate-limit.ts   # In-memory rate limiting
│   └── utils/
│       ├── supabase.ts     # Service-role Supabase client
│       ├── stripe.ts       # Stripe client + price ID helper
│       ├── huggingface.ts  # HuggingFace inference + timeout
│       ├── ats-prompt.ts   # Prompt builder + Zod result schema
│       ├── quota.ts        # checkQuota / consumeQuota / refundQuota
│       └── email.ts        # Welcome + quota warning emails
├── i18n/
│   └── locales/
│       ├── fr.json
│       └── en.json
└── supabase/
    └── migrations/
        ├── 001_initial_schema.sql
        ├── 002_welcome_email_flag.sql
        ├── 003_referral_source.sql
        ├── 004_locale.sql
        ├── 005_fix_profiles_rls.sql
        ├── 006_decrement_quota_fn.sql
        └── 007_add_indexes.sql
```

## Setup

### Prerequisites

- Node.js 20+
- A [Supabase](https://supabase.com) project
- A [Stripe](https://stripe.com) account (test mode for dev)
- A [HuggingFace](https://huggingface.co) account with Inference API access
- A [Resend](https://resend.com) account

### Environment variables

Copy `.env.example` and fill in your values:

```bash
cp .env.example .env
```

```env
# Supabase
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=eyJ...
SUPABASE_SERVICE_KEY=eyJ...

# HuggingFace
HUGGINGFACE_API_KEY=hf_...

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
NUXT_PUBLIC_STRIPE_PRICE_PRO_MONTHLY=price_...
NUXT_PUBLIC_STRIPE_PRICE_EXPERT_MONTHLY=price_...

# Resend
RESEND_API_KEY=re_...

# App
NUXT_PUBLIC_APP_URL=http://localhost:3000
ADMIN_EMAIL=your@email.com
```

### Database

Run migrations in order in the Supabase SQL editor:

```
supabase/migrations/001_initial_schema.sql
supabase/migrations/002_welcome_email_flag.sql
supabase/migrations/003_referral_source.sql
supabase/migrations/004_locale.sql
supabase/migrations/005_fix_profiles_rls.sql
supabase/migrations/006_decrement_quota_fn.sql
supabase/migrations/007_add_indexes.sql
```

### Install & run

```bash
npm install
npm run dev
```

### Stripe webhooks (local dev)

```bash
stripe listen --forward-to localhost:3000/api/stripe/webhook
```

Copy the `whsec_...` secret into `.env` as `STRIPE_WEBHOOK_SECRET`.

## Plans

| Plan | Analyses | Price |
|---|---|---|
| Free | 3 lifetime | €0 |
| Pro | 50 / month | €9.99/mo |
| Expert | Unlimited | €24.99/mo |

## Branch strategy

```
main   — stable, production-ready
dev    — active development
```

Open PRs from `dev` to `main`.

## License

MIT
