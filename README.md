# EBoxConsumptionChecker
Python script checking the consumption of an Electronic Box (EBOX) ISP account, buy new data block if the current data limit is reached and notify  the user on the current status.

## Details
Ebox is a great ISP but they don't notify you if you bust your monthly limit. You have to go check that yourself.

In its current form the script will: 
  * Fetch the data on the ebox client interface
  * Print data usage on screen
  * Send an SMS using Twilio to notify the user about current usage
  * Buy a new data block if the monthly limit has been reached

cron or the Windows Taks Scheduler could be used to run the script on a recurring basis.

TODO:
  * Add an alternative method to remotely notify the user, such as email, about the current status 
  * Convert the script for it to be run as an Azure function
  * When running locally, display status more convieniently such as a notification


*P.S. This project was written has a pretext to learn python. Code is working but isn't optimal and wasn't cleaned up.*
