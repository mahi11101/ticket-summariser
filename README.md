# Ticket summariser

Agents shouldn't have to read fifty messages to pick up a ticket. This turns a long support thread into a five-line CRM note: issue, customer impact, what's been done, next step and sentiment.

## Run it

```bash
python summarise.py sample_thread.txt
```

- With `ANTHROPIC_API_KEY` set, it uses Claude for the summary (set `MODEL` to change the model).
- Without a key it falls back to a rule-based summary, so it always runs. No dependencies, Python 3.9+.

## Example output (fallback mode)

```
Issue: Our SSO login has been failing since this morning.
Customer impact: This is the second outage this month and it is urgent.
Done so far: I have sent the new metadata file and escalated to the identity team to confirm once you upload it.
Next step: Agent to confirm the fix with the customer
Sentiment: frustrated
```

## Where it fits

Hook it to a helpdesk webhook (Zendesk, Intercom, Salesforce) on ticket transfer or escalation, and write the note back to the ticket, so the next person starts with context instead of re-asking the customer.

Built by Mahesh Kumar with AI coding tools.
