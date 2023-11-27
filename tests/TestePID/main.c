#include<time.h>
#include <stdio.h>
#include <stdlib.h>

#include "pid.c"

void delay(unsigned int milliseconds){

    clock_t start = clock();

    while((clock() - start) * 1000 / CLOCKS_PER_SEC < milliseconds);
}

float in,out,set,amb = 0.0f;
int temp = 0;
upid mainpid;

int main()
{
    srand(time(NULL));
    pid_create(&mainpid,&in,&out,&set,92.94,1.42,11.72,8192,0);

    amb = 25.0f;
    float pld[10] = {};
    int pldi = 0;
    out = 0.0f;
    set = 30.0f;
    temp = 0;
    float current = 4000/8192.0f;
    
    while(1)
    {
        float rc = 627;
        float c = 722.38f*current/(0.69f*current + 0.1325f);

        // pid_run(&mainpid);
        // pld[pldi++] = out;
        // in = amb + (((float)rand() / RAND_MAX) - 0.5);
        amb += (1.0f/c)*(((current*220.0f)*(current*220.0f)/67.0f)) - (amb-25.0f)/(10.1258*61.839);
        // if(pldi > 9) pldi = 0;        
        printf("Amb: %f\n",amb);
        //printf("IN: %f\nOUT: %f\nSETPOINT: %f\n\n", in,out,set);
        // if((temp++)%10 == 0)
        // {
        //     set += 1.0;
        // }
        delay(20);
    }

    return 0;
}