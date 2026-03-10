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

Contrainte : **100% gratuit, sans carte bancaire requise.**

| Couche | Outil choisi | Gratuit | Justification |
|---|---|---|---|
| Frontend | Nuxt 3 + TypeScript | Oui (open source) | SSR, file-based routing, excellent DX Vue |
| UI | Tailwind CSS + shadcn-vue | Oui (open source) | Composants accessibles, rapide |
| Backend | FastAPI (Python) | Oui (open source) | Async natif, parfait pour IA |
| ORM | SQLAlchemy + Alembic | Oui (open source) | Migrations propres, typage fort |
| Base de données | PostgreSQL | Oui (open source) | Robuste, JSON natif, full-text |
| Stockage fichiers | MinIO (self-hosted) | Oui (open source) | S3-compatible, tourne dans Docker |
| File queue | Redis + Celery | Oui (open source) | Traitement async des CVs |
| IA / Parsing | Ollama + Mistral 7B | Oui (local) | Modèle open source, tourne en local, zéro coût |
| Auth | JWT maison (PyJWT) | Oui (open source) | Tokens JWT signés, pas de service externe |

---

## 9. Outils de travail

Tous les outils sont **gratuits et sans carte bancaire**.

| Catégorie | Outil | Gratuit | Usage |
|---|---|---|---|
| Éditeur | VS Code | Oui | Développement principal |
| Extensions | Pylance, ESLint, Prettier, GitLens | Oui | Qualité de code |
| Versioning | GitHub | Oui (free tier) | Branches, PR, code review |
| Gestion projet | GitHub Issues + GitHub Projects | Oui | Issues, sprints — déjà dans la stack |
| Documentation | Markdown dans le repo (`/docs`) | Oui | Specs, runbooks, pas de service externe |
| API Testing | Bruno | Oui (open source) | Tests manuels des routes, collections versionnées en git |
| DB GUI | DBeaver Community | Oui (open source) | Explorer PostgreSQL |
| Diagrammes | Excalidraw | Oui (open source, self-hosted ou web) | Schémas d'archi rapides |

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

Tous les outils sont **gratuits et sans carte bancaire**.

| Composant | Outil | Gratuit | Rôle |
|---|---|---|---|
| Conteneurisation | Docker + Docker Compose | Oui (open source) | Environnement reproductible local + prod |
| CI/CD | GitHub Actions | Oui (2 000 min/mois) | Test → Build → Deploy automatique |
| Frontend | Cloudflare Pages | Oui (sans carte) | Deploy Nuxt 3, CDN global, preview par PR |
| Backend | Render free tier | Oui (sans carte) | FastAPI + Celery Worker |
| Base de données | PostgreSQL dans Docker (VPS) ou Render PostgreSQL | Oui | PostgreSQL managé, 1 Go gratuit sur Render |
| Stockage fichiers | MinIO dans Docker | Oui (open source) | Stockage CVs S3-compatible |
| Secrets | GitHub Secrets | Oui | Variables d'environnement sécurisées |
| Monitoring erreurs | Sentry | Oui (free tier, sans carte) | Erreurs runtime frontend + backend |

> **Note Render** : le free tier met le service en veille après 15 min d'inactivité (cold start ~30s). Acceptable pour un MVP. Pour éviter ça, un cron ping toutes les 10 min suffit.

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
       [Cloudflare Pages]                  [Render]
           Frontend                    Backend + Worker
