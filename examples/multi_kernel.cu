#include <iostream>

// CUDA kernel for vector addition
__global__ void vecAdd(float *a, float *b, float *c, int n) {
  int i = blockIdx.x * blockDim.x + threadIdx.x;
  if (i < n) c[i] = a[i] + b[i];
}

// CUDA kernel for vector multiplication
__global__ void vecMul(float *a, float *b, float *c, int n) {
  int i = blockIdx.x * blockDim.x + threadIdx.x;
  if (i < n) c[i] = a[i] * b[i];
}

// CUDA kernel for vector squaring
__global__ void vecSquare(float *a, float *b, int n) {
  int i = blockIdx.x * blockDim.x + threadIdx.x;
  if (i < n) b[i] = a[i] * a[i];
}

int main() {
  int N = 1 << 20;
  float *a, *b, *c;

  cudaMallocManaged(&a, N * sizeof(float));
  cudaMallocManaged(&b, N * sizeof(float));
  cudaMallocManaged(&c, N * sizeof(float));

  for (int i = 0; i < N; ++i) {
    a[i] = i * 0.5f;
    b[i] = i * 0.25f;
  }

  int threadsPerBlock = 256;
  int blocksPerGrid = (N + threadsPerBlock - 1) / threadsPerBlock;

  vecAdd<<<blocksPerGrid, threadsPerBlock>>>(a, b, c, N);
  cudaDeviceSynchronize();

  vecMul<<<blocksPerGrid, threadsPerBlock>>>(a, b, c, N);
  cudaDeviceSynchronize();

  vecSquare<<<blocksPerGrid, threadsPerBlock>>>(a, b, N);
  cudaDeviceSynchronize();

  std::cout << "c[42] after vecMul = " << c[42] << std::endl;
  std::cout << "b[42] after vecSquare = " << b[42] << std::endl;

  cudaFree(a);
  cudaFree(b);
  cudaFree(c);

  return 0;
}
