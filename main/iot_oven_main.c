#include "definitions.h"
#include "hal.c"
#include "comms.c"
#include "pid.c"

//GLOBAL VARIABLES


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
  while (1) {
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
    vTaskDelay(pdMS_TO_TICKS(300));
  }
}

void pid_task(void * pvParams) 
{
  ppid pid = pvParams;
  pid_create(pid,&in,&out,&set,2,0.5,0.02,256,0);
  while (1) 
  {
    in = temperature;
    set = 220;
    pid_run(pid);
    vTaskDelay(pdMS_TO_TICKS(350));
  }
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
    xTaskCreate(&temp_task, "Temperature_task", 4096, spi, 5, NULL);

    upid mainpid;    
    xTaskCreate(&pid_task, "PID_cycle", 4096, &mainpid, 2, NULL);

    wifi_init_softap();

    init_webserver();

    while (1) 
    {
      __uint16_t signal = mainpid->out * 32
      if(signal>8192) signal = 8192;
      change_pwm(signal);
      vTaskDelay(pdMS_TO_TICKS(400));
    }
}