```

Durée estimée par pipeline : **4 à 6 minutes**.

---

## 12. Analytics

Tous les outils sont **gratuits et sans carte bancaire**.

| Type | Outil | Gratuit | Usage |
|---|---|---|---|
| Product analytics | PostHog Cloud | Oui (1 M events/mois, sans carte) | Funnels, events, session replay |
| Error tracking | Sentry | Oui (5 000 erreurs/mois, sans carte) | Erreurs runtime frontend + backend |
| Logs | Logs fichiers + Loguru (Python) | Oui (open source) | Logs structurés API et workers, pas de service externe |
| Uptime | UptimeRobot | Oui (50 moniteurs, sans carte) | Monitoring disponibilité toutes les 5 min |
| Performance web | Cloudflare Pages Analytics | Oui (inclus avec Pages) | Core Web Vitals, remplace Vercel Analytics |

### KPIs à tracker dès le lancement

- CVs uploadés / jour
- Temps moyen de parsing (cible < 30s)
- Taux d'erreur du parser (cible < 5%)
- Score moyen par offre
- Taux de conversion pipeline (Reçu → Embauché)
- Taux d'ouverture des emails automatiques

---

## 13. Mailing

**Outil recommandé : Brevo (ex-Sendinblue)**

300 emails/jour gratuits, sans carte bancaire, SDK Python natif, webhooks inclus.

| Critère | Brevo | Resend | SendGrid |
|---|---|---|---|
| Carte bancaire requise | Non | Non | Non |
| Free tier | 300/jour (9 000/mois) | 3 000/mois | 100/jour |
| SDK Python | Oui | Oui | Oui |
| Webhooks | Oui | Oui | Oui |
| Deliverability | Bon | Excellent | Excellent |
| SMTP simple | Oui | Oui | Oui |

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

Synthèse rapide avant développement détaillé :

| Risque | Niveau | Détail |
|---|---|---|
| Qualité du parsing IA | HAUT | GPT-4o mini peut rater des CVs mal structurés (images, colonnes, caractères spéciaux). Aucune stratégie de fallback mentionnée. |
| Recalcul des scores | MOYEN | US Admin : "recalcule tous les scores existants" — aucune mention de la volumétrie limite ni du mode de déclenchement (sync/async). |
| Lien Calendly/Google Cal | MOYEN | L'intégration est mentionnée mais non détaillée. OAuth Google Calendar est non trivial à implémenter. |
| Sécurité des CVs | MOYEN | CVs stockés sur Supabase Storage — pas de mention de contrôle d'accès (URLs signées, expiration) ni de conformité RGPD. |
| Multi-tenant | MOYEN | Le document ne mentionne pas l'isolation des données entre entreprises clientes. S'il y a plusieurs entreprises sur la plateforme, c'est critique. |
| Page publique mobile | BAS | Seule la page candidat est prévue en 375px. Acceptable pour un MVP, mais à noter. |

---

### 14.1 Qualité du parsing IA — HAUT

**Problème**

GPT-4o mini est un modèle de langage : il lit du texte. Or une part significative des CVs reçus en pratique ne sont pas du texte pur :

- CVs en colonnes multiples (le PDF est encodé dans un ordre de lecture linéaire qui mélange les colonnes)
- CVs scannés ou photographiés (fichier PDF sans couche texte, juste une image)
- CVs en DOCX avec tableaux imbriqués, zones de texte flottantes ou headers/footers
- CVs avec caractères Unicode non standards (alphabets cyrilliques, arabes, caractères accentués mal encodés)
- CVs au format image dans un DOCX (logo, photo, graphiques de compétences visuels)

Dans tous ces cas, le texte extrait avant l'envoi à l'API sera corrompu ou incomplet, et GPT-4o mini extraira des données erronées ou partielles sans le signaler explicitement.

**Stratégie de fallback recommandée**

```
[Fichier uploadé]
       │
       ▼
[Extraction texte]
       │
       ├── PDF → pdfplumber (extraction texte natif)
       │              │
       │              ├── Texte extrait > 100 mots → OK, envoyer à GPT
       │              │
       │              └── Texte < 100 mots ou vide → fallback OCR (pytesseract / AWS Textract)
       │
       └── DOCX → python-docx
                      │
                      ├── Texte extrait > 100 mots → OK, envoyer à GPT
                      │
                      └── Texte < 100 mots → fallback OCR
                                    │
                                    ▼
                            [OCR échoue aussi]
                                    │
                                    └── Marquer le CV "parsing manuel requis"
                                        Notifier le recruteur
