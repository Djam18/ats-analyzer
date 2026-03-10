# ATS — Applicant Tracking System
> Dossier de cadrage projet · v1.0

---

## Sommaire

1. [Définition du problème](#1-définition-du-problème)
2. [Présentation brève](#2-présentation-brève)
3. [Présentation détaillée](#3-présentation-détaillée)
4. [User Stories](#4-user-stories)
5. [Maquettes](#5-maquettes)
6. [Architecture](#6-architecture)
7. [Outils de travail](#7-outils-de-travail)
8. [Outils de tests](#8-outils-de-tests)
9. [Outils de déploiement](#9-outils-de-déploiement)
10. [Analytics](#10-analytics)
11. [Mailing](#11-mailing)

---

## 1. Définition du problème

### Contexte

Le recrutement manuel est lent, subjectif et non traçable. Les équipes RH passent la majorité de leur temps à **trier** des CVs plutôt qu'à **évaluer** des talents.

### Douleurs identifiées

| Problème | Impact concret |
|---|---|
| Tri manuel des CVs | ~6h de lecture par offre pour ~250 candidatures |
| Pas de critères standardisés | Décisions subjectives, biais cognitifs |
| Données éparpillées | CVs dans emails, Drive, Slack — aucune traçabilité |
| Suivi pipeline absent | Impossible de savoir où en est chaque candidat |
| Matching flou | Le recruteur lit tout avant de savoir si le profil convient |
| Pas de reporting | Impossible de mesurer le coût ou le délai de recrutement |

### Chiffres clés

- **23 jours** : durée moyenne d'un recrutement sans outil dédié
- **4 500 €** : coût moyen d'un recrutement en PME
- **75 %** des CVs reçus ne sont pas qualifiés pour le poste

### Problème central

> Les équipes RH passent plus de temps à trier et suivre les CVs qu'à évaluer les vrais talents — faute d'un outil centralisé et intelligent.

---

## 2. Présentation brève

**ATS** est une plateforme web qui permet aux recruteurs de :

1. Centraliser tous les CVs en un seul endroit
2. Analyser automatiquement chaque CV grâce à l'IA
3. Scorer et classer les candidats par rapport à chaque offre
4. Gérer le pipeline de recrutement visuellement (Kanban)
5. Automatiser les communications avec les candidats

---

## 3. Présentation détaillée

### Module 1 — Gestion des offres

- Création d'offres avec critères pondérés (compétences, expérience, formation)
- Statuts : Brouillon / Active / Clôturée / Archivée
- URL unique par offre pour candidature directe

### Module 2 — Upload & parsing de CVs

- Formats acceptés : PDF, DOCX
- Traitement asynchrone : CV mis en file d'attente et analysé en arrière-plan
- Extraction IA : nom, email, compétences, expérience, formation, langues
- Stockage du fichier original + données structurées en base

### Module 3 — Scoring & matching

- Score de 0 à 100 calculé par rapport aux critères de l'offre
- Pondération configurable : compétences (40%), expérience (30%), formation (20%), langues (10%)
- Alerte automatique si score dépasse un seuil défini

### Module 4 — Pipeline Kanban

- Colonnes : Reçu → Présélection → Entretien RH → Entretien Tech → Offre → Embauché / Refusé
- Drag & drop des candidats entre les étapes
- Notes internes et historique des actions par candidat

### Module 5 — Communication

- Templates d'emails personnalisables
- Envoi automatique au changement d'étape
- Lien de planification d'entretien (Calendly ou Google Calendar)

### Module 6 — Dashboard & Reporting

- KPIs : nombre de candidatures, taux de conversion, délai moyen par étape
- Graphiques : sources, scores, évolution temporelle
- Export CSV des données

---

## 4. User Stories

### Acteurs

| Acteur | Rôle |
|---|---|
| **Recruteur** | Utilisateur principal. Gère les offres, analyse les CVs, fait avancer le pipeline. |
| **Admin RH** | Accès complet. Configure les critères, gère les utilisateurs et les templates. |
| **Candidat** | Pas de compte. Soumet son CV via un lien public. Reçoit des emails automatiques. |
| **Système (IA)** | Parse les CVs, calcule les scores, déclenche les notifications. |

### Tableau des user stories

| Acteur | Use Case | Description | Critère d'acceptation |
|---|---|---|---|
| Recruteur | Créer une offre | Je crée une offre avec titre, description et critères pondérés. | L'offre est sauvegardée et un lien de candidature est généré. |
| Recruteur | Uploader un CV | Je dépose un CV (PDF/DOCX) pour un poste donné. | Le CV est parsé et le candidat apparaît dans le pipeline avec un score. |
| Recruteur | Consulter un profil | Je clique sur un candidat pour voir ses infos extraites et son CV. | Données affichées avec score et compétences détectées. |
| Recruteur | Déplacer un candidat | Je glisse un candidat vers l'étape suivante. | Statut mis à jour, email automatique envoyé si configuré. |
| Recruteur | Filtrer les candidats | Je filtre par score, compétence ou statut. | La liste se met à jour instantanément. |
| Admin RH | Configurer les pondérations | Je modifie le poids de chaque critère de scoring. | Le système recalcule tous les scores existants. |
| Admin RH | Gérer les templates | Je crée ou modifie les emails automatiques. | Emails envoyés avec les bonnes variables (nom, poste, date). |
| Admin RH | Consulter le dashboard | J'accède aux KPIs globaux de recrutement. | Graphiques et indicateurs affichés en temps réel. |
| Candidat | Soumettre une candidature | Je remplis un formulaire et dépose mon CV via un lien. | Je reçois un email de confirmation. Mon CV entre dans le pipeline. |
| Système | Parser un CV | Dès qu'un CV est uploadé, le système l'analyse. | Données extraites et score calculé en moins de 30 secondes. |

---

## 5. Maquettes

13 écrans au total : Dashboard · Login · Liste offres · Création offre · Liste candidats · Page publique · Upload CV · Profil candidat · Pipeline Kanban · Templates email · Reporting · Scoring · Gestion utilisateurs

### Dashboard principal

```
┌─────────────────────────────────────────────────────────────────┐
│  ATS Platform         [Offres] [Candidats] [Reports]  [⚙ Admin] │
├─────────────────────────────────────────────────────────────────┤
│  Tableau de bord                                                 │
├───────────────┬───────────────┬───────────────┬─────────────────┤
│  📥 247       │  ⭐ 38         │  📅 12        │  ✅ 5           │
│  Candidatures │  Présélectés  │  Entretiens   │  Offres actives │
├───────────────┴───────────────┴───────────────┴─────────────────┤
│  Offres récentes                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Dev React Senior     🟢 Active    45 cv   Score moy: 72 │   │
│  │  Chef de Projet IT    🟢 Active    23 cv   Score moy: 61 │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Upload CV

```
┌─────────────────────────────────────────────────────────────────┐
│  Ajouter un candidat — Dev React Senior                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌───────────────────────────────────────────────────────┐     │
│   │   📄  Glissez-déposez votre CV ici                    │     │
│   │       ou  [Parcourir les fichiers]                    │     │
│   │       Formats : PDF, DOCX  (max 5 MB)                 │     │
│   └───────────────────────────────────────────────────────┘     │
│                                                                  │
│   Note interne (optionnel)                                       │
│   ┌───────────────────────────────────────────────────────┐     │
│   │                                                       │     │
│   └───────────────────────────────────────────────────────┘     │
│                                                                  │
│               [Annuler]        [⬆ Uploader et analyser]         │
└─────────────────────────────────────────────────────────────────┘
```

### Profil candidat

```
┌──────────────────────────────┬──────────────────────────────────┐
│  👤 Jean-Paul MBEKI           │  SCORE MATCHING                  │
│  jean.mbeki@email.com         │                                  │
│  +229 97 XX XX XX             │    82 / 100  ⭐⭐⭐⭐            │
│  Cotonou, Bénin               │                                  │
│                               │  Compétences  ████████  88%     │
│  COMPÉTENCES DÉTECTÉES        │  Expérience   ██████    78%     │
│  [React] [TypeScript] [Node]  │  Formation    ███████   80%     │
│  [GraphQL] [Docker] [AWS]     │  Langues      █████     72%     │
│                               │                                  │
│  EXPÉRIENCE (6 ans)           │  STATUT PIPELINE                 │
│  Senior Dev — Tech Corp 3 ans │  [●] Candidature reçue           │
│  Full Stack — StartupX 3 ans  │  [●] Présélection                │
│                               │  [○] Entretien RH  ← ici        │
│  FORMATION                    │  [○] Entretien Tech              │
│  Master Info — UAC 2019       │  [○] Offre                       │
│                               │                                  │
│  📎 [Voir CV original]         │  [📅 Planifier entretien]        │
└──────────────────────────────┴──────────────────────────────────┘
```

### Pipeline Kanban

```
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────┐
│ 📥 Reçus(45)│ ⭐ Prés.(12)│ 📅 Entr.(8) │ 🤝 Offre(3) │ ✅ Embau│
├─────────────┼─────────────┼─────────────┼─────────────┼─────────┤
│ ┌─────────┐ │ ┌─────────┐ │ ┌─────────┐ │ ┌─────────┐ │         │
│ │J. MBEKI │ │ │A. KOUNDE│ │ │F. TOURE │ │ │C. MENSAH│ │K. BELLO │
│ │Score: 82│ │ │Score: 79│ │ │Score: 88│ │ │Score: 91│ │Score: 94│
│ └─────────┘ │ └─────────┘ │ └─────────┘ │ └─────────┘ │         │
│ ┌─────────┐ │             │             │             │         │
│ │S. AGOSSA│ │             │             │             │         │
│ │Score: 71│ │             │             │             │         │
│ └─────────┘ │             │             │             │         │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────┘
```

### Page de connexion

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│                      ATS Platform                               │
│                                                                  │
│              ┌───────────────────────────────┐                  │
│              │           Connexion           │                  │
│              ├───────────────────────────────┤                  │
│              │  Email                        │                  │
│              │  ┌─────────────────────────┐  │                  │
│              │  │ email@entreprise.com     │  │                  │
│              │  └─────────────────────────┘  │                  │
│              │  Mot de passe                 │                  │
│              │  ┌─────────────────────────┐  │                  │
│              │  │ ••••••••                 │  │                  │
│              │  └─────────────────────────┘  │                  │
│              │                               │                  │
│              │  [      Se connecter       ]  │                  │
│              │                               │                  │
│              │  Mot de passe oublié ?        │                  │
│              └───────────────────────────────┘                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Liste des offres d'emploi

```
┌─────────────────────────────────────────────────────────────────┐
│  ATS Platform         [Offres] [Candidats] [Reports]  [⚙ Admin] │
├─────────────────────────────────────────────────────────────────┤
│  Offres d'emploi                        [+ Créer une offre]     │
│  Rechercher...  [Statut ▼]  [Département ▼]                     │
├─────────────────────────────────────────────────────────────────┤
│  Titre                  Statut     Candidatures  Score moy  Date│
├─────────────────────────────────────────────────────────────────┤
│  Dev React Senior       🟢 Active       45          72      J-12│
│  Chef de Projet IT      🟢 Active       23          61      J-8 │
│  UX Designer            🟡 Brouillon     0           —      J-1 │
│  Data Analyst           🔴 Clôturée     67          78      J-30│
│  DevOps Engineer        🟢 Active       12          69      J-3 │
├─────────────────────────────────────────────────────────────────┤
│  5 offres  ·  [< 1 2 3 >]                                       │
└─────────────────────────────────────────────────────────────────┘
```

### Création / édition d'une offre

```
┌─────────────────────────────────────────────────────────────────┐
│  ← Retour         Nouvelle offre                [Brouillon ▼]   │
├─────────────────────────────────────────────────────────────────┤
│  Titre du poste                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Ex : Développeur React Senior                             │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Description                                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                                                           │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Critères & pondérations                    Total : 100%        │
│  ┌──────────────────────────────┬─────────┬────────────────┐   │
│  │ Critère                      │ Poids % │ Valeur requise │   │
│  ├──────────────────────────────┼─────────┼────────────────┤   │
│  │ Compétences techniques       │   40    │ React, Node.js │   │
│  │ Années d'expérience          │   30    │ ≥ 4 ans        │   │
│  │ Formation                    │   20    │ Bac+3 min.     │   │
│  │ Langues                      │   10    │ Français, Angl.│   │
│  └──────────────────────────────┴─────────┴────────────────┘   │
│  [+ Ajouter un critère]                                         │
│                                                                  │
│              [Annuler]    [Sauvegarder brouillon]   [Publier]   │
└─────────────────────────────────────────────────────────────────┘
```

### Liste des candidats (vue tableau + filtres)

```
┌─────────────────────────────────────────────────────────────────┐
│  Candidats                                      [⬆ Importer CV] │
│  Offre [Dev React Senior ▼]  Score [Tous ▼]  Étape [Tous ▼]    │
├──────┬──────────────────┬──────────┬────────┬───────────────────┤
│  ☐   │  Candidat        │  Score   │  Étape │  Dernière action  │
├──────┼──────────────────┼──────────┼────────┼───────────────────┤
│  ☐   │  Jean-Paul MBEKI │  82/100  │  Entr. │  Hier 14h32       │
│  ☐   │  Aïcha KOUNDE    │  79/100  │  Prés. │  Il y a 2 jours   │
│  ☐   │  Fatou TOURE     │  88/100  │  Entr. │  Aujourd'hui 9h   │
│  ☐   │  Samuel AGOSSA   │  71/100  │  Reçu  │  Il y a 3 jours   │
│  ☐   │  Marie DOSSOU    │  55/100  │  Reçu  │  Il y a 5 jours   │
├──────┴──────────────────┴──────────┴────────┴───────────────────┤
│  5 candidats sélectionnés  [Déplacer vers ▼]  [Envoyer email]   │
└─────────────────────────────────────────────────────────────────┘
```

### Page publique de candidature (vue candidat)

```
┌─────────────────────────────────────────────────────────────────┐
│                      Entreprise XYZ                             │
├─────────────────────────────────────────────────────────────────┤
│                  Développeur React Senior                        │
│                  📍 Cotonou · 💼 CDI · 🕐 Temps plein           │
│                                                                  │
│  À propos du poste                                               │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Nous recherchons un développeur React expérimenté pour... │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Postuler                                                        │
│  ┌──────────────────────┐  ┌──────────────────────────────┐    │
│  │ Prénom               │  │ Nom                          │    │
│  └──────────────────────┘  └──────────────────────────────┘    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Email                                                     │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  📄  Déposer votre CV (PDF, DOCX · max 5 MB)              │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│                    [  Envoyer ma candidature  ]                  │
└─────────────────────────────────────────────────────────────────┘
```

### Éditeur de templates email

```
┌─────────────────────────────────────────────────────────────────┐
│  Templates email                          [+ Nouveau template]   │
├───────────────────────┬─────────────────────────────────────────┤
│  TEMPLATES            │  Modifier : Confirmation de candidature  │
│  ─────────────────    ├─────────────────────────────────────────┤
│  ✉ Confirmation       │  Objet                                   │
│  ✉ Invitation RH      │  ┌───────────────────────────────────┐  │
│  ✉ Invitation Tech    │  │ Votre candidature — {{poste}}     │  │
│  ✉ Offre              │  └───────────────────────────────────┘  │
│  ✉ Refus              │  Corps du message                        │
│  ✉ Rapport hebdo      │  ┌───────────────────────────────────┐  │
│                       │  │ Bonjour {{prenom}},               │  │
│  VARIABLES DISPO.     │  │                                   │  │
│  ─────────────────    │  │ Nous avons bien reçu votre        │  │
│  {{prenom}}           │  │ candidature pour le poste de      │  │
│  {{nom}}              │  │ {{poste}}.                        │  │
│  {{poste}}            │  │                                   │  │
│  {{entreprise}}       │  │ Cordialement,                     │  │
│  {{date_entretien}}   │  │ L'équipe RH                       │  │
│                       │  └───────────────────────────────────┘  │
│                       │  [Aperçu]    [Annuler]    [Sauvegarder] │
└───────────────────────┴─────────────────────────────────────────┘
```

### Dashboard analytics / Reporting

```
┌─────────────────────────────────────────────────────────────────┐
│  Reporting                    Période [Ce mois ▼]  [Exporter ▼] │
├────────────────────────┬────────────────────────────────────────┤
│  CONVERSIONS           │  DÉLAI MOYEN PAR ÉTAPE (jours)         │
│                        │                                        │
│  Reçus      247  100%  │  Reçu → Présél.   ████  3j            │
│  Présélect.  38   15%  │  Présél. → Entr.  ██████  5j          │
│  Entretiens  12    5%  │  Entr. → Offre    ████████  7j        │
│  Offres       3    1%  │  Offre → Embauche ██  2j              │
│  Embauchés    2   0.8% │                                        │
├────────────────────────┼────────────────────────────────────────┤
│  SOURCES                │  SCORES PAR OFFRE                      │
│                        │                                        │
│  Lien direct    45%    │  Dev React     ████████  72/100        │
│  LinkedIn       30%    │  Chef Projet   ██████    61/100        │
│  Indeed         15%    │  UX Designer   █████████ 83/100        │
│  Recommandation 10%    │  DevOps        ███████   69/100        │
└────────────────────────┴────────────────────────────────────────┘
```

### Paramètres de scoring

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚙ Paramètres · Scoring                                         │
├─────────────────────────────────────────────────────────────────┤
│  Pondérations globales (s'appliquent à toutes les offres)       │
│  Chaque offre peut ensuite les surcharger individuellement.     │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Compétences techniques      [████████████░░░░]  40 %   │   │
│  │  Années d'expérience         [█████████░░░░░░░]  30 %   │   │
│  │  Formation                   [██████░░░░░░░░░░]  20 %   │   │
│  │  Langues                     [███░░░░░░░░░░░░░]  10 %   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                          Total : 100% ✅        │
│                                                                  │
│  Seuils d'alerte                                                 │
│  Score minimum pour alerte recruteur    [ 75 ]                  │
│  Délai max sans action sur un candidat  [ 5 ] jours             │
│                                                                  │
│              [Annuler]              [Sauvegarder]               │
└─────────────────────────────────────────────────────────────────┘
```

### Gestion des utilisateurs (Admin)

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚙ Admin · Utilisateurs                  [+ Inviter un membre]  │
├──────────────────────┬──────────┬──────────────┬───────────────┤
│  Nom                 │  Rôle    │  Statut      │  Actions      │
├──────────────────────┼──────────┼──────────────┼───────────────┤
│  Marie DUPONT        │  Admin   │  🟢 Actif    │  [Modifier]   │
│  Thomas GARCIA       │  Recruteur│ 🟢 Actif    │  [Modifier]   │
│  Inès KOUASSI        │  Recruteur│ 🟡 Invité   │  [Renvoyer]   │
│  Paul MENSAH         │  Lecteur │  🔴 Inactif  │  [Réactiver]  │
├──────────────────────┴──────────┴──────────────┴───────────────┤
│  Rôles disponibles                                               │
│  Admin    → accès complet, gestion utilisateurs et paramètres   │
│  Recruteur → gestion offres, candidats, pipeline, emails        │
│  Lecteur  → consultation uniquement, aucune modification        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Charte graphique & Design System

> Tout ce dont le designer a besoin pour produire les écrans Figma.

---

### 6.1 Identité visuelle

**Nom du produit :** ATS Platform
**Positionnement visuel :** Outil professionnel, sobre, efficace. Pas de fioriture. L'interface s'efface derrière les données.
**Ambiance :** SaaS B2B moderne — entre Linear et Notion. Pas corporate, pas startup flashy.

---

### 6.2 Logo

Pas de logo illustratif complexe. Un **logotype typographique** suffi en phase MVP.

```
  Concept 1 — Typographique simple
  ┌──────────────────────┐
  │  ▣ ATS               │
  │     Platform         │
  └──────────────────────┘
  Icône : carré avec coin arrondi contenant
  une silhouette de document stylisée (▣)

  Concept 2 — Monogramme
  ┌──────────────────────┐
  │  [ A ]  ATS Platform │
  └──────────────────────┘
  Carré arrondi plein (couleur Primary)
  Lettre A blanche centrée, bold

  Déclinaisons à prévoir :
  - Logo complet (icône + nom)      → navbar, page login
  - Icône seule                     → favicon, onglet, app mobile
  - Logo fond clair                 → usage principal
  - Logo fond sombre                → sidebar collapsed, splash screen
```

---

### 6.3 Palette de couleurs

#### Couleurs principales

| Rôle | Nom | HEX | Usage |
|---|---|---|---|
| Primary | Blue Dark | `#1E3A5F` | Navbar, titres, boutons primaires |
| Secondary | Blue Mid | `#2E86AB` | Liens, badges, accents |
| Background | White | `#FFFFFF` | Fond principal |
| Surface | Gray Light | `#F8F9FA` | Cartes, panels, sidebar |
| Border | Gray Mid | `#E2E8F0` | Séparateurs, bordures inputs |
| Text Primary | Gray Dark | `#1A202C` | Corps de texte principal |
| Text Secondary | Gray | `#718096` | Labels, placeholders, metadata |

#### Couleurs sémantiques

| Rôle | HEX | Usage |
|---|---|---|
| Success | `#38A169` | Offre active, candidat embauché, score élevé |
| Warning | `#D69E2E` | Offre brouillon, score moyen, délai dépassé |
| Danger | `#E53E3E` | Offre clôturée, candidat refusé, erreur |
| Info | `#3182CE` | Notifications, tooltips |

#### Couleurs pipeline (Kanban)

| Étape | HEX | |
|---|---|---|
| Reçu | `#718096` | Gris neutre |
| Présélection | `#3182CE` | Bleu |
| Entretien RH | `#D69E2E` | Jaune/Orange |
| Entretien Tech | `#805AD5` | Violet |
| Offre | `#38A169` | Vert |
| Embauché | `#276749` | Vert foncé |
| Refusé | `#E53E3E` | Rouge |

---

### 6.4 Typographie

**Police principale : Inter**
Raison : lisible à toutes tailles, gratuite (Google Fonts), standard SaaS, excellente sur écran.

**Police code : JetBrains Mono**
Raison : affichage des scores, valeurs numériques, champs techniques.

```
  Hiérarchie typographique
  ─────────────────────────────────────────────

  H1 — Inter Bold · 32px · #1A202C
  Utilisé pour les titres de pages (Dashboard, Candidats...)

  H2 — Inter SemiBold · 24px · #1A202C
  Titres de sections dans les pages

  H3 — Inter SemiBold · 18px · #1A202C
  Sous-sections, titres de cartes

  Body — Inter Regular · 14px · #1A202C
  Texte courant, descriptions, contenu

  Body Small — Inter Regular · 12px · #718096
  Metadata, dates, labels secondaires

  Label — Inter Medium · 12px · #718096 · UPPERCASE · letter-spacing 0.05em
  Labels de formulaires, colonnes de tableaux

  Score / Chiffre clé — JetBrains Mono Bold · 28px · Primary
  KPIs du dashboard, score candidat

  Code / Tag — JetBrains Mono Regular · 13px · fond #F1F5F9
  Compétences détectées, tags techniques
```

---

### 6.5 Espacement & grille

Système basé sur une **base 4px**.

| Token | Valeur | Usage |
|---|---|---|
| space-1 | 4px | Espacement interne minimum |
| space-2 | 8px | Gap entre éléments proches |
| space-3 | 12px | Padding interne des badges/tags |
| space-4 | 16px | Padding standard des cartes |
| space-6 | 24px | Espacement entre sections |
| space-8 | 32px | Marges de page |
| space-12 | 48px | Sections majeures |

**Grille de mise en page :**

```
  Layout principal (sidebar + contenu)
  ┌──────────────────────────────────────────────┐
  │ Sidebar │              Contenu               │
  │  240px  │         max-width: 1200px          │
  │         │         padding: 32px              │
  └──────────────────────────────────────────────┘

  Sidebar collapsed (icônes seules) : 64px
  Breakpoints : sm 640px · md 768px · lg 1024px · xl 1280px
```

---

### 6.6 Bordures & ombres

| Élément | Valeur |
|---|---|
| Border radius — petit (inputs, badges) | `6px` |
| Border radius — moyen (cartes, modals) | `10px` |
| Border radius — grand (modals larges) | `16px` |
| Border radius — rond (avatars) | `50%` |
| Border color (défaut) | `#E2E8F0` |
| Shadow — card repos | `0 1px 3px rgba(0,0,0,0.08)` |
| Shadow — card hover | `0 4px 12px rgba(0,0,0,0.12)` |
| Shadow — modal | `0 20px 60px rgba(0,0,0,0.18)` |

---

### 6.7 Composants — États à prévoir

Pour chaque composant interactif, le designer doit produire **5 états** :

| État | Description |
|---|---|
| Default | Apparence au repos |
| Hover | Au survol souris |
| Focus | Sélectionné clavier / clic actif |
| Disabled | Non cliquable, opacité 40% |
| Loading | Spinner ou skeleton |

**Composants à designer en priorité :**

```
  Boutons
  ├── Primary (fond Primary, texte blanc)
  ├── Secondary (contour Primary, texte Primary)
  ├── Ghost (sans contour, texte Primary)
  ├── Danger (fond Danger, texte blanc)
  └── Icon-only (carré arrondi, icône centrée)

  Inputs
  ├── Text input (défaut, focus, erreur, disabled)
  ├── Textarea
  ├── Select / Dropdown
  ├── Search input (avec icône loupe)
  └── File upload zone (drag & drop)

  Cartes
  ├── Card offre (titre, statut, nb candidats, score)
  ├── Card candidat Kanban (nom, score, compétences)
  ├── Card KPI dashboard (icône, chiffre, label)
  └── Card profil candidat (détaillée)

  Navigation
  ├── Sidebar item (défaut, actif, hover)
  ├── Breadcrumb
  └── Tabs (horizontal)

  Feedback
  ├── Badge statut (couleurs sémantiques)
  ├── Score bar (progress colorée selon niveau)
  ├── Toast notification (success, error, info)
  ├── Modal de confirmation
  └── Empty state (illustration + CTA)

  Données
  ├── Tableau (header, ligne, ligne hover, pagination)
  ├── Kanban colonne + carte
  └── Graphique bar + ligne (recharts / Chart.js)
```

---

### 6.8 Iconographie

**Librairie recommandée : Lucide Icons**
Raison : cohérente, open source, disponible pour Vue/Nuxt, trait fin moderne.

| Icône | Usage |
|---|---|
| `Upload` | Upload CV |
| `User` | Profil candidat |
| `Briefcase` | Offre d'emploi |
| `LayoutKanban` | Pipeline |
| `BarChart2` | Reporting |
| `Mail` | Templates email |
| `Settings` | Paramètres |
| `Users` | Gestion utilisateurs |
| `Star` | Score / Présélection |
| `Calendar` | Entretien planifié |
| `CheckCircle` | Embauché / Validé |
| `XCircle` | Refusé |
| `Clock` | Délai / En attente |
| `ChevronRight` | Navigation, breadcrumb |
| `Search` | Recherche / Filtres |

Taille standard : **16px** dans les textes, **20px** standalone, **24px** dans les titres de section.

---

### 6.9 Design tokens — Résumé pour Figma

```
  À créer dans Figma comme Variables locales :

  Colors/
    primary-900   #1E3A5F
    primary-500   #2E86AB
    primary-100   #EBF4FA
    success       #38A169
    warning       #D69E2E
    danger        #E53E3E
    info          #3182CE
    gray-900      #1A202C
    gray-500      #718096
    gray-200      #E2E8F0
    gray-50       #F8F9FA
    white         #FFFFFF

  Spacing/
    xs    4px
    sm    8px
    md   16px
    lg   24px
    xl   32px
    2xl  48px

  Radius/
    sm    6px
    md   10px
    lg   16px
    full 9999px

  Typography/
    h1   Inter Bold 32px
    h2   Inter SemiBold 24px
    h3   Inter SemiBold 18px
    body Inter Regular 14px
    sm   Inter Regular 12px
    mono JetBrains Mono 13px
```

---

### 6.10 Checklist designer avant de démarrer Figma

- [ ] Installer la police **Inter** et **JetBrains Mono** dans Figma
- [ ] Installer le plugin **Lucide Icons** dans Figma
- [ ] Créer la page **Design Tokens** (couleurs, typo, espacement)
- [ ] Créer la page **Components** (tous les états des composants)
- [ ] Créer une page par écran (13 pages = 13 écrans)
- [ ] Utiliser une grille **12 colonnes · gutter 24px · margin 32px**
- [ ] Produire les écrans en **1440px de large** (desktop)
- [ ] Prévoir une version **375px** (mobile) pour la page publique candidat uniquement

---



### Recruteur

Flux principal du quotidien : gérer les offres actives et faire avancer le pipeline.

```
[Connexion]
     │
     ▼
[Dashboard]
     │
     ├──→ [Liste des offres]
     │          │
     │          ├──→ [Créer une offre]
     │          │
     │          └──→ [Offre sélectionnée]
     │                     │
     │                     ├──→ [Pipeline Kanban]
     │                     │          │
     │                     │          └──→ [Profil candidat]
     │                     │                     │
     │                     │                     ├──→ [Voir CV original]
     │                     │                     ├──→ [Déplacer dans le pipeline]
     │                     │                     └──→ [Planifier entretien]
     │                     │
     │                     └──→ [Upload CV]
     │
     └──→ [Liste des candidats]  (vue globale toutes offres confondues)
               │
               └──→ [Profil candidat]
```

**Pages accessibles :** Dashboard · Liste offres · Créer offre · Pipeline Kanban · Profil candidat · Upload CV · Liste candidats

---

### Admin RH

Accès complet + gestion de la configuration et des utilisateurs.

```
[Connexion]
     │
     ▼
[Dashboard]
     │
     ├──→ [Tout ce que voit le Recruteur]
     │
     ├──→ [Reporting / Analytics]
     │
     ├──→ [⚙ Paramètres]
     │          │
     │          ├──→ [Scoring — pondérations globales]
     │          ├──→ [Templates email]
     │          └──→ [Gestion des utilisateurs]
     │                     │
     │                     ├──→ [Inviter un membre]
     │                     └──→ [Modifier rôle / désactiver]
     │
     └──→ [Export données CSV / PDF]
```

**Pages accessibles :** Toutes (13 écrans).

---

### Candidat

Pas de compte. Parcours entièrement public, en dehors de l'application.

```
[Reçoit un lien] (email, LinkedIn, Indeed...)
     │
     ▼
[Page publique de candidature]
     │
     ├── Lit la description du poste
     │
     ├── Remplit le formulaire (prénom, nom, email)
     │
     ├── Dépose son CV
     │
     └── Soumet
          │
          ▼
     [Email de confirmation automatique]
          │
          ▼
     [Emails suivants selon avancement pipeline]
          ├── Invitation entretien RH
          ├── Invitation entretien Tech
          ├── Offre
          └── Refus
```

**Pages accessibles :** Page publique uniquement (1 écran). Tout le reste lui est invisible.

---

### Système (IA / automatisations)

Pas d'interface. Agit en arrière-plan sur déclencheurs.

```
[CV uploadé]
     │
     ▼
[Worker Celery déclenché]
     │
     ├──→ [Parse le CV (OpenAI)]
     │         └── Extrait : nom, email, compétences, expérience, formation
     │
     ├──→ [Calcule le score]
     │         └── Compare aux critères de l'offre
     │
     └──→ [Stocke en base + notifie le recruteur si score > seuil]


[Candidat déplacé dans le pipeline]
     │
     └──→ [Resend envoie l'email automatique correspondant]


[Cron job — lundi 8h00]
     │
     └──→ [Génère et envoie le rapport hebdo aux recruteurs]
```

---

### Récapitulatif des accès par écran

| Écran | Recruteur | Admin RH | Candidat | Système |
|---|---|---|---|---|
| Page de connexion | ✅ | ✅ | ✗ | ✗ |
| Dashboard | ✅ | ✅ | ✗ | ✗ |
| Liste des offres | ✅ | ✅ | ✗ | ✗ |
| Créer / éditer une offre | ✅ | ✅ | ✗ | ✗ |
| Pipeline Kanban | ✅ | ✅ | ✗ | ✗ |
| Profil candidat | ✅ | ✅ | ✗ | ✗ |
| Upload CV | ✅ | ✅ | ✗ | ✗ |
| Liste des candidats | ✅ | ✅ | ✗ | ✗ |
| Page publique candidature | ✗ | ✗ | ✅ | ✗ |
| Templates email | ✗ | ✅ | ✗ | ✗ |
| Reporting / Analytics | ✗ | ✅ | ✗ | ✗ |
| Paramètres scoring | ✗ | ✅ | ✗ | ✗ |
| Gestion utilisateurs | ✗ | ✅ | ✗ | ✗ |

---

## 8. Architecture

### Choix : Monolithe modulaire

Simple à développer et déployer en phase MVP. Chaque module reste découplé pour permettre une extraction future en microservices si la charge l'exige.

### Schéma

```
           [Navigateur]
                │
                ▼
        ┌───────────────┐
        │   Frontend    │  Next.js · Vercel
        └───────┬───────┘
                │ REST API
                ▼
        ┌───────────────┐
        │    Backend    │  FastAPI (Python) · Railway
        └──┬─────────┬──┘
           │         │
    ┌──────▼──┐  ┌───▼──────────┐
    │  Queue  │  │   Stockage   │
    │  Redis  │  │  PostgreSQL  │
    │  Celery │  │  S3 (fichiers│
    └──┬──────┘  └──────────────┘
       │
    ┌──▼────────────┐
    │  Service IA   │  OpenAI API
    │  Parsing CVs  │  Extraction + Scoring
    └───────────────┘
```

### Stack technique

| Couche | Outil choisi | Justification | Alternatives |
|---|---|---|---|
| Frontend | Nuxt 3 + TypeScript | SSR, file-based routing, excellent DX Vue | Next.js, SvelteKit |
| UI | Tailwind CSS + shadcn-vue | Composants accessibles, rapide | PrimeVue, Vuetify |
| Backend | FastAPI (Python) | Async natif, parfait pour IA | Node.js + Express |
| ORM | SQLAlchemy + Alembic | Migrations propres, typage fort | Prisma (JS) |
| Base de données | PostgreSQL | Robuste, JSON natif, full-text | MySQL |
| Stockage fichiers | Supabase Storage | S3-compatible, simple à intégrer | AWS S3, MinIO |
| File queue | Redis + Celery | Traitement async des CVs | BullMQ (Node) |
| IA / Parsing | OpenAI GPT-4o mini | Extraction précise, coût réduit | Mistral, Ollama |
| Auth | Supabase Auth (JWT) | OAuth2, gestion sessions clé en main | Auth0, Clerk |

---

## 9. Outils de travail

| Catégorie | Outil | Usage |
|---|---|---|
| Éditeur | VS Code | Développement principal |
| Extensions | Pylance, ESLint, Prettier, GitLens | Qualité de code |
| Versioning | GitHub | Branches, PR, code review |
| Gestion projet | Linear | Issues, sprints |
| Documentation | Notion | Specs, runbooks |
| API Testing | Postman | Tests manuels des routes |
| DB GUI | TablePlus | Explorer PostgreSQL |
| Diagrammes | Excalidraw | Schémas d'archi rapides |

---

## 10. Outils de tests

### Pyramide de tests

```
             ╔═══════════════╗
             ║    E2E  5%    ║  Playwright
          ╔══╩═══════════════╩══╗
          ║  Intégration  25%   ║  Pytest + httpx
       ╔══╩═════════════════════╩══╗
       ║      Unitaires  70%       ║  Pytest · Jest
       ╚═══════════════════════════╝
```

| Niveau | Outil | Usage |
|---|---|---|
| Unit backend | Pytest + pytest-cov | Fonctions parsing, scoring |
| Unit frontend | Vitest + Vue Testing Library | Composants, composables |
| Intégration API | Pytest + httpx | Routes FastAPI, auth, CRUD |
| E2E | Playwright | Parcours utilisateurs complets |
| Qualité code | Ruff (Python) + ESLint | Linting automatique |
| Sécurité | Bandit | Scan vulnérabilités Python |

### Couverture cible

- Backend : ≥ 80%
- Frontend : ≥ 70% sur les composants critiques
- E2E : les 5 parcours principaux (upload → score → kanban → email → rapport)

---

## 11. Outils de déploiement

| Composant | Outil | Rôle |
|---|---|---|
| Conteneurisation | Docker + Docker Compose | Environnement reproductible |
| CI/CD | GitHub Actions | Test → Build → Deploy automatique |
| Frontend | Vercel | Deploy Nuxt 3, CDN, preview par PR |
| Backend | Railway | FastAPI + Celery Worker |
| Base de données | Supabase | PostgreSQL managé + Auth + Storage |
| Secrets | GitHub Secrets | Variables d'environnement sécurisées |
| Monitoring erreurs | Sentry | Erreurs runtime frontend + backend |

### Pipeline CI/CD

```
[git push]
     │
     ▼
┌─────────────────────────────────────────┐
│            GitHub Actions               │
│  [Lint] → [Tests] → [Build] → [Deploy] │
└─────────────────────────────────────────┘
                                │
               ┌────────────────┴──────────────┐
               ▼                               ▼
           [Vercel]                        [Railway]
           Frontend                    Backend + Worker
```

Durée estimée par pipeline : **4 à 6 minutes**.

---

## 12. Analytics

| Type | Outil | Usage |
|---|---|---|
| Product analytics | PostHog | Funnels, events, session replay |
| Error tracking | Sentry | Erreurs runtime, alertes |
| Logs | Logtail | Logs structurés API et workers |
| Uptime | Better Uptime | Monitoring disponibilité |
| Performance web | Vercel Analytics | Core Web Vitals |

### KPIs à tracker dès le lancement

- CVs uploadés / jour
- Temps moyen de parsing (cible < 30s)
- Taux d'erreur du parser (cible < 5%)
- Score moyen par offre
- Taux de conversion pipeline (Reçu → Embauché)
- Taux d'ouverture des emails automatiques

---

## 13. Mailing

**Outil recommandé : Resend**

API simple, SDK Python natif, templates React Email, excellent deliverability. Free tier : 3 000 emails/mois.

| Critère | Resend | SendGrid | Brevo |
|---|---|---|---|
| DX (Developer Experience) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| SDK Python | Oui | Oui | Oui |
| Free tier | 3 000/mois | 100/jour | 300/jour |
| Prix Pro | 20$/mois | 19.95$/mois | 25$/mois |
| Deliverability | Excellent | Excellent | Bon |
| Webhooks | Oui | Oui | Oui |

### Emails à automatiser

| Email | Déclencheur |
|---|---|
| Confirmation de candidature | CV uploadé avec succès |
| Invitation entretien RH | Candidat déplacé vers Entretien RH |
| Invitation entretien tech | Candidat déplacé vers Entretien Tech |
| Offre d'emploi | Candidat déplacé vers Offre |
| Refus | Candidat déplacé vers Refusé |
| Rapport hebdo | Cron job chaque lundi 8h00 |

---

*ATS Project · Dossier de cadrage v1.0*

---

## 14. Points à clarifier et risques identifiés

| Risque | Niveau | Détail |
|---|---|---|
| Qualité du parsing IA | HAUT | GPT-4o mini peut rater des CVs mal structurés (images, colonnes, caractères spéciaux). Aucune stratégie de fallback mentionnée. |
| Recalcul des scores | MOYEN | US Admin : "recalcule tous les scores existants" — aucune mention de la volumétrie limite ni du mode de déclenchement (sync/async). |
| Lien Calendly/Google Cal | MOYEN | L'intégration est mentionnée mais non détaillée. OAuth Google Calendar est non trivial à implémenter. |
| Sécurité des CVs | MOYEN | CVs stockés sur Supabase Storage — pas de mention de contrôle d'accès (URLs signées, expiration) ni de conformité RGPD. |
| Multi-tenant | MOYEN | Le document ne mentionne pas l'isolation des données entre entreprises clientes. S'il y a plusieurs entreprises sur la plateforme, c'est critique. |
| Page publique mobile | BAS | Seule la page candidat est prévue en 375px. Acceptable pour un MVP, mais à noter. |

### Ce qui manque pour démarrer le développement

1. **Modèle de données** — pas de schéma ERD. Tables `jobs`, `candidates`, `applications`, `pipeline_stages`, `users`, `email_templates` à définir.
2. **Contrat API** — aucune liste des endpoints REST. Nécessaire avant d'aligner frontend/backend.
3. **Stratégie multi-tenant** — est-ce un SaaS multi-entreprises ou un outil monoclient ? Ça change l'architecture.
4. **RGPD** — données personnelles de candidats (email, CV, téléphone) = obligation légale de mentionner : durée de rétention, droit à l'oubli, consentement.
