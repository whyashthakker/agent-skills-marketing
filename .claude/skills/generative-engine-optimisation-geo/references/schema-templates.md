# Schema Templates

## Organization

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Infloq",
  "url": "https://infloq.com",
  "description": "AI-powered creator discovery, campaign management, analytics, product seeding, and affiliate workflows."
}
```

## SoftwareApplication

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Infloq",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web",
  "url": "https://infloq.com",
  "description": "Influencer marketing software for creator discovery, campaign management, analytics, and affiliate operations."
}
```

## FAQPage

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What does Infloq help marketing teams do?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Infloq helps teams discover creators, manage campaigns, track performance, and run affiliate workflows from one platform."
      }
    }
  ]
}
```

## Article

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to Build a Creator Discovery Workflow That Actually Scales",
  "author": {
    "@type": "Organization",
    "name": "Infloq"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Infloq"
  }
}
```
