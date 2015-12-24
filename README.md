# Mint texting app.

Ever since Mint disabled their quickview app I have been at a loss for a quick way
to track my spending. It is quite a pain to go through the process of opening up
the browser and logging in or opening up their really slow iPhone app.

This app is a quick script that scrapes the mint site for your recent purchases,
then sends you a text with how much you spent the previous day and what you should
be spending if you want to maintain your budget.

If you want to use if for yourself just add simple text files containing your
usernames and passwords as is specified in the beginning of the `.py` script.

If you want to schedule a launchd job to run this script for yourself everyday
you can use the following template for your plist:

```{xml}
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Label</key>
	<string>com.user.mintTexting</string>
	<key>ProgramArguments</key>
	<array>
		<string>python</string>
		<string>budgetApp.py</string>
	</array>
	<key>RunAtLoad</key>
	<true/>
	<key>StartInterval</key>
	<integer>86400</integer>
	<key>WorkingDirectory</key>
	<string>/path/to/the/app/spendingApp</string>
</dict>
</plist>
```
