/*
 * latency.c - pointer-chasing load-to-use latency sweep (ELL305 term paper)
 *
 * Walks a randomly permuted cyclic chain of cache lines inside a buffer of
 * increasing size and reports the average time per dependent load.
 * Each load's address depends on the previous load, so the processor cannot
 * overlap them: the time per step is the latency of whichever level of the
 * memory hierarchy holds the buffer.
 *
 * Build:  gcc -O2 -o latency latency.c
 * Run:    ./latency            (prints CSV to stdout)
 *         ./latency --huge     (asks Linux for 2 MB pages to reduce TLB effects)
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <sched.h>
#include <sys/mman.h>

#define LINE 64

static double now_ns(void) {
    struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec * 1e9 + t.tv_nsec;
}

static uint64_t rng = 88172645463325252ULL;           /* xorshift64 */
static uint64_t rnd(void) { rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }

int main(int argc, char **argv) {
    int huge = argc > 1 && strcmp(argv[1], "--huge") == 0;

    cpu_set_t set; CPU_ZERO(&set); CPU_SET(0, &set);   /* pin to logical CPU 0 */
    if (sched_setaffinity(0, sizeof set, &set) != 0) perror("sched_setaffinity (continuing)");

    const size_t max = (size_t)1 << 30;                  /* 1 GiB */
    char *buf = mmap(NULL, max, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (buf == MAP_FAILED) { perror("mmap"); return 1; }
    if (huge) madvise(buf, max, MADV_HUGEPAGE);
    memset(buf, 1, max);                                 /* touch every page once */

    printf("size_kib,ns_per_load\n");
    /* sizes: 4 KiB .. 1 GiB, four points per doubling */
    for (double s = 4096; s <= (double)max + 1; s *= 1.189207115) {
        size_t size = ((size_t)s / LINE) * LINE, n = size / LINE;
        if (n < 2) continue;

        /* random cyclic permutation of the n lines (Sattolo's algorithm) */
        size_t *order = malloc(n * sizeof *order);
        for (size_t i = 0; i < n; i++) order[i] = i;
        for (size_t i = n - 1; i > 0; i--) { size_t j = rnd() % i; size_t t = order[i]; order[i] = order[j]; order[j] = t; }
        for (size_t i = 0; i < n; i++)
            *(char **)(buf + order[i] * LINE) = buf + order[(i + 1) % n] * LINE;
        free(order);

        /* warm up, then time enough steps for ~0.2 s */
        char *p = buf;
        for (size_t i = 0; i < n; i++) p = *(char **)p;
        size_t steps = 1 << 20; double t;
        for (;;) {
            double t0 = now_ns();
            for (size_t i = 0; i < steps; i++) p = *(char **)p;
            t = now_ns() - t0;
            if (t > 2e8 || steps > ((size_t)1 << 30)) break;
            steps *= 2;
        }
        printf("%.1f,%.3f\n", size / 1024.0, t / steps + (p == NULL));  /* use p so it is not optimised away */
        fflush(stdout);
    }
    return 0;
}
