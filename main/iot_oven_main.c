#include "definitions.h"
#include "hal.c"
#include "comms.c"
#include "pid.c"

//GLOBAL VARIABLES


//TASK CREATION
void temp_task(void * pvParams) 
{
  TickType_t xLastWakeTime;
  const TickType_t xFrequency = pdMS_TO_TICKS(250);

  spi_device_handle_t spi = (spi_device_handle_t) pvParams;
  uint16_t data;
  spi_transaction_t tM = {
    .tx_buffer = NULL,
    .rx_buffer = &data,
    .length = 16 /* bits */,
    .rxlength = 16 /* bits */,
  };

  xLastWakeTime = xTaskGetTickCount();

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
      temperature = res*0.25f;
      in = (temperature/360.0f) * 100.0f;
    }

    vTaskDelayUntil(&xLastWakeTime, xFrequency);
  }
}

void pid_task(void * pvParams) 
{
  ppid pid = pvParams;

  TickType_t xLastWakeTime;
  const TickType_t xFrequency = pdMS_TO_TICKS(250);
  xLastWakeTime = xTaskGetTickCount();
  __uint16_t pwm = 0;
  //ZN - Kp 7.7289774 - Ki 2.3397828 - Kp 6.3827603
  //CC - Kp 8.8938832 - Ki 2.2633317 - Kp 5.3070582
  pid_create(pid,&in,&out,&set,7.729f,2.340f,6.383f,100,0); 
  while (1) 
  {
    change_pwm(pwm);
    pid_run(pid);
    pwm = (__uint16_t)(out * 81.92f);
    vTaskDelayUntil(&xLastWakeTime, xFrequency);
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
    xTaskCreate(&pid_task, "PID_cycle", 4096, &mainpid, 2, &pid_handle);

    wifi_init_softap();

    init_webserver();

    while (1) 
    {
      if(change)
      {
        if(local)
        {
          vTaskResume(pid_handle);
          change = 0;
        }
        else
        {
          vTaskSuspend(pid_handle);
          change = 0;
        }
      }

      if(tune)
      {
        pid_tune(&mainpid,kp,ki,kd);
        tune = 0;
        ESP_LOGI(TAG,"PID TUNED");
      }

  
      vTaskDelay(pdMS_TO_TICKS(250));
    }
}