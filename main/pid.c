struct controlpid
{
    float kp;
    float ki;
    float kd;

    float *in;
    float *out;
    float *setp;
    
    float iacc;
    float lastterm;

    float ulim;
    float llim;
};

typedef struct controlpid* upid;

upid pid_create(upid pid, float* in, float* out, float* setpoint, float kp, float ki, float kd,float ulim, float llim)
{
    pid->in = in;
    pid->out = out;
    pid->setp = setpoint;

    pid->ulim = ulim;
    pid->llim = llim;

    pid_tune(pid,kp,ki,kd);

    return pid;
}

void pid_tune(upid pid, float kp, float ki, float kd)
{
    if(kp<0 || ki <0 || kd<0) return;

    pid->kp = kp;
    pid->ki = ki;
    pid->kd = kd;
}

void pid_constrain(upid pid)
{
    if(pid->iacc > pid->ulim) pid->iacc = pid->ulim;
    if(pid->iacc < pid->llim) pid->iacc = pid->llim;
    return;
}

void pid_run(upid pid)
{
    float in = *(pid->in);
    float error = (*(pid->setp) - in);

    //Integral Output
    pid->iacc += (pid->ki * error);
    if(pid->iacc > pid->ulim) pid->iacc = pid->ulim;
    if(pid->iacc < pid->llim) pid->iacc = pid->llim;

    //Diferential Output
    float diff = in - pid->lastterm;

    //Output of the pid
    float output = pid->kp * error + pid->iacc - pid->kd * diff;

    if(output > pid->ulim) output = pid->ulim;
    if(output < pid->llim) output = pid->llim;

    *(pid->out) = output;

    pid-> lastterm = in;
}