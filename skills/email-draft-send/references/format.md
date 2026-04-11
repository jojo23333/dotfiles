# Email Draft Format

Use this exact plain-text structure for every draft:

```text
To: recipient@example.com
Cc:
Bcc:
Subject: Example subject line
Attachments:
---
Hello,

This is the email body.

Best,
Your Name
```

## Rules

- `To` is required. Use one or more comma-separated email addresses.
- `Subject` is required.
- `Cc`, `Bcc`, and `Attachments` are optional but the header lines should still exist.
- `Attachments` accepts comma-separated file paths. Prefer absolute paths.
- `---` must appear exactly once on its own line.
- Everything after `---` is the body and should be preserved verbatim.

## Example

```text
To: carolina.tropini@ubc.ca
Cc:
Bcc:
Subject: UBC interview request on science-lab data analysis workflows
Attachments:
---
Hi Dr. Tropini,

My name is Muchen Li, and I am a final-year PhD student at UBC working on machine learning and computer vision with Prof. Leonid Sigal and Prof. Renjie Liao.

I am exploring how to build customized AI software for science labs, especially groups with substantial data-analysis needs but limited internal AI or software engineering support. To ground this in real workflows, I am speaking with UBC labs to understand where current data-analysis processes are slow, frustrating, or poorly served by existing tools.

Your lab seems like a strong fit given the combination of microbiome, imaging, microfluidics, and computational work. Would you be open to a short 15-20 minute conversation in the next couple of weeks? If a student or postdoc in your lab is closer to the day-to-day analysis workflow, I would also be very grateful for an introduction.

I am not selling a product at this stage. My goal is to understand real needs and identify what kinds of AI software would genuinely be useful in practice.

Thank you for your time.

Best,
Muchen Li
Final-year PhD student, UBC
Advised by Prof. Leonid Sigal and Prof. Renjie Liao
```
