/*
 * clock.c - estimate the running core clock from a chain of dependent integer adds
 * (ELL305 term paper, 5600X measurement kit)
 *
 * Each add depends on the previous one and takes one cycle on Zen 3, so adds per
 * nanosecond = clock in GHz. This is the method Chips and Cheese use to estimate clocks.
 * Run it right before or after a measurement so ns can be converted to cycles.
 *
 * Build:  gcc -O1 -o clock clock.c
 * Run:    ./clock [--cpu N]
 */
#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static double now_ns(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec * 1e9 + t.tv_nsec; }

int main(int argc, char **argv) {
    int cpu = 0;
    for (int i = 1; i < argc; i++) if (!strcmp(argv[i], "--cpu") && i + 1 < argc) cpu = atoi(argv[++i]);
    cpu_set_t s; CPU_ZERO(&s); CPU_SET(cpu, &s); sched_setaffinity(0, sizeof s, &s);
    const long N = 400000000L;          /* 4e8 iterations x 10 adds */
    double best = 0;
    for (int trial = 0; trial < 5; trial++) {
        long x = trial, y = argc;        /* register-register adds: not removed by the renamer */
        double t0 = now_ns();
        for (long i = 0; i < N; i++) {
            __asm__ volatile("add %1, %0\n\tadd %1, %0\n\tadd %1, %0\n\tadd %1, %0\n\tadd %1, %0\n\t"
                             "add %1, %0\n\tadd %1, %0\n\tadd %1, %0\n\tadd %1, %0\n\tadd %1, %0" : "+r"(x) : "r"(y));
        }
        double t = now_ns() - t0;
        double ghz = 10.0 * N / t;         /* ten dependent one-cycle adds per iteration; the loop
                                              counter runs in parallel on another ALU */
        if (ghz > best) best = ghz;
        if (x == 42) printf(" ");
    }
    printf("cpu,estimated_ghz\n%d,%.3f\n", cpu, best);
    return 0;
}
