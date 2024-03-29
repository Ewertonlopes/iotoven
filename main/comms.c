#include "definitions.h"

static void wifi_event_handler(void* arg, esp_event_base_t event_base,
                                    int32_t event_id, void* event_data)
{
    if (event_id == WIFI_EVENT_AP_STACONNECTED) {
        wifi_event_ap_staconnected_t* event = (wifi_event_ap_staconnected_t*) event_data;
        ESP_LOGI(TAG, "station "MACSTR" join, AID=%d",
                 MAC2STR(event->mac), event->aid);
    } else if (event_id == WIFI_EVENT_AP_STADISCONNECTED) {
        wifi_event_ap_stadisconnected_t* event = (wifi_event_ap_stadisconnected_t*) event_data;
        ESP_LOGI(TAG, "station "MACSTR" leave, AID=%d",
                 MAC2STR(event->mac), event->aid);
    }
}

void wifi_init_softap(void)
{
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_t * p_netif = esp_netif_create_default_wifi_ap();
    esp_netif_ip_info_t if_info;
    ESP_ERROR_CHECK(esp_netif_get_ip_info(p_netif, &if_info));
    ESP_LOGI(TAG, "ESP32 IP:" IPSTR, IP2STR(&if_info.ip));

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    ESP_ERROR_CHECK(esp_event_handler_instance_register(WIFI_EVENT,
                                                        ESP_EVENT_ANY_ID,
                                                        &wifi_event_handler,
                                                        NULL,
                                                        NULL));

    wifi_config_t wifi_config = {
        .ap = {
            .ssid = EXAMPLE_ESP_WIFI_SSID,
            .ssid_len = strlen(EXAMPLE_ESP_WIFI_SSID),
            .channel = EXAMPLE_ESP_WIFI_CHANNEL,
            .password = EXAMPLE_ESP_WIFI_PASS,
            .max_connection = EXAMPLE_MAX_STA_CONN,
            .pmf_cfg = {
                    .required = true,
            },
        },
    };
    if (strlen(EXAMPLE_ESP_WIFI_PASS) == 0) {
        wifi_config.ap.authmode = WIFI_AUTH_OPEN;
    }

    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_AP));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_AP, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());

    ESP_LOGI(TAG, "wifi_init_softap finished. SSID:%s password:%s channel:%d",
             EXAMPLE_ESP_WIFI_SSID, EXAMPLE_ESP_WIFI_PASS, EXAMPLE_ESP_WIFI_CHANNEL);
}

esp_err_t data_handler(httpd_req_t *req)
{
    char resp[40];
    snprintf(resp, 40, "%f", temperature);
    httpd_resp_send(req, resp, HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

static esp_err_t echo_post_receiver(httpd_req_t *req)
{
    char buf[100];
    int ret, remaining = req->content_len;

    while (remaining > 0) {
        if ((ret = httpd_req_recv(req, buf,
                        MIN(remaining, sizeof(buf)))) <= 0) {
            if (ret == HTTPD_SOCK_ERR_TIMEOUT) {
                /* Retry receiving if timeout occurred */
                continue;
            }
            return ESP_FAIL;
        }

        remaining -= ret;

        /* Log data received */
        ESP_LOGI(TAG, "=========== RECEIVED DATA ==========");
        ESP_LOGI(TAG, "%.*s", ret, buf);
        ESP_LOGI(TAG, "====================================");

        int mod = 0;
        int count1 = sscanf(buf, "mod:%u", &mod);
        if(count1)
        {
            char* remainder = buf + 6;
            if(mod == 3)
            {
                int count2 = sscanf(remainder, "loc:%u", &local);
                if(!count2) ESP_LOGI(TAG, "Failed to Parse change Data");
                else change = 1;
            }
            else if(mod == 2)
            {
                int count2 = sscanf(remainder, "o:%f", &out);
                if(!count2) ESP_LOGI(TAG, "Failed to Parse Runner Data");
            }
            else if(mod == 1)
            {
                int count2 = sscanf(remainder, "kp:%f,ki:%f,kd:%f", &kp, &ki, &kd);
                if(count2 != 3) ESP_LOGI(TAG, "Failed to Parse Tune Data");
                else tune = 1;
            }
            else if(mod == 0)
            {
                int count2 = sscanf(remainder, "s:%f", &set);
                if(!count2) ESP_LOGI(TAG, "Failed to Parse Setpoint");
                else set /= 350;
            }
        }
        else
        {
            ESP_LOGI(TAG, "Failed to Parse Mod Type");
        }
    }

    // End response
    httpd_resp_send_chunk(req, NULL, 0);
    return ESP_OK;
}




void init_webserver()
{
    esp_err_t httpd_start(httpd_handle_t *handle, const httpd_config_t *config);
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();
    httpd_handle_t server = NULL;
    if (httpd_start(&server, &config) == ESP_OK) {}

    esp_err_t httpd_register_uri_handler(httpd_handle_t handle, const httpd_uri_t *uri_handler);

    httpd_uri_t data_uri = {
    .uri      = "/",
    .method   = HTTP_GET,
    .handler  = data_handler,
    .user_ctx = NULL
    };

    const httpd_uri_t receiver = {
    .uri       = "/receiver",
    .method    = HTTP_POST,
    .handler   = echo_post_receiver,
    .user_ctx  = NULL
    };

    httpd_register_uri_handler(server, &receiver);
    httpd_register_uri_handler(server, &data_uri);
}