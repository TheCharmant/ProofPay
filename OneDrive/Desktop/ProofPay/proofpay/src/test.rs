#![cfg(test)]

use soroban_sdk::{testutils::Address as _, Address, Env, Symbol};

use crate::{ProofPay, ProofPayClient};

#[test]
fn test_happy_path() {
    let env = Env::default();
    let contract_id = env.register_contract(None, ProofPay);
    let client = ProofPayClient::new(&env, &contract_id);

    let employer = Address::generate(&env);
    let student = Address::generate(&env);
    let job_id = Symbol::short("JOB1");

    client.create_job(&job_id, &employer, &student, &1000);
    client.submit_work(&job_id);
    client.release_payment(&job_id);

    let job = client.get_job(&job_id);
    assert!(job.completed);
}

#[test]
#[should_panic]
fn test_release_without_completion() {
    let env = Env::default();
    let contract_id = env.register_contract(None, ProofPay);
    let client = ProofPayClient::new(&env, &contract_id);

    let employer = Address::generate(&env);
    let student = Address::generate(&env);
    let job_id = Symbol::short("JOB2");

    client.create_job(&job_id, &employer, &student, &1000);
    client.release_payment(&job_id); // should fail
}

#[test]
fn test_state() {
    let env = Env::default();
    let contract_id = env.register_contract(None, ProofPay);
    let client = ProofPayClient::new(&env, &contract_id);

    let employer = Address::generate(&env);
    let student = Address::generate(&env);
    let job_id = Symbol::short("JOB3");

    client.create_job(&job_id, &employer, &student, &500);

    let job = client.get_job(&job_id);

    assert_eq!(job.amount, 500);
    assert_eq!(job.completed, false);
}