# ProofPay - Full Stack Job Marketplace on Stellar

ProofPay combines "Proof" (verified work) and "Pay" (secure payment). It literally means **"Verified Work Payment"** - a Soroban-powered student work and payment platform built on Stellar. It helps students and employers securely exchange work and payments with transparency, eliminating the need for manual verification and trust-based transactions.

Instead of relying on informal agreements, delayed payments, or unverified submissions, ProofPay records user identity, job agreements, proof of work, and escrowed payments on-chain.

---

## 🏗️ Full Stack Architecture

```
User Browser
    ↓
Next.js Frontend (React, TypeScript, Tailwind)
    ↓
Express.js Backend API (TypeScript)
    ↓
Stellar Blockchain
    ↓
Soroban Smart Contract (Rust)
```

---

## 🎯 Smart Contract Details

### Stellar Expert Link
https://stellar.expert/explorer/testnet/contract/CB4BTPTBQGDZJOH2Q2TVC2ZBMKB5ZH57IP2PGAL62XKWAM2MVUWN47TS

### Contract Account
GCYVFVPAICIHSLGPFV7TS4DFRHNXRF4U7T2XYEJCDZEY7CSHDAMWZOIV

### Contract ID (Testnet)
CB4BTPTBQGDZJOH2Q2TVC2ZBMKB5ZH57IP2PGAL62XKWAM2MVUWN47TS

### Description
This Soroban smart contract manages job agreements and escrow payments between students and employers on-chain. It ensures that payment is securely held in escrow and only released when valid proof of work is submitted. It enforces role-based permissions so only authorized users can create jobs, submit work, and release payments, while keeping all transactions transparent and verifiable.

### Contract Functions
- `create_job()` - Create new job with locked payment
- `submit_work()` - Mark job as completed 
- `release_payment()` - Release payment to student
- `get_job()` - Retrieve job details

---

## 📁 Project Structure

```
ProofPay/
├── proofpay/                         # Smart Contract (Rust/Soroban)
│   ├── Cargo.toml
│   ├── src/
│   │   ├── lib.rs                    # Main contract code
│   │   └── test.rs                   # Tests
│   └── target/
│
├── frontend/                         # React Frontend (Next.js)
│   ├── pages/                        # Next.js pages
│   │   ├── index.tsx                 # Landing page
│   │   ├── login.tsx                 # Wallet login
│   │   ├── jobs/                     # Job pages
│   │   ├── dashboard.tsx             # User dashboard
│   │   └── create-job.tsx            # Job creation
│   ├── components/                   # React components
│   │   ├── Header.tsx                # Navigation
│   │   ├── JobCard.tsx               # Job listing
│   │   ├── JobForm.tsx               # Forms
│   │   └── LoginForm.tsx
│   ├── lib/                          # Utilities
│   │   └── contract.ts               # Stellar SDK integration
│   ├── store/                        # Zustand state
│   ├── styles/                       # Tailwind CSS
│   ├── package.json
│   └── .env.local                    # Environment config
│
├── backend/                          # Express API Server
│   ├── src/
│   │   ├── server.ts                 # Express app
│   │   ├── routes/                   # API endpoints
│   │   │   ├── jobs.ts
│   │   │   ├── auth.ts
│   │   │   └── contract.ts
│   │   └── utils/                    # Services
│   │       ├── contract.ts
│   │       ├── auth.ts
│   │       └── storage.ts
│   ├── package.json
│   └── .env                          # Environment config
│
└── README.md

---

## 🎨 Tech Stack

### Frontend
- **Next.js 14+** - React framework with file-based routing
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Modern utility-first styling
- **Zustand** - Lightweight state management
- **Stellar SDK** - Blockchain interaction

### Backend  
- **Express.js** - Web framework
- **TypeScript** - Type safety
- **Stellar SDK** - Smart contract interaction
- **CORS** - Cross-origin support

### Smart Contract
- **Rust** - Programming language
- **Soroban SDK** - Stellar smart contracts

### Blockchain
- **Stellar Testnet** - Development network
- **Stellar Mainnet** - Production network (optional upgrade)

---

## 🚀 Full Stack Quick Start

### Prerequisites
- Node.js 18+ and npm/yarn
- Rust and Cargo
- Stellar CLI
- A Stellar testnet account (free)

### 1. Get Stellar Testnet Account

```bash
# Install Stellar CLI (if not already)
npm install -g stellar-cli

