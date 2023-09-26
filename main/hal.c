#include "definitions.h"

/* SPI CONFIG */
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

/* PWM CONFIG*/
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

void change_pwm(int change_value)
{
    ledc_set_duty(ledc_channel.speed_mode, ledc_channel.channel, change_value);
    ledc_update_duty(ledc_channel.speed_mode, ledc_channel.channel);
}