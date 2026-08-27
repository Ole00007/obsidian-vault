# Site Schema — alenakrot.com/news
**Generated:** 2026-07-09 | **Source:** Hermes Agent v0.17.0 SEO/AEO audit output

## Ready-to-Deploy JSON-LD Schema

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://alenakrot.com/#organization",
      "name": "Medicina Estetica Naturale con la Dott.ssa Alena Krot",
      "url": "https://alenakrot.com",
      "logo": "https://alenakrot.com/images/logo.png",
      "sameAs": [
        "https://www.facebook.com/p/Alena-Krot-100006215718904/",
        "https://www.instagram.com/dr.alena.krot/"
      ]
    },
    {
      "@type": "Physician",
      "@id": "https://alenakrot.com/#physician",
      "name": "Dr. Alena Krot",
      "url": "https://alenakrot.com/about",
      "image": "https://alenakrot.com/images/dr-alena-krot.jpg",
      "telephone": "+39 345 8302531",
      "email": "mailto:info@alenakrot.com",
      "gender": "Female",
      "knowsLanguage": ["it", "en", "ru"],
      "memberOf": [
        {"@type": "MedicalOrganization", "name": "SIME (Societa Italiana di Medicina Estetica)"},
        {"@type": "MedicalOrganization", "name": "AGORA"},
        {"@type": "MedicalOrganization", "name": "AITEB"}
      ],
      "knowsAbout": [
        "Aesthetic Medicine", "Preventive Medicine", "Natural Anti-Aging Treatments",
        "Non-Surgical Rejuvenation", "Biorevitalisation", "Aesthetic Dermatology"
      ],
      "medicalSpecialty": {"@type": "MedicalSpecialty", "name": "Aesthetic Medicine & Preventive Care"}
    },
    {
      "@type": "MedicalBusiness",
      "@id": "https://alenakrot.com/#clinic-genova",
      "name": "Dott.ssa Alena Krot - Clinica Visage Genova",
      "parentOrganization": {"@id": "https://alenakrot.com/#organization"},
      "employee": {"@id": "https://alenakrot.com/#physician"},
      "telephone": "+39 345 8302531",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Piazza Piccapietra 73/7",
        "addressLocality": "Genoa",
        "addressRegion": "Liguria",
        "postalCode": "16121",
        "addressCountry": "IT"
      }
    },
    {
      "@type": "MedicalBusiness",
      "@id": "https://alenakrot.com/#clinic-ventimiglia",
      "name": "Dott.ssa Alena Krot - Studio medico Visage Ventimiglia",
      "parentOrganization": {"@id": "https://alenakrot.com/#organization"},
      "employee": {"@id": "https://alenakrot.com/#physician"},
      "telephone": "+39 345 8302531",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Via Ruffini 10",
        "addressLocality": "Ventimiglia",
        "addressRegion": "Liguria",
        "postalCode": "18039",
        "addressCountry": "IT"
      }
    },
    {
      "@type": "MedicalBusiness",
      "@id": "https://alenakrot.com/#clinic-palermo",
      "name": "Dott.ssa Alena Krot - Umanis Polymedical Clinic Palermo",
      "parentOrganization": {"@id": "https://alenakrot.com/#organization"},
      "employee": {"@id": "https://alenakrot.com/#physician"},
      "telephone": "+39 345 8302531",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Via Agrigento 25",
        "addressLocality": "Palermo",
        "addressRegion": "Sicily",
        "postalCode": "90141",
        "addressCountry": "IT"
      }
    },
    {
      "@type": "WebPage",
      "@id": "https://alenakrot.com/news#webpage",
      "url": "https://alenakrot.com/news",
      "name": "News & Clinical Aesthetics Blog - Dott.ssa Alena Krot",
      "description": "Stay updated on the latest treatments, professional achievements, and clinical insights in natural aesthetic medicine with Dr. Alena Krot.",
      "about": {"@id": "https://alenakrot.com/#physician"}
    }
  ]
}
</script>
```

## Fixes Applied vs. Hermes Draft
- Removed duplicated/malformed `"telephone"` keys in the Ventimiglia node (syntax error in source).
- Replaced placeholder social links with verified real profiles (Facebook, Instagram).
- Corrected Genova address to the real street: Piazza Piccapietra 73/7 (source draft omitted street).
- Corrected Ventimiglia business name to "Studio medico Visage" (real listing name, not "Clinica Visage").
- Corrected Palermo business name to "Umanis Polymedical Clinic" (real host clinic, not standalone "Alena Krot - Palermo").
- Removed unverifiable `alumniOf: School of Aesthetic Medicine (SIME)` claim — SIME is a professional association (memberOf), not her degree-granting school.
- Removed unverifiable `Physician.url` pointing to non-existent `/who-i-am` — corrected to real `/about`.

## Links
- Parent: [[Reference-General-INDEX]]
- Related: [[Point4_Excel_Legal_Financial_Iteration]]
