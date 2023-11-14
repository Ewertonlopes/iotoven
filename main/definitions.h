#ifndef _definitions_h
#define _definitions_h

//Base definitions
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

//Operacional System
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

//Communication
#include "esp_mac.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include <esp_http_server.h>

#define EXAMPLE_ESP_WIFI_SSID      "IoTOven"
#define EXAMPLE_ESP_WIFI_PASS      "01234567"
#define EXAMPLE_ESP_WIFI_CHANNEL   3
#define EXAMPLE_MAX_STA_CONN       5

//Drivers
#include "driver/ledc.h"
#include "driver/adc.h"
#include "driver/spi_master.h"

static const char *TAG = "iotOven";

#define LEDC_GPIO 21
static ledc_channel_config_t ledc_channel;

#define MOSI_PIN 23
#define MISO_PIN 19
#define SCK_PIN 18
#define SS_PIN 5

#define DMA_CHAN 2

//Logs
#include "lwip/err.h"
#include "lwip/sys.h"
#include <esp_log.h>


// MACROS

#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))

// GLOBAL VARIABLES

float temperature = 0.0f;
float in = 0.0f;
float out = 0.0f;
float set = 60.0f;
float kp = 2.0f;
float ki = 0.5f;
float kd = 0.02f;

#endif