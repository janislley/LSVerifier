#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

// This function must be excluded from list since it is called by void_func()
void excluded() {
    printf("excluded()\n");
}

// This function might be excluded from list since it is called by main()
void void_func() {
    excluded();
    int i;
    i = 0;
}

void bit_shift() {
    int i;
    int j;
    i = 1;
    j = i << 1;
}

void malloc_func() {
    int *i = (int *)malloc(2*sizeof(int));
}

void* ptr_func(void *arg) {
  char *ptr = (char *)(arg);
  free(ptr);
  ptr = NULL;
  *ptr = 'a'; // Expected error here
}

// This function must be excluded from list since it is called by pthread_create()
void* do_job(void* arg) {
    char *msg = (char*)(arg);
    printf("%s\n", msg);
}

void thread_func() {
    pthread_t thread1;
    char* message = "thread1";
    pthread_create(&thread1, NULL, do_job, (void *)(message));
    pthread_join(thread1, NULL);
}

void vector_func(char c[]) {
    c[2] = 'a';
    int i[1];
    i[2] = 1; // Expected error here
}

int main(void) {
 void_func();
 return 0;
}

