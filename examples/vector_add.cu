#include <iostream>

// CUDA kernel for vector addition
__global__ void vecAdd(float *a, float *b, float *c, int n) {
  int i = blockIdx.x * blockDim.x + threadIdx.x;  //blockIdx = block index, blockDim = number of threads in a block, threadIdx = thread index within a block
  if (i < n) c[i] = a[i] + b[i];
}

int main() {
  int N = 1 << 20;  // Set N = 2^20 = 1,048,576 elements
  float *a, *b, *c; 

  // Allocate unified memory accessible by both CPU and GPU
  cudaMallocManaged(&a, N * sizeof(float));
  cudaMallocManaged(&b, N * sizeof(float));
  cudaMallocManaged(&c, N * sizeof(float));

  // Initialize vectors a and b
  for (int i = 0; i < N; ++i) { a[i] = i; b[i] = i; }

  // Launch the kernel with enough blocks and threads to cover N elements
  // 256 threads per block; (N + 255)/256 ensures we round up
  vecAdd<<<(N + 255)/256, 256>>>(a, b, c, N);

  // Wait for the GPU to finish before accessing results
  cudaDeviceSynchronize();

  // Output the value of c[42] to verify correctness (should be 42 + 42 = 84)
  std::cout << "c[42] = " << c[42] << std::endl;

  cudaFree(a); cudaFree(b); cudaFree(c);
  return 0;
}
