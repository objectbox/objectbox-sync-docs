// Schema Components for ObjectBox Documentation
// Place this file at: src/components/Schema/index.tsx

import React from 'react';
import Head from '@docusaurus/Head';

interface SoftwareDocumentationSchemaProps {
  description: string;
  version?: string;
  dateModified: string;
  programmingLanguage?: string;
  operatingSystem?: string[];
}

export function SoftwareDocumentationSchema({
  description,
  version,
  dateModified,
  programmingLanguage = "Data Sync",
  operatingSystem = ["Windows", "macOS", "Linux", "iOS", "Android", "QNX", "POSIX", "Raspbian"]
}: SoftwareDocumentationSchemaProps) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "ObjectBox Database",
    "description": description,
    "applicationCategory": "Database",
    "operatingSystem": operatingSystem,
    "programmingLanguage": programmingLanguage,
    "version": version,
    "dateModified": dateModified,
    "publisher": {
      "@type": "Organization",
      "name": "ObjectBox",
      "url": "https://objectbox.io"
    },
    "offers": {
      "@type": "Offer",
      "price": "0",
      "priceCurrency": "USD"
    }
  };

  return (
    <Head>
      <script type="application/ld+json">
        {JSON.stringify(schema)}
      </script>
    </Head>
  );
}

interface TechnicalArticleSchemaProps {
  headline: string;
  description: string;
  url: string;
  datePublished: string;
  dateModified: string;
  author?: string;
  publisher?: string;
}

export function TechnicalArticleSchema({
  headline,
  description,
  url,
  datePublished,
  dateModified,
  author = "ObjectBox Team",
  publisher = "ObjectBox"
}: TechnicalArticleSchemaProps) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": headline,
    "description": description,
    "url": url,
    "datePublished": datePublished,
    "dateModified": dateModified,
    "author": {
      "@type": "Organization",
      "name": author
    },
    "publisher": {
      "@type": "Organization",
      "name": publisher,
      "url": "https://objectbox.io"
    },
    "mainEntityOfPage": {
      "@type": "WebPage",
      "@id": url
    }
  };

  return (
    <Head>
      <script type="application/ld+json">
        {JSON.stringify(schema)}
      </script>
    </Head>
  );
}

interface FAQSchemaProps {
  questions: Array<{
    question: string;
    answer: string;
  }>;
}

export function FAQSchema({ questions }: FAQSchemaProps) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": questions.map(qa => ({
      "@type": "Question",
      "name": qa.question,
      "acceptedAnswer": {
        "@type": "Answer",
        "text": qa.answer
      }
    }))
  };

  return (
    <Head>
      <script type="application/ld+json">
        {JSON.stringify(schema)}
      </script>
    </Head>
  );
}

interface HowToSchemaProps {
  name: string;
  description: string;
  steps: Array<{
    name: string;
    text: string;
  }>;
  totalTime?: string;
  estimatedCost?: string;
}

export function HowToSchema({
  name,
  description,
  steps,
  totalTime,
  estimatedCost
}: HowToSchemaProps) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "HowTo",
    "name": name,
    "description": description,
    "totalTime": totalTime,
    "estimatedCost": estimatedCost,
    "step": steps.map((step, index) => ({
      "@type": "HowToStep",
      "position": index + 1,
      "name": step.name,
      "text": step.text
    }))
  };

  return (
    <Head>
      <script type="application/ld+json">
        {JSON.stringify(schema)}
      </script>
    </Head>
  );
}

// Default export for convenience
export default {
  SoftwareDocumentationSchema,
  TechnicalArticleSchema,
  FAQSchema,
  HowToSchema
};

