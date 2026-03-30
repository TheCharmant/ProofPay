# ProofPay

ProofPay is a Soroban smart contract built on the Stellar blockchain that enables secure job creation, work submission, and payment release between employers and students.

## Features

- **Job Management**: Employers can create jobs with specified compensation
- **Work Submission**: Students can submit work for review
- **Payment Release**: Secure payment release only after work completion
- **Smart Contract Security**: Built with Soroban SDK for robust contract logic

## Project Structure

```
proofpay/
├── Cargo.toml          # Project dependencies and configuration
├── src/
│   ├── lib.rs         # Main contract implementation
│   └── test.rs        # Unit tests
├── target/            # Build artifacts
└── README.md          # This file
```

## Prerequisites

- Rust 1.70+
- Soroban CLI
- Stellar testnet account (funded via friendbot)

## Setup

1. **Clone the repository**:
```bash
git clone https://github.com/TheCharmant/ProofPay.git
cd ProofPay/proofpay
```

2. **Install dependencies**:
```bash
cargo build
```

3. **Generate testnet account** (if needed):
```powershell
stellar keys generate --network testnet my-key
stellar keys public-key my-key
```

4. **Fund account with testnet lumens**:
```powershell
Invoke-WebRequest "https://friendbot.stellar.org?addr=YOUR_PUBLIC_KEY" -UseBasicParsing
```

## Building

```bash
cargo build
```

Build for WebAssembly:
```bash
cargo build --target wasm32-unknown-unknown --release
```

## Testing

Run unit tests:
```bash
cargo test
```

This will test the contract logic including:
- Happy path: Job creation → work submission → payment release
- Error handling: Payment release without completion

## Deploying

Deploy the contract to Stellar testnet:
```bash
stellar contract deploy \
  --wasm target/wasm32-unknown-unknown/release/proofpay.wasm \
  --source my-key \
  --network testnet
```

## Contract Interface

### Functions

- `create_job(job_id, employer, student, amount)` - Create a new job
- `submit_work(job_id)` - Mark work as completed
- `release_payment(job_id)` - Release payment to student
- `get_job(job_id)` - Get job details

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting.

## License

MIT

## Support

For issues and questions, please open an issue on GitHub.
