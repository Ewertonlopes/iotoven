#include "definitions.h"
#include "hal.c"
#include "comms.c"

// GLOBAL VARIABLES

float temperature = 0.0f;

//TASK CREATION

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
      temperature = res*0.25;
    }
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

esp_err_t data_handler(httpd_req_t *req)
{
    char resp[40];
    snprintf(buffer, 40 "%f", temperature);
    httpd_resp_send(req, resp, HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}


void app_main(void)
{
    //Initialize NVS
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
      ESP_ERROR_CHECK(nvs_flash_erase());
      ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    init_pwm();

    spi_device_handle_t spi;
    spi = spi_init();
    xTaskCreate(&temp_task, "temperature_task", 4096, spi, 5, NULL);

    wifi_init_softap();

    init_webserver();

    while (1) 
    {
        if(temperature >= 30)
        {
            change_pwm(4090);
        }
        else
        {
            change_pwm(1060);
        }
        
        vTaskDelay(500 / portTICK_PERIOD_MS);
    }
}
