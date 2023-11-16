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
  float MMtemp[WINDOW_SIZE] = {};
  int currentIndex = 0;
  while (1) 
  {
    spi_device_acquire_bus(spi, portMAX_DELAY);
    spi_device_transmit(spi, &tM);
    spi_device_release_bus(spi);
    uint16_t res = SPI_SWAP_DATA_RX(data, 16);
    if (res & (1 << 14))
      ESP_LOGE(TAG, "Temperature probe is not connected\n");
    else {
      res >>= 3;
      float ntemperature = res*0.25f;
      MMtemp[currentIndex] = ntemperature;
      currentIndex = (currentIndex + 1)%WINDOW_SIZE;
      float movingMean = 0.0f;
      for(int i=0;i<WINDOW_SIZE;++i)
      {
        movingMean+=MMtemp[i];
      }
      movingMean /= WINDOW_SIZE;
      temperature = movingMean;
    }

    vTaskDelay(pdMS_TO_TICKS(1500));
  }
}

void pid_task(void * pvParams) 
{
  ppid pid = pvParams;
  //pid_create(pid,&in,&out,&set,1.2f,0.0005f,0.5f,285,0);
  pid_create(pid,&in,&out,&set,30.0f,0.0f,0.0f,285,0);
  while (1) 
  {
    in = temperature;
    pid_run(pid);
    vTaskDelay(pdMS_TO_TICKS(1500));
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
      //ESP_LOGI(TAG,"\nsetpoint: %f\nKp: %f\nKi: %f\nKd: %f\nTune: %d", set,kp,ki,kd,tune);
      ///__uint16_t signal = out * 32;
      __uint16_t signal = (__uint16_t)set;
      if(signal>8192) signal = 8192;
      change_pwm(signal);
      if(tune)
      {
        pid_tune(&mainpid,kp,ki,kd);
        tune = 0;
        ESP_LOGI(TAG,"PID TUNED");
      }
  
      vTaskDelay(pdMS_TO_TICKS(160));
    }
}