pub const PRIME_MODULUS: u64 = 65537;

pub struct ShamirEngine;

impl ShamirEngine {
    pub fn split_secret_2_of_3(secret: u64, slope: u64) -> Vec<(u64, u64)> {
        let p = PRIME_MODULUS;
        let s = secret % p;
        let a = slope % p;
        vec![
            (1, (s + a * 1) % p),
            (2, (s + a * 2) % p),
            (3, (s + a * 3) % p),
        ]
    }

    pub fn lagrange_reconstruct(shares: &[(u64, u64)]) -> u64 {
        assert!(shares.len() >= 2);
        let p = PRIME_MODULUS as i64;
        let (x0, y0) = (shares[0].0 as i64, shares[0].1 as i64);
        let (x1, y1) = (shares[1].0 as i64, shares[1].1 as i64);

        // L0(0) = (0 - x1) / (x0 - x1)
        // L1(0) = (0 - x0) / (x1 - x0)
        let num0 = (-x1).rem_euclid(p);
        let den0 = (x0 - x1).rem_euclid(p);
        let inv0 = Self::mod_inverse(den0, p);
        let term0 = (y0 * num0 % p) * inv0 % p;

        let num1 = (-x0).rem_euclid(p);
        let den1 = (x1 - x0).rem_euclid(p);
        let inv1 = Self::mod_inverse(den1, p);
        let term1 = (y1 * num1 % p) * inv1 % p;

        ((term0 + term1) % p) as u64
    }

    fn mod_inverse(a: i64, m: i64) -> i64 {
        let mut t = 0i64;
        let mut newt = 1i64;
        let mut r = m;
        let mut newr = a;
        while newr != 0 {
            let quotient = r / newr;
            let temp_t = t - quotient * newt;
            t = newt;
            newt = temp_t;
            let temp_r = r - quotient * newr;
            r = newr;
            newr = temp_r;
        }
        if t < 0 { t += m; }
        t
    }
}
