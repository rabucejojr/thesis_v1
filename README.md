# Setting up Crontab for Automation

Crontab is a utility in Unix-like operating systems that allows users to schedule tasks to run periodically at fixed times, dates, or intervals. This README provides instructions on setting up Crontab for automating tasks, specifically for scheduling Python scripts to run at startup.

## For this project:

Use the following command:

```bash
@reboot python3 /home/admin/Desktop/thesis_v1/piggery_hardware_controller.py
```

## List Existing Cron Jobs

To view a list of existing cron jobs, use the following command:

```bash
crontab -l
```

## Edit Cron Jobs

To edit the list of cron jobs, use the following command:

```bash
crontab -e
```

## Remove Cron Jobs

To remove all cron jobs for the current user, use the following command:

```bash
crontab -r
```
