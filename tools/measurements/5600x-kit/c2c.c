/*
 * c2c.c - core-to-core round-trip latency through one shared cache line
 * (ELL305 term paper, 5600X measurement kit)
 *
 * Two threads pinned to logical CPUs A and B take turns writing a shared counter:
 * A writes an odd value and waits for B to write the next even value, and so on.
 * Every hand-over moves the cache line from one core's private caches to the other's,
 * the access pattern of the paper's MSI worked example. Prints the round-trip time
 * (two hand-overs) for every pair of logical CPUs.
 *
 * Build:  gcc -O2 -pthread -o c2c c2c.c
 * Run:    ./c2c > c2c.csv
 */
#define _GNU_SOURCE
#include <pthread.h>
#include <sched.h>
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#define ROUNDS 200000
static _Alignas(64) _Atomic long flag;
static int cpu_b;

static void pin(int cpu) { cpu_set_t s; CPU_ZERO(&s); CPU_SET(cpu, &s); pthread_setaffinity_np(pthread_self(), sizeof s, &s); }
static double now_ns(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec * 1e9 + t.tv_nsec; }

static void *partner(void *arg) {
    (void)arg; pin(cpu_b);
    for (long i = 1; i < 2L * ROUNDS; i += 2) {
        while (atomic_load_explicit(&flag, memory_order_acquire) != i) ;
        atomic_store_explicit(&flag, i + 1, memory_order_release);
    }
    return NULL;
}

int main(void) {
    int n = (int)sysconf(_SC_NPROCESSORS_ONLN);
    printf("cpu_a,cpu_b,roundtrip_ns\n");
    for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) {
        if (a == b) continue;
        double best = 1e18;
        for (int trial = 0; trial < 3; trial++) {
            atomic_store(&flag, 0); cpu_b = b;
            pthread_t th; pthread_create(&th, NULL, partner, NULL);
            pin(a);
            double t0 = now_ns();
            for (long i = 0; i < 2L * ROUNDS; i += 2) {
                atomic_store_explicit(&flag, i + 1, memory_order_release);
                while (atomic_load_explicit(&flag, memory_order_acquire) != i + 2) ;
            }
            double t = (now_ns() - t0) / ROUNDS;
            pthread_join(th, NULL);
            if (t < best) best = t;
        }
        printf("%d,%d,%.1f\n", a, b, best);
        fflush(stdout);
    }
    return 0;
}
