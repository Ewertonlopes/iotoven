#include <stdio.h>

void linearRegression(float time[], float temp[], int n, float *slope, float *intercept) {
    float sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;

    for (int i = 0; i < n; i++) {
        sumX += time[i];
        sumY += temp[i];
        sumXY += time[i] * temp[i];
        sumX2 += time[i] * time[i];
    }

    *slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    *intercept = (sumY - *slope * sumX) / n;
}


int main() {


    float temp[] = { 76.25,76.00,75.75,75.75,75.25,75.50,75.50,75.50,75.50,75.50,
                   75.50,75.50,75.00,74.75,75.25,79.00,79.25,79.00,79.00,78.75,
                   78.25,78.00,78.50,78.75,78.50,78.25,78.25,78.50,78.00,78.00,
                   78.00,78.25,77.50,77.75,78.00,77.50,77.25,77.50,76.75,77.50,
                   77.50,76.75,77.25,77.00,76.75,77.25,77.25,76.50,76.75,77.00,
                   76.75,76.50,76.25,76.25,76.50,76.50,76.25,76.25,76.25,76.00 };
    
    // float time[] = {60,60,60,60,60,60,60,60,60,60,
    //                 60,60,60,60,60,60,60,60,60,60,
    //                 60,60,60,60,60,60,60,60,60,60,
    //                 60,60,60,60,60,60,60,60,60,60,
    //                 60,60,60,60,60,60,60,60,60,60,
    //                 60,60,60,60,60,60,60,60,60,60};

    float time[] = { 1,2,3,4,5,6,7,8,9,10,
                   11,12,13,14,15,16,17,18,19,20,
                   21,22,23,24,25,26,27,28,29,30,
                   31,32,33,34,35,36,37,38,39,40,
                   41,42,43,44,45,46,47,48,49,50,
                   51,52,53,54,55,56,57,58,59,60};
                   
    int n = 60;

    float slope, intercept;

    // Calculate the slope and intercept of the best-fit line
    linearRegression(time, temp, n, &slope, &intercept);

    // Print the equation of the best-fit line
    printf("Best-fit line: y = %.2fx + %.2f\n", slope, intercept);

    return 0;
}