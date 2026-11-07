// File: src/cuda/flash_mhd_wgmma.cu
// Compile with: nvcc -O3 -arch=sm_90a src/cuda/flash_mhd_wgmma.cu -o flash_mhd_kernel

#include <cuda_runtime.h>
#include <math_constants.h>
#include <cstdio>

constexpr int WARP_SIZE = 32;
constexpr int BLOCK_DIM_X = 16;
constexpr int BLOCK_DIM_Y = 16;
constexpr int HALO = 1;

// ----------------------------------------------------------------------------
// 1. WARP-SHUFFLE ONLINE REDUCTION PRIMITIVES
// ----------------------------------------------------------------------------
__device__ __forceinline__ float warp_reduce_max(float val) {
    #pragma unroll
    for (int offset = WARP_SIZE / 2; offset > 0; offset /= 2) {
        val = fmaxf(val, __shfl_xor_sync(0xffffffff, val, offset));
    }
    return val;
}

__device__ __forceinline__ float warp_reduce_sum(float val) {
    #pragma unroll
    for (int offset = WARP_SIZE / 2; offset > 0; offset /= 2) {
        val += __shfl_xor_sync(0xffffffff, val, offset);
    }
    return val;
}

// ----------------------------------------------------------------------------
// 2. SHARED-MEMORY TILED 2D MAGNETOHYDRODYNAMIC (MHD) LAPLACIAN & LORENTZ KERNEL
// ----------------------------------------------------------------------------
__global__ void fused_mhd_sram_stencil_kernel(
    const float* __restrict__ omega_in,
    const float* __restrict__ psi_in,
    float* __restrict__ omega_out,
    int width,
    int height,
    float inv_dx,
    float inv_dx2,
    float nu_dt,
    float dt
) {
    // Dual On-Chip SRAM Tiles for Vorticity omega and Magnetic Flux psi
    __shared__ float s_omega[BLOCK_DIM_Y + 2 * HALO][BLOCK_DIM_X + 2 * HALO];
    __shared__ float s_psi[BLOCK_DIM_Y + 2 * HALO][BLOCK_DIM_X + 2 * HALO];

    const int gx = blockIdx.x * BLOCK_DIM_X + threadIdx.x;
    const int gy = blockIdx.y * BLOCK_DIM_Y + threadIdx.y;
    const int sx = threadIdx.x + HALO;
    const int sy = threadIdx.y + HALO;

    if (gx < width && gy < height) {
        const int idx = gy * width + gx;
        s_omega[sy][sx] = omega_in[idx];
        s_psi[sy][sx]   = psi_in[idx];

        // Periodic boundary halos
        if (threadIdx.x == 0) {
            int left_x = (gx == 0) ? (width - 1) : (gx - 1);
            s_omega[sy][0] = omega_in[gy * width + left_x];
            s_psi[sy][0]   = psi_in[gy * width + left_x];
        }
        if (threadIdx.x == BLOCK_DIM_X - 1 || gx == width - 1) {
            int right_x = (gx + 1) % width;
            s_omega[sy][sx + 1] = omega_in[gy * width + right_x];
            s_psi[sy][sx + 1]   = psi_in[gy * width + right_x];
        }
        if (threadIdx.y == 0) {
            int top_y = (gy == 0) ? (height - 1) : (gy - 1);
            s_omega[0][sx] = omega_in[top_y * width + gx];
            s_psi[0][sx]   = psi_in[top_y * width + gx];
        }
        if (threadIdx.y == BLOCK_DIM_Y - 1 || gy == height - 1) {
            int bot_y = (gy + 1) % height;
            s_omega[sy + 1][sx] = omega_in[bot_y * width + gx];
            s_psi[sy + 1][sx]   = psi_in[bot_y * width + gx];
        }
    }

    __syncthreads();

    if (gx < width && gy < height) {
        const float omega_center = s_omega[sy][sx];
        const float psi_center   = s_psi[sy][sx];

        // 1. Viscous Laplacian: nu * nabla^2(omega)
        const float laplacian_omega = (
            s_omega[sy][sx - 1] + s_omega[sy][sx + 1] +
            s_omega[sy - 1][sx] + s_omega[sy + 1][sx] -
            4.0f * omega_center
        ) * inv_dx2;

        // 2. Current Density J = -nabla^2(psi)
        const float current_density_j = -(
            s_psi[sy][sx - 1] + s_psi[sy][sx + 1] +
            s_psi[sy - 1][sx] + s_psi[sy + 1][sx] -
            4.0f * psi_center
        ) * inv_dx2;

        // 3. Magnetic Field B = (d_psi/dy, -d_psi/dx)
        const float bx = (s_psi[sy + 1][sx] - s_psi[sy - 1][sx]) * (0.5f * inv_dx);
        const float by = -(s_psi[sy][sx + 1] - s_psi[sy][sx - 1]) * (0.5f * inv_dx);

        // 4. Lorentz Magnetic Tension term: (B . grad) J
        const float dj_dx = (current_density_j) * (0.5f * inv_dx);
        const float lorentz_force = (bx * dj_dx + by * dj_dx);

        omega_out[gy * width + gx] = omega_center + nu_dt * laplacian_omega + dt * lorentz_force;
    }
}
