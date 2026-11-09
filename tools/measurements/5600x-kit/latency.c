/*
 * latency.c - pointer-chasing latency sweep and memory-level-parallelism test
 * (ELL305 term paper, 5600X measurement kit)
 *
 * Sweep mode (default): walks a randomly permuted cyclic chain of 64-byte lines in a
 * buffer of increasing size and reports the average time per dependent load. Each load's
 * address depends on the previous one, so the core cannot overlap them: the time per step
 * is the latency of whichever level of the hierarchy holds the buffer.
 *
 * MLP mode (--chains K --size-mib S): walks K independent chains through one buffer of S MiB,
 * one load from each chain per step. The loads of different chains do not depend on each
 * other, so the core can overlap them; the time per load shows how many misses it keeps in flight.
 *
 * Build:  gcc -O2 -o latency latency.c
 * Run:    ./latency [--huge] [--cpu N]                       sweep, CSV to stdout
 *         ./latency [--huge] [--cpu N] --chains 1..16 --size-mib 1024   MLP point
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
#define MAXCH 16

static double now_ns(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec * 1e9 + t.tv_nsec; }
static uint64_t rng = 88172645463325252ULL;
static uint64_t rnd(void) { rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }

static size_t *build_chain(char *buf, size_t n) {          /* Sattolo: one random cycle through n lines */
    size_t *order = malloc(n * sizeof *order);
    for (size_t i = 0; i < n; i++) order[i] = i;
    for (size_t i = n - 1; i > 0; i--) { size_t j = rnd() % i; size_t t = order[i]; order[i] = order[j]; order[j] = t; }
    for (size_t i = 0; i < n; i++) *(char **)(buf + order[i] * LINE) = buf + order[(i + 1) % n] * LINE;
    return order;
}

int main(int argc, char **argv) {
    int huge = 0, cpu = 0, chains = 0; double size_mib = 1024;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--huge")) huge = 1;
        else if (!strcmp(argv[i], "--cpu") && i + 1 < argc) cpu = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--chains") && i + 1 < argc) chains = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--size-mib") && i + 1 < argc) size_mib = atof(argv[++i]);
        else { fprintf(stderr, "usage: %s [--huge] [--cpu N] [--chains K --size-mib S]\n", argv[0]); return 2; }
    }
    cpu_set_t set; CPU_ZERO(&set); CPU_SET(cpu, &set);
    if (sched_setaffinity(0, sizeof set, &set) != 0) perror("sched_setaffinity (continuing)");

    const size_t max = (size_t)1 << 30;
    char *buf = mmap(NULL, max, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (buf == MAP_FAILED) { perror("mmap"); return 1; }
    if (huge) madvise(buf, max, MADV_HUGEPAGE);
    memset(buf, 1, max);

    if (chains > 0) {                                        /* ---- MLP mode ---- */
        if (chains > MAXCH) chains = MAXCH;
        size_t size = (size_t)(size_mib * 1048576.0); if (size > max) size = max;
        size_t n = size / LINE;
        size_t *order = build_chain(buf, n);
        char *p[MAXCH];
        for (int k = 0; k < chains; k++) p[k] = buf + order[(size_t)k * (n / chains)] * LINE;
        free(order);
        size_t steps = (size_t)1 << 18; double t;
        for (;;) {
            double t0 = now_ns();
            for (size_t i = 0; i < steps; i++)
                for (int k = 0; k < chains; k++) p[k] = *(char **)p[k];
            t = now_ns() - t0;
            if (t > 3e8 || steps > ((size_t)1 << 28)) break;
            steps *= 2;
        }
        uintptr_t sink = 0; for (int k = 0; k < chains; k++) sink ^= (uintptr_t)p[k];
        printf("chains,size_mib,ns_per_load,ns_per_step\n%d,%.0f,%.3f,%.3f\n", chains, size_mib,
               t / ((double)steps * chains) + (sink == 1), t / steps);
        return 0;
    }

    printf("size_kib,ns_per_load\n");                        /* ---- sweep mode ---- */
    for (double s = 4096; s <= (double)max + 1; s *= 1.189207115) {
        size_t size = ((size_t)s / LINE) * LINE, n = size / LINE;
        if (n < 2) continue;
        free(build_chain(buf, n));
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
        printf("%.1f,%.3f\n", size / 1024.0, t / steps + (p == NULL));
        fflush(stdout);
    }
    return 0;
}
