#include <stdio.h>
#include <stdlib.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "driver/ledc.h"
#include "driver/adc.h"
#include "driver/spi_master.h"

#include <esp_log.h>

static const char *TAG = "example";

#define LEDC_GPIO 21
static ledc_channel_config_t ledc_channel;

#define MOSI_PIN 23
#define MISO_PIN 19
#define SCK_PIN 18
#define SS_PIN 5

#define DMA_CHAN 2

//#define SAMPLE_CNT 32
//static const adc1_channel_t adc_channel = ADC_CHANNEL_5;

/* SPI Config */
spi_device_handle_t spi_init(void) {
  spi_device_handle_t spi;
  esp_err_t ret;
  spi_bus_config_t buscfg = {
    .miso_io_num = MISO_PIN,
    .mosi_io_num = MOSI_PIN,
    .sclk_io_num = SCK_PIN,
    .quadwp_io_num = -1,
    .quadhd_io_num = -1,
    .max_transfer_sz = (4 * 8)
  };
  /* Initialize the SPI bus */
  ret = spi_bus_initialize(VSPI_HOST, &buscfg, DMA_CHAN);
  ESP_ERROR_CHECK(ret);
  spi_device_interface_config_t devCfg={
    .mode = 0,
    .clock_speed_hz = 2*1000*1000,
    .spics_io_num=SS_PIN,
    .queue_size=3
  };
  ret = spi_bus_add_device(VSPI_HOST, &devCfg, &spi);
  ESP_ERROR_CHECK(ret);
  return spi;
}


void temp_task(void * pvParams) {
  spi_device_handle_t spi = (spi_device_handle_t) pvParams;
  uint16_t data;
  spi_transaction_t tM = {
    .tx_buffer = NULL,
    .rx_buffer = &data,
    .length = 16 /* bits */,
    .rxlength = 16 /* bits */,
  };
  for (;;) {
    spi_device_acquire_bus(spi, portMAX_DELAY);
    spi_device_transmit(spi, &tM);
    spi_device_release_bus(spi);
    uint16_t res = SPI_SWAP_DATA_RX(data, 16);
    if (res & (1 << 14))
      ESP_LOGE(TAG, "Temperature probe is not connected\n");
    else {
      res >>= 3;
      printf("SPI res = %d temp=%f\n", res, res * 0.25);
    }
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

void init_pwm()
{
    ledc_timer_config_t ledc_timer = 
    {
        .duty_resolution = LEDC_TIMER_13_BIT,
        .freq_hz = 500,
        .speed_mode = LEDC_HIGH_SPEED_MODE,
        .timer_num = LEDC_TIMER_0,
        .clk_cfg = LEDC_AUTO_CLK,
    };

    /* Configure the peripheral according to the LED type */
    ledc_timer_config(&ledc_timer);
    ledc_channel.channel = LEDC_CHANNEL_0;
    ledc_channel.duty = 0;
    ledc_channel.gpio_num = LEDC_GPIO;
    ledc_channel.speed_mode = LEDC_HIGH_SPEED_MODE;
    ledc_channel.hpoint = 0;
    ledc_channel.timer_sel = LEDC_TIMER_0;
    ledc_channel_config(&ledc_channel);
}

void app_main(void)
{
    //adc1_config_width(ADC_WIDTH_BIT_12);
    //adc1_config_channel_atten(adc_channel, ADC_ATTEN_DB_11);

    init_pwm();

    spi_device_handle_t spi;
    spi = spi_init();
    xTaskCreate(&temp_task, "temperature_task", 4096, spi, 5, NULL);


    while (1) 
    {
        // int adc_val = 0;
        // for (int i = 0; i < SAMPLE_CNT; ++i)
        // {
        //     adc_val += adc1_get_raw(adc_channel);
        // }
        // adc_val /= SAMPLE_CNT;
        // adc_val = adc_val*2;
        
        //ESP_LOGI(TAG, "Changing %d\r\n", adc_val);

        //ledc_set_duty(ledc_channel.speed_mode, ledc_channel.channel, adc_val);
        //ledc_update_duty(ledc_channel.speed_mode, ledc_channel.channel);
        vTaskDelay(500 / portTICK_PERIOD_MS);
    }
}
