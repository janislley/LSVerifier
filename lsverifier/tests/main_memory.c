#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>

// Global variables for data race example
int shared_counter = 0;

// Data Race Example
void *increment_shared_counter(void *arg) {
    shared_counter++;
    return NULL;
}

void data_race() {
    pthread_t thread1, thread2;
    pthread_create(&thread1, NULL, increment_shared_counter, NULL);
    pthread_create(&thread2, NULL, increment_shared_counter, NULL);
    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);
    printf("Data race example: shared_counter = %d (Should be 2)\n", shared_counter);
}

// Memory Leak Example
void memory_leak() {
    for (int i = 0; i < 1000; i++) {
        int *ptr = (int*) malloc(100 * sizeof(int));
        // forgetting to free the allocated memory
    }
    printf("Memory leak example executed\n");
}

// Overflow Example
void overflow() {
    int max_int = 2147483647;
    int overflowed = max_int + 1;
    printf("Overflow example: %d\n", overflowed);
}

// Deadlock Example
pthread_mutex_t lock1 = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t lock2 = PTHREAD_MUTEX_INITIALIZER;

void *task_one(void *arg) {
    pthread_mutex_lock(&lock1);
    printf("Task One acquired lock1...\n");
    sleep(1); // Simulating some task

    printf("Task One trying to acquire lock2...\n");
    pthread_mutex_lock(&lock2);

    printf("Task One acquired both locks, doing work...\n");

    pthread_mutex_unlock(&lock2);
    pthread_mutex_unlock(&lock1);
    return NULL;
}

void *task_two(void *arg) {
    pthread_mutex_lock(&lock2);
    printf("Task Two acquired lock2...\n");
    sleep(1); // Simulating some task

    printf("Task Two trying to acquire lock1...\n");
    pthread_mutex_lock(&lock1);

    printf("Task Two acquired both locks, doing work...\n");

    pthread_mutex_unlock(&lock1);
    pthread_mutex_unlock(&lock2);
    return NULL;
}

void deadlock() {
    pthread_t thread1, thread2;
    pthread_create(&thread1, NULL, task_one, NULL);
    pthread_create(&thread2, NULL, task_two, NULL);
    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);
    printf("Deadlock example executed (or not, if actually deadlocked)\n");
}

int main() {
    data_race();
    memory_leak();
    overflow();
    deadlock();
    return 0;
}
