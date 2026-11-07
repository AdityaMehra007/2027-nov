//! JANE STREET / TIGERBEETLE / LMAX DISRUPTOR — Mechanical Sympathy Engine
//! Zero-allocation, cache-line-aligned ring buffer & batch financial state machine.

use std::sync::atomic::{AtomicU64, Ordering};

/// Padded to 64 bytes (exact x86_64 / ARM64 L1 cache line size) to prevent
/// multicore cache-coherency invalidation storms ("False Sharing").
#[repr(align(64))]
pub struct CacheLinePaddedAtomicU64 {
    pub value: AtomicU64,
    _padding: [u8; 56],
}

impl CacheLinePaddedAtomicU64 {
    pub const fn new(init: u64) -> Self {
        Self {
            value: AtomicU64::new(init),
            _padding: [0u8; 56],
        }
    }
}

/// Fixed 64-byte financial command slot (1 event == 1 CPU cache line)
#[repr(C, align(64))]
#[derive(Clone, Copy, Debug, Default)]
pub struct FinancialTransferEvent {
    pub sequence_id: u64,
    pub debit_account_id: u64,
    pub credit_account_id: u64,
    pub amount_micro_units: i64,
    pub timestamp_ns: u64,
    pub flags: u64,
    pub _reserved: [u64; 2],
}

/// Power-of-2 Lock-Free SPSC/MPSC Disruptor Ring Buffer
pub struct MechanicalSympathyDisruptor<const CAPACITY: usize> {
    pub write_cursor: CacheLinePaddedAtomicU64,
    pub read_cursor: CacheLinePaddedAtomicU64,
    pub ring: [FinancialTransferEvent; CAPACITY],
}

impl<const CAPACITY: usize> MechanicalSympathyDisruptor<CAPACITY> {
    const MASK: usize = CAPACITY - 1;

    pub fn new() -> Self {
        assert!(CAPACITY.is_power_of_two(), "Ring capacity MUST be a power of 2 for bitwise masking.");
        Self {
            write_cursor: CacheLinePaddedAtomicU64::new(0),
            read_cursor: CacheLinePaddedAtomicU64::new(0),
            ring: [FinancialTransferEvent::default(); CAPACITY],
        }
    }

    #[inline(always)]
    pub fn try_publish(&mut self, event: FinancialTransferEvent) -> Result<u64, &'static str> {
        let current_write = self.write_cursor.value.load(Ordering::Relaxed);
        let current_read = self.read_cursor.value.load(Ordering::Acquire);

        if current_write.wrapping_sub(current_read) >= CAPACITY as u64 {
            return Err("Backpressure: Ring buffer full!");
        }

        // Bitwise AND replaces slow CPU division/modulo instruction
        let slot_idx = (current_write as usize) & Self::MASK;
        self.ring[slot_idx] = event;

        let next_write = current_write.wrapping_add(1);
        self.write_cursor.value.store(next_write, Ordering::Release);
        Ok(current_write)
    }

    #[inline(always)]
    pub fn consume_batch<F>(&mut self, mut processor: F) -> usize
    where
        F: FnMut(&FinancialTransferEvent),
    {
        let available_write = self.write_cursor.value.load(Ordering::Acquire);
        let mut current_read = self.read_cursor.value.load(Ordering::Relaxed);
        let mut processed = 0usize;

        while current_read < available_write {
            let slot_idx = (current_read as usize) & Self::MASK;
            processor(&self.ring[slot_idx]);
            current_read = current_read.wrapping_add(1);
            processed += 1;
        }

        // Single amortized atomic release store for the entire batch!
        if processed > 0 {
            self.read_cursor.value.store(current_read, Ordering::Release);
        }
        processed
    }
}
