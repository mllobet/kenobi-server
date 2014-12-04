kenobi-server
============

Have you ever forgotten an article/link that you bookmarked? Is your bookmark list growing exponentially because you never read back the stuff you put in? kenobiServer has the solution! Get random links to your long forgotten bookmark in [Pocket](www.getpocket.com)

This is a very simple Yo service, send a Yo to the account of your choice, log in to your [Pocket](www.getpocket.com) account and every time it receives a Yo, sends back a random link from your list. Using the kenobi-probe frontend, once you read the link it gets archived.

How to run the server?
---
```
python server.py -c <pocket consumer key> -k <YO api key> -f <kenobi-probe frontend url>
```

How to use?
---
Run kenobi-probe, run kenobi-server, send a Yo to the account
