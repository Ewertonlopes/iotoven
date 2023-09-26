#ifndef _definitions_h
#define _definitions_h

#include <stdio.h>
#include <stdlib.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "driver/ledc.h"
#include "driver/adc.h"
#include "driver/spi_master.h"

#include <esp_log.h>

static const char *TAG = "iotOven";

#define LEDC_GPIO 21
static ledc_channel_config_t ledc_channel;

#define MOSI_PIN 23
#define MISO_PIN 19
#define SCK_PIN 18
#define SS_PIN 5

#define DMA_CHAN 2

#endif