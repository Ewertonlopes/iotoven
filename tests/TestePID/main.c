#include<time.h>
#include <stdio.h>
#include <stdlib.h>

#include "pid.c"

void delay(unsigned int milliseconds){

    clock_t start = clock();

    while((clock() - start) * 1000 / CLOCKS_PER_SEC < milliseconds);
}

float in,out,set,amb = 0.0f;
upid mainpid;

int main()
{
    srand(time(NULL));
    pid_create(&mainpid,&in,&out,&set,6,0.02,0,280,0);

    amb = 25.0f;
    float pld[10] = {};
    int pldi = 0;
    out = 0.0f;
    set = 50.0f;
    
    while(1)
    {
        pid_run(&mainpid);
        pld[pldi++] = out;
        in = amb + (((float)rand() / RAND_MAX) - 0.5);
        amb += 0.008*pld[9]-0.001f*(in-25.0f);
        if(pldi > 9) pldi = 0;        
        printf("IN: %f\nOUT: %f\nSETPOINT: %f\n\n", in,out,set);
        delay(1000);
    }

    return 0;
}