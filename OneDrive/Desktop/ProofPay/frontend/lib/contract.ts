import * as StellarSdk from 'stellar-sdk'

const SERVER_URL = process.env.NEXT_PUBLIC_STELLAR_SERVER || 'https://soroban-testnet.stellar.org'
const NETWORK_PASSPHRASE = process.env.NEXT_PUBLIC_NETWORK_PASSPHRASE || 'Test SDF Network ; September 2015'
const CONTRACT_ID = process.env.NEXT_PUBLIC_CONTRACT_ID || ''

const server = new StellarSdk.SorobanRpc.Server(SERVER_URL)

export interface JobData {
  employer: string
  student: string
  amount: number
  completed: boolean
  jobId?: string
}

export class ProofPayContract {
  private keypair: StellarSdk.Keypair | null = null

  setKeypair(secret: string) {
    this.keypair = StellarSdk.Keypair.fromSecret(secret)
  }

  getPublicKey(): string {
    if (!this.keypair) throw new Error('Keypair not set')
    return this.keypair.publicKey()
  }

  async createJob(
    jobId: string,
    employerSecret: string,
    studentAddress: string,
    amount: number
  ): Promise<string> {
    if (!CONTRACT_ID) throw new Error('CONTRACT_ID not set')

    const contractAddress = CONTRACT_ID
    const account = await server.getAccount(StellarSdk.Keypair.fromSecret(employerSecret).publicKey())

    const contract = new StellarSdk.Contract(contractAddress)

    const transaction = new StellarSdk.TransactionBuilder(account, {
      fee: StellarSdk.BASE_FEE,
      networkPassphrase: NETWORK_PASSPHRASE,
    })
      .setTimeout(300)
      .addOperation(
        contract.call(
          'create_job',
          StellarSdk.nativeToScVal(jobId, { type: 'symbol' }),
          StellarSdk.nativeToScVal(StellarSdk.Keypair.fromSecret(employerSecret).publicKey()),
          StellarSdk.nativeToScVal(studentAddress),
          StellarSdk.nativeToScVal(BigInt(amount))
        )
      )
      .build()

    transaction.sign(StellarSdk.Keypair.fromSecret(employerSecret))

    const result = await server.submitTransaction(transaction)
    return result.hash
  }

  async submitWork(jobId: string, studentSecret: string): Promise<string> {
    if (!CONTRACT_ID) throw new Error('CONTRACT_ID not set')

    const keypair = StellarSdk.Keypair.fromSecret(studentSecret)
    const account = await server.getAccount(keypair.publicKey())

    const contract = new StellarSdk.Contract(CONTRACT_ID)

    const transaction = new StellarSdk.TransactionBuilder(account, {
      fee: StellarSdk.BASE_FEE,
      networkPassphrase: NETWORK_PASSPHRASE,
    })
      .setTimeout(300)
      .addOperation(contract.call('submit_work', StellarSdk.nativeToScVal(jobId, { type: 'symbol' })))
      .build()

    transaction.sign(keypair)
    const result = await server.submitTransaction(transaction)
    return result.hash
  }

  async releasePayment(jobId: string, employerSecret: string): Promise<string> {
    if (!CONTRACT_ID) throw new Error('CONTRACT_ID not set')

    const keypair = StellarSdk.Keypair.fromSecret(employerSecret)
    const account = await server.getAccount(keypair.publicKey())

    const contract = new StellarSdk.Contract(CONTRACT_ID)

    const transaction = new StellarSdk.TransactionBuilder(account, {
      fee: StellarSdk.BASE_FEE,
      networkPassphrase: NETWORK_PASSPHRASE,
    })
      .setTimeout(300)
      .addOperation(contract.call('release_payment', StellarSdk.nativeToScVal(jobId, { type: 'symbol' })))
      .build()

    transaction.sign(keypair)
    const result = await server.submitTransaction(transaction)
    return result.hash
  }

  async getJob(jobId: string): Promise<JobData> {
    if (!CONTRACT_ID) throw new Error('CONTRACT_ID not set')

    const contract = new StellarSdk.Contract(CONTRACT_ID)
    const result = await server.simulateTransaction({
      transaction: new StellarSdk.TransactionBuilder(
        new StellarSdk.Account(StellarSdk.Keypair.random().publicKey(), '0'),
        {
          fee: StellarSdk.BASE_FEE,
          networkPassphrase: NETWORK_PASSPHRASE,
        }
      )
        .addOperation(contract.call('get_job', StellarSdk.nativeToScVal(jobId, { type: 'symbol' })))
        .build(),
    } as any)

    if (result.error) throw new Error(result.error.detail)

    return result as any
  }
}

export const proofPayContract = new ProofPayContract()
