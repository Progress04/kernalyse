#include <iostream>

__global__ void vecAdd(float *a, float *b, float *c, int n) {
  int i = blockIdx.x * blockDim.x + threadIdx.x;
  if (i < n) c[i] = a[i] + b[i];
}

int main() {
  int N = 1 << 20;
  float *a, *b, *c;
  cudaMallocManaged(&a, N * sizeof(float));
  cudaMallocManaged(&b, N * sizeof(float));
  cudaMallocManaged(&c, N * sizeof(float));

  for (int i = 0; i < N; ++i) { a[i] = i; b[i] = i; }

  vecAdd<<<(N + 255)/256, 256>>>(a, b, c, N);
  cudaDeviceSynchronize();

  std::cout << "c[42] = " << c[42] << std::endl;

  cudaFree(a); cudaFree(b); cudaFree(c);
  return 0;
}