# Generate testnet key
stellar keys generate --global my-key --network testnet

# Display your public key
stellar keys address my-key

# Get free testnet lumens at:
# https://labs.stellar.org/tools/test-wallet
```

### 2. Build & Deploy Smart Contract

```bash
cd proofpay

# Build contract
cargo build --target wasm32-unknown-unknown --release

# Deploy to testnet
stellar contract deploy \
  --wasm target/wasm32-unknown-unknown/release/proofpay.wasm \
  --source my-key \
  --network testnet

# Save the CONTRACT_ID from output
```

### 3. Start Backend API

```bash
cd backend

# Install dependencies
npm install

# Create .env file with CONTRACT_ID
echo "CONTRACT_ID=your-deployed-contract-id" > .env

# Start development server
npm run dev

# Backend runs on http://localhost:3001
```

### 4. Start Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local with CONTRACT_ID
echo "NEXT_PUBLIC_CONTRACT_ID=your-deployed-contract-id" > .env.local

# Start development server
npm run dev

# Frontend runs on http://localhost:3000
```

### 5. Use the App

- Open http://localhost:3000
- Login with Stellar testnet key
- Choose role: Employer or Student
- Create jobs or browse available work!

---

## 🔌 API Endpoints

### Jobs Management
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/jobs` | List all jobs |
| GET | `/api/jobs/:jobId` | Get job details |
| POST | `/api/jobs` | Create new job |
| PATCH | `/api/jobs/:jobId/complete` | Mark job completed |
| DELETE | `/api/jobs/:jobId` | Delete job |

### User Authentication
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/auth/register` | Register user |
| GET | `/api/auth/:publicKey` | Get user profile |
| POST | `/api/auth/validate` | Validate address |

### Smart Contract
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/contract/create-job` | Create job on-chain |
| POST | `/api/contract/submit-work` | Submit work transaction |
| POST | `/api/contract/release-payment` | Release payment |
| GET | `/api/contract/job/:jobId` | Get job from contract |

## ✨ Features

### Employer Features
- ✅ Post jobs with secured payment amount
- ✅ Lock payment in smart contract escrow
- ✅ View job listings and details  
- ✅ Release payment to student after work approval
- ✅ Track job status in dashboard

### Student Features
- ✅ Browse available jobs in marketplace
- ✅ Submit work for job
- ✅ Receive instant blockchain payment
- ✅ View assigned jobs in dashboard
- ✅ Track payment status

### System Features
- ✅ Wallet-based authentication (Stellar)
- ✅ On-chain transaction verification
- ✅ Escrow-based payment security
- ✅ Modern responsive UI
- ✅ Real-time job status updates
- ✅ Type-safe TypeScript codebase
- ✅ RESTful API with validation

---

## 📚 Documentation

Comprehensive documentation available:

- **[FULLSTACK_README.md](../FULLSTACK_README.md)** - Complete project overview
- **[QUICKSTART.md](../QUICKSTART.md)** - 5-minute setup guide
- **[API_DOCUMENTATION.md](../API_DOCUMENTATION.md)** - Detailed API reference
- **[DEPLOYMENT.md](../DEPLOYMENT.md)** - Production deployment guide
- **[frontend/README.md](../frontend/README.md)** - Frontend documentation
- **[backend/README.md](../backend/README.md)** - Backend documentation
- **[PROJECT_STRUCTURE.md](../PROJECT_STRUCTURE.md)** - File structure guide

---

## 🚢 Deployment

### Frontend Deployment
- **Vercel** (recommended) - Automatic deployment from Git
- **Netlify** - Static site hosting
- **AWS S3 + CloudFront** - CDN-backed hosting

### Backend Deployment
- **Railway** - Simple container hosting
- **Heroku** - Platform-as-a-service (PaaS)
- **AWS EC2** - Virtual machines
- **Docker** - Container deployment

### Smart Contract
- Deploy to **Stellar Mainnet** for production
- Currently on **Stellar Testnet** for development

See [DEPLOYMENT.md](../DEPLOYMENT.md) for detailed instructions.

---

## 🔐 Security

- Client-side secret key handling (never sent to server)
- Stellar address validation  
- On-chain transaction verification
- Escrow-based payment security
- Environment variables for sensitive data
- Input sanitization and error handling

---

## 🎓 Learning Resources

- [Stellar Documentation](https://developers.stellar.org)
- [Soroban Smart Contracts](https://developers.stellar.org/docs/learn/soroban)
- [Next.js Guide](https://nextjs.org/docs)
- [Express.js Guide](https://expressjs.com)
- [Tailwind CSS](https://tailwindcss.com/docs)

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Contract not found | Update CONTRACT_ID in .env files |
| Port already in use | Change PORT in .env or kill existing process |
| Invalid secret key | Ensure key starts with 'S', regenerate if needed |
| CORS errors | Make sure backend is running on port 3001 |
| Module not found | Run `npm install` in the folder |

---

## 🚀 Future Scope

Planned features:
- List jobs and users directly in UI
- Reputation and rating system
- Milestone-based payments
- Proof-of-work history tracking
- Analytics dashboard
- Academic credential verification
- Email notifications
- Advanced search and filtering
- Dispute resolution system

---

## 👥 Development Team

Built with modern web3 technologies and Stellar blockchain.

---

## 📄 License

MIT License - See LICENSE file

---

## 🤝 Support

For issues or questions:
1. Check the documentation files
2. Review [API_DOCUMENTATION.md](../API_DOCUMENTATION.md)
3. See [QUICKSTART.md](../QUICKSTART.md) for setup help
4. Open an issue on GitHub

---

## Legacy Setup Guide (Reference)

Follow these steps to run ProofPay on your machine.

```bash
git clone https://github.com/<your-username>/ProofPay.git
cd ProofPay
```

### Install required tooling.

```bash
rustc --version
cargo --version
stellar --version
node --version
pnpm --version
```

### Install frontend dependencies.

```bash
cd frontend
pnpm install
cd ..
```

### Build and test the smart contract.

```bash
cargo test
stellar contract build
```

Expected WASM output:

```
target/wasm32v1-none/release/proofpay.wasm
```

---

### Deploy your contract to testnet.

```bash
stellar contract deploy \
  --wasm target/wasm32v1-none/release/proofpay.wasm \
  --source burner-key \
  --network testnet
