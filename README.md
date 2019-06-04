A python script to run as an AWS Lambda function.

Runs every hour and if it's the closest hour to sunset, it will send a
PushBullet notification.

Built using python `3.7`.

## How to deploy

  1. make sure you have `zappa` installed
      ```bash
      pip install zappa
      ```
  1. for the first deploy, use
      ```bash
      zappa deploy dev
      ```
  1. on subsequent deploys, use
      ```bash
      zappa update dev
      ```
  1. open the Lambda console and define an env var for the function: `PB_TOKEN`. The value is your PushBullet API token

## TODO

  - handle the env var better, but still keep it secret
  - look at getting the function to schedule the next run at the next sunset time, then it only needs to run once per day

## Timezones

5pm in Adelaide winter time is 7:30am GMT.
9pm in Adelaide summer time is 10:30am GMT.
