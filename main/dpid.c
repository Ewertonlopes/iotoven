#define N_filter 100

struct controlpid
{
    float __kp;
    float __ki;
    float __kd;

    float B0;
    float B1;
    float B2;
    float A0;
    float A1;
    float A2;

    float state[4];
    float Ts;

    float *in;
    float *out;
    float *setp;

    float ulim;
    float llim;
};

typedef struct controlpid upid;
typedef struct controlpid* ppid;

void pid_tune(ppid pid, float kp, float ki, float kd)
{
    if(kp<0 || ki <0 || kd<0) return;
    float Ts = pid->Ts;
    pid->B0 = kp*(1+N_filter*Ts) + ki*Ts*(1+N_filter*Ts) + kd*N_filter;
    pid->B1 = -kp*(1+N_filter*Ts) + ki*Ts + 2*kd*N_filter;
    pid->B2 = kp + kd*N_filter;

    pid->A0 = 1 + N_filter*Ts;
    pid->A1 = -(2 + N_filter*Ts);
    pid->A2 = 1;

    pid->__kp = kp;
    pid->__ki = ki;
    pid->__kd = kd;
}

void pid_stime(ppid pid, float sample_time)
{
    pid->Ts = sample_time;
    pid_tune(pid,pid->__kp,pid->__ki,pid->__kd);
}


ppid pid_create(ppid pid, float* in, float* out, float* setpoint, float kp, float ki, float kd,float ulim, float llim,float sTime)
{
    pid->in = in;
    pid->out = out;
    pid->setp = setpoint;

    pid->Ts = sTime;

    pid->ulim = ulim;
    pid->llim = llim;

    pid_tune(pid,kp,ki,kd);
    memset(pid->state,0,4u*sizeof(float));
    return pid;
}


void pid_run(ppid pid)
{
    float in = *(pid->in);
    float error = (*(pid->setp) - in);

    float output = -(pid->A1/pid->A0)*pid->state[2] - (pid->A2/pid->A0)*pid->state[3] 
                    + (pid->B0/pid->A0)*error + (pid->B1/pid->A0)*pid->state[0] + (pid->B2/pid->A0)*pid->state[1];


    if(output > pid->ulim) output = pid->ulim;
    else if(output < pid->llim) output = pid->llim;

    pid->state[1] = pid->state[0];
    pid->state[0] = error;
    pid->state[3] = pid->state[2];
    pid->state[2] = output;

    *(pid->out) = output;
}