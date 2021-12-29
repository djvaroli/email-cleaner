# Email Cleaner (for Gmail)


I have a problem. I let emails linger on for far too long. You know the emails I'm talking about. 
Those useless promotions that I signed up for to get the 10% discount for that one purchase.

So I built this little thing that lets me:

1. View who has sent me the most emails so that I can focus my deleting efforts.
2. Automatically delete emails from certain senders. 

In reality I probably could do this manually, or set a rule to delete emails that are older than some number of days, 
but often there are emails that I do want to hang on to and I am not always the best 
at starring or preserving said emails. Plus it's fun to get some data insights into your 
email inbox. 


## Running Yourself

If you decide to try this out yourself, I would advise that you familiarize yourself with how the code works.
The last thing you want is to put your entire inbox into the trash. 

You'll also need to create some directories and a  `.env` file. You should be able to just run
`cd app && bash scripts/setup.sh`. 

You might need a Twillio account (depending on what parts of the code you decide to try). (https://www.twilio.com/try-twilio).
You don't need to pay for a trial project.

And just to be safe - if you delete your entire inbox by accident, that is on you. Sorry :(.