```

**Score de confiance**

Le parser doit retourner un champ `parsing_confidence` (0–1) calculé sur :
- Nombre de champs extraits / nombre de champs attendus
- Présence d'un email valide (signal fort de parsing correct)
- Longueur du texte source

Si `parsing_confidence < 0.6` : afficher une alerte dans l'UI et désactiver le score automatique.

**Prompt engineering**

Le prompt envoyé à GPT doit être strict sur le format de sortie :

```python
SYSTEM_PROMPT = """
Tu es un parser de CV. Extrais les informations suivantes du texte fourni.
Réponds UNIQUEMENT en JSON valide avec exactement ces clés.
Si une information est absente, utilise null.
Ne génère rien en dehors du JSON.

{
  "full_name": string | null,
  "email": string | null,
  "phone": string | null,
  "location": string | null,
  "skills": string[],
  "experience_years": number | null,
  "experiences": [{"title": string, "company": string, "duration_months": number}],
  "education": [{"degree": string, "institution": string, "year": number | null}],
  "languages": [{"language": string, "level": string | null}]
}
"""
```

Utiliser `response_format={"type": "json_object"}` dans l'appel API pour forcer la sortie JSON.

**Métriques à surveiller (PostHog/Logtail)**

- `parsing_confidence` moyen par semaine
- Taux de CVs flaggés "parsing manuel requis" (cible < 5%)
- Taux d'erreur d'appel OpenAI (cible < 1%)

---

### 14.2 Recalcul des scores — MOYEN

**Problème**

L'user story Admin stipule que modifier les pondérations globales "recalcule tous les scores existants". Deux questions non résolues :

1. **Volumétrie** : si la plateforme a 10 000 candidats, recalculer en synchrone bloque la requête HTTP et timeout.
2. **Traçabilité** : écraser le score existant efface l'historique. Un recruteur qui avait présélectionné un candidat à 78 peut se retrouver avec un score recalculé à 52 sans comprendre pourquoi.

**Décision recommandée**

Toujours recalculer de manière **asynchrone via Celery**, avec versioning des scores.

```
Schéma de table scores (à la place d'un champ score sur candidates) :

scores
├── id
├── candidate_id
├── job_id
├── score_total         (0–100)
├── score_skills        (0–100)
├── score_experience    (0–100)
├── score_education     (0–100)
├── score_languages     (0–100)
├── weights_snapshot    (JSONB — copie des pondérations au moment du calcul)
├── triggered_by        (enum : "upload" | "weights_update" | "manual")
├── created_at
```

Ainsi le score affiché est toujours le dernier enregistrement, mais l'historique est conservé.

**Flow de recalcul en masse**

```
[Admin modifie les pondérations]
        │
        ▼
[Sauvegarde les nouvelles pondérations en base]
        │
        ▼
[Enqueue task Celery : recalculate_all_scores(new_weights_id)]
        │
        ▼
[Celery worker traite par batch de 100]
        │
        ├── Calcule le nouveau score pour chaque candidat
        ├── Insère une nouvelle ligne dans scores (ne supprime pas l'ancienne)
        └── Notifie l'Admin via websocket / email quand terminé
```

**UI**

Afficher dans le profil candidat : "Score calculé le [date] avec pondérations v3". Permettre de voir l'historique des scores.

---

### 14.3 Intégration Calendly / Google Calendar — MOYEN

**Problème**

Le dossier mentionne "Lien de planification d'entretien (Calendly ou Google Calendar)" sans préciser l'implémentation. Ces deux options ont des complexités très différentes.

**Option A — Lien libre (recommandée pour le MVP)**

Le recruteur renseigne n'importe quel lien de planification dans ses paramètres de profil (Cal.com gratuit et open source, lien Google Meet, lien Zoom, ou tout autre outil). L'ATS l'insère dans l'email d'invitation via la variable `{{lien_entretien}}`.

```
Avantages :
- Zéro OAuth, zéro webhook à gérer côté ATS
- Compatible avec n'importe quel outil (Cal.com, Google Meet, etc.)
- Implémentation : 1 champ user.calendar_link + variable {{lien_entretien}} dans le template
- Cal.com est 100% gratuit et open source (self-hostable)

Inconvénients :
- Pas de visibilité dans l'ATS sur les RDVs confirmés
- Le recruteur doit gérer ses disponibilités dans son propre outil
```

**Option B — Google Calendar API (MVP+ ou V2)**

Intégration native : l'ATS crée l'événement dans le calendrier du recruteur et envoie l'invitation au candidat.

```
Flux OAuth requis :
[Recruteur clique "Connecter Google Calendar"]
        │
        ▼
[Redirect OAuth Google — scopes : calendar.events]
        │
        ▼
[Callback ATS — stocke access_token + refresh_token chiffrés en base]
        │
        ▼
[À chaque invitation] POST /calendar/v3/calendars/primary/events
  avec attendees: [recruteur, candidat]
  et conferenceData: {createRequest} pour Google Meet automatique
```

Complexités à anticiper :
- Refresh token à gérer (expiration, révocation)
- Gestion des fuseaux horaires (candidat Cotonou, recruteur Paris)
- Rate limits Google API (quota par projet)

**Recommandation**

MVP : Option A (Calendly link). V2 : Option B (Google Calendar natif).
Prévoir dès maintenant le champ `user.calendar_link` générique pour ne pas avoir à migrer.

---

### 14.4 Sécurité des CVs et conformité RGPD — MOYEN

**Problème**

Les CVs contiennent des données personnelles sensibles (identité, adresse, téléphone, parfois photo, situation familiale). Deux dimensions à traiter : sécurité technique et conformité légale.

**Sécurité technique — accès aux fichiers**

Supabase Storage génère par défaut des URLs publiques permanentes. Un lien de CV partagé par erreur reste accessible indéfiniment.

Solution : utiliser des **URLs signées à durée limitée** pour tout accès aux CVs.

```python
# Mauvais — URL publique permanente
url = supabase.storage.from_("cvs").get_public_url("jean-mbeki-cv.pdf")

# Correct — URL signée valable 1 heure
url = supabase.storage.from_("cvs").create_signed_url(
    path="jean-mbeki-cv.pdf",
    expires_in=3600  # secondes
)
```

Le bucket Supabase doit être configuré en **privé**. Aucun fichier ne doit être accessible sans token signé.

**Nommage des fichiers**

Ne jamais stocker les CVs avec le nom original fourni par le candidat (risque de path traversal, collisions, exposition du nom).

```python
# Mauvais
filename = uploaded_file.filename  # "Jean Paul MBEKI CV.pdf"

# Correct
import uuid
filename = f"{uuid.uuid4()}.pdf"  # "a3f2c1d4-...pdf"
path = f"jobs/{job_id}/candidates/{candidate_id}/{filename}"
```

**Conformité RGPD**

Le RGPD (applicable dès qu'un candidat européen postule) impose :

| Obligation | Implémentation requise |
|---|---|
| Information du candidat | Ajouter sur la page publique : "Vos données sont traitées par [Entreprise] dans le cadre de votre candidature. Durée de conservation : 2 ans." |
| Droit d'accès | Endpoint `GET /api/candidates/{id}/export` — retourne toutes les données en JSON/PDF |
| Droit à l'effacement | Endpoint `DELETE /api/candidates/{id}` — supprime données en base + fichier Supabase + logs associés |
| Durée de conservation | Cron job mensuel : archiver ou supprimer les candidatures > 2 ans sans activité |
| Consentement | Checkbox obligatoire sur la page publique : "J'accepte que mes données soient conservées pour cette candidature" |
| Responsable de traitement | Mentionner dans les CGU qui est responsable (l'entreprise cliente, pas l'éditeur ATS) |

**Chiffrement**

Les données extraites par l'IA (email, téléphone) stockées en clair en PostgreSQL sont suffisantes pour un MVP, mais prévoir à terme le chiffrement des champs PII avec une clé par organisation.

---

### 14.5 Architecture multi-tenant — DÉCISION PRISE

**Décision : Option C — Row-Level Security PostgreSQL**

SaaS multi-clients. Toutes les organisations partagent la même base de données. L'isolation est assurée par PostgreSQL Row-Level Security (RLS) via un `organization_id` sur chaque ligne.

**Option C — Tenant par colonne (Row-Level Security) — RETENUE**

Toutes les entreprises partagent les mêmes tables. Chaque ligne a un `organization_id`. PostgreSQL Row-Level Security (RLS) garantit qu'une requête ne voit que les lignes de son organisation.

```sql
-- Politique RLS sur la table candidates
ALTER TABLE candidates ENABLE ROW LEVEL SECURITY;

CREATE POLICY candidates_isolation ON candidates
  USING (organization_id = current_setting('app.current_org_id')::uuid);
```

```python
# Dans le middleware FastAPI — à exécuter avant chaque requête
@app.middleware("http")
async def set_tenant_context(request: Request, call_next):
    org_id = extract_org_from_jwt(request.headers.get("Authorization"))
    async with db.begin():
        await db.execute(
            text("SET LOCAL app.current_org_id = :org_id"),
            {"org_id": str(org_id)}
        )
    return await call_next(request)
```

**Schéma de la table organizations**

```
organizations
├── id          (UUID, PK)
├── name        (string)
├── slug        (string, unique — pour les URLs publiques /apply/acme/dev-react)
├── logo_url    (string | null)
├── plan        (enum : free | pro | enterprise)
├── created_at
```

Toutes les tables principales (`jobs`, `candidates`, `users`, `email_templates`, `scores`) ont un `organization_id` FK vers `organizations`.

**Impact sur l'URL publique candidat**

Actuellement le dossier mentionne "URL unique par offre". Avec le multi-tenant, l'URL doit inclure l'organisation :

```
/apply/{organization_slug}/{job_slug}
ex : /apply/acme-corp/developpeur-react-senior
```

---

### 14.6 Page publique mobile — BAS

**Problème**

Le document prévoit un design responsive uniquement pour la page de candidature publique (375px). Toutes les pages internes (dashboard, kanban, profil) sont desktop-only (1440px).

**Impact concret**

- Les recruteurs qui consultent des profils depuis leur téléphone (en déplacement, entre deux réunions) auront une expérience dégradée.
- Le pipeline Kanban est intrinsèquement difficile à rendre responsive (colonnes horizontales, drag & drop).

**Recommandation par écran**

| Écran | Priorité mobile | Approche |
|---|---|---|
| Page publique candidature | Obligatoire MVP | Design 375px complet |
| Dashboard | Souhaitable V2 | Cards empilées, KPIs en grille 2×2 |
| Liste des candidats | Souhaitable V2 | Vue liste simplifiée, masquer colonnes secondaires |
| Profil candidat | Souhaitable V2 | Layout colonne unique, score en header |
| Pipeline Kanban | Complexe — V2+ | Vue liste filtrée par étape plutôt que colonnes |
| Création d'offre | Non prioritaire | Usage rare en mobilité |
| Reporting | Non prioritaire | Export PDF/CSV suffit en mobile |

**Pour le MVP**

Ajouter dans le CLAUDE.md du projet une contrainte : les pages internes doivent afficher un message "Interface optimisée pour desktop" en dessous de `md` (768px) plutôt que de casser la mise en page.

```html
<!-- Composant MobileWarning.vue -->
<div class="hidden md:hidden bg-warning-100 p-4 text-center text-sm">
  Cette interface est optimisée pour une utilisation sur desktop.
</div>
```

---

### 14.7 Ce qui manque pour démarrer le développement

#### Modèle de données (ERD)

Tables minimales à définir avant le premier sprint :

```
organizations ──< users
organizations ──< jobs ──< applications ──< scores
                           jobs ──< pipeline_stages (ordre configurable)
applications ──> candidates
applications ──< pipeline_events (historique des déplacements)
organizations ──< email_templates
```

Champs critiques à décider en équipe :
- `applications.status` : enum en base ou FK vers `pipeline_stages` ?
- `candidates` : un candidat est-il lié à une organisation ou global ? (impact multi-tenant)
- `scores` : une ligne par calcul (historique) ou une ligne mise à jour ?

#### Contrat API — Liste complète des endpoints

Légende des accès : **R** = Recruteur · **A** = Admin RH · **P** = Public (sans auth)

```
── AUTH ────────────────────────────────────────────────────────────────
  POST   /api/auth/login                   P   Email + password → JWT
  POST   /api/auth/logout                  R,A Invalide le refresh token
  POST   /api/auth/refresh                 R,A Renouvelle le JWT via refresh token
  GET    /api/auth/me                      R,A Profil de l'utilisateur connecté
  POST   /api/auth/forgot-password         P   Envoie un email de réinitialisation
  POST   /api/auth/reset-password          P   Réinitialise le mot de passe via token

── ORGANISATIONS ────────────────────────────────────────────────────────
  GET    /api/organizations/me             A   Infos de l'organisation courante
  PUT    /api/organizations/me             A   Modifier nom, logo, slug

── UTILISATEURS ─────────────────────────────────────────────────────────
  GET    /api/users                        A   Liste des membres de l'organisation
  POST   /api/users/invite                 A   Inviter un membre par email
  GET    /api/users/{id}                   A   Détail d'un utilisateur
  PUT    /api/users/{id}                   A   Modifier rôle
  DELETE /api/users/{id}                   A   Désactiver un compte
  PUT    /api/users/me                     R,A Modifier son propre profil
  PUT    /api/users/me/password            R,A Changer son mot de passe
  PUT    /api/users/me/calendar-link       R,A Enregistrer son lien de planification

── OFFRES D'EMPLOI ──────────────────────────────────────────────────────
  GET    /api/jobs                         R,A Liste des offres (filtre : statut, date)
  POST   /api/jobs                         R,A Créer une offre
  GET    /api/jobs/{id}                    R,A Détail d'une offre
  PUT    /api/jobs/{id}                    R,A Modifier une offre
  PATCH  /api/jobs/{id}/status             R,A Changer le statut (brouillon/active/clôturée/archivée)
  DELETE /api/jobs/{id}                    A   Supprimer une offre
  GET    /api/jobs/{id}/stats              R,A Statistiques de l'offre (nb candidats, score moyen)

── PAGE PUBLIQUE CANDIDAT ───────────────────────────────────────────────
  GET    /api/public/jobs/{slug}           P   Détail d'une offre (vue publique, sans critères internes)
  POST   /api/public/jobs/{slug}/apply     P   Soumettre une candidature + upload CV (multipart/form-data)

── CANDIDATURES ─────────────────────────────────────────────────────────
  GET    /api/jobs/{job_id}/applications   R,A Liste des candidatures d'une offre
                                               Filtres query : ?stage=&min_score=&max_score=&search=
  POST   /api/jobs/{job_id}/applications   R,A Uploader un CV manuellement (multipart/form-data)
  GET    /api/applications/{id}            R,A Détail d'une candidature
  DELETE /api/applications/{id}            A   Supprimer une candidature

── PIPELINE ─────────────────────────────────────────────────────────────
  PATCH  /api/applications/{id}/stage      R,A Déplacer vers une étape (body: {stage_id})
  GET    /api/applications/{id}/history    R,A Historique des déplacements dans le pipeline
  POST   /api/applications/{id}/notes      R,A Ajouter une note interne
  GET    /api/applications/{id}/notes      R,A Lister les notes internes
  DELETE /api/applications/{id}/notes/{note_id}  R,A Supprimer une note

── CANDIDATS ────────────────────────────────────────────────────────────
  GET    /api/candidates                   R,A Liste globale (toutes offres)
                                               Filtres query : ?search=&stage=&job_id=
  GET    /api/candidates/{id}              R,A Profil complet du candidat
  GET    /api/candidates/{id}/cv           R,A URL signée pour télécharger le CV original (valable 1h)
  DELETE /api/candidates/{id}              A   Supprimer le candidat + données + CV (droit à l'effacement RGPD)
  GET    /api/candidates/{id}/export       R,A Export JSON des données personnelles (droit d'accès RGPD)

── SCORING ──────────────────────────────────────────────────────────────
  GET    /api/applications/{id}/scores     R,A Historique des scores d'une candidature
  POST   /api/applications/{id}/scores/recalculate  R,A Recalculer manuellement le score
  GET    /api/scoring/weights              A   Pondérations globales actuelles
  PUT    /api/scoring/weights              A   Modifier les pondérations (déclenche recalcul async)
  GET    /api/scoring/weights/history      A   Historique des versions de pondérations

── ÉTAPES PIPELINE (configuration) ─────────────────────────────────────
  GET    /api/pipeline/stages              R,A Liste des étapes configurées
  PUT    /api/pipeline/stages              A   Réordonner ou renommer les étapes

── TEMPLATES EMAIL ──────────────────────────────────────────────────────
  GET    /api/email-templates              A   Liste des templates
  POST   /api/email-templates              A   Créer un template
  GET    /api/email-templates/{id}         A   Détail d'un template
  PUT    /api/email-templates/{id}         A   Modifier un template
  DELETE /api/email-templates/{id}         A   Supprimer un template
  POST   /api/email-templates/{id}/preview A   Aperçu rendu avec variables fictives
  POST   /api/email-templates/{id}/test    A   Envoyer un email de test à l'Admin

── EMAILS ENVOYÉS ───────────────────────────────────────────────────────
  GET    /api/applications/{id}/emails     R,A Historique des emails envoyés à ce candidat
  POST   /api/applications/{id}/emails     R,A Envoyer un email manuel (body: {template_id, variables})

── REPORTING ────────────────────────────────────────────────────────────
  GET    /api/reports/overview             A   KPIs globaux (nb candidatures, taux conversion, délai moyen)
                                               Query : ?period=month|quarter|year&job_id=
  GET    /api/reports/pipeline             A   Taux de conversion par étape
  GET    /api/reports/sources              A   Répartition des sources de candidatures
  GET    /api/reports/scores               A   Distribution des scores par offre
  GET    /api/reports/timeline             A   Évolution temporelle des candidatures
  GET    /api/reports/export               A   Export CSV de toutes les données
                                               Query : ?format=csv|json&job_id=&from=&to=

── WORKERS / TÂCHES ASYNC (usage interne, non exposé) ──────────────────
  POST   /api/internal/parse-cv            Worker  Déclenché par Celery après upload
  POST   /api/internal/send-email          Worker  Déclenché par Celery après changement d'étape
  POST   /api/internal/weekly-report       Worker  Déclenché par cron job lundi 8h00
```

**Récapitulatif par module**

| Module | Endpoints | Accès |
|---|---|---|
| Auth | 6 | Public + R + A |
| Organisations | 2 | A |
| Utilisateurs | 8 | A + R |
| Offres | 7 | R + A |
| Page publique | 2 | Public |
| Candidatures | 4 | R + A |
| Pipeline | 5 | R + A |
| Candidats | 5 | R + A |
| Scoring | 5 | R + A |
| Pipeline config | 2 | R + A |
| Templates email | 7 | A |
| Emails envoyés | 2 | R + A |
| Reporting | 6 | A |
| **Total** | **61** | |

#### Décision architecture multi-tenant

- [x] **SaaS multi-clients — Option C (RLS PostgreSQL) — DÉCIDÉ**

#### Conformité RGPD

À valider avec le DPO ou un juriste si le produit est destiné à traiter des données de candidats européens :
- [ ] Politique de confidentialité rédigée
- [ ] Durée de rétention des données définie (recommandation : 2 ans)
- [ ] Endpoints droit d'accès et droit à l'effacement planifiés dans le backlog
- [ ] Checkbox de consentement sur la page publique
