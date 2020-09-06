use std::cmp::{max, min};
use std::collections::HashMap;
use std::error::Error;
use std::fs::File;
use std::path::Path;

extern crate csv;

enum TransactionType {
    CREDIT,
    DEBIT,
}

#[derive(Debug, Deserialize)]
#[serde(field_identifier, rename_all = "snake_case")] // just a precaution
struct Transaction {
    user_id: i64,
    account_id: i64,
    amount: f32,
    desc: str,
    date: str, // TODO: better date type?
    transaction_type: TransactionType,
    // TODO: what is this? Is it needed?
    misc: Optional<str>,
}

impl Transaction {
    fn signed_amount(&self) -> f32 {
        match self.transaction_type {
            TransactionType::CREDIT => self.amount,
            TransactionType::DEBIT => -self.amount,
        }
    }
}

struct UserInfo {
    user_id: i64,
    num_transactions: i32,
    total_transaction: f32,
    min_transaction: f32,
    max_transaction: f32,
}

impl UserInfo {
    fn merge_with(&self, other: &UserInfo) -> UserInfo {
        UserInfo {
            user_id: self.user_id,
            num_transactions: self.num_transactions + other.num_transactions,
            total_transaction: self.total_transaction + other.total_transaction,
            min_transaction: min(self.min_transaction, other.min_transaction),
            max_transaction: max(self.max_transaction, other.max_transaction),
        }
    }

    fn append_transaction(&self, txn: &Transaction) -> UserInfo {
        let new_amount = txn.signed_amount() + self.total_transaction;
        UserInfo {
            user_id: self.user_id,
            num_transactions: self.num_transactions + 1,
            total_transaction: self.total_transaction + new_amount,
            min_transaction: min(self.min_transaction, new_amount),
            max_transaction: max(self.max_transaction, new_amount),
        }
    }

    fn default(user_id: i64) -> UserInfo {
        UserInfo {
            user_id: user_id,
            num_transactions: 0,
            total_transaction: 0.0,
            min_transaction: 0.0,
            max_transaction: 0.0,
        }
    }
}

fn read_stream(path: &str, input: &mut impl Read) {
    let mut reader = csv::Reader::from_reader(input);
    reader
        .deserialize::<Result<Transaction, _>>()
        .iter()
        .map(|r| match r {
            Err(e) => {
                println!("Error reading transactions: {}", e.description());
                Option::None
            }
            Ok(txn) => Option::Some(txn),
        })
        .filter(Option::is_some)
        .map(Option::unwrap)
        .group_by(|txn| txn.user_id)
        .into_iter()
        .map(|(user_id, txns)| {
            let mut daily_summaries: HashMap<str, UserInfo> = HashMap::new();
            txns.group_by(|txn| txn.date)
                .into_iter()
                .for_each(|(date, txns)| {
                    let current_ref = daily_summaries
                        .entry(date)
                        .or_insert(UserInfo::default(user_id));
                    *current_ref =
                        txns.fold(*current_ref, |info, txn| info.append_transaction(txn));
                });
            (user_id, daily_summaries)
        })
}

fn handle_one_file(path: &str) {
    match File::open(Path::new(path)) {
        Err(why) => println!("Couldn't open '{}': {}", path, why.description()),
        Ok(file) => read_stream(path, file),
    }
}

fn main() {
    println!("Hello, world!");
}
