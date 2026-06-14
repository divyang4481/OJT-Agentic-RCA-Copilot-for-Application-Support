# Standard Operating Procedure: Service X High CPU and 5xx Errors

## Overview
This runbook covers the triage and remediation steps for when Service X experiences a sudden spike in CPU utilization accompanied by 5xx HTTP responses.

## Symptoms
- CloudWatch alarms trigger for `CPUUtilization > 85%` for 5 consecutive minutes.
- API Gateway reports increased 500 or 502 error rates for Service X.
- Application logs show `Memory exhaustion detected` or `OOM killer` invocations.

## Probable Causes
1. **Memory Leak**: A recent deployment introduced a memory leak, causing the garbage collector to consume excessive CPU, eventually leading to OOM.
2. **Traffic Spike**: A sudden influx of requests overwhelming the current autoscaling group limits.
3. **Database Connection Starvation**: Connections to the database pool are timing out, causing threads to hang and consume resources.

## Immediate Remediation Steps
1. **Restart Instances**: Temporarily mitigate the issue by restarting the failing pods/instances to clear memory.
2. **Scale Up**: Increase the `DesiredCapacity` of the Auto Scaling Group by 50% to handle immediate load.
3. **Check Deployments**: Review the CI/CD pipeline for any deployments within the last 24 hours. Roll back if a suspect commit is identified.

## Escalation
If the issue persists after instance restarts and scaling, escalate to the **L3 Backend Engineering Team** immediately. Include logs showing memory dumps or OOM events.
