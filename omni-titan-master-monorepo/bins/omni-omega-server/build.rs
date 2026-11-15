use std::path::Path;

fn main() {
    let proto_path = Path::new("../../proto/omni_omega.proto");
    if proto_path.exists() {
        println!("cargo:rerun-if-changed=../../proto/omni_omega.proto");
    }
    println!("cargo:rerun-if-changed=src/frontier_12_kernels.rs");
    println!("cargo:rerun-if-changed=src/individual_100_kernels.rs");
    println!("cargo:rerun-if-changed=src/kernels.rs");
    println!("cargo:rerun-if-changed=src/main.rs");
}
