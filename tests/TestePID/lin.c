#include <stdio.h>

// Function to calculate the slope (m) and intercept (b) of the best-fit line
void linearRegression(int time[], int temp[], int n, float *slope, float *intercept) {
    int sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;

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
    int time[] = { /* Your time values here */ };
    int temp[] = { /* Your temperature values here */ };
    int n = sizeof(time) / sizeof(time[0]);

    float slope, intercept;

    // Calculate the slope and intercept of the best-fit line
    linearRegression(time, temp, n, &slope, &intercept);

    // Print the equation of the best-fit line
    printf("Best-fit line: y = %.2fx + %.2f\n", slope, intercept);

    return 0;
}