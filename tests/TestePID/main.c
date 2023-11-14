#include<time.h>
#include <stdio.h>

#include "pid.c"

void delay(unsigned int milliseconds){

    clock_t start = clock();

    while((clock() - start) * 1000 / CLOCKS_PER_SEC < milliseconds);
}

float in,out,set = 100;
upid mainpid;

int main()
{
    // upid mainpid = (upid)malloc(sizeof(upid));
    // float* in = (float*)malloc(sizeof(float));
    // float* out = (float*)malloc(sizeof(float));
    // float* set = (float*)malloc(sizeof(float));

    pid_create(&mainpid,&in,&out,&set,2,0.5,0.02,280,2);

    in = 1.0f;
    out = 0.0f;
    set = 20.0f;

    
    while(1)
    {
        pid_run(&mainpid);
        in += 0.05*out-0.05*in;
        printf("IN: %f\nOUT: %f\nSETPOINT: %f\n", in,out,set);
        delay(1000);
    }

    return 0;
}