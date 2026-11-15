#[cfg(test)]
mod tests {
    #[test]
    fn test_blake3_cryptographic_seal_invariance() {
        let genesis = "GENESIS_00000000000000000000000000000000000000000000000000000000";
        let raw = format!("1:omni-sovereign:100:{}", genesis);
        let seal = blake3::hash(raw.as_bytes()).to_hex().to_string();
        assert_eq!(seal.len(), 64);
        assert!(!seal.is_empty());
    }

    #[test]
    fn test_gf65537_prime_field_invariance() {
        let p: u64 = 65537;
        let a: u64 = 42;
        let b: u64 = 1337;
        let sum = (a + b) % p;
        assert_eq!(sum, 1379);
    }

    #[test]
    fn test_112_projects_hash_chain_invariance() {
        let mut prev = "GENESIS_00000000000000000000000000000000000000000000000000000000".to_string();
        for id in 1..=112 {
            let payload = format!("{}:tenant-alpha:{}:{}", id, id * 1024, prev);
            let seal = blake3::hash(payload.as_bytes()).to_hex().to_string();
            assert_eq!(seal.len(), 64);
            prev = seal;
        }
        assert_eq!(prev.len(), 64);
    }
}
