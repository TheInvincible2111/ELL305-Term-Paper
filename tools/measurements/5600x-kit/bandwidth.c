/*
 * bandwidth.c - read and triad bandwidth against buffer size and thread count
 * (ELL305 term paper, 5600X measurement kit)
 *
 * For each total buffer size, every thread works on its own slice (no sharing).
 *   read:  sum += a[i]                      (8 bytes read per element)
 *   triad: a[i] = b[i] + s * c[i]           (24 bytes moved per element, counting the write once)
 * Reports GB/s (10^9 bytes per second). Small buffers measure the caches, large ones DRAM.
 *
 * Build:  gcc -O3 -march=native -fopenmp -o bandwidth bandwidth.c
 * Run:    ./bandwidth --threads 6        (CSV to stdout)
 */
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static double now_s(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec * 1e-9; }

int main(int argc, char **argv) {
    int threads = 1;
    for (int i = 1; i < argc; i++) if (!strcmp(argv[i], "--threads") && i + 1 < argc) threads = atoi(argv[++i]);
    omp_set_num_threads(threads);
    const size_t maxb = (size_t)256 << 20;                   /* 256 MiB per array, three arrays */
    double *a = aligned_alloc(64, maxb), *b = aligned_alloc(64, maxb), *c = aligned_alloc(64, maxb);
    #pragma omp parallel for schedule(static)
    for (size_t i = 0; i < maxb / 8; i++) { a[i] = 1; b[i] = 2; c[i] = 3; }

    printf("threads,kernel,bytes_per_array_kib,gb_per_s\n");
    for (size_t bytes = 16 << 10; bytes <= maxb; bytes *= 2) {
        size_t n = bytes / 8;
        for (int kern = 0; kern < 2; kern++) {
            double best = 0; volatile double sink = 0;
            size_t reps = (size_t)(1e9 / (double)bytes) + 1;
            for (int trial = 0; trial < 3; trial++) {
                double t0 = now_s(), sum = 0;
                for (size_t r = 0; r < reps; r++) {
                    if (kern == 0) {
                        #pragma omp parallel reduction(+:sum)
                        {   /* read every element of this thread's slice */
                            int t = omp_get_thread_num(), T = omp_get_num_threads();
                            size_t lo = n * t / T, hi = n * (t + 1) / T;
                            const long *ai = (const long *)a;   /* integer adds vectorise freely */
                            long s0 = 0;
                            for (size_t i = lo; i < hi; i++) s0 += ai[i];
                            sum += (double)s0;
                        }
                    } else {
                        #pragma omp parallel for schedule(static)
                        for (size_t i = 0; i < n; i++) a[i] = b[i] + 0.5 * c[i];
                    }
                }
                double t = now_s() - t0; sink += sum;
                double moved = (double)reps * n * (kern == 0 ? 8 : 24);
                if (moved / t > best) best = moved / t;
            }
            printf("%d,%s,%zu,%.2f\n", threads, kern == 0 ? "read" : "triad", bytes >> 10, best / 1e9);
            fflush(stdout);
        }
    }
    return 0;
}