```

---

### Configure frontend environment variables.

```bash
cd frontend
cp .env.example .env.local
```

Set these values in frontend/.env.local:

```
NEXT_PUBLIC_STELLAR_RPC_URL=https://soroban-testnet.stellar.org
NEXT_PUBLIC_STELLAR_NETWORK=TESTNET
NEXT_PUBLIC_STELLAR_NETWORK_PASSPHRASE=Test SDF Network ; September 2015
NEXT_PUBLIC_PROOFPAY_CONTRACT_ID=GCYVFVPAICIHSLGPFV7TS4DFRHNXRF4U7T2XYEJCDZEY7CSHDAMWZOIV
NEXT_PUBLIC_PROOFPAY_ASSET_ADDRESS=<TOKEN_CONTRACT_ADDRESS>
NEXT_PUBLIC_PROOFPAY_ASSET_CODE=XLM
NEXT_PUBLIC_PROOFPAY_ASSET_DECIMALS=7
NEXT_PUBLIC_STELLAR_EXPLORER_URL=https://stellar.expert/explorer/testnet
NEXT_PUBLIC_STELLAR_READ_ADDRESS=<FUNDED_TESTNET_WALLET_ADDRESS>
```

---

### Start the frontend development server.

```bash
pnpm dev
```

---

### Validate frontend quality checks.

```bash
pnpm exec tsc --noEmit
pnpm lint
pnpm build
```

---

### Open the app in your browser.

```
http://localhost:3000
```

---

## Prerequisites

Install:

Rust
rustup
Stellar CLI
Node.js
pnpm
Freighter browser extension

Helpful checks:

```bash
rustc --version
cargo --version
stellar --version
pnpm --version
```

---

## Smart Contract Development

Run tests:

```bash
cargo test
```

Build a Soroban-compatible WASM artifact:

```bash
stellar contract build
```

This produces:

```
target/wasm32v1-none/release/proofpay.wasm
```

Important:

use stellar contract build
do not deploy the old wasm32-unknown-unknown artifact

---

## Deploy To Testnet

Deploy the contract:

```bash
stellar contract deploy \
  --wasm target/wasm32v1-none/release/proofpay.wasm \
  --source burner-key \
  --network testnet
