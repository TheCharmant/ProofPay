#![no_std]

use soroban_sdk::{
    contract, contractimpl, contracttype, symbol_short, Address, Env, Symbol,
};

#[contracttype]
#[derive(Clone)]
pub struct Job {
    pub employer: Address,
    pub student: Address,
    pub amount: i128,
    pub completed: bool,
}

#[contracttype]
pub enum DataKey {
    Job(Symbol), // job_id
}

#[contract]
pub struct ProofPay;

#[contractimpl]
impl ProofPay {
    // Employer creates job and locks payment
    pub fn create_job(env: Env, job_id: Symbol, employer: Address, student: Address, amount: i128) {
        let key = DataKey::Job(job_id.clone());

        if env.storage().instance().has(&key) {
            panic!("Job already exists");
        }

        let job = Job {
            employer,
            student,
            amount,
            completed: false,
        };

        env.storage().instance().set(&key, &job);

        env.events().publish(
            (symbol_short!("create"), job_id),
            amount,
        );
    }

    // Student submits work (marks complete)
    pub fn submit_work(env: Env, job_id: Symbol) {
        let key = DataKey::Job(job_id.clone());

        let mut job: Job = env.storage().instance().get(&key).unwrap();

        job.completed = true;

        env.storage().instance().set(&key, &job);

        env.events().publish(
            (symbol_short!("submit"), job_id),
            true,
        );
    }

    // Release payment to student
    pub fn release_payment(env: Env, job_id: Symbol) {
        let key = DataKey::Job(job_id.clone());

        let job: Job = env.storage().instance().get(&key).unwrap();

        if !job.completed {
            panic!("Work not completed");
        }

        // Simulated payment (event)
        env.events().publish(
            (symbol_short!("pay"), job_id),
            (job.employer, job.student, job.amount),
        );
    }

    // Getter for testing
    pub fn get_job(env: Env, job_id: Symbol) -> Job {
        let key = DataKey::Job(job_id);
        env.storage().instance().get(&key).unwrap()
    }
}