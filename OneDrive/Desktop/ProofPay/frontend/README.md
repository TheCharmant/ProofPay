# ProofPay Frontend

Modern, minimal web interface for the ProofPay job marketplace.

## 📦 Tech Stack

- **Next.js 14+** - React framework with file-based routing
- **TypeScript** - Type-safe code
- **Tailwind CSS** - Utility-first CSS framework
- **Zustand** - Lightweight state management
- **Stellar SDK** - Blockchain interaction

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Configure environment
# Create .env.local with your contract ID
echo "NEXT_PUBLIC_CONTRACT_ID=your-contract-id" >> .env.local
echo "NEXT_PUBLIC_STELLAR_SERVER=https://soroban-testnet.stellar.org" >> .env.local
echo "NEXT_PUBLIC_NETWORK_PASSPHRASE=Test SDF Network ; September 2015" >> .env.local

# Start development server
npm run dev

# Open http://localhost:3000
```

## 📁 Project Structure

```
frontend/
├── pages/
│   ├── _app.tsx              # App wrapper
│   ├── _document.tsx         # HTML document
│   ├── index.tsx             # Home page
│   ├── login.tsx             # Login page
│   ├── dashboard.tsx         # User dashboard
│   ├── create-job.tsx        # Job creation
│   ├── jobs/
│   │   ├── index.tsx         # Jobs list
│   │   └── [id].tsx          # Job details
│   └── api/
│       └── jobs.ts           # API handler
│
├── components/
│   ├── Header.tsx            # Navigation header
│   ├── JobCard.tsx           # Job listing card
│   ├── JobForm.tsx           # Job creation form
│   └── LoginForm.tsx         # Login form
│
├── lib/
│   └── contract.ts           # Soroban contract integration
│
├── store/
│   └── useAppStore.ts        # Zustand state management
│
├── styles/
│   └── globals.css           # Tailwind globals
│
├── package.json
├── tsconfig.json
├── next.config.js
├── tailwind.config.js
└── postcss.config.js
```

## 🎨 Pages

### Home (`/`)
- Landing page with features overview
- Call-to-action for login/browsing

### Login (`/login`)
- Stellar wallet connection
- Role selection (employer/student)
- Secret key input

### Jobs Browse (`/jobs`)
- List all available jobs
- Filter by status
- Post new job button (employer only)

### Job Details (`/jobs/[id]`)
- Job information and payment amount
- Submit work button (student)
- Release payment button (employer)
- Transaction history

### Dashboard (`/dashboard`)
- User profile info
- My jobs list
- Job statistics
- Quick links

### Create Job (`/create-job`)
- Job ID input
- Student address input
- Payment amount input
- Form validation
- Success confirmation

## 🔧 Components

### Header
Global navigation with:
- Logo and branding
- Navigation links
- User connection status
- Logout button

### JobCard
Job listing component showing:
- Job ID and employer address
- Payment amount
- Job status badge
- View details button

### JobForm
Reusable form for creating jobs with:
- Input validation
- Error handling
- Loading states
- Submit callback

### LoginForm
Wallet connection with:
- Secret key input
- Role selection
- Validation
- Error messages

## 📊 State Management

Using Zustand for global state:

```typescript
const { user, jobs, isLoading, error } = useAppStore()
```

## 🌐 API Integration

### Jobs API
```typescript
GET /api/jobs              // List all jobs
GET /api/jobs/:id          // Get job details
POST /api/jobs             // Create job
PATCH /api/jobs/:id        // Update job
```

## 🔐 Security

- Secret keys handled client-side only
- No sensitive data in localStorage
- Environment variables for contract ID
- URL validation for addresses

## 🎯 Key Features

1. **Responsive Design**
   - Mobile-first approach
   - Works on all screen sizes
   - Touch-friendly buttons

2. **Type Safety**
   - TypeScript throughout
   - Proper error handling
   - Type-safe components

3. **Modern UX**
   - Clean, minimal design
   - Smooth transitions
   - Clear visual hierarchy

4. **Web3 Integration**
   - Stellar SDK integration
   - Transaction handling
   - Event monitoring

## 🚀 Build & Deploy

### Build
```bash
npm run build
```

### Production Start
```bash
npm start
```

### Deploy to Vercel
```bash
vercel deploy
```

## 🧪 Development

### Run with Hot Reload
```bash
npm run dev
```

### Lint Code
```bash
npm run lint
```

## 📝 Environment Variables

```env
# Required
NEXT_PUBLIC_CONTRACT_ID=your-contract-id

# Optional (defaults provided)
NEXT_PUBLIC_STELLAR_SERVER=https://soroban-testnet.stellar.org
NEXT_PUBLIC_NETWORK_PASSPHRASE=Test SDF Network ; September 2015
```

## 🐛 Common Issues

### Content Security Policy Error
Update `next.config.js` with CSP headers if needed.

### CORS Issues
Ensure backend is running and CORS is configured.

### Contract Not Found
Verify `CONTRACT_ID` in `.env.local`.

## 📚 Resources

- [Next.js Documentation](https://nextjs.org)
- [Tailwind CSS](https://tailwindcss.com)
- [Stellar SDK](https://github.com/stellar/py-stellar-base)
- [Zustand](https://github.com/pmndrs/zustand)

---

**Modern Frontend for ProofPay Marketplace**