```

After deployment, copy the returned contract ID into:

```
NEXT_PUBLIC_PROOFPAY_CONTRACT_ID=
```
CB4BTPTBQGDZJOH2Q2TVC2ZBMKB5ZH57IP2PGAL62XKWAM2MVUWN47TS
---

## Asset Configuration

ProofPay needs a token contract address for escrow payments.

If you are using native XLM on Soroban, use the Stellar Asset Contract for native.

Example commands:

```bash
stellar contract asset deploy \
  --source burner-key \
  --network testnet \
  --asset native

stellar contract id asset \
  --network testnet \
  --asset native
```

---

## Frontend Setup

Install dependencies:

```bash
cd frontend
pnpm install
```

Create a local environment file:

```bash
cp .env.example .env.local
```

---

## What These Values Mean

NEXT_PUBLIC_PROOFPAY_CONTRACT_ID
The deployed ProofPay smart contract ID.

NEXT_PUBLIC_PROOFPAY_ASSET_ADDRESS
The token contract used for escrow payments.

NEXT_PUBLIC_STELLAR_READ_ADDRESS
A funded testnet account used for read-only contract simulation.

---

## Contract API Reference

create_job(employer, title, payment) -> u32
Creates a new job listing.

submit_work(student, job_id, proof)
Submits proof of completed work.

approve_work(employer, job_id)
Approves submitted work and releases payment.

job(job_id) -> Job
Returns job details.

escrow_balance(job_id) -> i128
Returns escrowed amount for a job.

---

## CLI Examples

Create a job:

```bash
stellar contract invoke \
  --id <CONTRACT_ID> \
  --source employer \
  --network testnet \
  -- create_job \
  --employer <EMPLOYER_ADDRESS> \
  --title "Web Development Task" \
  --payment 10000000
```

Submit work:

```bash
stellar contract invoke \
  --id <CONTRACT_ID> \
  --source student \
  --network testnet \
  -- submit_work \
  --student <STUDENT_ADDRESS> \
  --job_id 1 \
  --proof "github.com/work-link"
```

Approve work:

```bash
stellar contract invoke \
  --id <CONTRACT_ID> \
  --source employer \
  --network testnet \
  -- approve_work \
  --employer <EMPLOYER_ADDRESS> \
  --job_id 1
```

---

## What The Project Solves

Students often face:

delayed or unpaid freelance work
lack of trust between employer and student
no verification of submitted work
manual and unreliable payment tracking

ProofPay solves this by using smart contracts as a trustless escrow system.

---

## How ProofPay Works

ProofPay is built around 3 concepts:

Jobs
Each job has:
an employer
a payment amount
a status

Proof of Work
Students submit verifiable outputs (links, files, etc.)

Escrow
Funds are locked in the contract and only released upon approval

---

## Core Rules Enforced By The Contract

The smart contract guarantees the following:

only employers can create jobs
payments are locked before work begins
only assigned students can submit work
only employers can approve and release payment
funds cannot be accessed unless conditions are met

---

## Example User Flow

Employer creates a job with payment escrow
Student accepts and completes the task
Student submits proof of work
Employer verifies the work
Payment is automatically released to the student
All data is recorded on-chain

---

## Project Architecture

This repository is a small monorepo with 2 main parts:

Soroban smart contract in src/lib.rs
Next.js frontend in frontend/

---

## Smart Contract

The contract is written in Rust with soroban-sdk and stores:

job records
escrow balances
proof submissions

Primary contract methods:

create_job
submit_work
approve_work
job
escrow_balance

Tests live in src/test.rs.

---

## Frontend

The frontend is a Next.js app that integrates with:

@stellar/stellar-sdk
@stellar/freighter-api
Freighter wallet
Soroban RPC on Stellar testnet

---

## Technology Stack

Rust
Soroban SDK
Stellar CLI
Next.js
React
TypeScript
pnpm
Freighter

---

## Repo Structure

```
.
├── src/
│   ├── lib.rs
│   └── test.rs
├── frontend/
│   ├── src/
│   ├── .env.example
│   └── package.json
├── Cargo.toml
└── README.md
```

---

## Current Status

This project currently includes:

* a working Soroban escrow contract for job payments
* Rust tests for contract logic
* frontend integration with Freighter wallet
* smart contract interaction via client-side code
* testnet deployment configuration


