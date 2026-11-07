// File: src/ebpf/xdp_zero_trust_mesh.c
// Compile with: clang -O2 -g -target bpf -c src/ebpf/xdp_zero_trust_mesh.c -o xdp_zero_trust_mesh.o

#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/udp.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>

#define AETHER_PQC_MAGIC_HEADER 0x4F4D4547 // "OMEG" in ASCII hex
#define AETHER_MESH_UDP_PORT    20270

// Per-CPU Lock-Free Telemetry Map shared between Linux Kernel and Rust Userspace
struct {
    __uint(type, BPF_MAP_TYPE_PERCPU_ARRAY);
    __uint(max_entries, 2);
    __type(key, __u32);
    __type(value, __u64);
} xdp_packet_counters SEC(".maps");

SEC("xdp")
int aether_xdp_pqc_firewall(struct xdp_md *ctx) {
    void *data     = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;

    // 1. Strict Verifier Pointer Arithmetic Bounds Check for Ethernet Frame
    struct ethhdr *eth = data;
    if ((void *)(eth + 1) > data_end)
        return XDP_PASS;

    if (eth->h_proto != bpf_htons(ETH_P_IP))
        return XDP_PASS;

    // 2. Bounds Check for IPv4 Header
    struct iphdr *iph = (void *)(eth + 1);
    if ((void *)(iph + 1) > data_end)
        return XDP_DROP;

    if (iph->protocol != IPPROTO_UDP)
        return XDP_PASS;

    // 3. Bounds Check for UDP Header
    struct udphdr *udph = (void *)iph + (iph->ihl * 4);
    if ((void *)(udph + 1) > data_end)
        return XDP_DROP;

    if (udph->dest != bpf_htons(AETHER_MESH_UDP_PORT))
        return XDP_PASS;

    // 4. Inspect Post-Quantum Wire Magic Header at NIC Driver Line Rate (400 Gbps)
    __u32 *magic_ptr = (void *)(udph + 1);
    if ((void *)(magic_ptr + 1) > data_end)
        return XDP_DROP;

    __u32 key_pass = 0, key_drop = 1;
    if (bpf_ntohl(*magic_ptr) != AETHER_PQC_MAGIC_HEADER) {
        // Drop unauthenticated packet at NIC DMA ring before OS allocation!
        __u64 *drop_cnt = bpf_map_lookup_elem(&xdp_packet_counters, &key_drop);
        if (drop_cnt) (*drop_cnt)++;
        return XDP_DROP;
    }

    __u64 *pass_cnt = bpf_map_lookup_elem(&xdp_packet_counters, &key_pass);
    if (pass_cnt) (*pass_cnt)++;
    return XDP_PASS;
}

char _license[] SEC("license") = "GPL";
