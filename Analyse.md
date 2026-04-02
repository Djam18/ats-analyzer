## 📋 Les 6 étapes pré-développement (rappel)

| Étape | Livrable | Objectif |
|-------|----------|----------|
| **1. Cadrage** | Brief produit / User Stories | Définir le périmètre et les acteurs |
| **2. Analyse fonctionnelle** | Spécifications fonctionnelles détaillées | Décrire précisément ce que fait chaque fonction |
| **3. Modélisation des données** | Schéma de base de données (MCD/MLD) | Structurer les entités et leurs relations |
| **4. Architecture technique** | Schéma d'architecture | Choisir les technologies et leur interaction |
| **5. Spécifications techniques** | Documentation technique (API, séquences) | Décrire *comment* c'est construit |
| **6. Plan de déploiement** | Stratégie Git, environnements, CI/CD | Organiser le travail local et la prod |

---

Voici mon **plan pour réaliser l'étape 1 : Cadrage** de votre solution ATS.

L'objectif du cadrage est de **définir précisément le périmètre, les utilisateurs, et les règles métier** avant toute conception technique.

---

## Plan d'exécution du cadrage

### 1. Identifier les acteurs (personas)
| Acteur | Rôle | Objectif principal |
|--------|------|--------------------|
| **Recruteur / RH** | Utilisateur principal | Gérer offres, candidats, pipeline |
| **Manager opérationnel** | Utilisateur secondaire | Consulter les profils, donner avis |
| **Candidat** | Utilisateur externe | Postuler, suivre son statut |
| **Admin technique** | Support | Configurer, exporter, gérer les droits |

**À faire** : Lister les actions clés par acteur (ex: le recruteur crée une offre, le candidat dépose un CV).

---

### 2. Définir les périmètres fonctionnels (MVP vs V2)
À partir de votre liste de fonctionnalités, je propose de découper en :

| Périmètre | Inclus (MVP) | Reporté (V2) |
|-----------|--------------|---------------|
| **Offres** | Création, statuts (brouillon/active/clôturée), URL publique | Archivage automatique, duplication |
| **CV parsing** | PDF/DOCX, extraction nom/email/compétences/exp/formation | Extraction de langues, diplômes précis |
| **Scoring** | Score 0-100 sur 4 critères pondérables, alerte seuil | Historique des versions de pondération |
| **Pipeline** | Colonnes fixes (Reçu → Présélection → Entretien RH → Entretien Tech → Offre → Embauché), drag & drop | Colonnes personnalisables |
| **Communications** | Templates d'emails basiques, envoi manuel | Déclenchement automatique par changement d'étape |
| **Reporting** | Export CSV, KPIs basiques (taux conversion, délais) | Graphiques, dashboard interactif |
| **Utilisateurs** | Un seul recruteur (pas de rôles) | Multi-utilisateurs, droits, SSO |

**À faire** : Valider ce découpage avec vous (ou votre équipe). Le MVP doit être livrable en ~4-6 semaines.

---

### 3. Rédiger les User Stories (format standard)
Exemple pour la gestion des offres :
```
En tant que recruteur, je veux créer une offre d'emploi avec un titre, une description, et des critères pondérés,
afin de recevoir des candidatures ciblées et d'obtenir un score automatique.

Critères d'acceptation :
- Je peux saisir : titre, description, localisation, type de contrat, liste de compétences requises (avec poids)
- Je peux définir 4 critères de scoring (ex: compétences, expérience, formation, langues) avec pourcentage
- Je peux sauvegarder en brouillon ou publier (devient active)
- Une URL publique unique est générée automatiquement
```

**À faire** : Produire une trentaine de user stories couvrant le MVP (je peux vous les générer).

---

### 4. Identifier les règles métier et contraintes
- **RGPD** : droit à l'oubli, consentement explicite du candidat, hébergement France
- **Sécurité** : URLs signées pour CV (expiration 1h), pas d'envoi de CV à des API externes (IA locale)
- **Performances** : parsing CV < 30s asynchrone
- **Tarification** : Plans gratuits/Pro/Entreprise (à intégrer dans le modèle de données)

**À faire** : Lister toutes les contraintes non fonctionnelles (sécurité, conformité, volumétrie).

---

### 5. Livrables finaux du cadrage
| Livrable | Description | Format |
|----------|-------------|--------|
| **Matrice acteurs/fonctionnalités** | Qui fait quoi | Tableau Excel/Markdown |
| **Backlog priorisé (MVP + V2)** | Liste des features avec priorité | Document texte |
| **User stories (20-30)** | Détail des fonctionnalités de base | Fichier Markdown ou outil (Notion, Jira) |
| **Règles métier & contraintes** | Liste des obligations techniques et légales | Document |

---
Voici le début de la rédaction du **document de cadrage** pour votre solution ATS, au format Markdown. J’ai suivi le plan d’exécution en commençant par l’identification des acteurs.

---

# Document de cadrage – ATS Platform (MVP)

## 1. Identifier les acteurs (personas)

| Acteur | Rôle | Objectif principal | Actions clés (MVP) |
|--------|------|--------------------|--------------------|
| **Recruteur / RH** | Utilisateur principal | Gérer l’ensemble du processus de recrutement (offres, candidats, pipeline) de manière autonome | – Créer, modifier, publier ou clôturer une offre<br>– Définir les critères pondérés de scoring<br>– Consulter les candidatures reçues et leur score<br>– Faire glisser un candidat d’une étape à l’autre (Kanban)<br>– Ajouter des notes internes<br>– Déclencher l’envoi d’un email à un candidat<br>– Exporter les données (CSV) |
| **Manager opérationnel** | Utilisateur secondaire (lecture seule ou commentaires) | Suivre l’avancement des recrutements pour son équipe, donner un avis technique | – Visualiser le pipeline Kanban (filtré par offre)<br>– Consulter le détail d’un candidat (CV, score, compétences)<br>– Ajouter un commentaire ou une note (sans modifier l’étape) |
| **Candidat** | Utilisateur externe | Postuler à une offre, suivre son statut (sans compte) | – Accéder à l’URL publique d’une offre<br>– Remplir le formulaire de candidature (nom, email, CV)<br>– Recevoir un accusé de réception par email<br>– (optionnel V2) Consulter son statut via un lien personnel |
| **Admin technique** | Support interne (équipe projet) | Configurer la plateforme, gérer les sauvegardes, assurer la conformité | – Accéder aux logs d’exécution (parsing, emails)<br>– Gérer les templates d’emails globaux<br>– Superviser l’hébergement France & RGPD<br>– Réaliser les exports complets |

### Interactions entre acteurs (flux simplifié)

```mermaid
graph LR
    C[Candidat] -->|postule via URL| O[Offre publique]
    O -->|créée par| R[Recruteur]
    R -->|consulte/note| D[Candidature]
    M[Manager] -->|donne avis| D
    R -->|change étape| D
    D -->|email auto| C
    A[Admin] -->|configure| R
```

---

## 2. Périmètre fonctionnel – MVP vs V2

| Fonctionnalité | Inclus dans le MVP | Reporté à V2 |
|----------------|--------------------|---------------|
| **Offres** : création, statuts (brouillon/active/clôturée), URL publique | ✅ | – |
| **Offres** : archivage automatique, duplication | ❌ | ✅ |
| **CV parsing** : PDF/DOCX, extraction nom/email/compétences/exp/formation | ✅ | – |
| **CV parsing** : extraction langues, diplômes précis, détection dates | ❌ | ✅ |
| **Scoring** : score 0-100 sur 4 critères pondérables (paramétrage offre) | ✅ | – |
| **Scoring** : alerte email si score > seuil | ✅ | – |
| **Scoring** : historique des versions de pondération | ❌ | ✅ |
| **Pipeline** : colonnes fixes (6 étapes), drag & drop | ✅ | – |
| **Pipeline** : colonnes personnalisables, filtres avancés | ❌ | ✅ |
| **Communications** : templates d’emails de base, envoi manuel (bouton) | ✅ | – |
| **Communications** : déclenchement automatique par changement d’étape | ❌ | ✅ |
| **Reporting** : export CSV (toutes données offres/candidats) | ✅ | – |
| **Reporting** : dashboard avec graphiques (taux conv., délais) | ❌ | ✅ |
| **Utilisateurs** : compte unique recruteur (pas de rôles) | ✅ | – |
| **Utilisateurs** : multi-utilisateurs, droits, SSO | ❌ | ✅ |

---

## 3. User stories (extrait – les 5 premières)

*Format* : **En tant que** [acteur] **je veux** [action] **afin de** [objectif].
*Critères d’acceptation* succincts.

1. **US‑OFF‑01** – En tant que recruteur, je veux créer une offre avec un titre, une description, un type de contrat et une localisation, afin de la publier ensuite.
   - *CA* : tous les champs obligatoires sont présents ; l’offre est sauvegardée en “brouillon”.

2. **US‑OFF‑02** – En tant que recruteur, je veux définir 4 critères de scoring (ex: compétences, expérience, formation, langues) avec un poids (en %) pour chaque critère, afin que le score IA soit personnalisé par offre.
   - *CA* : la somme des poids doit faire 100 % ; les poids sont modifiables même après publication.

3. **US‑OFF‑03** – En tant que recruteur, je veux publier une offre (statut “active”) et obtenir une URL publique unique, afin de la diffuser aux candidats.
   - *CA* : l’URL est de la forme `/offre/{slug}` ; un candidat non connecté peut y accéder.

4. **US‑CV‑01** – En tant que candidat, je veux déposer mon CV (PDF ou DOCX) et renseigner mon nom/email sur la page de l’offre, afin de postuler.
   - *CA* : après soumission, un email de confirmation lui est envoyé ; le CV est stocké de façon sécurisée.

5. **US‑SCORE‑01** – En tant que recruteur, je veux voir pour chaque candidature un score global (0–100) et le détail par critère, afin d’identifier rapidement les profils les plus pertinents.
   - *CA* : le score est calculé automatiquement dans les 30 secondes suivant le dépôt.

*(La liste complète des user stories MVP sera fournie dans le prochain livrable si vous le souhaitez.)*

---

## 4. Règles métier & contraintes non fonctionnelles

| Domaine | Règle / Contrainte |
|---------|--------------------|
| **RGPD** | – Le candidat doit consentir explicitement au traitement de ses données avant soumission.<br>– Un candidat peut demander l’accès, la rectification ou la suppression de ses données (interface dédiée ou email).<br>– Toutes les données (CV, extractions, scores) sont hébergées en France. |
| **Sécurité** | – Les CV stockés sont accessibles uniquement via des URLs signées (expiration 1 heure).<br>– L’IA de parsing tourne en local (pas d’envoi à des API tierces).<br>– Les sessions recruteur sont protégées par mot de passe fort (ou SSO en V2). |
| **Performances** | – Parsing d’un CV ≤ 30 secondes (traitement asynchrone).<br>– La page publique de candidature se charge en < 2 secondes. |
| **Disponibilité** | – L’application doit être disponible 99,5 % du temps (hors maintenance programmée). |
| **Tarification** | – Les plans gratuits/Pro/Entreprise sont gérés en V2 ; en MVP, un seul compte recruteur “gratuit” sans limitation de volume. |

---
Voici le **plan pour l’étape 2 : Analyse fonctionnelle détaillée**.

L’objectif est de décrire **précisément le comportement attendu** du système, fonction par fonction, sans encore parler de technologie. On produit des diagrammes et des règles métier exploitables par les développeurs.

---

## Plan d’exécution – Analyse fonctionnelle

### 1. Décomposition en modules fonctionnels
Découper le périmètre MVP en modules indépendants mais interconnectés :

| Module | Fonctions couvertes |
|--------|---------------------|
| **Gestion des offres** | CRUD offres, statuts, génération d’URL publique, paramétrage des critères pondérés |
| **Candidature publique** | Formulaire de dépôt, validation, stockage, accusé de réception |
| **Parsing & extraction IA** | Réception fichier, file d’attente, extraction (nom, email, compétences, expérience, formation), stockage structuré |
| **Scoring & matching** | Calcul du score selon pondérations de l’offre, déclenchement d’alerte si seuil dépassé |
| **Pipeline Kanban** | Affichage des colonnes, drag & drop, changement d’étape, historique, notes internes |
| **Communication** | Templates d’emails, envoi manuel (depuis la fiche candidat) |
| **Reporting & export** | Export CSV (candidats + offres), KPIs de base (calculés à la demande) |

---

### 2. Pour chaque module : rédiger les spécifications fonctionnelles

#### Format type par fonction
```
## Module : [nom]
### Fonction : [nom]
- **Acteur déclencheur** : (recruteur / candidat / système)
- **Pré-conditions** : ce qui doit être vrai avant
- **Post-conditions** : ce qui est vrai après
- **Scénario nominal** (pas à pas)
- **Scénarios alternatifs / erreurs**
- **Règles de gestion** (ex: un score ne peut être calculé sans extraction complète)
- **Données manipulées** (entrées/sorties)
```

#### Exemple concret pour une fonction (extrait)
```
Module : Scoring & matching
Fonction : Calcul automatique du score à la réception d’un CV

- Acteur : système (déclenché après parsing)
- Pré-conditions :
   - Offre existe et est active
   - Critères pondérés sont définis (4 critères, somme = 100%)
   - CV a été parsé avec succès (champs extraits)
- Post-conditions :
   - Un score global (0-100) est stocké dans la candidature
   - Le détail par critère est stocké
   - Si score > seuil (paramétré dans l’offre), une alerte email est envoyée au recruteur
- Scénario nominal :
   1. Le système reçoit un événement “Parsing terminé”
   2. Il charge l’offre associée et ses pondérations
   3. Pour chaque critère (compétences, expérience, formation, langues) :
      - Compare les données extraites avec les exigences de l’offre
      - Calcule un score partiel (0-100) pondéré
   4. Additionne les scores partiels → score global
   5. Persiste le résultat
   6. Compare avec le seuil et envoie une alerte si nécessaire
- Alternatifs :
   - Parsing incomplet (ex: pas d’email) → score = 0, alerte système au recruteur
   - Offre sans pondérations → valeur par défaut (25% chacun)
- Règles de gestion :
   - Seul un score calculé après parsing compte (pas de recalcul manuel)
   - Le seuil d’alerte est modifiable par offre même après publication
```

---

### 3. Diagrammes UML / notations (obligatoires pour l’analyse fonctionnelle)

| Diagramme | Usage | Outil conseillé |
|-----------|-------|------------------|
| **Diagramme de cas d’utilisation** | Vue globale acteurs/fonctions | Mermaid, Draw.io |
| **Diagramme de séquence** (au moins 3) | Dépôt candidature, calcul scoring, changement d’étape Kanban | Mermaid (intégrable dans Markdown) |
| **Diagramme d’activité / état** | Pipeline (états d’une candidature) | Mermaid |

*Exemple d’ordre pour les séquences :*
1. **Séquence “Dépôt candidature”** : Candidat → Offre publique → Système → Parsing asynchrone → Email accusé.
2. **Séquence “Calcul du score”** : Parsing terminé → Scoring → Mise à jour candidature → Alerte si seuil.
3. **Séquence “Changement étape Kanban”** : Recruteur → Drag & drop → Mise à jour statut → (optionnel) email auto (V2).

---

### 4. Traitement des erreurs et cas limites (détaillés par fonction)

- Fichier CV corrompu ou format non supporté → message clair au candidat.
- Timeout du parsing (>30s) → mise en file d’attente avec nouvelle tentative (max 3).
- Suppression d’une offre active alors que des candidatures existent → règle métier à définir (archivage forcé ? blocage ?).
- Score calculé avant que toutes les données soient extraites → ne pas afficher de score partiel.

---

### 5. Règles de gestion transverse

- **Unicité** : Un candidat ne peut pas postuler deux fois à la même offre avec le même email (contrôle à l’envoi).
- **Consentement** : La case “J’accepte que mes données soient traitées” est obligatoire avant soumission.
- **Audit** : Toute modification (changement d’étape, note, suppression) est horodatée avec l’identifiant du recruteur.

---

### 6. Livrables finaux de l’analyse fonctionnelle

| Livrable | Contenu |
|----------|---------|
| **Spécifications détaillées** (document texte) | 1 section par module, avec cas nominaux/alternatifs/règles |
| **Diagrammes** (intégrés ou à part) | Cas d’utilisation, séquences, activité/état |
| **Glossaire fonctionnel** | Définition des termes métier (ex: “score seuil”, “parsing”, “pipeline”) |
| **Matrice de traçabilité** | Lien entre chaque user story (étape 1) et spécification fonctionnelle |

---
Voici la **décomposition en modules fonctionnels** pour l’analyse fonctionnelle de votre ATS Platform (MVP), au format Markdown.

---

# Analyse fonctionnelle – ATS Platform (MVP)

## 1. Décomposition en modules fonctionnels

Le périmètre MVP est découpé en **7 modules indépendants mais interconnectés**. Chaque module regroupe un ensemble cohérent de fonctionnalités.

| Module | Fonctions couvertes (MVP) |
|--------|----------------------------|
| **M1 – Gestion des offres** | – Création d’une offre (titre, description, localisation, type contrat)<br>– Modification d’une offre (brouillon uniquement)<br>– Suppression (soft delete) d’une offre brouillon<br>– Changement de statut : brouillon → active → clôturée<br>– Définition des 4 critères de scoring avec pondération (%, somme=100)<br>– Génération automatique d’une URL publique par offre (slug unique)<br>– Consultation de la liste des offres (avec filtres par statut) |
| **M2 – Candidature publique** | – Affichage d’une page publique par offre (titre, description, formulaire)<br>– Formulaire de dépôt : nom, email, upload CV (PDF/DOCX)<br>– Validation champs (email valide, fichier présent, taille max 5 Mo)<br>– Consentement RGPD obligatoire (case à cocher)<br>– Envoi asynchrone des données vers le module de parsing<br>– Accusé de réception par email au candidat (template simple) |
| **M3 – Parsing & extraction IA** | – Réception des fichiers depuis le formulaire ou dépôt direct recruteur<br>– File d’attente asynchrone (priorité FIFO)<br>– Extraction automatique des champs : nom, email, compétences (liste), expérience (années totales), formation (dernier diplôme)<br>– Stockage structuré des données extraites dans la candidature<br>– Gestion des erreurs (format invalide, fichier corrompu, timeout < 30s) avec tentative max 3 |
| **M4 – Scoring & matching** | – Déclenchement automatique après parsing réussi<br>– Chargement des pondérations de l’offre (4 critères)<br>– Calcul du score partiel par critère (0–100) basé sur comparaison avec exigences de l’offre<br>– Agrégation en score global (0–100)<br>– Persistance du score (global + détail)<br>– Comparaison avec seuil d’alerte défini dans l’offre<br>– Envoi d’un email d’alerte au recruteur si score > seuil |
| **M5 – Pipeline Kanban** | – Affichage des 6 colonnes fixes : Reçu → Présélection → Entretien RH → Entretien Tech → Offre → Embauché<br>– Visualisation des candidats sous forme de cartes (nom, score, étape actuelle)<br>– Drag & drop pour déplacer un candidat d’une colonne à l’autre<br>– Changement d’étape avec horodatage et traçabilité (qui, quand)<br>– Ajout de notes internes sur une carte (texte libre)<br>– Historique des actions affiché dans le détail du candidat<br>– Filtrage simple (par score > X, par compétence détectée) |
| **M6 – Communication manuelle** | – Consultation de la liste des templates d’emails (4 par défaut : confirmation réception, relance entretien, refus, offre)<br>– Personnalisation basique des templates (objet, corps) par le recruteur<br>– Envoi manuel d’un email depuis la fiche candidat (choix du template, variables dynamiques : nom, poste, date)<br>– Journal des envois (date, destinataire, template utilisé) |
| **M7 – Reporting & export** | – Page de tableau de bord avec KPIs calculés à la demande :<br>  * Taux de conversion global (candidats reçus → embauchés)<br>  * Délai moyen par étape (en jours, calculé sur historique)<br>– Export CSV : toutes les données des offres et candidatures (champs structurés, scores, dates, statuts)<br>– Filtrage avant export (par offre, par période) |

---

### Interactions entre modules (flux fonctionnel)

```mermaid
flowchart TD
    A[M1 - Offres] -->|génère URL| B[M2 - Candidature publique]
    B -->|dépose CV| C[M3 - Parsing IA]
    C -->|données extraites| D[M4 - Scoring]
    D -->|candidature scorée| E[M5 - Pipeline Kanban]
    E -->|changement étape| F[M6 - Communication manuelle]
    E -->|données historisées| G[M7 - Reporting/Export]
```

---

## Prochaines étapes dans l’analyse fonctionnelle

Une fois les modules identifiés, l’analyse fonctionnelle détaille **chaque fonction** avec :

- Acteur déclencheur
- Pré-conditions / post-conditions
- Scénario nominal
- Scénarios alternatifs / erreurs
- Règles de gestion associées

Voici les **spécifications détaillées** du module **M1 – Gestion des offres**, conformément au format défini dans l’analyse fonctionnelle.

---

# Spécifications fonctionnelles – Module M1 : Gestion des offres

## 1. Vue d’ensemble du module

| Propriété | Description |
|-----------|-------------|
| **Objectif** | Permettre au recruteur de créer, modifier, publier, clôturer et supprimer des offres d’emploi, ainsi que de paramétrer les critères de scoring associés. |
| **Acteur principal** | Recruteur (utilisateur connecté) |
| **Dépendances** | Aucune (module autonome, mais alimente M2, M3, M4) |
| **Données manipulées** | Offre (titre, description, localisation, type contrat, statut, URL slug, critères pondérés, seuil alerte) |

---

## 2. Liste des fonctions

| Fonction | Code | Description sommaire |
|----------|------|----------------------|
| Créer une offre | M1-F1 | Saisie des champs de base, sauvegarde en brouillon |
| Modifier une offre (brouillon) | M1-F2 | Mise à jour des champs tant que l’offre n’est pas active |
| Définir les critères de scoring | M1-F3 | Paramétrage des 4 critères avec pondération (%) |
| Générer l’URL publique | M1-F4 | Création automatique d’un slug unique à la première publication |
| Publier une offre (brouillon → active) | M1-F5 | Passage en actif, l’URL devient accessible au public |
| Clôturer une offre (active → clôturée) | M1-F6 | Fermeture aux nouvelles candidatures |
| Archiver / supprimer une offre | M1-F7 | Suppression logique (soft delete) d’une offre brouillon ou clôturée |
| Lister / filtrer les offres | M1-F8 | Affichage avec filtres par statut (brouillon, active, clôturée) |

---

## 3. Spécification détaillée par fonction

### M1-F1 : Créer une offre

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Recruteur |
| **Pré-conditions** | Le recruteur est authentifié. |
| **Post-conditions** | Une nouvelle offre est créée en base avec le statut `brouillon`. Aucune URL publique n’est encore générée. |
| **Scénario nominal** | 1. Le recruteur clique sur « Nouvelle offre ».<br>2. Le système affiche un formulaire avec les champs : titre, description, localisation, type contrat (CDI, CDD, stage, freelance).<br>3. Le recruteur remplit les champs obligatoires (titre, description).<br>4. Le système valide que le titre n’est pas vide et que la description n’est pas vide.<br>5. Le système crée l’offre avec un ID unique, date de création, statut `brouillon`.<br>6. Le système redirige vers la page de détail de l’offre (en brouillon). |
| **Alternatifs / erreurs** | – Champs obligatoires manquants → message d’erreur, pas de création.<br>– Titre déjà utilisé pour une autre offre non archivée → avertissement mais autorisé (pas d’unicité stricte). |
| **Règles de gestion** | – Les offres en brouillon ne sont pas visibles publiquement.<br>– Les champs localisation et type contrat sont optionnels.<br>– Date de création automatique (horodatage serveur). |

---

### M1-F2 : Modifier une offre (brouillon)

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Recruteur |
| **Pré-conditions** | L’offre existe et son statut est `brouillon`. |
| **Post-conditions** | Les champs modifiables (titre, description, localisation, type contrat) sont mis à jour. |
| **Scénario nominal** | 1. Le recruteur accède à la page de détail d’une offre brouillon.<br>2. Il clique sur « Modifier ».<br>3. Le système affiche le formulaire pré-rempli.<br>4. Le recruteur modifie un ou plusieurs champs et valide.<br>5. Le système sauvegarde les modifications, conserve le statut `brouillon`. |
| **Alternatifs / erreurs** | – Si l’offre est active ou clôturée → modification interdite (bouton désactivé).<br>– Si les modifications violent les validations (ex: titre vide) → message d’erreur, pas de sauvegarde. |
| **Règles de gestion** | – La modification d’une offre brouillon n’affecte aucune candidature (pas encore de candidatures possibles).<br>– Historique des modifications non requis en MVP. |

---

### M1-F3 : Définir les critères de scoring

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Recruteur |
| **Pré-conditions** | L’offre existe (brouillon ou active). |
| **Post-conditions** | Les 4 critères de scoring avec leurs pondérations (en %) sont enregistrés pour l’offre. La somme des pondérations doit être 100 %. |
| **Scénario nominal** | 1. Depuis la page de détail de l’offre, le recruteur clique sur « Configurer le scoring ».<br>2. Le système affiche 4 champs (ex: Compétences, Expérience, Formation, Langues) avec un slider ou champ numérique pour le poids (%).<br>3. Le recruteur saisit les poids (ex: 40, 30, 20, 10).<br>4. Le système vérifie que la somme = 100.<br>5. Le système enregistre la configuration.<br>6. Un seuil d’alerte (score minimum pour déclencher une alerte) peut être saisi optionnellement (valeur par défaut 80). |
| **Alternatifs / erreurs** | – Somme des poids ≠ 100 → message d’erreur, pas d’enregistrement.<br>– Un critère avec poids 0 est autorisé (critère ignoré).<br>– Si l’offre est déjà active et a reçu des candidatures, la modification des pondérations est autorisée mais ne recalculera pas les scores existants (seulement pour les nouveaux candidats). |
| **Règles de gestion** | – Les 4 critères sont fixes (nom non modifiable).<br>– Si jamais aucun critère n’est configuré avant la première candidature, une configuration par défaut est appliquée (25% chacun).<br>– La configuration peut être modifiée à tout moment, mais sans rétroactivité sur les scores déjà calculés. |

---

### M1-F4 : Générer l’URL publique

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Système (automatique à la première publication) |
| **Pré-conditions** | L’offre passe de `brouillon` à `active` pour la première fois. |
| **Post-conditions** | Une URL unique de type `https://domaine/offre/{slug}` est générée et stockée. Le slug est basé sur le titre de l’offre (nettoyé). |
| **Scénario nominal** | 1. Le recruteur publie l’offre (M1-F5).<br>2. Le système génère un slug : conversion du titre en minuscules, suppression des accents, remplacement des espaces par des tirets, ajout d’un suffixe numérique si conflit.<br>3. Le système stocke le slug et l’URL complète.<br>4. L’URL est affichée au recruteur et utilisable par les candidats. |
| **Alternatifs / erreurs** | – Conflit de slug (déjà utilisé pour une autre offre active ou brouillon) → ajout d’un tiret et d’un compteur (ex: `developpeur-python-2`).<br>– Titre vide (normalement impossible) → slug par défaut `offre-{id}`. |
| **Règles de gestion** | – Une fois généré, le slug ne change jamais, même si le titre est modifié ultérieurement (pour ne pas casser les liens).<br>– L’URL publique n’est accessible que si le statut est `active`. Si l’offre est clôturée, la page affiche « Cette offre n’accepte plus de candidatures ». |

---

### M1-F5 : Publier une offre (brouillon → active)

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Recruteur |
| **Pré-conditions** | L’offre est en statut `brouillon`. |
| **Post-conditions** | Statut de l’offre passe à `active`. L’URL publique est générée (si ce n’est pas déjà fait). L’offre devient visible sur la page publique. |
| **Scénario nominal** | 1. Le recruteur, sur la page de détail de l’offre brouillon, clique sur « Publier ».<br>2. Le système vérifie que les champs obligatoires (titre, description) sont remplis.<br>3. Le système vérifie qu’une configuration de scoring existe (sinon applique la config par défaut).<br>4. Le système génère le slug (M1-F4) si nécessaire.<br>5. Le système passe le statut à `active`.<br>6. L’offre est désormais accessible à l’URL publique. |
| **Alternatifs / erreurs** | – Si des champs obligatoires manquent → message d’erreur, pas de publication.<br> – Si l’offre est déjà active → le bouton « Publier » est désactivé. |
| **Règles de gestion** | – Une fois active, l’offre ne peut plus être modifiée (sauf scoring et seuil d’alerte).<br>– On peut toujours clôturer une offre active (M1-F6). |

---

### M1-F6 : Clôturer une offre (active → clôturée)

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Recruteur |
| **Pré-conditions** | L’offre est en statut `active`. |
| **Post-conditions** | Statut passe à `clôturée`. La page publique affiche un message « Cette offre n’accepte plus de candidatures ». Le formulaire de dépôt est désactivé. |
| **Scénario nominal** | 1. Depuis la page de détail de l’offre active, le recruteur clique sur « Clôturer ».<br>2. Le système demande confirmation.<br>3. Le système passe le statut à `clôturée`.<br>4. La date de clôture est enregistrée (optionnel). |
| **Alternatifs / erreurs** | – Si l’offre est déjà clôturée ou brouillon → bouton désactivé.<br>– Si l’offre a des candidatures en cours, la clôture ne les supprime pas (elles restent consultables dans le pipeline). |
| **Règles de gestion** | – Une offre clôturée peut être réactivée ? (MVP : non, prévoir une fonction d’archivage ou de duplication en V2).<br>– Les statistiques (taux de conversion) incluent les offres clôturées. |

---

### M1-F7 : Archiver / supprimer une offre (soft delete)

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Recruteur |
| **Pré-conditions** | L’offre est en statut `brouillon` ou `clôturée`. (Une offre active ne peut pas être supprimée directement, il faut d’abord la clôturer.) |
| **Post-conditions** | L’offre n’apparaît plus dans les listes actives (filtrage par défaut exclut les archivées). Elle est conservée en base pour l’historique. |
| **Scénario nominal** | 1. Le recruteur, sur la liste des offres, clique sur l’icône « Archiver » pour une offre brouillon ou clôturée.<br>2. Le système demande confirmation.<br>3. Le système marque l’offre comme `archivée` (soft delete).<br>4. L’offre disparaît de la liste par défaut. |
| **Alternatifs / erreurs** | – Si l’offre est active → l’option d’archivage est désactivée (invite à clôturer d’abord).<br>– Une offre archivée peut être restaurée ? (V2). |
| **Règles de gestion** | – Les offres archivées ne sont pas supprimées physiquement (conformité RGPD ? Si un candidat demande suppression de ses données, l’offre elle-même peut rester anonymisée). |

---

### M1-F8 : Lister / filtrer les offres

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Recruteur |
| **Pré-conditions** | Aucune. |
| **Post-conditions** | Affichage d’un tableau/liste des offres selon les filtres choisis. |
| **Scénario nominal** | 1. Le recruteur accède à la page « Mes offres ».<br>2. Par défaut, le système affiche les offres actives + brouillons (exclut les clôturées et archivées).<br>3. Le recruteur peut sélectionner un filtre : « Toutes », « Brouillons », « Actives », « Clôturées », « Archivées ».<br>4. Le système affiche la liste correspondante avec pour chaque offre : titre, statut, date de création, nombre de candidatures, URL publique (icône copier). |
| **Alternatifs / erreurs** | – Aucune offre correspondant au filtre → message « Aucune offre trouvée ». |
| **Règles de gestion** | – Le nombre de candidatures affiché est un compteur en temps réel (requête SQL).<br>– Un clic sur le titre mène à la page de détail de l’offre. |

---

## 4. Règles de gestion transverses du module M1

| Règle | Description |
|-------|-------------|
| **RG‑01** | Les offres clôturées ou archivées ne doivent pas pouvoir recevoir de nouvelles candidatures. |
| **RG‑02** | La suppression d’une offre (archivage) ne supprime pas les candidatures associées (elles restent visibles dans le pipeline, mais l’offre étant archivée, elles sont en lecture seule). |
| **RG‑03** | Un recruteur ne peut pas avoir deux offres actives avec exactement le même slug, mais peut avoir le même titre (le slug est rendu unique). |
| **RG‑04** | Toute modification des pondérations de scoring sur une offre active n’affecte que les futurs candidats (pas de recalcul rétroactif). |

---

## 5. Écrans associés (esquisses fonctionnelles)

| Écran | Éléments clés |
|-------|----------------|
| **Liste des offres** | Tableau : titre, statut, date création, nb candidatures, actions (modifier, publier, clôturer, archiver) |
| **Formulaire création / modification** | Champs texte (titre, description), select (localisation, type contrat) |
| **Page détail offre** | Résumé + onglets : « Candidatures » (pipeline), « Configuration scoring », « Paramètres » (publier/clôturer/archiver) |
| **Configuration scoring** | 4 sliders numériques (somme 100), champ seuil alerte |

---
Voici les **spécifications détaillées** du module **M2 – Candidature publique**, conformément au format défini dans l’analyse fonctionnelle.

---

# Spécifications fonctionnelles – Module M2 : Candidature publique

## 1. Vue d’ensemble du module

| Propriété | Description |
|-----------|-------------|
| **Objectif** | Permettre à un candidat de consulter une offre d’emploi et de déposer sa candidature (nom, email, CV) via une page publique sécurisée. |
| **Acteur principal** | Candidat (non authentifié, utilisateur externe) |
| **Dépendances** | Dépend du module M1 (les offres actives fournissent le contenu et l’URL publique). Alimente le module M3 (Parsing & extraction IA). |
| **Données manipulées** | Candidature (nom, email, fichier CV, date de dépôt, consentement RGPD, IP, user-agent) |

---

## 2. Liste des fonctions

| Fonction | Code | Description sommaire |
|----------|------|----------------------|
| Afficher la page publique d’une offre | M2-F1 | Affichage du titre, description et formulaire de candidature |
| Soumettre une candidature | M2-F2 | Envoi du formulaire avec validation des champs et du CV |
| Valider le consentement RGPD | M2-F3 | Case à cocher obligatoire, enregistrement de la preuve de consentement |
| Envoyer un accusé de réception | M2-F4 | Email automatique au candidat après soumission réussie |
| Gérer les erreurs de soumission | M2-F5 | Messages d’erreur clairs (format CV, taille, doublon, etc.) |
| Bloquer les candidatures sur offre clôturée | M2-F6 | Affichage d’un message et désactivation du formulaire si offre inactive |

---

## 3. Spécification détaillée par fonction

### M2-F1 : Afficher la page publique d’une offre

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Candidat (accède à l’URL `/offre/{slug}`) |
| **Pré-conditions** | L’offre existe en base et a un statut `active`. |
| **Post-conditions** | La page s’affiche avec les informations de l’offre et le formulaire de candidature. |
| **Scénario nominal** | 1. Le candidat saisit l’URL publique (ex: `https://ats.exemple/offre/developpeur-python`).<br>2. Le système recherche l’offre correspondant au slug.<br>3. Si l’offre est `active`, le système affiche :<br>   - Titre, description, localisation, type contrat.<br>   - Formulaire (nom, email, upload CV, case consentement).<br>4. Si l’offre est `clôturée` ou `archivée`, le système affiche un message « Cette offre n’accepte plus de candidatures » et aucun formulaire. |
| **Alternatifs / erreurs** | – Slug invalide ou offre inexistante → page 404 personnalisée.<br>– Offre en brouillon (normalement jamais exposée, mais sécurité) → redirection vers 404. |
| **Règles de gestion** | – La page doit être responsive (mobile friendly).<br>– Aucune authentification requise.<br>– Le slug est insensible à la casse (normalisé en minuscules). |

---

### M2-F2 : Soumettre une candidature

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Candidat (clic sur « Postuler » après remplissage du formulaire) |
| **Pré-conditions** | – L’offre est `active`.<br>– Le candidat a rempli tous les champs obligatoires.<br>– Le consentement RGPD est coché.<br>– Le fichier CV est au format PDF ou DOCX, taille ≤ 5 Mo. |
| **Post-conditions** | – Une candidature est créée en base avec statut `reçu`.<br>– Le CV est stocké de manière sécurisée (URL signée).<br>– Un événement asynchrone est déclenché pour le parsing (M3).<br>– Un accusé de réception est envoyé (M2-F4). |
| **Scénario nominal** | 1. Le candidat saisit son nom, son email, sélectionne son fichier CV.<br>2. Il coche la case « J’accepte que mes données soient traitées… ».<br>3. Il clique sur « Postuler ».<br>4. Le système valide :<br>   - Nom non vide, email valide (format).<br>   - Fichier présent, type autorisé, taille ≤ 5 Mo.<br>   - Consentement = true.<br>5. Le système vérifie qu’aucune candidature identique (même email + même offre) n’existe déjà (optionnel selon règle métier).<br>6. Le système crée l’enregistrement `candidature` avec :<br>   - offre_id, nom, email, date_dépôt (timestamp), statut = `reçu`, IP, user-agent.<br>   - Chemin du fichier stocké (dossier sécurisé).<br>7. Le système met le fichier dans une file d’attente pour parsing (M3).<br>8. Le système affiche une page de confirmation « Merci, votre candidature a bien été envoyée ».<br>9. Un email d’accusé est envoyé en arrière-plan. |
| **Alternatifs / erreurs** | – Email déjà utilisé pour cette offre (si règle anti-doublon activée) → message « Vous avez déjà postulé à cette offre ».<br>– Fichier corrompu ou mauvais type → message « Format non accepté. Utilisez PDF ou DOCX ».<br>– Fichier trop volumineux (>5 Mo) → message « Le fichier ne doit pas dépasser 5 Mo ».<br>– Case consentement non cochée → message « Vous devez accepter le traitement de vos données ».<br> – Erreur technique lors du stockage du fichier → la candidature n’est pas créée, message d’erreur générique. |
| **Règles de gestion** | – **Anti-doublon** : En MVP, on peut choisir d’autoriser ou non les doublons. Par défaut, on interdit : une même adresse email ne peut postuler deux fois à la même offre (vérification avant insertion).<br>– L’adresse IP et le user-agent sont stockés pour traçabilité (RGPD, lutte contre le spam).<br>– Le fichier CV est renommé en `{uuid}_{nom_original}` pour éviter les collisions. |

---

### M2-F3 : Valider le consentement RGPD

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Candidat (action de cocher la case) |
| **Pré-conditions** | Formulaire affiché. |
| **Post-conditions** | Le consentement est enregistré avec sa date et le texte exact de la mention. |
| **Scénario nominal** | 1. Le candidat voit le texte : « En soumettant ce formulaire, j’accepte que mes données (nom, email, CV) soient utilisées par [Nom Société] dans le cadre de ce recrutement. Je peux demander leur suppression à tout moment. »<br>2. Il coche la case obligatoire.<br>3. Lors de la soumission, le système enregistre un booléen `consentement` à `true` avec la date et l’empreinte du texte de consentement. |
| **Alternatifs / erreurs** | – Case non cochée → soumission refusée, message d’erreur. |
| **Règles de gestion** | – Le texte de consentement doit être stocké en base (ou version) pour preuve.<br> – En MVP, on stocke simplement le booléen + date ; une version plus avancée stockerait le texte exact. |

---

### M2-F4 : Envoyer un accusé de réception

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Système (après création réussie d’une candidature) |
| **Pré-conditions** | La candidature a été enregistrée. |
| **Post-conditions** | Un email est envoyé au candidat. |
| **Scénario nominal** | 1. Le système place une tâche d’envoi d’email dans une file asynchrone.<br>2. L’email utilise un template simple : « Bonjour {nom}, nous avons bien reçu votre candidature pour l’offre {titre_offre}. Nous reviendrons vers vous sous peu. »<br>3. L’email est expédié depuis une adresse noreply. |
| **Alternatifs / erreurs** | – Échec d’envoi (SMTP down) → tentative de réessai (3 fois, intervalle 5 min). Si persistant, log d’erreur mais la candidature est quand même enregistrée.<br>– Pas d’email de relance en MVP. |
| **Règles de gestion** | – L’envoi est asynchrone pour ne pas ralentir la réponse HTTP.<br>– Le template peut être modifié par le recruteur (module M6). |

---

### M2-F5 : Gérer les erreurs de soumission

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Système, lors de la validation du formulaire |
| **Pré-conditions** | Une ou plusieurs règles de validation échouent. |
| **Post-conditions** | Le formulaire est réaffiché avec les erreurs clairement indiquées, les champs déjà saisis sont pré-remplis (sauf le CV, à re-sélectionner). |
| **Scénario nominal** | 1. Le candidat soumet un formulaire invalide (ex: email mal formé).<br>2. Le système renvoie la même page avec un message d’erreur en haut : « L’email n’est pas valide ».<br>3. Les champs nom et email sont pré-remplis avec les valeurs saisies.<br>4. Le champ CV est réinitialisé (mesure de sécurité, l’utilisateur doit re-sélectionner le fichier). |
| **Alternatifs / erreurs** | – Erreur technique (base de données inaccessible) → afficher un message générique « Problème technique, veuillez réessayer plus tard ». |
| **Règles de gestion** | – Ne jamais afficher les détails techniques à l’utilisateur.<br> – Journaliser les erreurs techniques dans les logs serveur. |

---

### M2-F6 : Bloquer les candidatures sur offre clôturée

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Candidat tentant d’accéder à une offre clôturée ou archivée |
| **Pré-conditions** | L’offre existe mais son statut n’est pas `active` (clôturée, archivée, brouillon). |
| **Post-conditions** | La page s’affiche avec un message informatif, sans formulaire. |
| **Scénario nominal** | 1. Le candidat accède à l’URL d’une offre clôturée.<br>2. Le système affiche : « Cette offre n’accepte plus de candidatures. Consultez nos autres offres. »<br>3. Pas de formulaire. |
| **Alternatifs / erreurs** | – Offre brouillon (ne devrait pas être publique, mais si accès direct) → même comportement que clôturée. |
| **Règles de gestion** | – Les offres archivées suivent la même règle.<br>– Un lien vers la liste des offres actives peut être proposé. |

---

## 4. Règles de gestion transverses du module M2

| Règle | Description |
|-------|-------------|
| **RG‑05** | La page publique ne doit contenir aucune information confidentielle (ex: email du recruteur). |
| **RG‑06** | Le fichier CV téléversé est immédiatement scanné antivirus (option V2) ; en MVP, on se fie à l’extension et à la taille. |
| **RG‑07** | L’envoi de l’email d’accusé ne doit pas divulguer d’informations sensibles (ex: date d’entretien). |
| **RG‑08** | Le stockage du CV doit utiliser des URLs signées avec expiration (1h) pour tout accès ultérieur par le recruteur. |
| **RG‑09** | Le taux de soumission (rate limiting) par IP : limiter à 5 candidatures par heure pour éviter les abus. |

---

## 5. Écrans associés (esquisses fonctionnelles)

| Écran | Éléments clés |
|-------|----------------|
| **Page publique d’une offre (active)** | Titre, description, localisation, contrat ; formulaire : nom, email, upload CV, case consentement, bouton « Postuler » |
| **Page publique d’une offre (clôturée)** | Message « Offre clôturée » + mention « Plus de candidatures » |
| **Page de confirmation** | Message de remerciement + info sur email accusé |
| **Page d’erreur** | Affichage des erreurs de validation en haut du formulaire |

---

## 6. Interactions avec les autres modules

```mermaid
sequenceDiagram
    participant Candidat
    participant M2 as M2 - Page publique
    participant M1 as M1 - Offres
    participant Base
    participant M3 as M3 - Parsing IA
    participant Email as Service email

    Candidat->>M2: GET /offre/{slug}
    M2->>M1: Vérifier statut offre
    M1-->>M2: active
    M2-->>Candidat: Affiche formulaire

    Candidat->>M2: POST candidature (nom, email, CV)
    M2->>Base: Créer candidature (statut reçu)
    Base-->>M2: ID candidature
    M2->>M3: Déclencher parsing asynchrone
    M2->>Email: Envoyer accusé réception
    M2-->>Candidat: Page confirmation
```

---
Voici les **spécifications détaillées** du module **M3 – Parsing & extraction IA**, conformément au format établi.

---

# Spécifications fonctionnelles – Module M3 : Parsing & extraction IA

## 1. Vue d’ensemble du module

| Propriété | Description |
|-----------|-------------|
| **Objectif** | Extraire automatiquement les informations structurées (nom, email, compétences, expérience, formation) à partir du fichier CV (PDF/DOCX) déposé par un candidat, afin d’alimenter le scoring et le pipeline. |
| **Acteur déclencheur** | Système (déclenché après création d’une candidature par M2, ou après dépôt direct par recruteur) |
| **Dépendances** | Reçoit des fichiers depuis M2. Alimente M4 (Scoring) après extraction. |
| **Données manipulées** | Fichier CV (PDF/DOCX), données extraites (nom, email, compétences, années expérience, formation), statut du parsing, logs d’erreur. |

---

## 2. Liste des fonctions

| Fonction | Code | Description sommaire |
|----------|------|----------------------|
| Mettre en file d’attente un CV | M3-F1 | Réception d’un fichier et ajout dans une queue asynchrone |
| Traiter un CV (parsing) | M3-F2 | Extraction des champs via IA, mise à jour de la candidature |
| Extraire le nom et l’email | M3-F3 | Détection du nom complet et adresse email (priorité au formulaire) |
| Extraire les compétences | M3-F4 | Identification d’une liste de compétences (techniques et transverses) |
| Extraire l’expérience (années) | M3-F5 | Calcul du nombre total d’années d’expérience professionnelle |
| Extraire la formation (dernier diplôme) | M3-F6 | Détection du niveau de formation (ex: Bac+5, Master, Doctorat) |
| Gérer les erreurs de parsing | M3-F7 | Tentatives, fallback, statut d’échec, notification |
| Stocker le CV original | M3-F8 | Sauvegarde sécurisée avec URL signée |

---

## 3. Spécification détaillée par fonction

### M3-F1 : Mettre en file d’attente un CV

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Système (après création d’une candidature dans M2, ou après upload manuel par recruteur) |
| **Pré-conditions** | – La candidature existe en base avec un ID valide.<br>– Le fichier CV a été stocké physiquement (dossier sécurisé).<br>– Le chemin du fichier est enregistré dans la candidature. |
| **Post-conditions** | – Un job est ajouté dans la file d’attente (ex: Redis Bull, RabbitMQ, ou simple table `parsing_jobs`).<br>– Statut du parsing passe à `pending`. |
| **Scénario nominal** | 1. M2 appelle une API interne `/parsing/enqueue` avec `candidature_id` et `chemin_fichier`.<br>2. Le système crée un enregistrement dans `parsing_jobs` (id, candidature_id, statut='pending', tentative=0, créé_le).<br>3. Le système déclenche un worker asynchrone (ou planifie un job).<br>4. La réponse est immédiate (pas d’attente). |
| **Alternatifs / erreurs** | – Si la file d’attente est saturée, le job est quand même accepté (tampon).<br> – Si l’appel échoue, on réessaie (max 3 fois avec backoff). |
| **Règles de gestion** | – Le traitement est asynchrone pour ne pas bloquer l’utilisateur.<br> – Le temps maximal avant début de traitement est < 5 secondes (en conditions normales). |

---

### M3-F2 : Traiter un CV (parsing global)

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Worker asynchrone (consomme la file d’attente) |
| **Pré-conditions** | – Un job existe avec statut `pending`.<br>– Le fichier CV est accessible. |
| **Post-conditions** | – Les champs extraits sont mis à jour dans la table `candidatures` (ou une table dédiée `cv_extractions`).<br>– Le statut du parsing passe à `success` ou `failed`.<br> – Un événement `parsing_completed` est émis pour déclencher M4 (scoring). |
| **Scénario nominal** | 1. Le worker récupère le job.<br>2. Il télécharge le fichier depuis le stockage sécurisé.<br>3. Il appelle le pipeline d’extraction (M3-F3 à M3-F6).<br>4. Si l’extraction réussit, il met à jour la candidature avec les données.<br>5. Il change le statut du job en `success` et enregistre le temps de traitement.<br>6. Il émet un événement `parsing_completed` (pour M4). |
| **Alternatifs / erreurs** | – Fichier corrompu ou format non supporté → statut `failed`, raison enregistrée.<br>– Timeout (>30 secondes) → arrêt, tentative +1, relance si tentative < 3.<br> – Service d’IA indisponible → mise en attente (retry). |
| **Règles de gestion** | – Une tentative ne doit pas dépasser 30 secondes.<br>– Maximum 3 tentatives par CV ; après, statut `failed` définitif et notification au recruteur. |

---

### M3-F3 : Extraire le nom et l’email

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Worker (appelé par M3-F2) |
| **Pré-conditions** | Le texte du CV a été extrait (via bibliothèque comme pdfplumber, PyPDF2, ou docx2txt). |
| **Post-conditions** | – `nom_candidat` et `email_candidat` sont renseignés dans la candidature.<br> – En cas de conflit, l’email saisi dans le formulaire M2 a priorité. |
| **Scénario nominal** | 1. Le worker extrait le texte brut du CV.<br>2. Il applique une regex pour détecter une adresse email (pattern standard).<br>3. Pour le nom, il cherche une ligne en début de document contenant probablement le prénom et nom (ou utilise une bibliothèque NER légère).<br>4. Il compare avec l’email du formulaire : si l’email extrait diffère, on garde celui du formulaire (saisie candidat).<br>5. Il stocke les valeurs. |
| **Alternatifs / erreurs** | – Aucun email trouvé dans le CV → on utilise l’email du formulaire (obligatoire).<br>– Nom non trouvé → on met une valeur par défaut `"Candidat"` ou on laisse vide (mais requis pour le scoring). |
| **Règles de gestion** | – L’email extrait est normalisé (minuscules, sans espace).<br>– Le nom est stocké tel quel (sans titre, ex: M. Mme). |

---

### M3-F4 : Extraire les compétences

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Worker |
| **Pré-conditions** | Texte du CV disponible. |
| **Post-conditions** | Une liste de compétences (mots-clés) est extraite et stockée (sous forme de tableau ou JSON). |
| **Scénario nominal** | 1. Le worker utilise une base de données de compétences prédéfinies (ex: Python, Java, Project Management, Communication, etc.) – environ 200 termes courants.<br>2. Il recherche ces termes dans le texte du CV (match insensible à la casse, gestion des accents).<br>3. Il constitue une liste des compétences détectées.<br>4. Il stocke cette liste dans `competences_detectees` (format JSON ou relation many-to-many). |
| **Alternatifs / erreurs** | – Aucune compétence trouvée → liste vide.<br> – La liste de référence peut être enrichie par l’admin (V2). |
| **Règles de gestion** | – Seule la présence compte, pas la fréquence (MVP).<br> – Les compétences sont stockées sous forme normalisée (minuscules, sans accents). |

---

### M3-F5 : Extraire l’expérience (années)

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Worker |
| **Pré-conditions** | Texte du CV disponible. |
| **Post-conditions** | Un nombre approximatif d’années d’expérience totale est calculé. |
| **Scénario nominal** | 1. Le worker cherche des périodes de travail (ex: `2018 - 2022`, `janv. 2015 – déc. 2020`).<br>2. Il extrait toutes les durées en années (arrondi à l’année supérieure si >6 mois).<br>3. Il somme les années (sans double compter les chevauchements – simplification : on additionne toutes les durées trouvées).<br>4. Il stocke le total dans `annees_experience`. |
| **Alternatifs / erreurs** | – Aucune période trouvée → 0 année.<br> – Format de date non reconnu → on ignore cette entrée.<br> – Chevauchement possible (deux emplois en même temps) → on additionne quand même (approximatif). |
| **Règles de gestion** | – Les stages et alternances sont comptés comme expérience (sauf si spécifié).<br> – MVP : pas de distinction entre expérience pertinente et non pertinente. |

---

### M3-F6 : Extraire la formation (dernier diplôme)

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Worker |
| **Pré-conditions** | Texte du CV disponible. |
| **Post-conditions** | Un niveau de formation est déterminé (ex: `Bac+2`, `Bac+5`, `Doctorat`, `Autre`). |
| **Scénario nominal** | 1. Le worker recherche des mots-clés indicateurs : `Master`, `MSc`, `Bac+5`, `Diplôme d'ingénieur`, `Doctorat`, `PhD`, `Licence`, `Bac+3`, `BTS`, `DUT`, `Bac+2`.<br>2. Il prend le niveau le plus élevé trouvé (ex: si présence de "Doctorat", alors niveau = `Doctorat` ; sinon si "Master" → `Bac+5`, etc.).<br>3. Il stocke une valeur normalisée (enum : `bac+2`, `bac+3`, `bac+5`, `doctorat`, `autre`). |
| **Alternatifs / erreurs** | – Aucune formation détectée → niveau `non_renseigne`.<br> – Plusieurs diplômes : on garde le plus haut. |
| **Règles de gestion** | – La correspondance est basée sur des règles simples (pas d’IA).<br> – Les diplômes étrangers sont mappés de manière basique (ex: "Bachelor" → `bac+3`). |

---

### M3-F7 : Gérer les erreurs de parsing

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Worker (en cas d’exception ou d’échec) |
| **Pré-conditions** | Le traitement a échoué (fichier corrompu, timeout, service IA en erreur). |
| **Post-conditions** | – Le job est marqué `failed` après épuisement des tentatives.<br> – Une notification est écrite dans les logs.<br> – Optionnel : un email est envoyé au recruteur pour l’informer. |
| **Scénario nominal** | 1. Une exception se produit (ex: bibliothèque de parsing ne peut pas ouvrir le PDF).<br>2. Le worker incrémente le compteur `tentative`.<br>3. Si tentative < 3, il replanifie le job avec un délai (backoff exponentiel : 1 min, 5 min, 15 min).<br>4. Si tentative == 3, il marque le job `failed` et enregistre la raison.<br>5. Il met à jour le statut de parsing de la candidature à `failed`. |
| **Alternatifs / erreurs** | – Si le fichier est introuvable (chemin invalide) → échec immédiat sans réessai. |
| **Règles de gestion** | – Les logs d’erreur sont conservés pour analyse.<br> – Un tableau de bord administrateur permet de voir les jobs en échec. |

---

### M3-F8 : Stocker le CV original

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | M2 (lors du dépôt) ou M3 (lors du traitement) |
| **Pré-conditions** | Le fichier a été reçu via le formulaire. |
| **Post-conditions** | Le fichier est sauvegardé dans un bucket/stockage sécurisé (S3, disque avec accès contrôlé). Une URL signée (expiration 1h) est générable pour le recruteur. |
| **Scénario nominal** | 1. Le fichier est renommé en `{candidature_uuid}.{ext}`.<br>2. Il est placé dans un dossier non accessible directement par le web (hors du `public`).<br>3. Un chemin relatif ou une référence est stockée dans la colonne `cv_path` de la candidature.<br>4. À la demande d’affichage, un endpoint sécurisé génère une URL signée (expiration 1h) pour le téléchargement. |
| **Alternatifs / erreurs** | – Échec d’écriture disque → rollback de la candidature (M2). |
| **Règles de gestion** | – Le fichier original n’est jamais modifié.<br> – Les droits d’accès sont limités aux recruteurs authentifiés. |

---

## 4. Règles de gestion transverses du module M3

| Règle | Description |
|-------|-------------|
| **RG‑10** | Le parsing ne doit jamais exposer le contenu du CV en dehors du système (pas de logs contenant le texte intégral). |
| **RG‑11** | En cas d’échec de parsing, la candidature reste valide (le recruteur peut consulter le CV manuellement). Le score sera 0 ou non calculé. |
| **RG‑12** | Les données extraites sont stockées de manière structurée pour permettre le filtrage et le scoring. |
| **RG‑13** | Les temps de parsing sont monitorés (métrique : P95 < 30s). |
| **RG‑14** | Les CV sont conservés pour une durée conforme au RGPD (ex: 2 ans après dernière action, puis anonymisation ou suppression). |

---

## 5. Écrans associés (esquisses fonctionnelles)

| Écran | Éléments clés |
|-------|----------------|
| **Tableau de bord admin parsing** | Liste des jobs (pending, success, failed), avec temps de traitement, tentatives. |
| **Détail candidature (recruteur)** | Affichage des champs extraits (nom, email, compétences, expérience, formation) + statut du parsing (succès/échec). |
| **Logs d’erreur** | Consultation des erreurs techniques par le support. |

---

## 6. Interactions avec les autres modules

```mermaid
sequenceDiagram
    participant M2 as M2 - Candidature
    participant Queue as File d'attente
    participant Worker as Worker Parsing
    participant Stockage as Stockage CV
    participant M4 as M4 - Scoring

    M2->>Queue: Enqueue job (candidature_id, chemin)
    Queue-->>Worker: Consomme job
    Worker->>Stockage: Lit fichier CV
    Worker->>Worker: Extraction (nom, email, compétences, expérience, formation)
    Worker->>M2: Mise à jour candidature avec données extraites
    Worker->>Queue: Marque job success
    Worker-->>M4: Événement parsing_completed
```

---
Voici les **spécifications détaillées** du module **M4 – Scoring & matching**, conformément au format établi.

---

# Spécifications fonctionnelles – Module M4 : Scoring & matching

## 1. Vue d’ensemble du module

| Propriété | Description |
|-----------|-------------|
| **Objectif** | Calculer automatiquement un score de pertinence (0 à 100) pour chaque candidature en fonction des critères pondérés définis dans l’offre, puis déclencher des alertes si le score dépasse un seuil configuré. |
| **Acteur déclencheur** | Système (déclenché après succès du parsing – module M3). |
| **Dépendances** | Dépend de M1 (pondérations et seuil de l’offre) et de M3 (données extraites du CV). Alimente M5 (Pipeline Kanban) avec le score affiché. |
| **Données manipulées** | Score global (0-100), scores détaillés par critère, seuil d’alerte, date de calcul, historique des versions de pondération (V2). |

---

## 2. Liste des fonctions

| Fonction | Code | Description sommaire |
|----------|------|----------------------|
| Déclencher le calcul du score | M4-F1 | Réception de l’événement `parsing_completed`, lancement du scoring asynchrone |
| Calculer le score par critère | M4-F2 | Pour chaque critère (compétences, expérience, formation, langues), générer une note sur 100 |
| Calculer le score global | M4-F3 | Agréger les scores partiels avec les pondérations de l’offre |
| Persister le score | M4-F4 | Enregistrer score global et détail dans la candidature |
| Comparer avec le seuil d’alerte | M4-F5 | Vérifier si score > seuil, et déclencher une notification |
| Envoyer une alerte au recruteur | M4-F6 | Email ou notification in-app pour les candidats qualifiés |
| Gérer les erreurs de scoring | M4-F7 | Que faire si données manquantes ou offre sans pondération |

---

## 3. Spécification détaillée par fonction

### M4-F1 : Déclencher le calcul du score

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Système (événement `parsing_completed` émis par M3) |
| **Pré-conditions** | – La candidature a un statut `reçu`.<br>– Les données extraites (compétences, années expérience, formation) sont disponibles, même partiellement.<br>– L’offre associée existe et a une configuration de scoring (4 critères avec pondérations). |
| **Post-conditions** | – Un job de scoring est créé ou le calcul est exécuté immédiatement.<br> – La candidature reçoit un score (global et détail) dans un délai < 5 secondes après la fin du parsing. |
| **Scénario nominal** | 1. M3 émet un événement `parsing_completed(candidature_id)`.<br>2. M4 écoute cet événement et déclenche une fonction de calcul.<br>3. La fonction charge la candidature, l’offre, et les pondérations.<br>4. Le calcul est effectué (M4-F2, M4-F3).<br>5. Le résultat est persistant (M4-F4).<6. Si score > seuil, alerte envoyée (M4-F5, M4-F6). |
| **Alternatifs / erreurs** | – Si le parsing a échoué (pas de données), le scoring n’est pas déclenché (ou score = 0).<br>– Si l’offre n’a pas de pondérations (cas par défaut), on applique 25% chacun. |
| **Règles de gestion** | – Le scoring est synchrone par rapport à l’événement (peut être fait dans le même worker que M3).<br> – En cas d’indisponibilité, le scoring est réessayé (max 3 fois). |

---

### M4-F2 : Calculer le score par critère

Cette fonction définit comment chaque critère est noté de 0 à 100.

#### a) Critère « Compétences »

| Élément | Description |
|---------|-------------|
| **Méthode** | Comparer la liste des compétences requises dans l’offre (saisie par le recruteur sous forme de mots-clés) avec la liste des compétences détectées dans le CV. |
| **Scénario nominal** | 1. Le recruteur a défini pour l’offre une liste de compétences obligatoires/souhaitées (ex: `["Python", "JavaScript", "React"]`).<br>2. Le système compte le nombre de compétences requises présentes dans le CV.<br>3. Score = (nb compétences_match / nb compétences_requises_total) * 100.<br>4. Si aucune compétence requise, score = 100 (non pertinent). |
| **Règles** | – Les compétences sont matchées en insensible à la casse et sans accent.<br> – Les synonymes ne sont pas pris en compte en MVP. |

#### b) Critère « Expérience »

| Élément | Description |
|---------|-------------|
| **Méthode** | Comparer les années d’expérience requises (champ optionnel dans l’offre) avec les années extraites du CV. |
| **Scénario nominal** | 1. Offre définit `annees_experience_requises` (ex: 3 ans).<br>2. CV a `annees_experience` = 5 ans.<br>3. Score = min(100, (annees_CV / annees_requises) * 100). Plafonné à 100.<br>4. Si offre ne spécifie pas d’années requises, score = 100 (critère neutre). |
| **Règles** | – Si expérience CV = 0 et offre requiert > 0, score = 0.<br> – Expérience supérieure à 2x le requis donne 100. |

#### c) Critère « Formation »

| Élément | Description |
|---------|-------------|
| **Méthode** | Comparer le niveau de formation requis (ex: `Bac+5`) avec le niveau extrait du CV. |
| **Scénario nominal** | 1. Offre définit `niveau_formation_requis` (enum: bac+2, bac+3, bac+5, doctorat).<br>2. CV a `niveau_formation`.<br>3. Score = 100 si niveau_CV >= niveau_requis (ordre hiérarchique), sinon 0.<br>4. Si offre ne spécifie pas de formation requise, score = 100. |
| **Règles** | – Hiérarchie simplifiée : bac+2 < bac+3 < bac+5 < doctorat.<br> – Si niveau CV = "non_renseigné", score = 0. |

#### d) Critère « Langues » (optionnel, mais présent dans les 4 critères)

| Élément | Description |
|---------|-------------|
| **Méthode** | L’offre peut définir des langues requises avec niveau (ex: Anglais B2). En MVP simplifié, on compare la présence de la langue dans le CV (détection basique). |
| **Scénario nominal** | 1. Offre liste des langues requises (ex: `["Anglais", "Allemand"]`).<br>2. Le CV est analysé pour détecter ces langues (mots-clés).<br>3. Score = (nb langues_match / nb langues_requises) * 100.<br>4. Si aucune langue requise, score = 100. |
| **Règles** | – En MVP, on ne gère pas les niveaux (B2, C1) – simple présence.<br> – Détection basée sur une liste prédéfinie (Anglais, Allemand, Espagnol, etc.). |

---

### M4-F3 : Calculer le score global

| Élément | Description |
|---------|-------------|
| **Méthode** | Combiner les scores des 4 critères avec les pondérations définies dans l’offre. |
| **Formule** | `Score_global = (Score_compétences * Poids_compétences + Score_expérience * Poids_expérience + Score_formation * Poids_formation + Score_langues * Poids_langues) / 100`<br>Où les poids sont en pourcentage (somme = 100). |
| **Scénario nominal** | 1. Pondérations : Compétences 40%, Expérience 30%, Formation 20%, Langues 10%.<br>2. Scores partiels : Compétences 80, Expérience 60, Formation 100, Langues 50.<br>3. Score global = (80*0.4 + 60*0.3 + 100*0.2 + 50*0.1) = 32 + 18 + 20 + 5 = 75.<br>4. Arrondi à l’entier le plus proche. |
| **Règles** | – Le score global est stocké dans `candidatures.score_global`.<br> – Les scores détaillés par critère sont stockés dans un champ JSON `scores_detail`. |

---

### M4-F4 : Persister le score

| Élément | Description |
|---------|-------------|
| **Acteur** | Système (après calcul) |
| **Pré-conditions** | Le score global et les scores détaillés sont calculés. |
| **Post-conditions** | Les champs de la candidature sont mis à jour. |
| **Scénario nominal** | 1. Mise à jour SQL : `UPDATE candidatures SET score_global = 75, scores_detail = '{"competences":80,"experience":60,"formation":100,"langues":50}', date_scoring = NOW() WHERE id = X`.<br>2. Le pipeline Kanban (M5) peut maintenant afficher le score. |
| **Alternatifs** | – Si le scoring échoue (division par zéro, etc.), on stocke `score_global = NULL` et un champ `scoring_error`. |

---

### M4-F5 : Comparer avec le seuil d’alerte

| Élément | Description |
|---------|-------------|
| **Acteur** | Système (après persistance du score) |
| **Pré-conditions** | L’offre a un `seuil_alerte` (entier entre 0 et 100). Par défaut 80. |
| **Post-conditions** | Si score_global >= seuil_alerte, une alerte est déclenchée (M4-F6). |
| **Scénario nominal** | 1. Lecture du seuil depuis l’offre.<br>2. Comparaison `score_global >= seuil_alerte`.<br>3. Si vrai, appel à M4-F6. |
| **Règles** | – Le seuil peut être modifié après publication ; les futures alertes utilisent le nouveau seuil.<br> – On n’alerte qu’une seule fois par candidature (marque `alerte_envoyee` = true après envoi). |

---

### M4-F6 : Envoyer une alerte au recruteur

| Élément | Description |
|---------|-------------|
| **Acteur** | Système |
| **Destinataire** | Recruteur (email configuré dans son profil, ou email principal du compte) |
| **Contenu de l’alerte** | – Nom du candidat<br>– Titre de l’offre<br>– Score global<br>– Lien direct vers la candidature dans le pipeline |
| **Scénario nominal** | 1. Le système compose un email avec template `alerte_score`. Exemple :<br>   *"Candidat [nom] a obtenu un score de [score] pour l'offre [offre_titre]. Cliquez ici pour le voir."*<br>2. Envoi via le service email (asynchrone).<br>3. On marque `candidatures.alerte_envoyee = true`. |
| **Alternatifs** | – Si l’envoi échoue, on réessaie 2 fois, puis on logge l’erreur sans bloquer. |
| **Règles** | – En MVP, l’alerte est seulement par email. Une notification in-app (V2) est possible. |

---

### M4-F7 : Gérer les erreurs de scoring

| Cas | Comportement |
|-----|---------------|
| **Données de parsing manquantes** | Score global = 0, scores détaillés = 0. Une mention « Scoring non disponible (parsing échoué) » est affichée dans l’interface. |
| **Offre sans pondérations** | Appliquer pondérations par défaut : 25% pour chaque critère. |
| **Critère sans données (ex: langues non demandées)** | Pour ce critère, on ignore son poids et on redistribue proportionnellement sur les autres critères (ou on met poids à 0). En MVP, on laisse le poids mais le score partiel = 100 (neutre). |
| **Division par zéro** | Score global = 0, log d’erreur. |

---

## 4. Règles de gestion transverses du module M4

| Règle | Description |
|-------|-------------|
| **RG‑15** | Le scoring n’est recalculé qu’en cas de nouvelle candidature ou si le recruteur modifie les pondérations (dans ce cas, optionnel en V2). En MVP, pas de recalcul rétroactif. |
| **RG‑16** | Le score global est affiché dans le pipeline Kanban (carte candidat). |
| **RG‑17** | Les scores détaillés sont visibles dans la fiche candidat. |
| **RG‑18** | Le seuil d’alerte est modifiable par offre, même après publication. |
| **RG‑19** | L’alerte email n’est pas envoyée si la candidature a déjà été notifiée (évite spam). |

---

## 5. Écrans associés (esquisses fonctionnelles)

| Écran | Éléments clés |
|-------|----------------|
| **Fiche candidat (recruteur)** | Score global en gros, jauge 0-100, détail par critère avec notes et pondérations. |
| **Configuration scoring (offre)** | Quatre sliders (somme 100), champ seuil alerte, liste compétences requises, années expérience requise, formation requise, langues requises. |
| **Email d’alerte** | Objet : « Candidat qualifié pour [offre] – Score [X] » ; corps avec lien. |

---

## 6. Interactions avec les autres modules

```mermaid
sequenceDiagram
    participant M3 as M3 Parsing
    participant M4 as M4 Scoring
    participant Base as Base de données
    participant M5 as M5 Pipeline
    participant Email as Service email

    M3->>M4: événement parsing_completed(candidature_id)
    M4->>Base: Charger offre (pondérations, seuil)
    M4->>Base: Charger données extraites
    M4->>M4: Calcul scores partiels puis global
    M4->>Base: Persister score_global et scores_detail
    alt score >= seuil
        M4->>Email: Envoyer alerte au recruteur
    end
    M4->>M5: Mettre à jour candidature (score affiché)
```

---
Voici les **spécifications détaillées** du module **M5 – Pipeline Kanban**, conformément au format établi.

---

# Spécifications fonctionnelles – Module M5 : Pipeline Kanban

## 1. Vue d’ensemble du module

| Propriété | Description |
|-----------|-------------|
| **Objectif** | Permettre au recruteur de visualiser, trier et faire avancer les candidats à travers les étapes du processus de recrutement via une interface de type Kanban (glisser-déposer). |
| **Acteur principal** | Recruteur (utilisateur connecté) |
| **Dépendances** | Reçoit les candidatures depuis M2/M3/M4 (avec score et données extraites). Alimente l’historique des actions. |
| **Données manipulées** | Candidature (statut étape, notes internes, historique des changements d’étape, date de dernière action) |

---

## 2. Liste des fonctions

| Fonction | Code | Description sommaire |
|----------|------|----------------------|
| Afficher le pipeline Kanban | M5-F1 | Présentation des 6 colonnes fixes avec les cartes candidats |
| Visualiser le détail d’un candidat | M5-F2 | Modale ou page dédiée avec toutes les infos (CV, score, notes, historique) |
| Déplacer un candidat (drag & drop) | M5-F3 | Changer l’étape d’un candidat manuellement |
| Ajouter une note interne | M5-F4 | Texte libre associé à un candidat, visible par l’équipe |
| Consulter l’historique des actions | M5-F5 | Log des changements d’étape, notes, dates, utilisateur |
| Filtrer les candidats | M5-F6 | Filtrage par score, compétence, statut, offre |
| Gérer les candidatures (archivage / suppression) | M5-F7 | Archiver ou supprimer une candidature (RGPD) |

---

## 3. Spécification détaillée par fonction

### M5-F1 : Afficher le pipeline Kanban

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Recruteur (clic sur « Pipeline » dans le menu) |
| **Pré-conditions** | Au moins une offre et des candidatures existent. |
| **Post-conditions** | Affichage du tableau Kanban avec 6 colonnes verticales. |
| **Colonnes (fixes)** | 1. Reçu<br>2. Présélection<br>3. Entretien RH<br>4. Entretien Tech<br>5. Offre<br>6. Embauché |
| **Scénario nominal** | 1. Le recruteur sélectionne une offre dans un menu déroulant (filtre principal).<br>2. Le système affiche 6 colonnes côte à côte (scroll horizontal si nécessaire).<br>3. Chaque colonne contient les cartes des candidats à cette étape, triées par date de dépôt (plus récent en haut).<br>4. Chaque carte affiche : nom du candidat, score global (0-100 avec icône), compétences principales (max 3), date de dépôt.<br>5. Un indicateur de nombre de candidats par colonne est affiché en en-tête. |
| **Alternatifs / erreurs** | – Aucune offre sélectionnée → message « Veuillez choisir une offre ».<br> – Aucun candidat pour une colonne → colonne vide avec message « Aucun candidat ». |
| **Règles de gestion** | – L’ordre des colonnes est fixe (pas de personnalisation en MVP).<br> – Les cartes peuvent être glissées d’une colonne à l’autre (M5-F3).<br> – Le pipeline est mis à jour en temps réel après chaque action (drag & drop, ajout de note, nouvelle candidature). |

---

### M5-F2 : Visualiser le détail d’un candidat

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Recruteur (clic sur une carte candidat) |
| **Pré-conditions** | La candidature existe. |
| **Post-conditions** | Affichage d’une modale ou d’une page dédiée avec toutes les informations. |
| **Contenu de la vue détail** | – Nom, email, score global et détail par critère.<br>– CV original (téléchargement via URL signée).<br>– Compétences détectées, années expérience, formation, langues.<br>– Historique des actions (changements d’étape, notes).<br>– Champ d’ajout de note interne.<br>– Boutons pour changer d’étape (équivalent drag & drop).<br>– Bouton « Envoyer un email » (déclenche M6). |
| **Scénario nominal** | 1. Clic sur une carte → ouverture modale.<br>2. Le système charge les données de la candidature.<br>3. Le recruteur consulte, ajoute une note, change d’étape, ou télécharge le CV.<br>4. Fermeture de la modale. |
| **Règles de gestion** | – L’URL de téléchargement du CV expire après 1 heure (sécurité).<br> – Toute action (changement étape, note) est immédiatement persistée et visible dans l’historique. |

---

### M5-F3 : Déplacer un candidat (drag & drop)

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Recruteur (glisse une carte d’une colonne à une autre) |
| **Pré-conditions** | L’utilisateur est authentifié. La carte est dans une colonne source. |
| **Post-conditions** | Le statut de la candidature est mis à jour vers la nouvelle étape. Un événement est ajouté dans l’historique. |
| **Scénario nominal** | 1. Le recruteur prend la carte avec la souris.<br>2. Il la dépose sur une autre colonne (ex: de « Reçu » à « Présélection »).<br>3. Le système affiche un indicateur de chargement.<br>4. Mise à jour AJAX du statut dans la base (colonne cible).<br>5. La carte disparaît de la colonne source et apparaît dans la colonne cible (en haut de la liste).<br>6. L’historique enregistre : « Statut changé de Reçu à Présélection par [utilisateur] le [date] ». |
| **Alternatifs / erreurs** | – Perte de réseau → message d’erreur, la carte revient à sa position initiale.<br> – Conflit (ex: deux recruteurs déplacent le même candidat) → dernier écrivain gagne, pas de conflit géré en MVP. |
| **Règles de gestion** | – Le déplacement est possible vers n’importe quelle colonne, même en arrière (ex: de « Entretien Tech » vers « Présélection »).<br> – Aucune validation supplémentaire requise (pas de conditions de passage).<br> – Un historique est conservé pour chaque changement. |

---

### M5-F4 : Ajouter une note interne

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Recruteur (depuis la vue détail candidat) |
| **Pré-conditions** | La candidature est affichée. |
| **Post-conditions** | Une nouvelle note est ajoutée à la candidature, avec horodatage et auteur. |
| **Scénario nominal** | 1. Le recruteur clique sur « Ajouter une note ».<br>2. Un champ texte s’affiche (textarea).<br>3. Il saisit son commentaire (ex: « Bon profil technique, à revoir en entretien »).<br>4. Il valide.<br>5. Le système enregistre la note (texte, date, auteur, candidature_id).<br>6. La note apparaît dans l’historique et dans le fil de la vue détail. |
| **Alternatifs / erreurs** | – Texte vide → désactiver le bouton de validation.<br> – Échec enregistrement → message d’erreur, perte de la note (à ressaisir). |
| **Règles de gestion** | – Les notes sont visibles par tous les recruteurs (pas de privé en MVP).<br> – Les notes ne sont pas modifiables ni supprimables (V2). |

---

### M5-F5 : Consulter l’historique des actions

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Recruteur (vue détail candidat, onglet « Historique ») |
| **Pré-conditions** | La candidature existe. |
| **Post-conditions** | Affichage chronologique des actions. |
| **Types d’actions enregistrées** | – Changement d’étape (ancienne → nouvelle, utilisateur, date)<br> – Ajout de note (utilisateur, date, texte)<br> – (Optionnel) Envoi d’email (date, template)<br> – (Optionnel) Téléchargement du CV (log sécurité) |
| **Scénario nominal** | 1. Le recruteur ouvre l’onglet « Historique ».<br>2. Le système affiche une liste chronologique inverse (plus récent en premier).<br>3. Chaque ligne : icône action, date, utilisateur, détail. |
| **Règles de gestion** | – L’historique est immutable (ne peut pas être modifié ou supprimé).<br> – Conservation pour toute la durée de vie de la candidature. |

---

### M5-F6 : Filtrer les candidats

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Recruteur (utilisation des filtres dans le pipeline) |
| **Pré-conditions** | Au moins une offre sélectionnée. |
| **Post-conditions** | Le pipeline n’affiche que les candidats correspondant aux filtres. |
| **Filtres disponibles (MVP)** | – Par score : supérieur à un seuil (ex: >70).<br> – Par compétence : sélection d’une ou plusieurs compétences (match exact).<br> – Par statut (déjà fait par colonne). |
| **Scénario nominal** | 1. Le recruteur clique sur « Filtres ».<br>2. Il choisit « Score > 80 » et « Compétence = Python ».<br>3. Le système recharge les cartes : seuls les candidats avec score > 80 ET compétence Python apparaissent dans leurs colonnes respectives.<br>4. Les colonnes vides affichent « Aucun candidat ». |
| **Alternatifs / erreurs** | – Aucun candidat ne correspond → toutes colonnes vides avec message.<br> – Combinaison de filtres trop restrictive → l’utilisateur peut réinitialiser. |
| **Règles de gestion** | – Les filtres sont cumulatifs (ET logique).<br> – L’état des filtres n’est pas persistant d’une session à l’autre. |

---

### M5-F7 : Gérer les candidatures (archivage / suppression)

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Recruteur (depuis la vue détail ou un menu sur la carte) |
| **Pré-conditions** | La candidature existe. |
| **Post-conditions** | La candidature est marquée comme « archivée » (n’apparaît plus dans le pipeline par défaut) ou supprimée physiquement (conformité RGPD à la demande du candidat). |
| **Scénario nominal (archivage)** | 1. Le recruteur clique sur « Archiver ».<br>2. Le système demande confirmation.<br>3. La candidature passe en `archive = true`.<br>4. Elle disparaît du pipeline actif (mais reste accessible via un filtre « Afficher les archivées »). |
| **Scénario nominal (suppression RGPD)** | 1. Le recruteur reçoit une demande de suppression d’un candidat.<br>2. Il recherche la candidature, clique sur « Supprimer définitivement ».<br>3. Le système supprime toutes les données personnelles (nom, email, CV, notes, historique) et conserve un anonymat (ex: « Candidat supprimé à sa demande »). |
| **Règles de gestion** | – La suppression physique n’est possible que si aucun engagement contractuel (ex: candidat embauché). En MVP, on autorise la suppression de toute candidature non « Embauché ». <br> – Un audit log de la suppression est conservé (sans données personnelles). |

---

## 4. Règles de gestion transverses du module M5

| Règle | Description |
|-------|-------------|
| **RG‑20** | Les colonnes sont fixes (6 étapes). Pas de colonnes personnalisables en MVP. |
| **RG‑21** | Le drag & drop est permis pour toutes les étapes, sans contrainte de séquence. |
| **RG‑22** | Chaque changement d’étape est horodaté et associé à l’utilisateur connecté. |
| **RG‑23** | Les notes internes ne sont pas visibles par les candidats. |
| **RG‑24** | Un candidat ne peut pas être déplacé vers « Embauché » sans passer par les étapes antérieures (pas de validation technique en MVP, mais recommandation UI). |
| **RG‑25** | Les candidatures archivées ne sont pas supprimées ; elles peuvent être restaurées (V2). |

---

## 5. Écrans associés (esquisses fonctionnelles)

| Écran | Éléments clés |
|-------|----------------|
| **Pipeline Kanban** | Sélecteur offre en haut, 6 colonnes horizontales, cartes avec nom/score/compétences, zone de drop, indicateur de chargement. |
| **Modale détail candidat** | En-tête (nom, score), onglets (Détails, CV, Historique, Notes), boutons (Changer étape, Email, Archiver). |
| **Filtres** | Overlay avec slider score, liste déroulante compétences, boutons Appliquer / Réinitialiser. |

---

## 6. Interactions avec les autres modules

```mermaid
sequenceDiagram
    participant UI as Interface Kanban
    participant API as Backend API
    participant Base as Base de données
    participant M6 as M6 Communication

    UI->>API: GET /candidatures?offre_id=X&etape=*
    API->>Base: Requête avec filtres
    Base-->>API: Liste candidatures
    API-->>UI: Rendu colonnes

    UI->>API: PATCH /candidatures/{id}/etape (drag & drop)
    API->>Base: Mise à jour statut + ajout historique
    Base-->>API: OK
    API-->>UI: Succès, refresh colonnes

    UI->>API: POST /candidatures/{id}/notes
    API->>Base: Ajout note
    Base-->>API: OK
    API-->>UI: Note ajoutée

    UI->>M6: Déclencher envoi email (via bouton)
```

---

Voici les **spécifications détaillées** du module **M6 – Communication manuelle**, conformément au format établi.

---

# Spécifications fonctionnelles – Module M6 : Communication manuelle

## 1. Vue d’ensemble du module

| Propriété | Description |
|-----------|-------------|
| **Objectif** | Permettre au recruteur d’envoyer manuellement des emails aux candidats à partir de templates personnalisables, afin de communiquer facilement (relance, convocation, refus, offre). |
| **Acteur principal** | Recruteur (utilisateur connecté) |
| **Dépendances** | Utilise les templates d’emails (stockés en base). S’appuie sur les données candidat et offre pour les variables dynamiques. |
| **Données manipulées** | Templates (nom, objet, corps, variables utilisées), envois (date, destinataire, template utilisé, statut). |

---

## 2. Liste des fonctions

| Fonction | Code | Description sommaire |
|----------|------|----------------------|
| Gérer les templates d’emails | M6-F1 | Créer, modifier, supprimer des templates (objets, corps, variables) |
| Consulter la liste des templates | M6-F2 | Afficher les templates disponibles (4 par défaut) |
| Envoyer un email à un candidat | M6-F3 | Depuis la fiche candidat, choisir un template, personnaliser, envoyer |
| Prévisualiser un email | M6-F4 | Afficher l’aperçu avec les variables du candidat (sans envoyer) |
| Journaliser les envois | M6-F5 | Conserver la trace de chaque email envoyé (date, destinataire, template) |

---

## 3. Spécification détaillée par fonction

### M6-F1 : Gérer les templates d’emails

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Recruteur (menu « Templates emails ») |
| **Pré-conditions** | L’utilisateur est authentifié. |
| **Post-conditions** | Un template est créé, modifié ou supprimé. |
| **Templates par défaut (MVP)** | 1. **Accusé réception** (déjà utilisé par M2, mais modifiable)<br>2. **Convocation entretien**<br>3. **Refus de candidature**<br>4. **Proposition d’embauche** |
| **Scénario nominal (création)** | 1. Le recruteur clique sur « Nouveau template ».<br>2. Il saisit un nom (ex: « Relance entretien technique »).<br>3. Il saisit l’objet (ex: « Entretien technique pour [poste] »).<br>4. Il saisit le corps (texte riche simple, avec variables supportées).<br>5. Il peut insérer des variables depuis une liste déroulante (`[nom]`, `[poste]`, `[date_entretien]`, etc.).<br>6. Il sauvegarde. |
| **Scénario nominal (modification)** | 1. Il sélectionne un template existant.<br>2. Modifie l’objet ou le corps.<br>3. Sauvegarde. |
| **Scénario nominal (suppression)** | 1. Il clique sur l’icône poubelle.<br>2. Confirmation.<br>3. Le template est supprimé (sauf s’il est utilisé dans l’historique, alors archivage). |
| **Règles de gestion** | – Les templates par défaut ne peuvent pas être supprimés, mais peuvent être modifiés.<br> – Les variables sont entourées de crochets (ex: `[nom]`, `[poste]`, `[date_entretien]`).<br> – Le corps est stocké en HTML (éditeur WYSIWYG simple) et en texte brut pour fallback. |

---

### M6-F2 : Consulter la liste des templates

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Recruteur (page « Templates ») |
| **Pré-conditions** | Aucune. |
| **Post-conditions** | Affichage des templates sous forme de tableau. |
| **Scénario nominal** | 1. Le système affiche tous les templates (nom, date de dernière modification).<br>2. Chaque ligne a des actions : Modifier, Dupliquer, Supprimer (si non par défaut).<br>3. Un bouton « + Nouveau template » est présent. |
| **Règles** | – Les templates sont globaux (partagés par tous les recruteurs). |

---

### M6-F3 : Envoyer un email à un candidat

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Recruteur (depuis la fiche candidat, bouton « Envoyer un email ») |
| **Pré-conditions** | – La candidature existe avec nom, email, offre.<br> – Au moins un template existe. |
| **Post-conditions** | – Un email est envoyé au candidat.<br> – Un enregistrement est ajouté dans l’historique des communications (M6-F5). |
| **Scénario nominal** | 1. Le recruteur clique sur « Envoyer un email ».<br>2. Une modale s’ouvre avec :<br>   - Sélection du template (menu déroulant)<br>   - Aperçu du sujet et du corps (variables remplacées par les données du candidat)<br>   - Champ facultatif pour personnaliser le message (ajout de texte)<br>3. Il peut modifier le sujet ou le corps avant envoi (sans sauvegarder le template).<br>4. Il clique sur « Envoyer ».<br>5. Le système construit l’email :<br>   - Sujet : template avec variables résolues<br>   - Corps : template + personnalisation éventuelle<br>6. L’email est placé dans une file d’attente asynchrone.<br>7. Un message de confirmation « Email envoyé » apparaît.<br>8. L’envoi est journalisé. |
| **Alternatifs / erreurs** | – Template sélectionné contient une variable non supportée (ex: `[date_entretien]` non renseignée) → afficher un message d’avertissement, mais laisser envoyer (variable remplacée par chaîne vide).<br> – Échec d’envoi (SMTP) → réessai automatique 3 fois, puis log d’erreur. |
| **Règles de gestion** | – L’email est envoyé depuis une adresse noreply (ex: `recrutement@domaine.com`).<br> – Le candidat peut répondre ; la réponse est redirigée vers l’email du recruteur (paramétré).<br> – Les envois ne sont pas limités en MVP (pas de quota). |

---

### M6-F4 : Prévisualiser un email

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Recruteur (lors de la sélection d’un template dans la modale d’envoi) |
| **Pré-conditions** | Un candidat est sélectionné. |
| **Post-conditions** | Affichage du sujet et du corps avec les variables remplacées par les vraies valeurs du candidat. |
| **Scénario nominal** | 1. Le recruteur choisit un template.<br>2. Le système résout les variables : `[nom]` → « Dupont », `[poste]` → « Développeur Python », etc.<br>3. Il affiche un aperçu dans la modale (sujet en haut, corps en dessous).<br>4. Le recruteur peut alors modifier le texte avant envoi. |
| **Règles** | – L’aperçu est en lecture seule (sauf si modification manuelle).<br> – Les variables non trouvées apparaissent comme `[variable_inconnue]`. |

---

### M6-F5 : Journaliser les envois

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Système (après envoi réussi) |
| **Pré-conditions** | Un email a été envoyé. |
| **Post-conditions** | Un enregistrement est ajouté dans la table `communications`. |
| **Champs stockés** | – `candidature_id`<br> – `template_id` (ou `null` si personnalisé sans template)<br> – `objet` (le sujet réel envoyé)<br> – `corps` (le corps réel envoyé, optionnel pour économie de base)<br> – `destinataire` (email du candidat)<br> – `date_envoi`<br> – `statut` (success, failed)<br> – `utilisateur_id` (recruteur qui a envoyé) |
| **Scénario nominal** | 1. Après envoi réussi, le système insère une ligne.<br>2. L’historique du candidat (M5-F5) affiche la ligne correspondante. |
| **Règles** | – En MVP, on stocke uniquement l’objet et la date, pas le corps complet (économie d’espace).<br> – Les envois échoués sont loggés avec une raison technique (non visible par le recruteur dans l’UI, mais accessible via logs admin). |

---

## 4. Règles de gestion transverses du module M6

| Règle | Description |
|-------|-------------|
| **RG‑26** | Les templates sont globaux à l’ensemble des recruteurs (pas de templates personnels en MVP). |
| **RG‑27** | Les emails envoyés ne sont pas modifiables après envoi. |
| **RG‑28** | Un template peut contenir un nombre illimité de variables ; le système ne vérifie pas leur présence. |
| **RG‑29** | Les variables supportées en MVP : `[nom]`, `[prenom]`, `[poste]`, `[offre_titre]`, `[date_entretien]` (à saisir manuellement par le recruteur dans la modale), `[lien]` (lien vers l’offre). |
| **RG‑30** | L’envoi d’email est asynchrone pour ne pas bloquer l’interface. |

---

## 5. Écrans associés (esquisses fonctionnelles)

| Écran | Éléments clés |
|-------|----------------|
| **Liste des templates** | Tableau avec nom, date modif, actions (Modifier, Dupliquer, Supprimer) ; bouton « Nouveau template ». |
| **Formulaire template** | Champ nom, sujet, éditeur HTML (corps), bouton « Insérer variable », liste déroulante des variables disponibles. |
| **Modale d’envoi** | Sélecteur template, aperçu (sujet + corps) avec champs éditables, bouton « Envoyer », message de confirmation. |
| **Historique des communications** (dans fiche candidat) | Liste chronologique des envois : date, objet, destinataire, template utilisé. |

---

## 6. Interactions avec les autres modules

```mermaid
sequenceDiagram
    participant UI as Interface recruteur
    participant API as Backend API
    participant Base as Base de données
    participant Queue as File d'attente
    participant SMTP as Service email

    UI->>API: GET /templates
    API->>Base: SELECT * FROM templates
    Base-->>API: Liste templates
    API-->>UI: Affichage

    UI->>API: POST /candidatures/{id}/send-email (template_id, sujet, corps, variables)
    API->>Base: Récupérer candidat (nom, email) et offre
    API->>Queue: Ajouter job d'envoi
    API-->>UI: { success: true, message: "Email en file d'attente" }

    Queue->>SMTP: Envoi effectif
    SMTP-->>Queue: Succès/échec
    Queue->>Base: Journaliser envoi dans communications
```

---
Voici les **spécifications détaillées** du module **M7 – Reporting & export**, conformément au format établi.

---

# Spécifications fonctionnelles – Module M7 : Reporting & export

## 1. Vue d’ensemble du module

| Propriété | Description |
|-----------|-------------|
| **Objectif** | Fournir au recruteur des indicateurs clés sur l’efficacité du recrutement, ainsi que la possibilité d’exporter les données (offres, candidatures) au format CSV pour une analyse externe. |
| **Acteur principal** | Recruteur (utilisateur connecté) |
| **Dépendances** | S’appuie sur les données des modules M1 (offres), M2/M3/M4 (candidatures, scores), M5 (étapes, historique). |
| **Données manipulées** | KPIs calculés à la demande, exports CSV (fichiers temporaires). |

---

## 2. Liste des fonctions

| Fonction | Code | Description sommaire |
|----------|------|----------------------|
| Afficher le tableau de bord des KPIs | M7-F1 | Indicateurs clés : taux de conversion, délais moyens, volume |
| Calculer le taux de conversion global | M7-F2 | (Candidats embauchés) / (Candidats reçus) × 100 |
| Calculer le délai moyen par étape | M7-F3 | Temps moyen passé dans chaque colonne du pipeline |
| Afficher des graphiques simples | M7-F4 | Évolution temporelle des candidatures, répartition par source (V2) |
| Exporter les données en CSV | M7-F5 | Export complet ou filtré des offres et candidatures |
| Programmer des exports automatiques (option V2) | – | Non inclus en MVP |

---

## 3. Spécification détaillée par fonction

### M7-F1 : Afficher le tableau de bord des KPIs

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Recruteur (clic sur « Dashboard » dans le menu) |
| **Pré-conditions** | Au moins une offre et des candidatures existent (sinon afficher zéros). |
| **Post-conditions** | Affichage des KPIs pour l’ensemble des offres ou pour une offre sélectionnée. |
| **KPIs affichés (MVP)** | – **Candidatures totales** (toutes offres confondues)<br>– **Taux de conversion global** (embauchés / reçus)<br>– **Délai moyen de recrutement** (du dépôt à l’étape « Embauché »)<br>– **Score moyen** des candidatures<br>– **Répartition par étape** (nombre de candidats dans chaque colonne) |
| **Scénario nominal** | 1. Le recruteur sélectionne une offre (ou « Toutes »).<br>2. Le système calcule les KPIs à partir des données en base (requêtes agrégées).<br>3. Les valeurs sont affichées sous forme de cartes numériques.<br>4. Un rafraîchissement automatique est possible (bouton). |
| **Règles de gestion** | – Les KPIs sont calculés en temps réel (pas de pré-agrégation).<br> – Les candidatures archivées ou supprimées ne sont pas prises en compte.<br> – Si aucune candidature, afficher « 0 » ou « N/A ». |

---

### M7-F2 : Calculer le taux de conversion global

| Élément | Description |
|---------|-------------|
| **Méthode** | `(nb_candidats_statut = 'Embauché') / (nb_candidats_total) * 100` |
| **Périmètre** | Par offre ou toutes offres. |
| **Exemple** | 120 candidatures reçues, 12 embauchés → taux = 10%. |
| **Règle** | Les candidatures encore en cours (autres étapes) ne comptent pas dans le numérateur. |

---

### M7-F3 : Calculer le délai moyen par étape

| Élément | Description |
|---------|-------------|
| **Méthode** | Pour chaque étape (colonne), calculer le temps moyen passé par les candidats dans cette étape, en jours (ou heures). |
| **Formule** | `AVG(date_entree_etape_suivante - date_entree_etape_courante)` pour tous les candidats ayant quitté cette étape. |
| **Affichage** | Soit un tableau des 6 étapes avec délai moyen, soit un graphique à barres. |
| **Exemple** | Étape « Reçu » → délai moyen 2.3 jours avant passage en « Présélection ». |
| **Règles** | – Les candidats encore bloqués dans une étape ne sont pas comptés (pas de délai final).<br> – Si pas assez de données, afficher « N/A ». |

---

### M7-F4 : Afficher des graphiques simples (MVP léger)

| Élément | Description |
|---------|-------------|
| **Graphique 1 : Évolution des candidatures** | Courbe du nombre de candidatures reçues par jour / semaine sur une période (30 derniers jours). |
| **Graphique 2 : Répartition des scores** | Histogramme des scores (0-100) des candidatures. |
| **Technologie** | En MVP, on peut utiliser une librairie frontale simple (Chart.js) ou afficher des valeurs textuelles. |
| **Scénario** | Le recruteur voit ces graphiques dans le dashboard. |
| **Règles** | Les données sont calculées à la demande (pas de stockage périodique). |

---

### M7-F5 : Exporter les données en CSV

| Élément | Description |
|---------|-------------|
| **Acteur déclencheur** | Recruteur (page « Export » ou bouton depuis le dashboard) |
| **Pré-conditions** | L’utilisateur est authentifié. |
| **Post-conditions** | Un fichier CSV est généré et téléchargé par le navigateur. |
| **Types d’export** | – **Offres** : liste des offres (titre, statut, date création, nb candidatures, score moyen, taux conversion).<br> – **Candidatures** : liste détaillée (nom, email, offre, score global, scores détaillés, dates étapes, statut actuel, notes, etc.). |
| **Filtres possibles** | – Par offre (une ou plusieurs)<br> – Par période (date de dépôt)<br> – Par statut (étapes) |
| **Scénario nominal** | 1. Le recruteur va sur la page « Exports ».<br>2. Il choisit le type (Offres ou Candidatures).<br>3. Il applique des filtres (ex: offre = « Développeur », période = janvier 2025).<br>4. Il clique sur « Générer CSV ».<br>5. Le système exécute la requête, construit le CSV (séparateur point-virgule, encodage UTF-8).<br>6. Le fichier est téléchargé (nom automatique : `candidatures_offre123_2025-04-02.csv`). |
| **Alternatifs / erreurs** | – Volume de données important (>10 000 lignes) → traitement asynchrone avec notification par email (option V2). En MVP, on limite à 10 000 lignes et on affiche un avertissement.<br> – Aucune donnée correspondant aux filtres → message « Aucune donnée à exporter ». |
| **Contenu du CSV (candidatures)** | Colonnes : ID candidature, Nom, Email, Offre, Score global, Score compétences, Score expérience, Score formation, Score langues, Date dépôt, Étape actuelle, Date étape Reçu, Date étape Présélection, …, Dernière note, URL CV (optionnel mais sécurisé à éviter). En MVP, on exclut l’URL CV pour des raisons de sécurité (ou on met un lien signé expirant). |
| **Règles de gestion** | – Les exports sont limités à 10 000 lignes (alerte).<br> – L’export est synchrone (génération immédiate).<br> – Les données personnelles (nom, email) sont incluses ; le recruteur est responsable de leur traitement.<br> – Le CSV est généré en mémoire et envoyé ; aucun stockage permanent sur le serveur. |

---

## 4. Règles de gestion transverses du module M7

| Règle | Description |
|-------|-------------|
| **RG‑31** | Tous les KPIs sont calculés en temps réel (pas de cache en MVP). |
| **RG‑32** | Les délais sont exprimés en jours (arrondis à 1 décimale). |
| **RG‑33** | L’export CSV n’inclut pas les CV (fichiers binaires) mais seulement les métadonnées. |
| **RG‑34** | Seul le recruteur connecté peut exporter (pas d’accès public). |
| **RG‑35** | Les données supprimées (RGPD) ne remontent pas dans les exports. |

---

## 5. Écrans associés (esquisses fonctionnelles)

| Écran | Éléments clés |
|-------|----------------|
| **Dashboard** | Sélecteur offre, cartes KPIs (4-6 indicateurs), graphiques (évolution, répartition scores), tableau récapitulatif simple (optionnel). |
| **Page Exports** | Radio / select (Offres ou Candidatures), filtres (offre, période, statut), bouton « Générer CSV », zone de message. |

---

## 6. Interactions avec les autres modules

```mermaid
sequenceDiagram
    participant UI as Interface recruteur
    participant API as Backend API
    participant Base as Base de données

    UI->>API: GET /dashboard?offre_id=X
    API->>Base: Agrégations (COUNT, AVG, SUM) sur candidatures, offres, historique étapes
    Base-->>API: Résultats
    API-->>UI: JSON des KPIs + graphiques

    UI->>API: POST /export/candidatures (filtres)
    API->>Base: SELECT avec filtres
    Base-->>API: Lignes de données
    API->>API: Génération CSV (buffer)
    API-->>UI: Fichier CSV (Content-Disposition)
```

---

## 7. Synthèse des modules (pour mémoire)

| Module | Nom | Statut |
|--------|-----|--------|
| M1 | Gestion des offres | ✅ Spécifié |
| M2 | Candidature publique | ✅ Spécifié |
| M3 | Parsing & extraction IA | ✅ Spécifié |
| M4 | Scoring & matching | ✅ Spécifié |
| M5 | Pipeline Kanban | ✅ Spécifié |
| M6 | Communication manuelle | ✅ Spécifié |
| M7 | Reporting & export | ✅ Spécifié |

---
Voici le **plan pour l’étape 3 : Modélisation des données**.

L’objectif est de définir la structure des données nécessaire au fonctionnement des modules M1 à M7, en identifiant les entités, leurs attributs, les relations et les contraintes d’intégrité.

---

# Plan d’exécution – Modélisation des données

## 1. Objectif de l’étape
- Produire un **schéma conceptuel** (MCD) puis un **schéma logique relationnel** (MLD) exploitables pour l’implémentation SQL.
- Garantir la cohérence, l’intégrité référentielle et la performance des requêtes.

## 2. Démarche en 6 sous‑étapes

### 2.1. Lister les entités principales (à partir des modules)
| Module | Entités identifiées |
|--------|---------------------|
| M1 – Offres | Offre, CritèrePondération |
| M2 – Candidature publique | Candidature, Candidat (fusion possible avec Candidature) |
| M3 – Parsing | ExtractionDonnees, FichierCV, JobParsing |
| M4 – Scoring | ScoreDetail, AlerteScore |
| M5 – Pipeline | EtapePipeline, HistoriqueAction, NoteInterne |
| M6 – Communication | TemplateEmail, EnvoiEmail |
| M7 – Reporting | (pas d’entité spécifique, vues agrégées) |

### 2.2. Définir les attributs par entité
Pour chaque entité, lister :
- Identifiant (clé primaire)
- Attributs simples (type, longueur, contraintes)
- Attributs calculés (stockés ou virtuels)

### 2.3. Définir les relations entre entités
- Cardinalités (1-1, 1-n, n-n)
- Contraintes d’intégrité référentielle (suppression en cascade, restriction, etc.)
- Tables d’association pour les relations n-n (ex: Offre ↔ CompétenceRequise)

### 2.4. Appliquer les règles de gestion issues des spécifications
Exemples :
- Une offre a 4 critères de scoring avec pondération (somme 100).
- Une candidature appartient à une seule offre.
- Une candidature a un seul CV associé.
- Un historique d’actions (changements d’étape, notes) est lié à une candidature.

### 2.5. Produire le schéma conceptuel (MCD) – notation entité‑relation
- Utilisation de Mermaid ou texte structuré.
- Représentation des entités, attributs clés, relations et cardinalités.

### 2.6. Transformer en schéma logique relationnel (MLD)
- Tables SQL avec colonnes, types, clés primaires/étrangères, index suggérés.
- Normalisation minimale (3NF).

## 3. Livrables de l’étape 3

| Livrable | Format | Description |
|----------|--------|-------------|
| **Liste des entités et attributs** | Tableau Markdown | Détail des colonnes par table |
| **MCD (diagramme)** | Mermaid ou image | Relations et cardinalités |
| **MLD (script SQL)** | Code SQL (CREATE TABLE) | Définition des tables, clés, contraintes |
| **Index recommandés** | Liste | Pour les requêtes fréquentes (recherche par offre, score, statut) |

## 4. Exemple d’entité (pour illustrer)

**Entité `offre`**
- id (PK, UUID ou serial)
- titre (VARCHAR(255), NOT NULL)
- description (TEXT)
- statut (ENUM: brouillon, active, cloturee, archivee)
- date_creation (TIMESTAMP)
- seuil_alerte (INT, default 80)
- (autres champs : localisation, type_contrat)

**Relation** : une offre a plusieurs candidatures (1-n), une offre a plusieurs critères pondérés (1-n).

---

Je vais maintenant produire le **schéma conceptuel (MCD)** puis le **schéma logique relationnel (MLD)** conformément à l’objectif.

---

# Modélisation des données – ATS Platform (MVP)

## 1. Liste des entités et attributs (par module)

### Entités principales

| Entité | Attributs (champs) | Clé primaire | Commentaire |
|--------|--------------------|--------------|-------------|
| **offre** | id, titre, description, localisation, type_contrat, statut (brouillon/active/cloturee/archivee), date_creation, seuil_alerte (INT, default 80), slug (URL) | id | Une offre correspond à un poste à pourvoir |
| **critere_ponderation** | id, offre_id, critere_nom (competences, experience, formation, langues), poids (INT, 0-100) | id | 4 enregistrements par offre (un par critère) |
| **competence_requise** | id, offre_id, nom_competence (VARCHAR) | id | Liste des compétences souhaitées pour le scoring |
| **langue_requise** | id, offre_id, nom_langue | id | Liste des langues requises |
| **candidature** | id, offre_id, nom_candidat, email, statut_etape (reçu, preselection, entretien_rh, entretien_tech, offre, embauche), date_depot, ip, user_agent, consentement (BOOLEAN), date_consentement, score_global (INT), scores_detail (JSON), date_scoring, alerte_envoyee (BOOLEAN) | id | Une candidature est liée à une offre |
| **cv_fichier** | id, candidature_id, chemin_fichier, nom_original, taille, type_mime, date_upload | id | Relation 1-1 avec candidature |
| **extraction_cv** | id, candidature_id, nom_extrait, email_extrait, competences (JSON), annees_experience (INT), formation_niveau (ENUM), statut_parsing (pending/success/failed), date_extraction, tentative | id | Données extraites par l’IA |
| **job_parsing** | id, candidature_id, statut, tentative, dernier_erreur, date_creation, date_debut, date_fin | id | File d’attente parsing |
| **historique_action** | id, candidature_id, utilisateur_id, action_type (changement_etape, ajout_note, envoi_email), ancienne_valeur, nouvelle_valeur, commentaire, date_action | id | Traçabilité |
| **note_interne** | id, candidature_id, utilisateur_id, contenu, date_creation | id | Notes libres (peut être fusionné avec historique_action mais séparé pour clarté) |
| **template_email** | id, nom, objet, corps_html, corps_texte, est_par_defaut (BOOLEAN), date_creation, date_modif | id | Templates globaux |
| **envoi_email** | id, candidature_id, template_id (nullable), objet_envoye, destinataire, date_envoi, statut (success/échec), utilisateur_id | id | Journal des envois |
| **utilisateur** | id, email, nom, mot_de_passe_hash, role (recruteur, admin) | id | Un seul recruteur en MVP, mais structure pour extension |

---

## 2. Schéma conceptuel (MCD) – Diagramme entité-relation

```mermaid
erDiagram
    OFFRE {
        uuid id PK
        string titre
        text description
        string localisation
        string type_contrat
        enum statut
        datetime date_creation
        int seuil_alerte
        string slug
    }
    CRITERE_PONDERATION {
        uuid id PK
        uuid offre_id FK
        string critere_nom
        int poids
    }
    COMPETENCE_REQUISE {
        uuid id PK
        uuid offre_id FK
        string nom_competence
    }
    LANGUE_REQUISE {
        uuid id PK
        uuid offre_id FK
        string nom_langue
    }
    CANDIDATURE {
        uuid id PK
        uuid offre_id FK
        string nom_candidat
        string email
        enum statut_etape
        datetime date_depot
        string ip
        string user_agent
        boolean consentement
        datetime date_consentement
        int score_global
        json scores_detail
        datetime date_scoring
        boolean alerte_envoyee
    }
    CV_FICHIER {
        uuid id PK
        uuid candidature_id FK
        string chemin_fichier
        string nom_original
        int taille
        string type_mime
        datetime date_upload
    }
    EXTRACTION_CV {
        uuid id PK
        uuid candidature_id FK
        string nom_extrait
        string email_extrait
        json competences
        int annees_experience
        enum formation_niveau
        enum statut_parsing
        datetime date_extraction
        int tentative
    }
    JOB_PARSING {
        uuid id PK
        uuid candidature_id FK
        enum statut
        int tentative
        text dernier_erreur
        datetime date_creation
        datetime date_debut
        datetime date_fin
    }
    HISTORIQUE_ACTION {
        uuid id PK
        uuid candidature_id FK
        uuid utilisateur_id FK
        string action_type
        string ancienne_valeur
        string nouvelle_valeur
        text commentaire
        datetime date_action
    }
    NOTE_INTERNE {
        uuid id PK
        uuid candidature_id FK
        uuid utilisateur_id FK
        text contenu
        datetime date_creation
    }
    TEMPLATE_EMAIL {
        uuid id PK
        string nom
        string objet
        text corps_html
        text corps_texte
        boolean est_par_defaut
        datetime date_creation
        datetime date_modif
    }
    ENVOI_EMAIL {
        uuid id PK
        uuid candidature_id FK
        uuid template_id FK
        string objet_envoye
        string destinataire
        datetime date_envoi
        enum statut
        uuid utilisateur_id FK
    }
    UTILISATEUR {
        uuid id PK
        string email
        string nom
        string mot_de_passe_hash
        enum role
    }

    OFFRE ||--o{ CRITERE_PONDERATION : a
    OFFRE ||--o{ COMPETENCE_REQUISE : definit
    OFFRE ||--o{ LANGUE_REQUISE : definit
    OFFRE ||--o{ CANDIDATURE : recoit
    CANDIDATURE ||--|| CV_FICHIER : possede
    CANDIDATURE ||--|| EXTRACTION_CV : extraite_par
    CANDIDATURE ||--o{ JOB_PARSING : declenche
    CANDIDATURE ||--o{ HISTORIQUE_ACTION : genere
    CANDIDATURE ||--o{ NOTE_INTERNE : contient
    CANDIDATURE ||--o{ ENVOI_EMAIL : recoit
    TEMPLATE_EMAIL ||--o{ ENVOI_EMAIL : utilise
    UTILISATEUR ||--o{ HISTORIQUE_ACTION : execute
    UTILISATEUR ||--o{ NOTE_INTERNE : ecrit
    UTILISATEUR ||--o{ ENVOI_EMAIL : envoie
```

---

## 3. Schéma logique relationnel (MLD) – Tables SQL (script DDL simplifié)

```sql
-- Types enum (PostgreSQL)
CREATE TYPE offre_statut AS ENUM ('brouillon', 'active', 'cloturee', 'archivee');
CREATE TYPE candidature_etape AS ENUM ('recu', 'preselection', 'entretien_rh', 'entretien_tech', 'offre', 'embauche');
CREATE TYPE formation_niveau AS ENUM ('non_renseigne', 'bac+2', 'bac+3', 'bac+5', 'doctorat');
CREATE TYPE parsing_statut AS ENUM ('pending', 'success', 'failed');
CREATE TYPE email_statut AS ENUM ('success', 'echec');
CREATE TYPE utilisateur_role AS ENUM ('recruteur', 'admin');

-- Table offre
CREATE TABLE offre (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titre VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    localisation VARCHAR(255),
    type_contrat VARCHAR(100),
    statut offre_statut NOT NULL DEFAULT 'brouillon',
    date_creation TIMESTAMP NOT NULL DEFAULT NOW(),
    seuil_alerte INT NOT NULL DEFAULT 80,
    slug VARCHAR(255) NOT NULL UNIQUE
);

-- Table critere_ponderation
CREATE TABLE critere_ponderation (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    offre_id UUID NOT NULL REFERENCES offre(id) ON DELETE CASCADE,
    critere_nom VARCHAR(50) NOT NULL CHECK (critere_nom IN ('competences', 'experience', 'formation', 'langues')),
    poids INT NOT NULL CHECK (poids >= 0 AND poids <= 100),
    UNIQUE(offre_id, critere_nom)
);

-- Table competence_requise
CREATE TABLE competence_requise (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    offre_id UUID NOT NULL REFERENCES offre(id) ON DELETE CASCADE,
    nom_competence VARCHAR(100) NOT NULL
);

-- Table langue_requise
CREATE TABLE langue_requise (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    offre_id UUID NOT NULL REFERENCES offre(id) ON DELETE CASCADE,
    nom_langue VARCHAR(50) NOT NULL
);

-- Table candidature
CREATE TABLE candidature (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    offre_id UUID NOT NULL REFERENCES offre(id) ON DELETE CASCADE,
    nom_candidat VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    statut_etape candidature_etape NOT NULL DEFAULT 'recu',
    date_depot TIMESTAMP NOT NULL DEFAULT NOW(),
    ip INET,
    user_agent TEXT,
    consentement BOOLEAN NOT NULL,
    date_consentement TIMESTAMP NOT NULL DEFAULT NOW(),
    score_global INT CHECK (score_global BETWEEN 0 AND 100),
    scores_detail JSONB,
    date_scoring TIMESTAMP,
    alerte_envoyee BOOLEAN DEFAULT FALSE
);

-- Table cv_fichier
CREATE TABLE cv_fichier (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidature_id UUID NOT NULL UNIQUE REFERENCES candidature(id) ON DELETE CASCADE,
    chemin_fichier VARCHAR(500) NOT NULL,
    nom_original VARCHAR(255) NOT NULL,
    taille INT NOT NULL,
    type_mime VARCHAR(100) NOT NULL,
    date_upload TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Table extraction_cv
CREATE TABLE extraction_cv (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidature_id UUID NOT NULL UNIQUE REFERENCES candidature(id) ON DELETE CASCADE,
    nom_extrait VARCHAR(255),
    email_extrait VARCHAR(255),
    competences JSONB,
    annees_experience INT DEFAULT 0,
    formation_niveau formation_niveau DEFAULT 'non_renseigne',
    statut_parsing parsing_statut NOT NULL DEFAULT 'pending',
    date_extraction TIMESTAMP,
    tentative INT DEFAULT 0
);

-- Table job_parsing
CREATE TABLE job_parsing (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidature_id UUID NOT NULL REFERENCES candidature(id) ON DELETE CASCADE,
    statut parsing_statut NOT NULL DEFAULT 'pending',
    tentative INT NOT NULL DEFAULT 0,
    dernier_erreur TEXT,
    date_creation TIMESTAMP NOT NULL DEFAULT NOW(),
    date_debut TIMESTAMP,
    date_fin TIMESTAMP
);

-- Table utilisateur
CREATE TABLE utilisateur (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    nom VARCHAR(255) NOT NULL,
    mot_de_passe_hash VARCHAR(255) NOT NULL,
    role utilisateur_role NOT NULL DEFAULT 'recruteur'
);

-- Table historique_action
CREATE TABLE historique_action (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidature_id UUID NOT NULL REFERENCES candidature(id) ON DELETE CASCADE,
    utilisateur_id UUID NOT NULL REFERENCES utilisateur(id),
    action_type VARCHAR(50) NOT NULL,
    ancienne_valeur VARCHAR(255),
    nouvelle_valeur VARCHAR(255),
    commentaire TEXT,
    date_action TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Table note_interne
CREATE TABLE note_interne (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidature_id UUID NOT NULL REFERENCES candidature(id) ON DELETE CASCADE,
    utilisateur_id UUID NOT NULL REFERENCES utilisateur(id),
    contenu TEXT NOT NULL,
    date_creation TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Table template_email
CREATE TABLE template_email (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nom VARCHAR(100) NOT NULL UNIQUE,
    objet VARCHAR(255) NOT NULL,
    corps_html TEXT,
    corps_texte TEXT,
    est_par_defaut BOOLEAN NOT NULL DEFAULT FALSE,
    date_creation TIMESTAMP NOT NULL DEFAULT NOW(),
    date_modif TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Table envoi_email
CREATE TABLE envoi_email (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidature_id UUID NOT NULL REFERENCES candidature(id) ON DELETE CASCADE,
    template_id UUID REFERENCES template_email(id) ON DELETE SET NULL,
    objet_envoye VARCHAR(255) NOT NULL,
    destinataire VARCHAR(255) NOT NULL,
    date_envoi TIMESTAMP NOT NULL DEFAULT NOW(),
    statut email_statut NOT NULL,
    utilisateur_id UUID NOT NULL REFERENCES utilisateur(id)
);

-- Index recommandés
CREATE INDEX idx_candidature_offre_id ON candidature(offre_id);
CREATE INDEX idx_candidature_statut_etape ON candidature(statut_etape);
CREATE INDEX idx_candidature_score_global ON candidature(score_global);
CREATE INDEX idx_candidature_date_depot ON candidature(date_depot);
CREATE INDEX idx_offre_statut ON offre(statut);
CREATE INDEX idx_offre_slug ON offre(slug);
CREATE INDEX idx_historique_candidature ON historique_action(candidature_id, date_action);
CREATE INDEX idx_extraction_cv_candidature ON extraction_cv(candidature_id);
CREATE INDEX idx_job_parsing_statut ON job_parsing(statut);
```

---

## 4. Contraintes d’intégrité et règles de gestion implémentées

| Règle | Implémentation SQL |
|-------|--------------------|
| Les 4 critères de scoring par offre | Table `critere_ponderation` avec contrainte UNIQUE(offre_id, critere_nom) et CHECK sur `poids` (0-100). La somme à 100 est à vérifier en application. |
| Un CV par candidature | `cv_fichier.candidature_id` UNIQUE |
| Une extraction par candidature | `extraction_cv.candidature_id` UNIQUE |
| Suppression en cascade (offre supprimée → candidatures supprimées) | `ON DELETE CASCADE` sur les clés étrangères |
| Historique immutable | Pas de `ON UPDATE CASCADE` ; les valeurs historisées sont figées |
| Score global entre 0 et 100 | `CHECK` sur `score_global` |

---

Voici la rédaction de la **sous-étape 2.1 – Lister les entités principales (à partir des modules)**.

---

## 2. Démarche en 6 sous‑étapes

### 2.1. Lister les entités principales (à partir des modules)

**Objectif** : Identifier toutes les entités (tables) nécessaires au fonctionnement du système, en s’appuyant sur les modules fonctionnels définis lors de l’analyse fonctionnelle.

**Méthode** : Pour chaque module (M1 à M7), on extrait les noms des objets métier qui doivent être persistants. On regroupe les synonymes et on élimine les redondances.

#### Résultat : liste des entités principales

| Module | Entités candidates | Entités retenues (nom normalisé) | Justification |
|--------|--------------------|----------------------------------|----------------|
| **M1 – Gestion des offres** | Offre, Critère de scoring, Compétence requise, Langue requise | `offre`, `critere_ponderation`, `competence_requise`, `langue_requise` | Une offre a ses propres critères pondérés et listes de compétences/langues. |
| **M2 – Candidature publique** | Candidature, Candidat (les données du formulaire) | `candidature` | On fusionne « Candidat » dans `candidature` car pas de compte séparé. |
| **M3 – Parsing & extraction IA** | CV, Extraction, Job de parsing | `cv_fichier`, `extraction_cv`, `job_parsing` | Le fichier CV est distinct des données extraites ; le job de parsing gère la file d’attente. |
| **M4 – Scoring & matching** | Score (global et détail), Alerte | (intégré dans `candidature` et `extraction_cv`) | Le score global est stocké dans `candidature`, les scores détaillés dans `extraction_cv` (ou un champ JSON). Pas d’entité séparée pour l’alerte (simple booléen). |
| **M5 – Pipeline Kanban** | Étape, Historique, Note | `historique_action`, `note_interne` | L’étape courante est un attribut de `candidature`. L’historique des changements et les notes sont des entités séparées. |
| **M6 – Communication manuelle** | Template d’email, Envoi d’email | `template_email`, `envoi_email` | Les templates sont globaux ; chaque envoi est journalisé. |
| **M7 – Reporting & export** | (aucune entité propre) | – | Les indicateurs sont calculés à la demande, pas de stockage spécifique. |
| **Transverse** | Utilisateur (recruteur) | `utilisateur` | Pour authentification et traçabilité des actions. |

#### Liste consolidée des entités (ordre alphabétique) :

1. `candidature`
2. `competence_requise`
3. `critere_ponderation`
4. `cv_fichier`
5. `envoi_email`
6. `extraction_cv`
7. `historique_action`
8. `job_parsing`
9. `langue_requise`
10. `note_interne`
11. `offre`
12. `template_email`
13. `utilisateur`

**Total : 13 entités** pour le MVP.

#### Vérification des dépendances fonctionnelles :

- Chaque entité correspond à un besoin explicite des modules.
- Pas d’entité redondante (ex: « Candidat » et « Candidature » sont fusionnés).
- Les entités `competence_requise` et `langue_requise` sont séparées pour faciliter les requêtes de matching.

Cette liste servira de base pour la définition des attributs (2.2) et des relations (2.3).

---

## 2.2. Définir les attributs par entité

**Objectif** : Pour chaque entité identifiée, lister précisément les attributs (champs) nécessaires, leur type de données, les contraintes (clé primaire, obligatoire, unicité, valeurs par défaut) et une brève description.

**Méthode** : On reprend les spécifications fonctionnelles (modules M1 à M7) et le schéma relationnel esquissé précédemment. On normalise les noms (snake_case) et on choisit des types SQL cohérents (UUID pour les clés, VARCHAR, TEXT, INT, TIMESTAMP, ENUM, JSONB, etc.).

---

### Entité 1 : `offre`

| Attribut | Type | Contraintes | Description |
|----------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Identifiant unique de l’offre |
| `titre` | VARCHAR(255) | NOT NULL | Titre du poste |
| `description` | TEXT | NOT NULL | Description détaillée de l’offre |
| `localisation` | VARCHAR(255) | NULL | Ville / télétravail |
| `type_contrat` | VARCHAR(100) | NULL | CDI, CDD, stage, freelance |
| `statut` | ENUM ('brouillon','active','cloturee','archivee') | NOT NULL, DEFAULT 'brouillon' | État de l’offre |
| `date_creation` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de création |
| `seuil_alerte` | INT | NOT NULL, DEFAULT 80, CHECK (0-100) | Score minimum pour déclencher une alerte email |
| `slug` | VARCHAR(255) | NOT NULL, UNIQUE | Identifiant d’URL publique (ex: "developpeur-python") |

---

### Entité 2 : `critere_ponderation`

| Attribut | Type | Contraintes | Description |
|----------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Identifiant unique |
| `offre_id` | UUID | FOREIGN KEY REFERENCES offre(id) ON DELETE CASCADE | Offre associée |
| `critere_nom` | VARCHAR(50) | NOT NULL, CHECK (IN ('competences','experience','formation','langues')) | Nom du critère (fixe) |
| `poids` | INT | NOT NULL, CHECK (poids >= 0 AND poids <= 100) | Pondération en % (somme 100 à vérifier en application) |

**Contrainte unique** : (`offre_id`, `critere_nom`)

---

### Entité 3 : `competence_requise`

| Attribut | Type | Contraintes | Description |
|----------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Identifiant unique |
| `offre_id` | UUID | FOREIGN KEY REFERENCES offre(id) ON DELETE CASCADE | Offre associée |
| `nom_competence` | VARCHAR(100) | NOT NULL | Nom de la compétence (ex: "Python", "Gestion de projet") |

---

### Entité 4 : `langue_requise`

| Attribut | Type | Contraintes | Description |
|----------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Identifiant unique |
| `offre_id` | UUID | FOREIGN KEY REFERENCES offre(id) ON DELETE CASCADE | Offre associée |
| `nom_langue` | VARCHAR(50) | NOT NULL | Nom de la langue (ex: "Anglais", "Allemand") |

---

### Entité 5 : `candidature`

| Attribut | Type | Contraintes | Description |
|----------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Identifiant unique |
| `offre_id` | UUID | FOREIGN KEY REFERENCES offre(id) ON DELETE CASCADE | Offre postulée |
| `nom_candidat` | VARCHAR(255) | NOT NULL | Nom complet du candidat |
| `email` | VARCHAR(255) | NOT NULL | Adresse email |
| `statut_etape` | ENUM ('recu','preselection','entretien_rh','entretien_tech','offre','embauche') | NOT NULL, DEFAULT 'recu' | Étape courante dans le pipeline |
| `date_depot` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de réception de la candidature |
| `ip` | INET | NULL | Adresse IP du candidat (traçabilité) |
| `user_agent` | TEXT | NULL | User-agent du navigateur |
| `consentement` | BOOLEAN | NOT NULL | Consentement RGPD |
| `date_consentement` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date du consentement |
| `score_global` | INT | NULL, CHECK (0-100) | Score calculé (0-100) |
| `scores_detail` | JSONB | NULL | Détail des scores par critère (ex: {"competences":80, "experience":60}) |
| `date_scoring` | TIMESTAMP | NULL | Date du dernier calcul de score |
| `alerte_envoyee` | BOOLEAN | NOT NULL, DEFAULT FALSE | Indique si une alerte score a déjà été envoyée |

---

### Entité 6 : `cv_fichier`

| Attribut | Type | Contraintes | Description |
|----------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Identifiant unique |
| `candidature_id` | UUID | FOREIGN KEY REFERENCES candidature(id) ON DELETE CASCADE, UNIQUE | Lien 1-1 avec candidature |
| `chemin_fichier` | VARCHAR(500) | NOT NULL | Chemin de stockage sécurisé |
| `nom_original` | VARCHAR(255) | NOT NULL | Nom original du fichier (pour téléchargement) |
| `taille` | INT | NOT NULL | Taille en octets |
| `type_mime` | VARCHAR(100) | NOT NULL | MIME type (application/pdf, application/vnd.openxmlformats-officedocument.wordprocessingml.document) |
| `date_upload` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date d’upload |

---

### Entité 7 : `extraction_cv`

| Attribut | Type | Contraintes | Description |
|----------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Identifiant unique |
| `candidature_id` | UUID | FOREIGN KEY REFERENCES candidature(id) ON DELETE CASCADE, UNIQUE | Lien 1-1 avec candidature |
| `nom_extrait` | VARCHAR(255) | NULL | Nom extrait par l’IA (peut différer du formulaire) |
| `email_extrait` | VARCHAR(255) | NULL | Email extrait (fallback si formulaire vide) |
| `competences` | JSONB | NULL | Liste des compétences détectées (ex: ["Python","SQL"]) |
| `annees_experience` | INT | DEFAULT 0 | Nombre total d’années d’expérience |
| `formation_niveau` | ENUM ('non_renseigne','bac+2','bac+3','bac+5','doctorat') | DEFAULT 'non_renseigne' | Niveau de formation |
| `statut_parsing` | ENUM ('pending','success','failed') | NOT NULL, DEFAULT 'pending' | État du traitement |
| `date_extraction` | TIMESTAMP | NULL | Date de fin d’extraction |
| `tentative` | INT | DEFAULT 0 | Nombre de tentatives (max 3) |

---

### Entité 8 : `job_parsing`

| Attribut | Type | Contraintes | Description |
|----------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Identifiant unique |
| `candidature_id` | UUID | FOREIGN KEY REFERENCES candidature(id) ON DELETE CASCADE | Lien vers la candidature |
| `statut` | ENUM ('pending','success','failed') | NOT NULL, DEFAULT 'pending' | État du job |
| `tentative` | INT | NOT NULL, DEFAULT 0 | Nombre de tentatives effectuées |
| `dernier_erreur` | TEXT | NULL | Message d’erreur si échec |
| `date_creation` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date d’ajout dans la file |
| `date_debut` | TIMESTAMP | NULL | Date de début de traitement |
| `date_fin` | TIMESTAMP | NULL | Date de fin (succès ou échec définitif) |

---

### Entité 9 : `utilisateur`

| Attribut | Type | Contraintes | Description |
|----------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Identifiant unique |
| `email` | VARCHAR(255) | NOT NULL, UNIQUE | Email de connexion |
| `nom` | VARCHAR(255) | NOT NULL | Nom affiché |
| `mot_de_passe_hash` | VARCHAR(255) | NOT NULL | Hash du mot de passe (bcrypt) |
| `role` | ENUM ('recruteur','admin') | NOT NULL, DEFAULT 'recruteur' | Rôle (admin pour support technique) |

---

### Entité 10 : `historique_action`

| Attribut | Type | Contraintes | Description |
|----------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Identifiant unique |
| `candidature_id` | UUID | FOREIGN KEY REFERENCES candidature(id) ON DELETE CASCADE | Candidature concernée |
| `utilisateur_id` | UUID | FOREIGN KEY REFERENCES utilisateur(id) | Recruteur ayant agi |
| `action_type` | VARCHAR(50) | NOT NULL | Type d’action ('changement_etape', 'ajout_note', 'envoi_email') |
| `ancienne_valeur` | VARCHAR(255) | NULL | Ancienne étape ou ancienne valeur |
| `nouvelle_valeur` | VARCHAR(255) | NULL | Nouvelle étape ou nouvelle valeur |
| `commentaire` | TEXT | NULL | Détail (ex: contenu d’une note) |
| `date_action` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Horodatage |

---

### Entité 11 : `note_interne`

| Attribut | Type | Contraintes | Description |
|----------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Identifiant unique |
| `candidature_id` | UUID | FOREIGN KEY REFERENCES candidature(id) ON DELETE CASCADE | Candidature associée |
| `utilisateur_id` | UUID | FOREIGN KEY REFERENCES utilisateur(id) | Auteur de la note |
| `contenu` | TEXT | NOT NULL | Texte libre |
| `date_creation` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de création |

---

### Entité 12 : `template_email`

| Attribut | Type | Contraintes | Description |
|----------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Identifiant unique |
| `nom` | VARCHAR(100) | NOT NULL, UNIQUE | Nom du template (ex: "Convocation entretien") |
| `objet` | VARCHAR(255) | NOT NULL | Sujet de l’email (peut contenir des variables comme [nom]) |
| `corps_html` | TEXT | NULL | Version HTML (WYSIWYG) |
| `corps_texte` | TEXT | NULL | Version texte brut (fallback) |
| `est_par_defaut` | BOOLEAN | NOT NULL, DEFAULT FALSE | True pour les 4 templates fournis par défaut |
| `date_creation` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de création |
| `date_modif` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de dernière modification |

---

### Entité 13 : `envoi_email`

| Attribut | Type | Contraintes | Description |
|----------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Identifiant unique |
| `candidature_id` | UUID | FOREIGN KEY REFERENCES candidature(id) ON DELETE CASCADE | Candidature destinataire |
| `template_id` | UUID | FOREIGN KEY REFERENCES template_email(id) ON DELETE SET NULL | Template utilisé (si applicable) |
| `objet_envoye` | VARCHAR(255) | NOT NULL | Sujet réel envoyé (variables résolues) |
| `destinataire` | VARCHAR(255) | NOT NULL | Adresse email du candidat |
| `date_envoi` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date d’envoi |
| `statut` | ENUM ('success','echec') | NOT NULL | Résultat de l’envoi |
| `utilisateur_id` | UUID | FOREIGN KEY REFERENCES utilisateur(id) | Recruteur qui a déclenché l’envoi |

---

**Récapitulatif** : 13 entités, chacune avec ses attributs typés et contraints, conformes aux spécifications fonctionnelles.

---

Voici la rédaction de la **sous-étape 2.3 – Définir les relations entre entités (cardinalités, contraintes référentielles)**.

---

## 2.3. Définir les relations entre entités

**Objectif** : Spécifier comment les entités sont reliées entre elles (associations), en précisant les cardinalités (1-1, 1-n, n-n) et les contraintes d’intégrité référentielle (suppression en cascade, restriction, etc.).

**Méthode** : Pour chaque paire d’entités en interaction, on détermine le sens de la relation, le nombre d’occurrences attendues, et les règles de gestion associées.

---

### Liste des relations (par ordre d’importance)

| Relation | Entité source | Entité cible | Cardinalité | Contraintes / Commentaires |
|----------|---------------|--------------|-------------|----------------------------|
| **R1** | `offre` | `critere_ponderation` | 1 → n | Une offre a exactement 4 critères de scoring (un par nom de critère). Suppression de l’offre → suppression des critères (CASCADE). |
| **R2** | `offre` | `competence_requise` | 1 → n | Une offre peut avoir 0 à n compétences requises. Suppression offre → suppression compétences (CASCADE). |
| **R3** | `offre` | `langue_requise` | 1 → n | Une offre peut avoir 0 à n langues requises. Suppression offre → suppression langues (CASCADE). |
| **R4** | `offre` | `candidature` | 1 → n | Une offre reçoit 0 à n candidatures. Suppression offre → suppression candidatures (CASCADE) – option discutable métier (on peut vouloir conserver l’historique). En MVP, on choisit CASCADE pour simplifier, mais en réalité on pourrait mettre RESTRICT ou SET NULL selon les besoins. |
| **R5** | `candidature` | `cv_fichier` | 1 → 1 | Une candidature a un seul CV. Relation 1-1. Suppression candidature → suppression du fichier CV (CASCADE). |
| **R6** | `candidature` | `extraction_cv` | 1 → 1 | Une candidature a une seule extraction (données structurées). 1-1. Suppression candidature → suppression extraction (CASCADE). |
| **R7** | `candidature` | `job_parsing` | 1 → n | Une candidature peut avoir plusieurs jobs de parsing (en cas de réessais). En pratique, on conserve le dernier job actif, mais on peut stocker l’historique. Cardinalité 1-n. |
| **R8** | `candidature` | `historique_action` | 1 → n | Une candidature peut avoir 0 à n actions historisées. Suppression candidature → suppression historique (CASCADE). |
| **R9** | `candidature` | `note_interne` | 1 → n | Une candidature peut avoir 0 à n notes internes. Suppression candidature → suppression notes (CASCADE). |
| **R10** | `candidature` | `envoi_email` | 1 → n | Une candidature peut avoir 0 à n envois d’email. Suppression candidature → suppression envois (CASCADE). |
| **R11** | `utilisateur` | `historique_action` | 1 → n | Un utilisateur peut être à l’origine de plusieurs actions historisées. Si l’utilisateur est supprimé (rare), on peut mettre `ON DELETE SET NULL` ou `RESTRICT`. MVP : `ON DELETE RESTRICT` (on empêche la suppression d’un utilisateur ayant des actions). |
| **R12** | `utilisateur` | `note_interne` | 1 → n | Un utilisateur peut écrire plusieurs notes. Même contrainte : `ON DELETE RESTRICT`. |
| **R13** | `utilisateur` | `envoi_email` | 1 → n | Un utilisateur peut envoyer plusieurs emails. `ON DELETE RESTRICT`. |
| **R14** | `template_email` | `envoi_email` | 1 → n | Un template peut être utilisé dans plusieurs envois. Si un template est supprimé, on peut garder l’envoi avec `template_id = NULL` (`ON DELETE SET NULL`). |

---

### Diagramme des relations (Mermaid) – simplifié

```mermaid
erDiagram
    OFFRE ||--o{ CRITERE_PONDERATION : possede
    OFFRE ||--o{ COMPETENCE_REQUISE : definit
    OFFRE ||--o{ LANGUE_REQUISE : definit
    OFFRE ||--o{ CANDIDATURE : recoit

    CANDIDATURE ||--|| CV_FICHIER : possede
    CANDIDATURE ||--|| EXTRACTION_CV : extraite_par
    CANDIDATURE ||--o{ JOB_PARSING : declenche
    CANDIDATURE ||--o{ HISTORIQUE_ACTION : genere
    CANDIDATURE ||--o{ NOTE_INTERNE : contient
    CANDIDATURE ||--o{ ENVOI_EMAIL : recoit

    UTILISATEUR ||--o{ HISTORIQUE_ACTION : execute
    UTILISATEUR ||--o{ NOTE_INTERNE : ecrit
    UTILISATEUR ||--o{ ENVOI_EMAIL : envoie

    TEMPLATE_EMAIL ||--o{ ENVOI_EMAIL : utilise
```

---

### Détail des cardinalités (lecture)

- **1 → n** (un à plusieurs) : L’entité source peut avoir plusieurs entités cibles, mais chaque entité cible appartient à une seule source.
- **1 → 1** (un à un) : Chaque candidature a exactement un fichier CV et une extraction.
- **0 → n** (zéro à plusieurs) : Certaines relations sont optionnelles (ex: une offre peut n’avoir aucune compétence requise).

---

### Contraintes référentielles (synthèse pour le MLD)

| Clé étrangère | Table cible | Suppression | Mise à jour | Justification |
|---------------|-------------|-------------|-------------|----------------|
| `critere_ponderation.offre_id` | `offre` | CASCADE | CASCADE | Si offre supprimée, ses critères n’ont plus de sens |
| `competence_requise.offre_id` | `offre` | CASCADE | CASCADE | Idem |
| `langue_requise.offre_id` | `offre` | CASCADE | CASCADE | Idem |
| `candidature.offre_id` | `offre` | RESTRICT | CASCADE | En MVP, on évite de supprimer une offre qui a des candidatures (sinon perte d’historique). On peut autoriser l’archivage via statut. |
| `cv_fichier.candidature_id` | `candidature` | CASCADE | CASCADE | Le CV n’existe pas sans candidature |
| `extraction_cv.candidature_id` | `candidature` | CASCADE | CASCADE | Idem |
| `job_parsing.candidature_id` | `candidature` | CASCADE | CASCADE | Idem |
| `historique_action.candidature_id` | `candidature` | CASCADE | CASCADE | Idem |
| `note_interne.candidature_id` | `candidature` | CASCADE | CASCADE | Idem |
| `envoi_email.candidature_id` | `candidature` | CASCADE | CASCADE | Idem |
| `historique_action.utilisateur_id` | `utilisateur` | RESTRICT | CASCADE | On ne supprime pas un utilisateur qui a des actions |
| `note_interne.utilisateur_id` | `utilisateur` | RESTRICT | CASCADE | Idem |
| `envoi_email.utilisateur_id` | `utilisateur` | RESTRICT | CASCADE | Idem |
| `envoi_email.template_id` | `template_email` | SET NULL | CASCADE | Si un template est supprimé, l’envoi garde trace (template devient NULL) |

---

**Vérification des cardinalités** : Toutes les relations respectent les règles métier issues des spécifications fonctionnelles (M1 à M7). Aucune relation many-to-many n’est présente en MVP (les listes de compétences/langues sont gérées par des tables enfants).
---
Voici la rédaction de la **sous-étape 2.4 – Appliquer les règles de gestion issues des spécifications**.

---

## 2.4. Appliquer les règles de gestion issues des spécifications

**Objectif** : Identifier les règles métier (issues de l’analyse fonctionnelle) qui ont un impact sur la structure des données, les contraintes d’intégrité, ou le comportement du système (déclencheurs, vérifications). Pour chaque règle, on précise comment elle est implémentée dans le schéma relationnel.

**Méthode** : On parcourt les spécifications des modules M1 à M7 et on extrait les règles de gestion déjà listées (RG‑01 à RG‑35). On ne retient que celles qui contraignent directement les données (valeurs autorisées, unicités, cycles de vie, intégrité référentielle). On ignore les règles purement procédurales (ex: envoi d’email asynchrone).

---

### Règles de gestion applicables à la modélisation des données

| Réf. règle | Énoncé | Implémentation dans le schéma |
|------------|--------|--------------------------------|
| **RG‑01** | Les offres clôturées ou archivées ne doivent pas pouvoir recevoir de nouvelles candidatures. | Contrôle au niveau applicatif (le formulaire public vérifie le statut de l’offre avant acceptation). Pas de contrainte SQL directe. |
| **RG‑02** | La suppression d’une offre (archivage) ne supprime pas les candidatures associées. | On utilise un statut `archivee` et non une suppression physique. La clé étrangère `candidature.offre_id` reste intacte. On évite `ON DELETE CASCADE` sur cette relation (on a choisi `RESTRICT`). |
| **RG‑03** | Un recruteur ne peut pas avoir deux offres actives avec le même slug. | Contrainte `UNIQUE` sur `offre.slug`. |
| **RG‑04** | La modification des pondérations de scoring sur une offre active n’affecte que les futurs candidats (pas de recalcul rétroactif). | Pas de contrainte SQL ; la règle est appliquée dans le code (le scoring ne recalcule que les nouvelles candidatures). On stocke la date de modification des pondérations si besoin (attribut `date_modif` dans `critere_ponderation`). |
| **RG‑05** | La page publique ne doit contenir aucune information confidentielle. | Pas de contrainte base de données. |
| **RG‑06** | Le fichier CV téléversé est immédiatement scanné antivirus (V2). | Non applicable MVP. |
| **RG‑07** | L’email d’accusé ne doit pas divulguer d’informations sensibles. | Pas de contrainte base de données. |
| **RG‑08** | Le stockage du CV doit utiliser des URLs signées avec expiration. | Pas de contrainte base de données ; stockage du chemin et génération d’URL signée au moment de l’accès. |
| **RG‑09** | Taux de soumission par IP : limiter à 5 candidatures par heure. | Contrôle applicatif (pas de contrainte SQL). |
| **RG‑10** | Le parsing ne doit jamais exposer le contenu du CV dans les logs. | Pas de contrainte base de données. |
| **RG‑11** | En cas d’échec de parsing, la candidature reste valide ; le score sera 0. | Accepté : `score_global` peut être NULL ou 0 ; `extraction_cv.statut_parsing = 'failed'`. |
| **RG‑12** | Les données extraites sont stockées de manière structurée. | Table `extraction_cv` avec colonnes typées (JSONB pour compétences, INT pour années, ENUM pour formation). |
| **RG‑13** | Les temps de parsing sont monitorés (P95 < 30s). | Pas de contrainte SQL, mais attributs `date_debut`, `date_fin` dans `job_parsing` pour calculs. |
| **RG‑14** | Les CV sont conservés pour une durée conforme RGPD (2 ans). | Attribut `date_upload` dans `cv_fichier` ; une tâche planifiée supprime les fichiers plus vieux que 2 ans. |
| **RG‑15** | Pas de recalcul rétroactif du score. | Règle applicative, pas de contrainte SQL. |
| **RG‑16** | Le score global est affiché dans le pipeline. | Attribut `candidature.score_global`. |
| **RG‑17** | Les scores détaillés sont visibles dans la fiche candidat. | Attribut `candidature.scores_detail` (JSONB). |
| **RG‑18** | Le seuil d’alerte est modifiable par offre, même après publication. | Attribut `offre.seuil_alerte` modifiable sans contrainte. |
| **RG‑19** | L’alerte email n’est pas envoyée si la candidature a déjà été notifiée. | Attribut `candidature.alerte_envoyee` booléen. |
| **RG‑20** | Les colonnes du pipeline sont fixes (6 étapes). | Enum `candidature_etape` avec les 6 valeurs. |
| **RG‑21** | Le drag & drop est permis sans contrainte de séquence. | Pas de contrainte SQL ; géré par l’application. |
| **RG‑22** | Chaque changement d’étape est horodaté et associé à l’utilisateur. | Table `historique_action` avec `action_type='changement_etape'`, `ancienne_valeur`, `nouvelle_valeur`, `utilisateur_id`, `date_action`. |
| **RG‑23** | Les notes internes ne sont pas visibles par les candidats. | Pas de contrainte SQL ; géré par les droits d’accès. |
| **RG‑24** | Un candidat ne peut pas être déplacé vers « Embauché » sans étapes antérieures (recommandation UI). | Pas de contrainte SQL. |
| **RG‑25** | Les candidatures archivées peuvent être restaurées (V2). | Non applicable MVP. |
| **RG‑26** | Les templates sont globaux. | Table `template_email` unique, partagée. |
| **RG‑27** | Les emails envoyés ne sont pas modifiables après envoi. | Table `envoi_email` en lecture seule après insertion (pas de UPDATE dans le code). |
| **RG‑28** | Un template peut contenir des variables illimitées. | Pas de contrainte SQL ; stockage en texte. |
| **RG‑29** | Variables supportées : [nom], [prenom], [poste], [offre_titre], [date_entretien], [lien]. | Pas de contrainte SQL ; vérification applicative. |
| **RG‑30** | L’envoi d’email est asynchrone. | Pas de contrainte SQL. |
| **RG‑31** | Les KPIs sont calculés en temps réel (pas de cache). | Pas de table de pré-agrégation ; vues ou requêtes directes. |
| **RG‑32** | Les délais sont exprimés en jours (arrondi 1 décimale). | Calcul via requêtes SQL (`EXTRACT` ou `AGE`). |
| **RG‑33** | L’export CSV n’inclut pas les CV. | Pas de contrainte SQL ; géré par l’application. |
| **RG‑34** | Seul le recruteur connecté peut exporter. | Contrôle d’accès, pas de contrainte SQL. |
| **RG‑35** | Les données supprimées (RGPD) ne remontent pas dans les exports. | Les suppressions physiques suppriment les lignes ; les anonymisations logiques (ex: `nom_candidat = 'ANONYMISE'`) doivent être traitées par le code. |

---

### Règles de gestion non directement implémentables en SQL (mais documentées)

Les règles suivantes sont des **règles fonctionnelles ou procédurales** qui ne peuvent pas être exprimées par des contraintes de base de données. Elles doivent être assurées par le code applicatif ou par des processus externes :

- RG‑01, RG‑05, RG‑06, RG‑07, RG‑08, RG‑09, RG‑10, RG‑13, RG‑15, RG‑21, RG‑23, RG‑24, RG‑25, RG‑27, RG‑28, RG‑29, RG‑30, RG‑31, RG‑32, RG‑33, RG‑34.

Ces règles sont néanmoins **traçables** dans la documentation technique et seront vérifiées lors des tests d’acceptation.

---

### Synthèse des contraintes SQL déduites des règles de gestion

| Type de contrainte | Exemple |
|--------------------|---------|
| **UNIQUE** | `offre.slug`, `template_email.nom`, (`offre_id`, `critere_nom`) dans `critere_ponderation` |
| **NOT NULL** | `offre.titre`, `candidature.nom_candidat`, `candidature.email`, etc. |
| **CHECK** | `poids BETWEEN 0 AND 100`, `score_global BETWEEN 0 AND 100`, enum values |
| **FOREIGN KEY avec actions** | `ON DELETE CASCADE` pour les dépendances faibles (cv, extraction, historique), `ON DELETE RESTRICT` pour `candidature.offre_id` (protège l’intégrité des candidatures), `ON DELETE SET NULL` pour `envoi_email.template_id` |
| **ENUM** | `offre_statut`, `candidature_etape`, `formation_niveau`, `parsing_statut`, `email_statut`, `utilisateur_role` |
| **DEFAULT** | `date_creation NOW()`, `seuil_alerte 80`, `statut_parsing 'pending'`, `role 'recruteur'` |

---
Voici la rédaction de la **sous-étape 2.5 – Produire le schéma conceptuel (MCD)**.

---

## 2.5. Produire le schéma conceptuel (MCD)

**Objectif** : Représenter graphiquement les entités, leurs attributs (clés uniquement dans le MCD) et les relations avec leurs cardinalités, indépendamment de toute technologie de base de données. Le MCD sert de modèle conceptuel pour garantir la cohérence métier avant le passage au MLD (logique) et au PSD (physique).

**Méthodologie** :
1. À partir de la liste des entités et des relations définies en 2.1 et 2.3, on dessine les boîtes entités.
2. Pour chaque entité, on ne mentionne que les attributs qui sont des **identifiants** (clé primaire) ou des **attributs descriptifs essentiels**. On laisse les attributs secondaires pour le MLD.
3. On représente les associations par des traits portant les cardinalités (notation (0,1), (1,1), (0,n), (1,n) par exemple).
4. On identifie les éventuelles associations réflexives ou ternaires (aucune ici).

---

### Schéma conceptuel (MCD) – notation entité-association

Ci-dessous la représentation textuelle (puis graphique) des entités et leurs liens.

#### Entités et identifiants

| Entité | Identifiant (clé primaire) | Autres attributs (clés étrangères incluses) |
|--------|----------------------------|----------------------------------------------|
| `OFFRE` | id | titre, statut, slug, seuil_alerte |
| `CRITERE_PONDERATION` | id | offre_id (FK), critere_nom, poids |
| `COMPETENCE_REQUISE` | id | offre_id (FK), nom_competence |
| `LANGUE_REQUISE` | id | offre_id (FK), nom_langue |
| `CANDIDATURE` | id | offre_id (FK), nom_candidat, email, statut_etape, score_global, alerte_envoyee |
| `CV_FICHIER` | id | candidature_id (FK), chemin_fichier |
| `EXTRACTION_CV` | id | candidature_id (FK), statut_parsing, annees_experience |
| `JOB_PARSING` | id | candidature_id (FK), statut, tentative |
| `UTILISATEUR` | id | email, nom, role |
| `HISTORIQUE_ACTION` | id | candidature_id (FK), utilisateur_id (FK), action_type, date_action |
| `NOTE_INTERNE` | id | candidature_id (FK), utilisateur_id (FK), contenu |
| `TEMPLATE_EMAIL` | id | nom, objet, est_par_defaut |
| `ENVOI_EMAIL` | id | candidature_id (FK), template_id (FK), utilisateur_id (FK), date_envoi, statut |

---

#### Associations et cardinalités

| Association | Entités liées | Cardinalité (de gauche à droite) | Signification |
|-------------|---------------|----------------------------------|----------------|
| `possede` | OFFRE → CRITERE_PONDERATION | (1,1) → (0,n) | Une offre possède exactement 4 critères ; un critère appartient à une seule offre. |
| `definit_competence` | OFFRE → COMPETENCE_REQUISE | (0,n) → (1,1) | Une offre définit 0 à n compétences ; une compétence est liée à une seule offre. |
| `definit_langue` | OFFRE → LANGUE_REQUISE | (0,n) → (1,1) | Une offre définit 0 à n langues ; une langue est liée à une seule offre. |
| `recoit` | OFFRE → CANDIDATURE | (1,1) → (0,n) | Une offre reçoit 0 à n candidatures ; une candidature est liée à une seule offre. |
| `possede_cv` | CANDIDATURE → CV_FICHIER | (1,1) → (1,1) | Une candidature possède un seul CV ; un CV appartient à une seule candidature. |
| `extrait` | CANDIDATURE → EXTRACTION_CV | (1,1) → (1,1) | Une candidature a une seule extraction ; une extraction est liée à une seule candidature. |
| `genere_job` | CANDIDATURE → JOB_PARSING | (1,1) → (0,n) | Une candidature peut générer plusieurs jobs de parsing (réessais). |
| `enregistre_action` | CANDIDATURE → HISTORIQUE_ACTION | (1,1) → (0,n) | Une candidature peut avoir plusieurs actions historisées. |
| `contient_note` | CANDIDATURE → NOTE_INTERNE | (1,1) → (0,n) | Une candidature peut avoir plusieurs notes internes. |
| `recoit_email` | CANDIDATURE → ENVOI_EMAIL | (1,1) → (0,n) | Une candidature peut recevoir plusieurs emails. |
| `execute` | UTILISATEUR → HISTORIQUE_ACTION | (1,1) → (0,n) | Un utilisateur peut exécuter plusieurs actions. |
| `ecrit` | UTILISATEUR → NOTE_INTERNE | (1,1) → (0,n) | Un utilisateur peut écrire plusieurs notes. |
| `envoie` | UTILISATEUR → ENVOI_EMAIL | (1,1) → (0,n) | Un utilisateur peut envoyer plusieurs emails. |
| `utilise` | TEMPLATE_EMAIL → ENVOI_EMAIL | (1,1) → (0,n) | Un template peut être utilisé dans plusieurs envois ; un envoi utilise au plus un template. |

---

### Diagramme MCD (graphique) – version texte structuré

```mermaid
erDiagram
    OFFRE {
        uuid id PK
        string titre
        string slug
        enum statut
        int seuil_alerte
    }
    CRITERE_PONDERATION {
        uuid id PK
        uuid offre_id FK
        string critere_nom
        int poids
    }
    COMPETENCE_REQUISE {
        uuid id PK
        uuid offre_id FK
        string nom_competence
    }
    LANGUE_REQUISE {
        uuid id PK
        uuid offre_id FK
        string nom_langue
    }
    CANDIDATURE {
        uuid id PK
        uuid offre_id FK
        string nom_candidat
        string email
        enum statut_etape
        int score_global
        boolean alerte_envoyee
    }
    CV_FICHIER {
        uuid id PK
        uuid candidature_id FK
        string chemin_fichier
    }
    EXTRACTION_CV {
        uuid id PK
        uuid candidature_id FK
        enum statut_parsing
        int annees_experience
    }
    JOB_PARSING {
        uuid id PK
        uuid candidature_id FK
        enum statut
        int tentative
    }
    UTILISATEUR {
        uuid id PK
        string email
        string nom
        enum role
    }
    HISTORIQUE_ACTION {
        uuid id PK
        uuid candidature_id FK
        uuid utilisateur_id FK
        string action_type
        datetime date_action
    }
    NOTE_INTERNE {
        uuid id PK
        uuid candidature_id FK
        uuid utilisateur_id FK
        text contenu
    }
    TEMPLATE_EMAIL {
        uuid id PK
        string nom
        string objet
        boolean est_par_defaut
    }
    ENVOI_EMAIL {
        uuid id PK
        uuid candidature_id FK
        uuid template_id FK
        uuid utilisateur_id FK
        datetime date_envoi
        enum statut
    }

    OFFRE ||--o{ CRITERE_PONDERATION : possede
    OFFRE ||--o{ COMPETENCE_REQUISE : definit
    OFFRE ||--o{ LANGUE_REQUISE : definit
    OFFRE ||--o{ CANDIDATURE : recoit
    CANDIDATURE ||--|| CV_FICHIER : possede
    CANDIDATURE ||--|| EXTRACTION_CV : extrait
    CANDIDATURE ||--o{ JOB_PARSING : genere
    CANDIDATURE ||--o{ HISTORIQUE_ACTION : enregistre
    CANDIDATURE ||--o{ NOTE_INTERNE : contient
    CANDIDATURE ||--o{ ENVOI_EMAIL : recoit
    UTILISATEUR ||--o{ HISTORIQUE_ACTION : execute
    UTILISATEUR ||--o{ NOTE_INTERNE : ecrit
    UTILISATEUR ||--o{ ENVOI_EMAIL : envoie
    TEMPLATE_EMAIL ||--o{ ENVOI_EMAIL : utilise
```

---

### Validation du MCD

- **Respect des règles de gestion** : Les cardinalités (1,n) traduisent bien les dépendances (ex: une offre a plusieurs candidatures, une candidature a un seul CV).
- **Absence de redondance** : Chaque information est stockée une seule fois.
- **Normalisation** : Déjà en 3NF (pas de dépendances fonctionnelles transitives).
- **Évolutivité** : L’ajout d’un nouveau type de critère (ex: "soft skills") nécessiterait une extension, mais la structure est ouverte.

**Ce MCD servira de base pour le passage au MLD (déjà produit en 2.6) et au script SQL.**

---

Voici la rédaction de la **sous-étape 2.6 – Transformer en schéma logique relationnel (MLD)**.

---

## 2.6. Transformer en schéma logique relationnel (MLD)

**Objectif** : Convertir le schéma conceptuel (MCD) en un schéma logique relationnel (MLD) c’est-à-dire un ensemble de tables (relations) avec leurs colonnes, leurs types, leurs contraintes d’intégrité (clés primaires, clés étrangères) et leurs dépendances. Ce MLD est directement implémentable dans un SGBD relationnel (PostgreSQL, MySQL, etc.).

**Méthodologie** :
1. Chaque entité du MCD devient une table.
2. Chaque attribut (identifiant ou descriptif) devient une colonne.
3. Les associations (1-1, 1-n) sont matérialisées par l’ajout de clés étrangères dans la table fille.
4. Les associations (n-n) nécessitent une table de liaison, mais aucune n’est présente dans notre MCD.
5. On choisit des types de données concrets (UUID, VARCHAR, INT, TIMESTAMP, ENUM, JSONB, etc.) adaptés au SGBD cible (PostgreSQL).
6. On ajoute des contraintes : NOT NULL, UNIQUE, CHECK, DEFAULT, et les actions sur les clés étrangères (ON DELETE CASCADE / RESTRICT / SET NULL).
7. On propose des index pour optimiser les requêtes fréquentes.

---

### 2.6.1. Passage des entités aux tables

| Entité MCD | Nom table | Commentaire |
|------------|-----------|-------------|
| OFFRE | `offre` | Table principale des offres |
| CRITERE_PONDERATION | `critere_ponderation` | Dépend de offre |
| COMPETENCE_REQUISE | `competence_requise` | Dépend de offre |
| LANGUE_REQUISE | `langue_requise` | Dépend de offre |
| CANDIDATURE | `candidature` | Dépend de offre |
| CV_FICHIER | `cv_fichier` | Dépend de candidature (1-1) |
| EXTRACTION_CV | `extraction_cv` | Dépend de candidature (1-1) |
| JOB_PARSING | `job_parsing` | Dépend de candidature |
| UTILISATEUR | `utilisateur` | Table autonome |
| HISTORIQUE_ACTION | `historique_action` | Dépend de candidature et utilisateur |
| NOTE_INTERNE | `note_interne` | Dépend de candidature et utilisateur |
| TEMPLATE_EMAIL | `template_email` | Table autonome |
| ENVOI_EMAIL | `envoi_email` | Dépend de candidature, template, utilisateur |

---

### 2.6.2. Schéma logique (DDL SQL)

Voici le script complet de création des tables pour PostgreSQL (v15+), avec les types énumérés et les contraintes.

```sql
-- Types énumérés
CREATE TYPE offre_statut AS ENUM ('brouillon', 'active', 'cloturee', 'archivee');
CREATE TYPE candidature_etape AS ENUM ('recu', 'preselection', 'entretien_rh', 'entretien_tech', 'offre', 'embauche');
CREATE TYPE formation_niveau AS ENUM ('non_renseigne', 'bac+2', 'bac+3', 'bac+5', 'doctorat');
CREATE TYPE parsing_statut AS ENUM ('pending', 'success', 'failed');
CREATE TYPE email_statut AS ENUM ('success', 'echec');
CREATE TYPE utilisateur_role AS ENUM ('recruteur', 'admin');

-- Table offre
CREATE TABLE offre (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titre VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    localisation VARCHAR(255),
    type_contrat VARCHAR(100),
    statut offre_statut NOT NULL DEFAULT 'brouillon',
    date_creation TIMESTAMP NOT NULL DEFAULT NOW(),
    seuil_alerte INT NOT NULL DEFAULT 80,
    slug VARCHAR(255) NOT NULL UNIQUE
);

-- Table critere_ponderation
CREATE TABLE critere_ponderation (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    offre_id UUID NOT NULL REFERENCES offre(id) ON DELETE CASCADE,
    critere_nom VARCHAR(50) NOT NULL,
    poids INT NOT NULL CHECK (poids >= 0 AND poids <= 100),
    UNIQUE(offre_id, critere_nom),
    CONSTRAINT critere_nom_check CHECK (critere_nom IN ('competences', 'experience', 'formation', 'langues'))
);

-- Table competence_requise
CREATE TABLE competence_requise (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    offre_id UUID NOT NULL REFERENCES offre(id) ON DELETE CASCADE,
    nom_competence VARCHAR(100) NOT NULL
);

-- Table langue_requise
CREATE TABLE langue_requise (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    offre_id UUID NOT NULL REFERENCES offre(id) ON DELETE CASCADE,
    nom_langue VARCHAR(50) NOT NULL
);

-- Table candidature
CREATE TABLE candidature (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    offre_id UUID NOT NULL REFERENCES offre(id) ON DELETE RESTRICT,
    nom_candidat VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    statut_etape candidature_etape NOT NULL DEFAULT 'recu',
    date_depot TIMESTAMP NOT NULL DEFAULT NOW(),
    ip INET,
    user_agent TEXT,
    consentement BOOLEAN NOT NULL,
    date_consentement TIMESTAMP NOT NULL DEFAULT NOW(),
    score_global INT CHECK (score_global BETWEEN 0 AND 100),
    scores_detail JSONB,
    date_scoring TIMESTAMP,
    alerte_envoyee BOOLEAN DEFAULT FALSE
);

-- Table cv_fichier
CREATE TABLE cv_fichier (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidature_id UUID NOT NULL UNIQUE REFERENCES candidature(id) ON DELETE CASCADE,
    chemin_fichier VARCHAR(500) NOT NULL,
    nom_original VARCHAR(255) NOT NULL,
    taille INT NOT NULL,
    type_mime VARCHAR(100) NOT NULL,
    date_upload TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Table extraction_cv
CREATE TABLE extraction_cv (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidature_id UUID NOT NULL UNIQUE REFERENCES candidature(id) ON DELETE CASCADE,
    nom_extrait VARCHAR(255),
    email_extrait VARCHAR(255),
    competences JSONB,
    annees_experience INT DEFAULT 0,
    formation_niveau formation_niveau DEFAULT 'non_renseigne',
    statut_parsing parsing_statut NOT NULL DEFAULT 'pending',
    date_extraction TIMESTAMP,
    tentative INT DEFAULT 0
);

-- Table job_parsing
CREATE TABLE job_parsing (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidature_id UUID NOT NULL REFERENCES candidature(id) ON DELETE CASCADE,
    statut parsing_statut NOT NULL DEFAULT 'pending',
    tentative INT NOT NULL DEFAULT 0,
    dernier_erreur TEXT,
    date_creation TIMESTAMP NOT NULL DEFAULT NOW(),
    date_debut TIMESTAMP,
    date_fin TIMESTAMP
);

-- Table utilisateur
CREATE TABLE utilisateur (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    nom VARCHAR(255) NOT NULL,
    mot_de_passe_hash VARCHAR(255) NOT NULL,
    role utilisateur_role NOT NULL DEFAULT 'recruteur'
);

-- Table historique_action
CREATE TABLE historique_action (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidature_id UUID NOT NULL REFERENCES candidature(id) ON DELETE CASCADE,
    utilisateur_id UUID NOT NULL REFERENCES utilisateur(id) ON DELETE RESTRICT,
    action_type VARCHAR(50) NOT NULL,
    ancienne_valeur VARCHAR(255),
    nouvelle_valeur VARCHAR(255),
    commentaire TEXT,
    date_action TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Table note_interne
CREATE TABLE note_interne (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidature_id UUID NOT NULL REFERENCES candidature(id) ON DELETE CASCADE,
    utilisateur_id UUID NOT NULL REFERENCES utilisateur(id) ON DELETE RESTRICT,
    contenu TEXT NOT NULL,
    date_creation TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Table template_email
CREATE TABLE template_email (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nom VARCHAR(100) NOT NULL UNIQUE,
    objet VARCHAR(255) NOT NULL,
    corps_html TEXT,
    corps_texte TEXT,
    est_par_defaut BOOLEAN NOT NULL DEFAULT FALSE,
    date_creation TIMESTAMP NOT NULL DEFAULT NOW(),
    date_modif TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Table envoi_email
CREATE TABLE envoi_email (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidature_id UUID NOT NULL REFERENCES candidature(id) ON DELETE CASCADE,
    template_id UUID REFERENCES template_email(id) ON DELETE SET NULL,
    objet_envoye VARCHAR(255) NOT NULL,
    destinataire VARCHAR(255) NOT NULL,
    date_envoi TIMESTAMP NOT NULL DEFAULT NOW(),
    statut email_statut NOT NULL,
    utilisateur_id UUID NOT NULL REFERENCES utilisateur(id) ON DELETE RESTRICT
);

-- Index recommandés
CREATE INDEX idx_candidature_offre_id ON candidature(offre_id);
CREATE INDEX idx_candidature_statut_etape ON candidature(statut_etape);
CREATE INDEX idx_candidature_score_global ON candidature(score_global);
CREATE INDEX idx_candidature_date_depot ON candidature(date_depot);
CREATE INDEX idx_offre_statut ON offre(statut);
CREATE INDEX idx_offre_slug ON offre(slug);
CREATE INDEX idx_historique_candidature ON historique_action(candidature_id, date_action);
CREATE INDEX idx_extraction_cv_candidature ON extraction_cv(candidature_id);
CREATE INDEX idx_job_parsing_statut ON job_parsing(statut);
CREATE INDEX idx_envoi_email_candidature ON envoi_email(candidature_id);
```

---

### 2.6.3. Vérification des contraintes de transformation

- **Respect des cardinalités** : Les clés étrangères et les contraintes UNIQUE traduisent les cardinalités (ex: `UNIQUE(candidature_id)` dans `cv_fichier` pour la relation 1-1).
- **Actions sur suppression** :
  - `ON DELETE CASCADE` pour les dépendances faibles (critères, compétences, CV, extraction, jobs, historique, notes, envois).
  - `ON DELETE RESTRICT` pour `candidature.offre_id` (on ne supprime pas une offre qui a des candidatures) et pour les références à `utilisateur` (on garde l’historique).
  - `ON DELETE SET NULL` pour `envoi_email.template_id` (on conserve la trace même si le template est supprimé).
- **Normalisation** : Toutes les tables sont en 3NF (pas de redondance, chaque fait dépend de la clé primaire).

---

### 2.6.4. Récapitulatif des tables (13 tables)

| Table | Clé primaire | Clés étrangères | Principales contraintes |
|-------|--------------|-----------------|-------------------------|
| `offre` | id | – | slug unique |
| `critere_ponderation` | id | offre_id | unique(offre_id, critere_nom), poids 0-100 |
| `competence_requise` | id | offre_id | – |
| `langue_requise` | id | offre_id | – |
| `candidature` | id | offre_id | score_global 0-100 |
| `cv_fichier` | id | candidature_id unique | – |
| `extraction_cv` | id | candidature_id unique | – |
| `job_parsing` | id | candidature_id | – |
| `utilisateur` | id | – | email unique |
| `historique_action` | id | candidature_id, utilisateur_id | – |
| `note_interne` | id | candidature_id, utilisateur_id | – |
| `template_email` | id | – | nom unique |
| `envoi_email` | id | candidature_id, template_id, utilisateur_id | – |

---

**Ce MLD est prêt pour l’implémentation physique (choix du SGBD, réglages de performance, partitionnement éventuel).**

Voici le **plan pour l’étape 4 : Architecture technique**.

L’objectif est de définir l’architecture technique de la solution ATS (SaaS) : choix technologiques, interactions entre composants, hébergement, sécurité, et performances.

---

# Plan d’exécution – Architecture technique

## 1. Objectif de l’étape
- Définir les **composants logiciels** (frontend, backend, base de données, workers, stockage, etc.).
- Choisir les **technologies** (langages, frameworks, bases de données, services cloud) adaptées au MVP et à l’évolution future.
- Décrire les **flux de données** entre composants (séquences techniques).
- Préciser les **contraintes non fonctionnelles** (sécurité, RGPD, montée en charge, disponibilité).

## 2. Démarche en 6 sous‑étapes

### 2.1. Définir l’architecture logique (composants)
- Identifier les briques nécessaires :
  - **Frontend** (interface recruteur + page publique candidat)
  - **API backend** (REST ou GraphQL)
  - **Base de données relationnelle** (PostgreSQL)
  - **Stockage de fichiers** (CV)
  - **File d’attente / workers** (pour parsing asynchrone)
  - **Service d’IA pour le parsing** (local ou externalisé)
  - **Service d’envoi d’emails** (SMTP ou API tierce)
  - **Cache** (optionnel MVP, mais anticipé)
- Produire un **schéma d’architecture logique** (blocs + flux).

### 2.2. Choisir les technologies
Pour chaque composant, proposer des options (avec justification) et une recommandation MVP :

| Composant | Options | Recommandation MVP |
|-----------|---------|---------------------|
| Frontend | React, Vue, Svelte, Angular | React (large écosystème, Vercel compatible) |
| Backend API | Node.js/Express, Python/Django, Python/FastAPI, Ruby on Rails, Go | Python/FastAPI (rapide à développer, bon pour l’IA) ou Node.js (homogène avec front) |
| Base de données | PostgreSQL, MySQL, SQLite | PostgreSQL (supporte JSONB, full-text search, robuste) |
| File d’attente | Redis Bull, RabbitMQ, AWS SQS | Redis Bull (léger, facile à déployer avec Node.js ou Python) |
| Worker parsing | Python (avec bibliothèques PDF/docx) | Python (univoque pour l’IA) |
| Stockage CV | Système de fichiers local, S3, Google Cloud Storage | S3 ou équivalent (scalable, sécurisé) |
| Service email | SMTP (SendGrid, Mailgun, AWS SES) | SendGrid ou AWS SES (API fiable) |
| Hébergement | Vercel, Heroku, AWS, GCP, self-hosted | Vercel pour frontend, AWS (EC2 + RDS + S3) ou Railway.app pour backend |
| IA parsing | Bibliothèques open-source (spaCy, pdfplumber, docx2txt) ou API tierce (OpenAI, HireVue) | Bibliothèques locales (RGPD, pas d’envoi de CV à l’extérieur) : pdfplumber + docx2txt + regex + petites règles NER |

### 2.3. Décrire l’architecture de déploiement (environnements)
- **Environnement de développement local** : Docker Compose (backend, base de données, Redis, worker).
- **Environnement de test / staging** : Hébergé sur une plateforme (ex: Vercel + Railway) avec base de données séparée.
- **Environnement de production** : Infrastructure cloud (AWS, GCP, ou équivalent) avec redondance, sauvegardes, monitoring.

### 2.4. Spécifier les flux techniques (diagrammes de séquence système)
- **Flux 1 : Dépôt de candidature** (candidat → front public → API → stockage CV → file d’attente → accusé email)
- **Flux 2 : Parsing et scoring** (worker → extraction → mise à jour base → alerte si score élevé)
- **Flux 3 : Recruteur consulte le pipeline** (front recruteur → API → base de données)
- **Flux 4 : Drag & drop Kanban** (front → API → mise à jour candidature + historique)
- **Flux 5 : Envoi manuel d’email** (front → API → file d’attente email → journalisation)

### 2.5. Définir la stratégie de sécurité & RGPD
- **Authentification** : JWT (JSON Web Tokens) ou sessions HTTP-only. MVP : simple email/mot de passe avec hash bcrypt.
- **Autorisation** : middleware vérifiant le rôle (recruteur / admin).
- **Protection des CV** : URLs signées (expiration 1h), stockage hors du dossier public.
- **Chiffrement** : HTTPS obligatoire, chiffrement des CV au repos (optionnel MVP).
- **RGPD** : Consentement explicite, droit à l’oubli (suppression physique anonymisée), logs d’accès.
- **Rate limiting** : Sur les endpoints publics (candidature) et privés (prévention brute force).

### 2.6. Anticiper la scalabilité et la performance (options pour V2)
- Mise à l’échelle horizontale des workers (plusieurs instances).
- Mise en cache des scores et offres fréquemment consultées (Redis).
- Indexation base de données (déjà prévue).
- Partitionnement des tables (ex: candidatures par date).

## 3. Livrables de l’étape 4

| Livrable | Format | Description |
|----------|--------|-------------|
| **Schéma d’architecture logique** | Diagramme Mermaid / Draw.io | Composants et flux |
| **Tableau des choix technologiques** | Markdown | Technologie retenue + justification |
| **Diagrammes de séquence système** (5 flux) | Mermaid | Détail des interactions techniques |
| **Stratégie de déploiement** | Texte | Environnements, hébergement, variables d’environnement |
| **Spécifications sécurité / RGPD** | Liste | Mesures concrètes |
| **Plan de montée en charge** (V2) | Texte | Recommandations pour l’avenir |

---

## 1. Objectif de l’étape

L’objectif de l’étape **« Architecture technique »** est de définir l’ensemble des composants logiciels, des technologies et des interactions nécessaires à la réalisation de la plateforme ATS (SaaS), en respectant les spécifications fonctionnelles et de données établies précédemment.

Cette étape doit aboutir à une **architecture concrète, cohérente et prête à être implémentée**, en couvrant les aspects suivants :

- **Composants fonctionnels** : frontend (interface recruteur + page publique), backend (API), base de données, stockage de fichiers, file d’attente pour le parsing asynchrone, workers d’extraction IA, service d’envoi d’emails, etc.
- **Choix technologiques** : sélection des langages, frameworks, bases de données, services d’hébergement et bibliothèques adaptés à un MVP (Minimum Viable Product) mais extensibles pour la suite.
- **Flux de données techniques** : schémas de séquence illustrant le parcours des informations (dépôt de candidature, parsing, scoring, actions recruteur, envoi d’emails).
- **Déploiement et environnements** : organisation du travail en local, staging et production, avec une stratégie de mise à disposition continue (CI/CD).
- **Sécurité et conformité RGPD** : mesures de protection des données (CV, emails, consentement), authentification, chiffrement, traçabilité.
- **Performances et scalabilité** : anticipation des goulots d’étranglement (parsing, base de données) et pistes d’évolution pour la montée en charge.

**En résumé** : produire un plan technique détaillé et juste assez pour démarrer le développement du MVP, tout en posant les bases d’une architecture robuste et évolutive.

---
Voici la rédaction de la **sous‑étape 2.1 – Définir l’architecture logique (composants)** pour l’étape 4.

---

## 2. Démarche en 6 sous‑étapes

### 2.1. Définir l’architecture logique (composants)

**Objectif** : Identifier les briques logicielles nécessaires au fonctionnement de l’ATS, leurs responsabilités et leurs interactions, indépendamment des choix technologiques précis.

**Méthode** : On découpe le système en composants cohérents (séparation des préoccupations). On décrit chaque composant et on schématise les flux d’informations entre eux.

#### Liste des composants logiques

| Composant | Rôle / Responsabilités | Interactions principales |
|-----------|------------------------|--------------------------|
| **Frontend recruteur** | Interface web pour le recruteur : gestion des offres, pipeline Kanban, visualisation candidats, envoi d’emails, reporting. | Communique avec l’API backend (requêtes HTTP). Authentification via JWT/session. |
| **Frontend public** | Page publique de candidature (par offre) : affichage de l’offre, formulaire de dépôt, consentement RGPD. | Communique avec l’API backend (endpoints publics). Pas d’authentification. |
| **API backend** | Cœur métier : expose les endpoints REST (ou GraphQL) pour toutes les actions (CRUD offres, dépôt candidature, parsing, scoring, pipeline, emails, reporting). Gère l’authentification et les autorisations. | Dialogue avec la base de données, le stockage de fichiers, la file d’attente, et le service d’emails. |
| **Base de données relationnelle** | Persistance des données structurées : offres, candidatures, extractions, historiques, utilisateurs, templates, etc. | Interrogée par l’API backend et par les workers (en lecture/écriture). |
| **Stockage de fichiers (CV)** | Hébergement des fichiers CV téléversés. Doit être sécurisé (accès via URLs signées). | Reçoit les fichiers depuis l’API (dépôt candidature). Fournit des URLs temporaires pour le téléchargement par le recruteur. |
| **File d’attente (queue)** | Gestion asynchrone des tâches longues : parsing des CV, envoi d’emails (si asynchrone), éventuellement scoring. | L’API backend y dépose des jobs. Les workers consomment ces jobs. |
| **Worker parsing & IA** | Traite les CV : extraction du texte, analyse par IA (compétences, expérience, formation), mise à jour de la base de données avec les résultats. | Consomme les jobs de la file d’attente. Accède au stockage de fichiers pour lire le CV. Écrit le résultat dans la base de données. |
| **Worker email (optionnel)** | Envoi asynchrone des emails (accusé réception, alertes score, communications manuelles). Peut être fusionné avec le worker parsing en MVP, mais mieux séparé pour l’évolutivité. | Consomme une file d’attente dédiée ou la même. Appelle un service SMTP externe. |
| **Service d’IA (local)** | Moteur d’extraction : bibliothèques Python (pdfplumber, docx2txt, spaCy ou expressions régulières). Exécuté au sein du worker parsing. | Pas de service externe ; code embarqué pour respecter RGPD. |
| **Service d’emails** | Fournisseur SMTP externe (SendGrid, AWS SES, etc.). | Appelé par le worker email pour envoyer les messages. |
| **Cache (optionnel MVP)** | Stockage temporaire (ex: Redis) pour les sessions, les données fréquemment consultées (offres actives, scores). | En MVP, on peut s’en passer ; prévoir l’emplacement pour V2. |

#### Schéma d’architecture logique (blocs et flux)

```mermaid
flowchart TB
    subgraph Clients
        A[Recruteur - navigateur]
        B[Candidat - navigateur]
    end

    subgraph Frontends
        C[Frontend recruteur]
        D[Frontend public (page offre)]
    end

    subgraph Backend
        E[API backend]
        F[Base de données]
        G[File d'attente (Redis)]
        H[Stockage CV (S3/disque)]
        I[Worker parsing + IA]
        J[Worker email]
        K[Service SMTP externe]
    end

    A --> C
    B --> D
    C -->|HTTPS| E
    D -->|HTTPS| E

    E -->|CRUD| F
    E -->|upload / download| H
    E -->|dépose jobs| G

    G -->|job parsing| I
    G -->|job email| J

    I -->|lit CV| H
    I -->|écrit extraction| F

    J -->|envoi via| K
    J -->|journalise| F

    K -->|email| B
    K -->|alerte| A

```

#### Description des flux principaux (logiques)

1. **Dépôt de candidature** : Candidat → Frontend public → API → stockage CV → file d’attente parsing → email accusé (via file email).
2. **Parsing et scoring** : Worker parsing → lecture CV → extraction IA → mise à jour base → (optionnel) déclenchement scoring (dans le worker ou après).
3. **Pipeline Kanban** : Recruteur → Frontend recruteur → API → base de données → affichage des colonnes.
4. **Drag & drop** : Frontend recruteur → API (mise à jour étape) → base de données + historique.
5. **Envoi manuel d’email** : Recruteur → API → file email → worker email → SMTP.

**Ce découpage logique permet une implémentation modulaire, des tests isolés, et une scalabilité future (plusieurs workers).**

---
Voici la rédaction de la **sous‑étape 2.2 – Choisir les technologies** pour l’étape 4.

---

## 2.2. Choisir les technologies

**Objectif** : Pour chaque composant identifié dans l’architecture logique, sélectionner une technologie concrète (langage, framework, service, bibliothèque) qui respecte les contraintes du MVP : rapidité de développement, coût maîtrisé, conformité RGPD, et évolutivité future.

**Méthode** : On compare les options pertinentes, on justifie le choix, et on note les points d’attention.

---

### Tableau des choix technologiques (par composant)

| Composant | Options envisagées | Recommandation MVP | Justification |
|-----------|--------------------|--------------------|----------------|
| **Frontend recruteur** | React, Vue, Svelte, Angular | **React** (avec Vite ou Create React App) | Large écosystème, composants réutilisables, facilité de recrutement, compatible Vercel. |
| **Frontend public (page offre)** | React (même codebase) ou HTML/CSS simple | **React** (même projet que front recruteur, mais routes séparées) | Uniformité technologique, réutilisation des composants (formulaires, affichage). |
| **Backend API** | Node.js/Express, Python/Django, Python/FastAPI, Ruby on Rails, Go | **Python + FastAPI** | – Développement rapide (typage automatique, documentation OpenAPI générée)<br>– Idéal pour intégrer l’IA (bibliothèques Python)<br>– Asynchrone natif (performant pour les appels I/O)<br>– Grande communauté |
| **Base de données** | PostgreSQL, MySQL, SQLite | **PostgreSQL** | – Support natif des types JSONB (pour scores_detail, compétences)<br>– Excellente gestion des index et des requêtes full-text<br>– Conforme RGPD (hébergement France possible)<br>– Robuste et évolutive |
| **Stockage de fichiers (CV)** | Système de fichiers local, AWS S3, Google Cloud Storage, MinIO (self-hosted) | **AWS S3** (ou équivalent Scaleway / OVH pour rester en France) | – Scalable, sécurisé, URLs signées<br>– Coût faible pour le MVP<br>– Peut être remplacé par un stockage local en développement |
| **File d’attente** | Redis (Bull), RabbitMQ, AWS SQS, PostgreSQL (SKIP LOCKED) | **Redis + Bull** (si backend Node.js) **ou** **Redis + RQ** (si backend Python) | – Léger, rapide, persistant optionnel<br>– Bull (Node.js) ou RQ (Python) sont matures<br>– Permet une gestion simple des jobs asynchrones |
| **Worker parsing IA** | Python (même environnement que backend) ou worker dédié séparé | **Python** (script séparé mais même codebase que backend) | – On réutilise les bibliothèques d’extraction (pdfplumber, docx2txt, spaCy ou regex)<br> – Déploiement simplifié (même container, mais processus distinct) |
| **Bibliothèques IA parsing** | pdfplumber (PDF), docx2txt (DOCX), spaCy (NER), ou regex maison | **pdfplumber + docx2txt + regex** (pas de spaCy en MVP) | – Pas d’envoi de CV à un service externe (RGPD)<br> – Leger, suffisant pour extraire nom, email, compétences, dates<br> – spaCy pourrait être ajouté en V2 pour plus de précision |
| **Service d’emails** | SendGrid, Mailgun, AWS SES, SMTP interne | **AWS SES** ou **SendGrid** (niveau gratuit) | – Fiable, bonnes délivrabilités<br> – API simple<br> – Coût faible (gratuit jusqu’à 3000 emails/mois pour SES) |
| **Authentification** | JWT, sessions HTTP-only, OAuth2 (Google, GitHub) | **JWT** (stocké en HttpOnly cookie) | – Stateless, facile à implémenter avec FastAPI (python-jose)<br> – Sécurisé si cookie HttpOnly + SameSite=Lax<br> – On pourra ajouter OAuth en V2 |
| **Hébergement** | Vercel (front), Heroku, Railway, AWS (EC2+RDS+S3), self-hosted | **Vercel** (frontend React) + **Railway.app** ou **AWS** (backend + base de données) | – Vercel : déploiement continu gratuit pour front<br> – Railway : facile pour backend Python + PostgreSQL + Redis (hébergement intégré)<br> – Alternative AWS plus complexe mais plus contrôlée |
| **Cache (optionnel MVP)** | Redis, Memcached, pas de cache | **Redis** (même instance que la file d’attente) | – En MVP, on peut se passer de cache, mais Redis est déjà présent pour la queue ; on pourra l’utiliser pour stocker les sessions ou les offres actives |
| **CI/CD** | GitHub Actions, GitLab CI, Vercel native | **GitHub Actions** (pour backend) + **Vercel** (front) | – Gratuit pour petits projets<br> – Tests automatisés, déploiement sur push |

---

### Schéma technologique récapitulatif

```mermaid
flowchart LR
    subgraph Front
        REACT[React - Vercel]
    end
    subgraph Backend
        FASTAPI[FastAPI - Railway/AWS]
        POSTGRE[PostgreSQL]
        REDIS[Redis]
        WORKER[Worker Python]
        S3[AWS S3 / Scaleway]
    end
    subgraph Externe
        SMTP[AWS SES / SendGrid]
    end

    REACT --> FASTAPI
    FASTAPI --> POSTGRE
    FASTAPI --> REDIS
    FASTAPI --> S3
    REDIS --> WORKER
    WORKER --> POSTGRE
    WORKER --> S3
    FASTAPI --> SMTP
    WORKER --> SMTP
```

---

### Justification globale des choix

- **Python + FastAPI** : cohérence avec le besoin d’IA (bibliothèques NLP, extraction) et rapidité de développement. L’asynchrone natif est un atout pour les appels externes (S3, emails, base).
- **PostgreSQL** : standard du marché, support JSONB (indispensable pour les scores détaillés et les compétences extraites), et respect RGPD.
- **React** : permet de partager du code entre l’interface recruteur et la page publique (ex: composant formulaire). Large communauté et intégration avec Vercel.
- **Redis** : à la fois pour la file d’attente (Bull ou RQ) et pour le cache futur. Solution légère.
- **Hébergement séparé** : Vercel pour le front (gratuit), Railway.app ou AWS pour le backend (choix selon budget et compétences). Railway simplifie la gestion de PostgreSQL et Redis.

**Ces choix permettent un MVP fonctionnel en quelques semaines, tout en restant ouverts à une montée en charge (passage à AWS, ajout de workers, etc.).**

---
Voici la rédaction de la **sous‑étape 2.3 – Décrire l’architecture de déploiement** pour l’étape 4.

---

## 2.3. Décrire l’architecture de déploiement

**Objectif** : Définir comment le code est organisé, les différents environnements (local, test, production), les stratégies de déploiement (CI/CD), et les mécanismes de gestion des variables d’environnement et des données.

**Méthode** : On décrit les environnements nécessaires, le workflow Git, la chaîne d’intégration continue, et les configurations spécifiques à chaque environnement.

---

### 2.3.1. Environnements cibles

| Environnement | Usage | Accès | Données | Hébergement |
|---------------|-------|-------|---------|--------------|
| **Développement local** | Développement et tests unitaires | Développeur uniquement | Base de données locale (Docker), stockage CV local, Redis local | Machine du développeur (Docker Compose) |
| **Staging** | Tests d’intégration, validation fonctionnelle, recette interne | Équipe projet (recruteurs, devs) | Base de données de test (anonymisée ou jeux de données fictifs) | Vercel (front) + Railway ou AWS (backend) – environnement séparé |
| **Production** | Utilisation réelle par les recruteurs | Clients finaux | Données réelles (RGPD) | Vercel (front) + AWS (backend scalable) ou Railway (simplifié) |

---

### 2.3.2. Organisation du code et branches Git

- **Monorepo** (recommandé) : un seul dépôt Git contenant :
  - `/front` (React – Vite ou Next.js)
  - `/backend` (FastAPI)
  - `/workers` (scripts Python pour parsing et email, partageant des modules avec backend)
  - `/docker` (fichiers Docker Compose pour le développement)
  - `/infra` (scripts de déploiement, configuration Nginx, etc.)

- **Stratégie de branches** (Git Flow simplifié) :
  - `main` : code de production (toujours déployable)
  - `develop` : intégration des fonctionnalités (déploiement automatique sur staging)
  - `feature/*` : branches pour chaque fonctionnalité (issues / user stories)
  - `hotfix/*` : correctifs urgents directement sur main

- **Règles de protection** : `main` protégée, nécessite une revue de code (pull request) et succès des tests CI.

---

### 2.3.3. Pipeline CI/CD (GitHub Actions)

| Étape | Déclencheur | Actions |
|-------|-------------|---------|
| **Linting & tests unitaires** | Sur chaque push (toutes branches) | Front : ESLint, Prettier, tests React (Jest)<br>Back : flake8, pytest (unitaires, mock DB) |
| **Build & tests d’intégration** | Sur push sur `develop` et `main` | Build des containers Docker, lancement de la base de test, exécution des tests d’intégration (API) |
| **Déploiement staging** | Sur push sur `develop` (automatique) | Front déployé sur Vercel (projet staging)<br>Backend déployé sur Railway/AWS (environnement staging) |
| **Déploiement production** | Sur push sur `main` (manuel via tag ou confirmation) | Front déployé sur Vercel (projet production)<br>Backend déployé sur environnement de production |
| **Migrations base de données** | Automatique avant déploiement backend | Exécution des scripts de migration (Alembic pour SQLAlchemy) – avec rollback possible |

---

### 2.3.4. Configuration des environnements (variables)

Toutes les informations sensibles sont stockées dans des **variables d’environnement** (fichiers `.env` non versionnés). Exemples :

| Variable | Développement local | Staging | Production |
|----------|---------------------|---------|-------------|
| `DATABASE_URL` | postgresql://user:pass@localhost:5432/ats_dev | URL base staging | URL base production |
| `REDIS_URL` | redis://localhost:6379 | URL Redis staging | URL Redis production |
| `AWS_S3_BUCKET` | ats-cv-local (mock) | ats-cv-staging | ats-cv-prod |
| `SENDGRID_API_KEY` | (mock) | clé réelle (sandbox) | clé réelle |
| `JWT_SECRET` | secret_dev | secret_staging | secret_prod (unique, fort) |
| `FRONTEND_URL` | http://localhost:3000 | https://staging.ats.exemple.com | https://ats.exemple.com |

---

### 2.3.5. Gestion des données sensibles et des migrations

- **Migrations** : outil Alembic (Python) avec révision en code. Les migrations sont testées en staging avant production.
- **Sauvegardes** :
  - Base de données : dump quotidien + sauvegarde continue (WAL) via service cloud (AWS RDS, ou cron sur serveur).
  - CV stockés : versionnage S3 (lifecycle rules) ou sauvegarde inter-région.
- **Anonymisation pour staging** : script qui copie la base de production (si besoin) et anonymise les noms, emails, IPs, et supprime les CV réels (remplacés par des fichiers factices).

---

### 2.3.6. Schéma de déploiement (Mermaid)

```mermaid
flowchart LR
    subgraph Git
        DEV[feature/*]
        DEVELOP[develop]
        MAIN[main]
    end

    subgraph CI
        LINT[Lint + tests unitaires]
        INTEG[Tests intégration]
    end

    subgraph Environnements
        LOCAL[Docker local]
        STAGING[Staging - Vercel + Railway]
        PROD[Production - Vercel + AWS]
    end

    DEV -->|push| LINT
    LINT -->|PR merge| DEVELOP
    DEVELOP -->|push| INTEG
    INTEG -->|auto| STAGING
    DEVELOP -->|PR merged to main| MAIN
    MAIN -->|tag release| PROD
```

---

### 2.3.7. Surveillance et monitoring (MVP léger)

- **Logs** : centralisés via service (Sentry pour les erreurs, Papertrail ou AWS CloudWatch).
- **Métriques** : via service simple (ex: UptimeRobot pour la disponibilité, ou Prometheus/Grafana en V2).
- **Alertes** : email au support technique si CPU backend > 80% ou file d’attente Redis > 1000 jobs.

**Cette architecture de déploiement permet une livraison continue, sécurisée, et maintenable dès le MVP.**

---
Voici la rédaction de la **sous‑étape 2.4 – Spécifier les flux techniques (diagrammes de séquence système)** pour l’étape 4.

---

## 2.4. Spécifier les flux techniques

**Objectif** : Décrire les interactions techniques entre composants pour chaque scénario fonctionnel clé, en utilisant des diagrammes de séquence UML. Ces diagrammes servent de base à l’implémentation (API endpoints, files d’attente, workers).

**Méthode** : Pour chaque flux, on identifie l’acteur déclencheur, les composants impliqués, l’ordre des appels (synchrone/asynchrone), et les réponses attendues.

---

### Flux F1 – Dépôt d’une candidature (candidat → front public → backend)

```mermaid
sequenceDiagram
    participant Candidat
    participant FrontPub as Frontend public (React)
    participant API as API FastAPI
    participant DB as PostgreSQL
    participant Storage as S3 (CV)
    participant Queue as Redis (Bull/RQ)
    participant Worker as Worker parsing
    participant Email as Service email (SES)

    Candidat->>FrontPub: Remplit formulaire + CV
    FrontPub->>API: POST /candidatures (offre_id, nom, email, CV)
    API->>DB: Vérifier offre active
    DB-->>API: offre active
    API->>Storage: Upload CV → chemin sécurisé
    Storage-->>API: URL/chemin
    API->>DB: Créer candidature (statut 'recu')
    DB-->>API: candidature_id
    API->>Queue: Ajouter job parsing (candidature_id, chemin)
    API->>Email: Envoyer accusé réception (asynchrone, optionnel via queue)
    API-->>FrontPub: 201 Created (confirmation)
    FrontPub-->>Candidat: Page "Merci, votre candidature a bien été envoyée"
```

---

### Flux F2 – Parsing & scoring (worker → extraction → alerte)

```mermaid
sequenceDiagram
    participant Queue as Redis (queue)
    participant Worker as Worker Python
    participant Storage as S3
    participant DB as PostgreSQL
    participant Email as Service email

    Queue->>Worker: Job parsing (candidature_id, chemin)
    Worker->>Storage: Télécharger CV
    Storage-->>Worker: fichier
    Worker->>Worker: Extraire texte (pdfplumber/docx2txt)
    Worker->>Worker: Extraire nom, email, compétences, années, formation
    Worker->>DB: Mettre à jour extraction_cv (statut='success', données)
    Worker->>DB: Déclencher scoring (lecture pondérations offre)
    DB-->>Worker: score_global et scores_detail
    Worker->>DB: Mettre à jour candidature (score_global, scores_detail)
    Worker->>DB: Lire seuil_alerte de l'offre
    alt score >= seuil_alerte ET alerte_envoyee = false
        Worker->>Email: Envoyer email alerte recruteur
        Worker->>DB: Mettre à jour alerte_envoyee = true
    end
    Worker->>DB: Mettre à jour job_parsing (statut='success')
```

---

### Flux F3 – Recruteur consulte le pipeline Kanban

```mermaid
sequenceDiagram
    participant Recruteur
    participant FrontRec as Frontend React
    participant API as FastAPI
    participant DB as PostgreSQL

    Recruteur->>FrontRec: Sélectionne une offre
    FrontRec->>API: GET /candidatures?offre_id=X&etape=*
    API->>DB: SELECT * FROM candidature WHERE offre_id=X ORDER BY date_depot
    DB-->>API: Liste candidatures (avec scores, extractions)
    API-->>FrontRec: JSON (candidatures par étape)
    FrontRec-->>Recruteur: Affichage 6 colonnes, cartes (nom, score)
```

---

### Flux F4 – Drag & drop (changement d’étape)

```mermaid
sequenceDiagram
    participant Recruteur
    participant FrontRec as Frontend React
    participant API as FastAPI
    participant DB as PostgreSQL
    participant Queue as Redis (optionnel email auto V2)

    Recruteur->>FrontRec: Déplace carte (colonne A → colonne B)
    FrontRec->>API: PATCH /candidatures/{id}/etape (nouvel_etape)
    API->>DB: Mettre à jour statut_etape
    API->>DB: Insérer historique_action (ancienne_valeur, nouvelle_valeur, utilisateur_id)
    DB-->>API: OK
    alt Envoi email automatique activé (V2)
        API->>Queue: Job email (changement étape)
    end
    API-->>FrontRec: 200 OK
    FrontRec-->>Recruteur: Carte déplacée visuellement
```

---

### Flux F5 – Envoi manuel d’email depuis la fiche candidat

```mermaid
sequenceDiagram
    participant Recruteur
    participant FrontRec as Frontend React
    participant API as FastAPI
    participant DB as PostgreSQL
    participant Queue as Redis
    participant Worker as Worker email
    participant SMTP as Service email

    Recruteur->>FrontRec: Clique "Envoyer email", choisit template, personnalise
    FrontRec->>API: POST /candidatures/{id}/send-email (template_id, sujet, corps)
    API->>DB: Récupérer email candidat, nom, offre titre
    API->>Queue: Ajouter job email (destinataire, sujet, corps, candidature_id, utilisateur_id)
    API-->>FrontRec: 202 Accepted (email en file)
    FrontRec-->>Recruteur: "Email en cours d'envoi"

    Queue->>Worker: Job email
    Worker->>SMTP: Envoyer email
    SMTP-->>Worker: succès/échec
    Worker->>DB: Insérer envoi_email (statut, objet_envoye, date)
```

---

### Synthèse des endpoints API correspondants (extrait)

| Flux | Méthode | Endpoint | Description |
|------|---------|----------|-------------|
| F1 | POST | `/candidatures` | Dépôt candidature |
| F2 | (interne) | – | Déclenché par queue |
| F3 | GET | `/candidatures?offre_id=` | Liste candidatures d’une offre |
| F4 | PATCH | `/candidatures/{id}/etape` | Changement d’étape |
| F5 | POST | `/candidatures/{id}/send-email` | Envoi manuel email |

**Ces diagrammes de séquence constituent le contrat technique entre le frontend, l’API, les workers et les services externes. Ils seront utilisés pour implémenter les routes et les tâches asynchrones.**

---
Voici la rédaction de la **sous‑étape 2.5 – Sécurité & RGPD** pour l’étape 4.

---

## 2.5. Sécurité & RGPD

**Objectif** : Définir les mesures techniques et organisationnelles pour protéger les données personnelles des candidats et des recruteurs, et garantir la conformité au Règlement Général sur la Protection des Données (RGPD).

**Méthode** : On liste les principes de sécurité (authentification, autorisation, chiffrement, traçabilité) et les exigences RGPD (consentement, droit à l’oubli, minimisation, hébergement, audits).

---

### 2.5.1. Principes généraux de sécurité

| Principe | Mise en œuvre dans l’ATS |
|----------|---------------------------|
| **Authentification forte** | – Mot de passe hashé (bcrypt, coût 12).<br> – Session via JWT stocké en cookie HttpOnly (Secure, SameSite=Lax).<br> – Possibilité d’ajouter 2FA en V2. |
| **Autorisation** | – Contrôle d’accès basé sur les rôles (RBAC) : recruteur (accès à ses offres/candidatures) et admin (support).<br> – Vérification à chaque endpoint (middleware FastAPI). |
| **Chiffrement des données** | – HTTPS obligatoire (TLS 1.2+) pour toutes les communications (front, API, workers).<br> – Chiffrement des CV au repos (optionnel MVP mais recommandé : SSE‑S3 ou LUKS). |
| **Protection des CV** | – Stockage hors du dossier public.<br> – Accès uniquement via URLs signées (expiration 1 heure).<br> – Pas d’indexation directe. |
| **Journalisation (logs)** | – Logs d’accès aux CV (qui, quand, quelle candidature).<br> – Logs des actions sensibles (changement étape, suppression, export).<br> – Conservation 6 mois, puis rotation. |
| **Rate limiting** | – Endpoint public de dépôt candidature : max 5 tentatives par heure par IP.<br> – Endpoints authentifiés : max 100 requêtes/minute par utilisateur. |

---

### 2.5.2. Conformité RGPD – Exigences et mise en œuvre

| Exigence RGPD | Implémentation dans l’ATS |
|---------------|----------------------------|
| **Consentement explicite** | – Case à cocher obligatoire sur le formulaire public, avec texte clair : « J’accepte que mes données (nom, email, CV) soient utilisées par [Nom Société] dans le cadre de ce recrutement. Je peux demander leur suppression à tout moment. »<br> – Enregistrement du consentement (booléen + date) dans `candidature.consentement` et `candidature.date_consentement`. |
| **Droit d’accès** | – Un candidat peut contacter le responsable (email dédié). Un endpoint API (authentifié par lien magique) peut être développé en V2.<br> – En MVP, le recruteur doit pouvoir fournir une copie des données sur demande (export CSV individuel). |
| **Droit à l’oubli (suppression)** | – Possibilité pour le recruteur de supprimer physiquement une candidature (via interface).<br> – Suppression en cascade : `candidature`, `cv_fichier`, `extraction_cv`, `job_parsing`, `historique_action`, `note_interne`, `envoi_email`.<br> – Conservation d’une trace anonyme (ex: `nom_candidat = 'ANONYMISE'`) si nécessaire. |
| **Minimisation des données** | – Ne collecter que le strict nécessaire : nom, email, CV, IP (pour anti‑spam). Pas de date de naissance, adresse postale, etc.<br> – Les données extraites (compétences, expérience) sont stockées mais ne sont pas personnelles en soi. |
| **Hébergement en France / UE** | – Choix d’un hébergeur avec des serveurs en France ou dans l’UE (ex: Scaleway, OVH, AWS eu-west-3).<br> – Contrat sous-traitant (art. 28 RGPD) signé avec l’hébergeur. |
| **Sécurité par défaut** | – Pseudonymisation possible (mais pas obligatoire en MVP).<br> – Durée de conservation : 2 ans après dernière action, puis anonymisation ou suppression automatique (batch mensuel). |
| **Notification de violation** | – Procédure interne pour notifier la CNIL et les personnes concernées sous 72h (à documenter). |
| **Registre des traitements** | – Tenir un registre (fichier Excel ou outil) listant les traitements (recrutement, analyse IA, communication). |

---

### 2.5.3. Mesures spécifiques à l’IA (parsing)

- **Pas d’envoi des CV à une API externe** (OpenAI, Google Vision) pour respecter le RGPD et la confidentialité.
- **Modèles d’IA locaux** (spaCy, regex) : exécutés dans le worker Python, aucune donnée ne quitte le serveur.
- **Anonymisation des logs** : les logs ne contiennent jamais le texte intégral du CV, uniquement des métadonnées (taille, temps de parsing, succès/échec).

---

### 2.5.4. Schéma des flux sécurisés (simplifié)

```mermaid
flowchart TB
    subgraph Candidat
        C[Utilisateur]
    end
    subgraph Frontend
        FP[Page publique]
    end
    subgraph Backend sécurisé
        API[FastAPI]
        DB[(PostgreSQL)]
        S3[(S3 - chiffré)]
        W[Worker]
    end
    subgraph Logs
        LOG[Logs centralisés]
    end

    C -->|HTTPS| FP
    FP -->|TLS| API
    API -->|JWT / RBAC| DB
    API -->|URL signée| S3
    W -->|lecture CV| S3
    W -->|écriture extraction| DB
    API -->|logs action| LOG
    W -->|logs technique| LOG
```

---

### 2.5.5. Checklist de conformité (à valider avant mise en production)

- [ ] Un avocat ou DPO a relu la politique de confidentialité et les mentions légales.
- [ ] La case de consentement est active et enregistrée en base.
- [ ] Les URLs de téléchargement des CV expirent automatiquement.
- [ ] Les logs ne contiennent pas de données personnelles superflues.
- [ ] Une procédure de demande de suppression est documentée et accessible.
- [ ] L’hébergeur est situé dans l’UE et propose un engagement de sous-traitant.

**Ces mesures garantissent un niveau de sécurité suffisant pour un MVP tout en respectant les obligations RGPD.**

---
Voici la rédaction de la **sous‑étape 2.6 – Anticiper la scalabilité et la performance** pour l’étape 4.

---

## 2.6. Anticiper la scalabilité et la performance

**Objectif** : Identifier les goulots d’étranglement potentiels du MVP (parsing, base de données, stockage) et proposer des évolutions simples pour passer à l’échelle (volume de candidatures, nombre de recruteurs) sans tout refaire.

**Méthode** : On analyse chaque composant, on fixe des ordres de grandeur cibles pour le MVP, et on propose des leviers d’optimisation (verticale puis horizontale) pour la V2.

---

### 2.6.1. Hypothèses de charge pour le MVP

| Indicateur | Valeur cible MVP | Seuil de déclenchement V2 |
|------------|------------------|---------------------------|
| Offres actives simultanées | ≤ 50 | > 200 |
| Candidatures par offre | ≤ 500 | > 2 000 |
| Candidatures totales | ≤ 10 000 | > 50 000 |
| Parsing de CV simultanés (pic) | ≤ 10 / minute | > 50 / minute |
| Recruteurs simultanés | ≤ 20 | > 100 |

Le MVP doit tenir ces volumes sans dégradation notable (< 2 s pour l’affichage du pipeline, parsing < 30 s par CV).

---

### 2.6.2. Composants critiques et leviers d’évolution

| Composant | Risque de goulot | MVP (simple) | V2 (scalable) |
|-----------|------------------|--------------|----------------|
| **Base de données (PostgreSQL)** | Requêtes lourdes sur `candidature` (filtres, tris, jointures) | – Index simples (déjà listés)<br> – Pagination sur l’API (limite 50 par page) | – Partitionnement par `offre_id` ou par date<br> – Réplication lecture (1 primaire + réplicas)<br> – Cache Redis des scores fréquents |
| **API backend (FastAPI)** | CPU ou I/O saturé | – Un seul processus (Uvicorn) avec workers Gunicorn (2-4)<br> – Rate limiting | – Horizontal scaling : plusieurs conteneurs derrière un load balancer (NLB/ALB)<br> – Mise en cache des endpoints GET (Redis) |
| **Worker parsing** | Temps de traitement long (30s/CV), accumulation | – Un seul worker (consomme la file)<br> – Timeout 30s, 3 tentatives | – Plusieurs workers en parallèle (configurable)<br> – Auto‑scaling selon longueur de queue (KEDA ou similaire) |
| **File d’attente (Redis)** | Taille de mémoire, persistance | – Redis en mémoire seule, sans persistance (reprise sur restart perdue) | – Redis cluster ou Redis avec persistance RDB/AOF<br> – Surveillance mémoire |
| **Stockage CV (S3)** | Débit en téléchargement | – URLs signées, pas de contrainte forte | – CDN devant S3 pour les zones géo-distantes<br> – Lifecycle : déplacer vers Glacier après 6 mois |
| **Service email** | API tierce rate‑limit | – File d’attente dédiée, réessais<br> – Monitoring des rejets | – Plusieurs fournisseurs en failover |

---

### 2.6.3. Optimisations spécifiques pour le pipeline Kanban

- **Requête pipeline** : pour éviter N requêtes (une par colonne), faire une seule requête groupant les candidatures par `statut_etape` et les compter.
- **Index composites** : `(offre_id, statut_etape, score_global)` pour les tris et filtres courants.
- **Pagination virtuelle** : ne charger que les 100 premières cartes par colonne (avec scroll infini en V2).

---

### 2.6.4. Monitoring des performances (MVP)

| Métrique | Outil / Méthode | Seuil d’alerte |
|----------|----------------|----------------|
| Temps de réponse API (P95) | Middleware FastAPI + log | > 1 s |
| Longueur de la file d’attente parsing | Redis `LLEN` | > 100 jobs |
| CPU / mémoire du worker | Docker stats, CloudWatch | > 80 % |
| Temps d’extraction CV (moyenne) | Log worker | > 45 s |

Ces métriques seront consultables via un tableau de bord simple (ex: UptimeRobot + custom checks) ou via l’hébergeur (Railway fournit des graphes basiques).

---

### 2.6.5. Évolution vers la V2 (feuille de route technique)

| Étape | Action | Bénéfice |
|-------|--------|----------|
| **V2.1** | Mettre en cache les offres actives (Redis) | Réduit la charge DB sur les pages publiques |
| **V2.2** | Passer à un cluster PostgreSQL (réplica lecture) | Permet d’isoler les exports et rapports |
| **V2.3** | Auto‑scaling des workers (basé sur longueur queue) | Absorbe les pics de candidatures |
| **V2.4** | Introduire un CDN pour les CV (CloudFront) | Accélère téléchargement pour les recruteurs distants |

**Conclusion** : Le MVP est conçu pour tenir une charge modérée (10k candidatures) sans modification. Les points d’attention sont documentés pour que l’équipe puisse réagir rapidement si la croissance dépasse les prévisions.

---

**L’étape 4 (Architecture technique) est désormais complète avec toutes ses sous‑étapes (2.1 à 2.6).**
Voici le **plan pour l’étape 5 – Plan de déploiement (stratégie Git, environnements, CI/CD)**.

L’objectif est de définir comment le code est versionné, comment les environnements (local, staging, production) sont organisés, et comment l’intégration et le déploiement continus (CI/CD) sont mis en œuvre.

---

# Plan d’exécution – Étape 5 : Plan de déploiement

## 1. Objectif de l’étape
- Définir la **stratégie de gestion de code source** (branches, conventions de commit, revues).
- Décrire les **environnements cibles** (développement, test, staging, production) et leurs configurations.
- Mettre en place une **chaîne CI/CD** automatisée (tests, build, déploiement) pour garantir la qualité et la rapidité de livraison.

## 2. Démarche en 5 sous‑étapes

### 2.1. Stratégie de gestion du code source (Git)
- Choix du dépôt unique (monorepo) ou multiples (polyrepo).
- Modèle de branches (Git Flow, GitHub Flow, Trunk‑based).
- Règles de nommage des branches (`feature/`, `fix/`, `chore/`).
- Protection des branches principales (ex: `main`, `develop`).
- Politique de commits (conventionnelle ou libre).

### 2.2. Environnements et leur configuration
- **Local** : machine du développeur, Docker Compose, données fictives.
- **Test / CI** : environnement éphémère lancé par GitHub Actions.
- **Staging** : environnement pré‑production (données anonymisées, similaire à la production).
- **Production** : environnement réel (données clients, haute disponibilité).
- Gestion des variables d’environnement / secrets (fichiers `.env`, gestionnaires de secrets).

### 2.3. Intégration continue (CI)
- Déclencheurs : `push` sur toutes les branches, `pull_request`.
- Jobs à exécuter :
  - Linting (ESLint, Prettier, flake8, black)
  - Tests unitaires (front et back)
  - Tests d’intégration (API avec base de données de test)
  - Build des images Docker (vérification)
- Publication des artefacts (logs, rapports de test).

### 2.4. Déploiement continu (CD)
- **Déploiement automatique sur staging** à chaque `push` sur `develop`.
- **Déploiement manuel sur production** (via tag ou confirmation) à partir de `main`.
- Outils : GitHub Actions, Vercel (frontend), Railway / AWS (backend).
- Gestion des migrations de base de données (exécutées avant le déploiement du backend).

### 2.5. Stratégie de rollback et de monitoring
- Procédure de rollback (annulation du dernier déploiement, restauration d’un tag).
- Monitoring de l’état des déploiements (slack, email).
- Vérification post‑déploiement (sondes de santé).

## 3. Livrables de l’étape 5

| Livrable | Format | Description |
|----------|--------|-------------|
| **Schéma des branches Git** | Mermaid / texte | Arborescence et flux de travail |
| **Tableau des environnements** | Markdown | URL, variables, données, accès |
| **Workflow CI/CD (ex: GitHub Actions)** | Fichier YAML (exemple) | Pipeline complet (lint, test, build, deploy) |
| **Procédure de gestion des secrets** | Texte | Où et comment stocker les variables sensibles |
| **Checklist de déploiement** | Liste | Actions manuelles avant mise en production |

## 4. Prochaine action concrète

**Souhaitez-vous que je commence à rédiger les sous‑étapes de l’étape 5 (par exemple 2.1 Stratégie Git) ou que je passe directement à l’étape 6 (Organisation du travail local vs prod) ?**

---

Voici la rédaction de la **sous‑étape 1 – Objectif de l’étape** pour le plan de déploiement.

---

## 1. Objectif de l’étape

L’objectif de l’étape **« Plan de déploiement (stratégie Git, environnements, CI/CD) »** est de définir l’ensemble des pratiques, des outils et des flux de travail qui permettront de gérer le code source, de tester les évolutions, et de livrer les nouvelles versions de l’ATS de manière fiable, automatisée et sécurisée.

Cet objectif se décline en trois axes principaux :

### 1.1. Définir la stratégie de gestion du code source

- **Branches** : choisir un modèle adapté à la taille de l’équipe (Git Flow simplifié, GitHub Flow, ou Trunk‑based) et définir les branches protégées (`main`, `develop`).
- **Conventions de commits** : adopter une norme lisible (ex: [Conventional Commits](https://www.conventionalcommits.org/)) pour faciliter la génération automatique des logs et des versions.
- **Revues de code** : imposer des pull requests avec validation par au moins un autre développeur avant fusion sur les branches principales.

### 1.2. Décrire les environnements cibles et leurs configurations

- **Environnement de développement local** : poste du développeur (Docker Compose, base de données locale, service de fichiers factice).
- **Environnement de test / intégration** : serveur éphémère lancé par la CI, avec données de test isolées.
- **Environnement de staging (pré‑production)** : réplique de la production, avec données anonymisées, destinée aux tests fonctionnels et à la validation par l’équipe.
- **Environnement de production** : serveurs réels hébergeant l’application pour les utilisateurs finaux, avec redondance, sauvegardes et monitoring.

Pour chaque environnement, on précisera :
- L’URL d’accès,
- Les variables d’environnement (base de données, clés API, secrets),
- Les droits d’accès,
- La politique de mise à jour.

### 1.3. Mettre en place une chaîne CI/CD automatisée

- **Intégration continue (CI)** : automatiser l’exécution des tests (linting, tests unitaires, tests d’intégration) à chaque `push` et `pull request`, afin de détecter les régressions au plus tôt.
- **Déploiement continu (CD)** : automatiser le déploiement sur l’environnement de staging à chaque fusion sur `develop`, et proposer un déploiement semi‑automatique (déclenché par tag ou bouton) vers la production.
- **Gestion des migrations** : exécuter automatiquement les scripts de migration de base de données avant le déploiement du backend, avec possibilité de rollback.
- **Surveillance post‑déploiement** : vérifier la santé des services (sondes HTTP) et notifier l’équipe en cas d’échec.

**En résumé** : cette étape doit produire un ensemble de règles, de fichiers de configuration (ex: `.github/workflows/ci-cd.yml`, `docker-compose.yml`, scripts de migration) et de documentation qui permettront à l’équipe de livrer des fonctionnalités rapidement et en toute confiance, dès le MVP.

---
Voici la rédaction de la **sous‑étape 2.1 – Stratégie de gestion du code source (Git)** pour l’étape 5.

---

## 2. Démarche en 5 sous‑étapes

### 2.1. Stratégie de gestion du code source (Git)

**Objectif** : Définir comment le code source est organisé, versionné, et collaboratif, afin de garantir la traçabilité, la qualité et la fluidité des livraisons.

#### 2.1.1. Choix du dépôt : monorepo

**Décision** : Un **dépôt unique (monorepo)** contenant tous les composants (frontend, backend, workers, scripts d’infrastructure).

| Option | Avantages | Inconvénients | Décision |
|--------|-----------|---------------|----------|
| **Monorepo** | – Cohérence des versions<br>– Réutilisation facile de code commun (types, utilitaires)<br>– Atomicité des commits (front+back)<br>– Une seule CI/CD à configurer | – Dépôt plus volumineux<br>– Nécessite des outils de build sélectifs | **Choisi** |
| Polyrepo | Isolation, scaling d’équipes | Complexité de synchronisation, duplication | Non retenu |

**Structure du monorepo** (proposée) :

```
ats-platform/
├── .github/
│   └── workflows/          # CI/CD (GitHub Actions)
├── front/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── ...
├── backend/
│   ├── app/
│   ├── tests/
│   ├── migrations/         # Alembic
│   ├── requirements.txt
│   └── Dockerfile
├── workers/
│   ├── parsing_worker.py
│   ├── email_worker.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml      # environnement local
├── .env.example
└── README.md
```

#### 2.1.2. Modèle de branches (Git Flow simplifié)

Pour une petite équipe (2‑5 développeurs), on adopte un **Git Flow allégé** :

| Branche | Rôle | Protection | Durée de vie |
|---------|------|------------|---------------|
| `main` | Code de production (toujours déployable) | Protégée : pas de push direct, uniquement via PR | Éternelle |
| `develop` | Intégration continue, pré‑production | Protégée : PR obligatoire | Éternelle |
| `feature/*` | Développement d’une nouvelle fonctionnalité | Non protégée | Supprimée après fusion dans `develop` |
| `hotfix/*` | Correction urgente sur `main` | Non protégée | Supprimée après fusion dans `main` et `develop` |
| `release/*` | Préparation d’une version (facultatif MVP) | Non protégée | Supprimée après fusion |

**Flux de travail** :
1. Créer une branche `feature/ma-fonctionnalite` depuis `develop`.
2. Développer, committer, pousser.
3. Ouvrir une **Pull Request (PR)** vers `develop`.
4. Passer la revue de code + tests CI.
5. Fusionner (squash merge recommandé pour garder l’historique propre).
6. (Occasionnellement) créer une branche `release/vX.Y.Z` depuis `develop` pour ajuster la version, puis fusionner dans `main` et `develop`.
7. Pour les correctifs urgents : `hotfix/description` depuis `main`, puis PR vers `main` **et** `develop`.

#### 2.1.3. Règles de nommage des branches

Les noms de branches doivent être explicites et suivre une convention :

| Type | Format | Exemple |
|------|--------|---------|
| Fonctionnalité | `feature/[courte-description]` | `feature/gestion-offres` |
| Correction de bug | `fix/[description]` | `fix/drag-drop-pipeline` |
| Correctif urgent | `hotfix/[description]` | `hotfix/upload-cv-broken` |
| Tâche non fonctionnelle | `chore/[description]` | `chore/mise-a-jour-deps` |
| Version | `release/[version]` | `release/v1.0.0` |

Utiliser des **tirets** pour séparer les mots, pas d’underscores. Maximum 50 caractères.

#### 2.1.4. Protection des branches principales

Via les réglages GitHub (ou GitLab) :

- **`main`** :
  - Exiger une PR avec au moins 1 approbation.
  - Exiger la réussite de tous les statuts CI (lint, tests unitaires, tests d’intégration).
  - Interdire le push direct.
  - Exiger que la branche soit à jour avec `main` avant fusion.
- **`develop`** :
  - Exiger une PR (sans revue obligatoire en première version, mais recommandée).
  - Exiger la réussite de la CI (au moins lint + tests unitaires).
  - Interdire le push direct.

#### 2.1.5. Politique de commits (Conventional Commits)

Pour faciliter la génération automatique du changelog et le versionnage sémantique, on impose le format **Conventional Commits** :

```
<type>(<scope> optionnel): <description>

[corps optionnel]

[footer optionnel]
```

**Types autorisés** :

| Type | Usage |
|------|-------|
| `feat` | Nouvelle fonctionnalité (→ incrément mineur de version) |
| `fix` | Correction de bug (→ incrément de correctif) |
| `docs` | Modification de documentation |
| `style` | Formatage, point‑virgule, etc. (pas de changement logique) |
| `refactor` | Refactorisation (ni fonctionnalité, ni correction) |
| `perf` | Amélioration de performance |
| `test` | Ajout ou correction de tests |
| `chore` | Mise à jour de dépendances, configuration |

**Exemples** :
- `feat(offre): ajout de l'URL publique générée automatiquement`
- `fix(parsing): gestion des fichiers DOCX corrompus`
- `docs(readme): mise à jour des instructions d'installation`

**Obligation** : chaque commit sur une branche de fonctionnalité doit respecter ce format (vérifié par un hook Git ou par la CI en lint des messages).

#### 2.1.6. Outillage associé

- **Husky** (front) / **pre-commit** (back) : linters automatiques avant chaque commit.
- **Commitlint** : valide le format des messages de commit.
- **GitHub Actions** : exécute la CI à chaque `push` et `pull_request`.

**Cette stratégie garantit un historique propre, des révisions faciles, et une livraison automatisée sans friction.**

---
Voici la rédaction de la **sous‑étape 2.2 – Environnements et leur configuration** pour l’étape 5.

---

## 2.2. Environnements et leur configuration

**Objectif** : Définir les différents environnements nécessaires au cycle de vie du logiciel, leurs caractéristiques (matériel, données, accès), et la manière dont les variables de configuration (notamment les secrets) sont gérées.

---

### 2.2.1. Tableau récapitulatif des environnements

| Environnement | Usage | Hébergement | Données | Accès | Mise à jour |
|---------------|-------|-------------|---------|-------|--------------|
| **Local** | Développement, tests unitaires | Machine du développeur (Docker Compose) | Données fictives (fixtures) | Développeur uniquement | Manuelle (docker compose up) |
| **Test / CI** | Exécution des tests automatisés | GitHub Actions (conteneurs éphémères) | Base de données temporaire (créée/détruite pour chaque run) | Système CI | Automatique (à chaque push) |
| **Staging** | Validation fonctionnelle, tests d’intégration, recette interne | Serveur dédié (Railway / AWS / VPS) | Données anonymisées (copie de prod sans informations personnelles) | Équipe projet, recruteurs tests | Automatique (sur push develop) |
| **Production** | Utilisation réelle par les clients | Infrastructure redondante (Vercel + AWS / Railway Pro) | Données réelles (RGPD) | Recruteurs clients | Manuelle (déclenchée par tag) |

---

### 2.2.2. Environnement local (développement)

**Composition** : un fichier `docker-compose.yml` lançant tous les services nécessaires.

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: ats_dev
      POSTGRES_USER: ats
      POSTGRES_PASSWORD: devpass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://ats:devpass@postgres:5432/ats_dev
      REDIS_URL: redis://redis:6379
      AWS_S3_BUCKET: local-bucket
      # Autres variables...

  worker_parsing:
    build: ./workers
    command: python parsing_worker.py
    depends_on:
      - postgres
      - redis
    environment:
      <<: *backend-env

volumes:
  postgres_data:
```

**Données fictives** :
- Script de seed (`backend/scripts/seed.py`) générant 2 offres, 20 candidatures fictives, scores aléatoires.
- Les CV sont des fichiers factices (texte ou faux PDF).

**Configuration** : fichier `.env` (non versionné) pour les secrets locaux (clés API mockées). Un fichier `.env.example` est versionné.

---

### 2.2.3. Environnement Test / CI (GitHub Actions)

**Caractéristiques** :
- Lancé à chaque `push` et `pull request`.
- Utilise des conteneurs (PostgreSQL, Redis) via `services` dans GitHub Actions.
- Base de données créée, migrations exécutées, puis détruite à la fin du workflow.
- Aucune persistance des données.

**Exemple de workflow (extrait)** :
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
      redis:
        image: redis:7
    steps:
      - uses: actions/checkout@v4
      - name: Run backend tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest tests/
        env:
          DATABASE_URL: postgresql://postgres:testpass@localhost:5432/postgres
          REDIS_URL: redis://localhost:6379
```

**Variables d’environnement** : stockées dans les secrets GitHub (pour les clés d’API externes mockées en CI, mais réelles pour les tests d’intégration).

---

### 2.2.4. Environnement Staging (pré‑production)

**Objectif** : reproduire la production au plus près, sans risque pour les données réelles.

**Hébergement** (recommandation) : Railway.app ou un VPS (Scaleway, OVH) avec :
- Base de données PostgreSQL (instance séparée)
- Redis (instance séparée)
- Backend (conteneur unique ou plusieurs workers)
- Stockage S3 (bucket staging)

**Données** :
- Copie de la base de production (journalière ou hebdomadaire) **anonymisée**.
- Anonymisation : remplacement des `nom_candidat`, `email` par des valeurs génériques (`Candidat_123`), suppression des IP, effacement des CV réels (remplacés par des fichiers factices).
- Les offres peuvent être conservées (non sensibles).

**Accès** : restreint aux membres de l’équipe (authentification HTTP basic en plus de l’authentification applicative, ou VPN).

**Configuration** : variables d’environnement définies dans la plateforme d’hébergement (Railway / AWS Secrets Manager). Pas de fichier `.env` sur le serveur.

---

### 2.2.5. Environnement Production

**Exigences** :
- Haute disponibilité (99,5 % minimum).
- Redondance : au moins 2 instances du backend (derrière un load balancer), base de données gérée (RDS avec failover automatique).
- Sauvegardes automatiques quotidiennes (base + CV).
- Monitoring (uptime, erreurs, performance).

**Hébergement** (recommandation) :
- Frontend : Vercel (gratuit ou pro selon volume).
- Backend : AWS (ECS Fargate ou EC2) ou Railway Pro (simplifié).
- Base de données : AWS RDS PostgreSQL (multi-AZ) ou Railway PostgreSQL.
- Stockage CV : AWS S3 (bucket production, versioning activé).
- File d’attente : Redis (AWS ElastiCache ou Railway Redis).

**Accès** : réservé aux recruteurs clients via l’interface web classique. L’accès administrateur se fait via des comptes spécifiques.

**Configuration** : toutes les variables sensibles sont stockées dans un gestionnaire de secrets (AWS Secrets Manager, GitHub Secrets pour la CI/CD, ou Railway’s native secrets). Les secrets ne sont jamais exposés dans le code.

---

### 2.2.6. Gestion des variables d’environnement et secrets

| Environnement | Où sont stockées les variables ? | Accès |
|---------------|----------------------------------|-------|
| **Local** | Fichier `.env` (ignoré par Git) | Développeur |
| **Test / CI** | Secrets GitHub (Settings > Secrets) | GitHub Actions |
| **Staging** | Secrets de la plateforme d’hébergement (ex: Railway / AWS Secrets Manager) | Équipe technique |
| **Production** | Secrets de la plateforme (ex: AWS Secrets Manager) + sauvegarde chiffrée | Administrateurs |

**Liste des secrets nécessaires** (exemples) :

| Nom | Description | Local (mock) | Prod (réel) |
|-----|-------------|--------------|--------------|
| `DATABASE_URL` | Connexion PostgreSQL | postgresql://ats:devpass@localhost:5432/ats_dev | URL réelle avec mot de passe |
| `REDIS_URL` | Connexion Redis | redis://localhost:6379 | URL réelle |
| `AWS_ACCESS_KEY_ID` | Accès S3 | clé factice (minio) | clé IAM réelle |
| `AWS_SECRET_ACCESS_KEY` | Accès S3 | clé factice | clé réelle |
| `SENDGRID_API_KEY` (ou SES) | Envoi emails | clé mock (désactivée) | clé réelle |
| `JWT_SECRET` | Signature JWT | secret_dev | secret aléatoire fort |
| `FRONTEND_URL` | URL publique | http://localhost:3000 | https://ats.exemple.com |

**Recommandations** :
- Ne jamais versionner les fichiers `.env`.
- Utiliser un outil comme `direnv` ou `dotenv` pour charger automatiquement les variables en local.
- En production, faire tourner un script de vérification au démarrage du backend pour s’assurer que tous les secrets requis sont présents.

---

**Cette configuration permet un workflow de développement fluide, des tests fiables, et une mise en production sécurisée.**

---

Voici la rédaction de la **sous‑étape 2.3 – Intégration continue (CI)** pour l’étape 5.

---

## 2.3. Intégration continue (CI)

**Objectif** : Automatiser l’exécution des vérifications et des tests à chaque modification du code, afin de détecter rapidement les erreurs, maintenir la qualité et éviter les régressions.

### 2.3.1. Déclencheurs (triggers)

La pipeline CI se déclenche automatiquement sur les événements suivants :

| Événement | Branches concernées | Objectif |
|-----------|---------------------|----------|
| `push` | Toutes les branches (sauf `main` si protégée) | Vérifier les commits intermédiaires |
| `pull_request` | Vers `develop` ou `main` | Valider les modifications avant fusion |

**Option** : On peut également déclencher la CI sur `schedule` (ex: une fois par jour) pour détecter des vulnérabilités, mais non nécessaire pour le MVP.

### 2.3.2. Jobs à exécuter

La pipeline CI se compose de plusieurs jobs, exécutés en parallèle lorsque c’est possible, afin d’accélérer le feedback.

#### Job 1 : Linting (vérification du style et de la syntaxe)

| Technologie | Commande | Objectif |
|-------------|----------|----------|
| **Frontend (React)** | `npm run lint` (ESLint) + `npm run format:check` (Prettier) | Vérifier les règles de codage et le formatage |
| **Backend (Python)** | `flake8 app/` + `black --check app/` + `isort --check-only app/` | Cohérence PEP 8, formatage auto |

Le job échoue si des erreurs sont détectées. Un rapport de linting peut être publié (optionnel).

#### Job 2 : Tests unitaires (frontend et backend)

**Frontend** :
- Framework : Jest + React Testing Library.
- Commande : `npm test -- --coverage` (génère un rapport de couverture).
- Fichiers cibles : `front/src/**/*.test.js`.

**Backend** :
- Framework : pytest.
- Commande : `pytest tests/unit/ --cov=app`.
- Cible : fonctions métier isolées (sans base de données réelle, avec mocks).

Les rapports de couverture (coverage.xml, html) sont sauvegardés comme artefacts.

#### Job 3 : Tests d’intégration (API + base de données réelle)

**Objectif** : Vérifier le bon fonctionnement des endpoints API avec une base de données temporaire (PostgreSQL) et un cache Redis.

**Environnement** :
- Base de données PostgreSQL lancée dans un conteneur (via `services` de GitHub Actions).
- Redis lancé de la même façon.
- Application backend démarrée (ou tests exécutés directement avec une fixture de base de données).

**Commandes typiques** :
```bash
pytest tests/integration/ --cov=app --cov-report=xml
```

**Exemple de test** :
- Créer une offre via API → vérifier le code 201.
- Poster une candidature → vérifier que le job de parsing est en file d’attente.

Les rapports de test (JUnit XML) et de couverture sont sauvegardés comme artefacts.

#### Job 4 : Build des images Docker (vérification)

**Objectif** : S’assurer que les Dockerfiles (backend, worker, éventuellement frontend) sont valides et que l’image se construit sans erreur.

**Commandes** :
```bash
docker build -t ats-backend:test ./backend
docker build -t ats-worker:test ./workers
```

**Optionnel** : Pousser les images vers un registre (Docker Hub, GitHub Container Registry) uniquement pour la branche `develop` ou `main` (cela peut être déplacé dans la partie CD).

#### Job 5 : Publication des artefacts (logs, rapports)

Les artefacts suivants sont sauvegardés (durée de conservation : 7 jours) :

| Artefact | Contenu | Utilisation |
|----------|---------|--------------|
| `test-reports-front` | Rapports Jest (JSON, HTML) | Analyse des tests frontend |
| `test-reports-back` | Rapports pytest (JUnit XML, HTML) | Analyse des tests backend |
| `coverage-front` | Couverture de code (lcov, html) | Suivi de la qualité |
| `coverage-back` | Couverture pytest (XML, HTML) | Suivi de la qualité |
| `docker-build-logs` | Logs de build Docker | Débogage en cas d’échec |

### 2.3.3. Exemple de workflow GitHub Actions (fichier `.github/workflows/ci.yml`)

```yaml
name: CI

on:
  push:
    branches: [ '**' ]  # toutes les branches
  pull_request:
    branches: [ develop, main ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: cd front && npm ci
      - run: cd front && npm run lint
      - run: cd front && npm run format:check
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install flake8 black isort
      - run: flake8 backend/
      - run: black --check backend/
      - run: isort --check-only backend/

  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Frontend unit tests
        run: cd front && npm ci && npm test -- --coverage
      - name: Backend unit tests
        run: cd backend && pip install -r requirements.txt && pytest tests/unit --cov=app
      - name: Upload coverage reports
        uses: actions/upload-artifact@v4
        with:
          name: coverage-reports
          path: |
            front/coverage
            backend/htmlcov

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
    steps:
      - uses: actions/checkout@v4
      - name: Run migrations
        run: cd backend && pip install alembic && alembic upgrade head
        env:
          DATABASE_URL: postgresql://postgres:testpass@localhost:5432/postgres
      - name: Run integration tests
        run: cd backend && pytest tests/integration --cov=app --cov-report=xml
        env:
          DATABASE_URL: postgresql://postgres:testpass@localhost:5432/postgres
          REDIS_URL: redis://localhost:6379
      - name: Upload test results
        uses: actions/upload-artifact@v4
        with:
          name: integration-test-reports
          path: backend/test-reports/

  docker-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build backend image
        run: docker build -t ats-backend:ci ./backend
      - name: Build worker image
        run: docker build -t ats-worker:ci ./workers
```

### 2.3.4. Politique de succès

Pour qu’une PR puisse être fusionnée, **tous les jobs CI doivent réussir**. En cas d’échec, la fusion est bloquée (protection de branche). Les développeurs peuvent consulter les logs et les artefacts pour diagnostiquer l’erreur.

**Cette CI garantit que le code fusionné est toujours de qualité et n’introduit pas de régression majeure.**

---
Voici la rédaction de la **sous‑étape 2.4 – Déploiement continu (CD)** pour l’étape 5.

---

## 2.4. Déploiement continu (CD)

**Objectif** : Automatiser la livraison des applications (frontend, backend, workers) vers les environnements de staging et de production, avec un minimum d’intervention manuelle, tout en garantissant la sécurité et la traçabilité.

### 2.4.1. Principes généraux

| Environnement | Déclencheur | Niveau d’automatisation | Stratégie |
|---------------|-------------|------------------------|-----------|
| **Staging** | `push` sur branche `develop` | Automatique (sans intervention) | Déploiement immédiat après succès des tests CI |
| **Production** | Création d’un tag `v*` sur `main` | Semi‑automatique (déclenchement manuel via un workflow ou confirmation) | Nécessite une validation humaine (pull request + tag) |

### 2.4.2. Déploiement sur Staging (automatique)

**Objectif** : Rendre la dernière version en développement immédiatement disponible pour les tests de l’équipe.

**Composants et cibles** :

| Composant | Cible de déploiement | Méthode |
|-----------|----------------------|---------|
| Frontend (React) | Vercel (projet staging) | `vercel --prod` (via GitHub Action) |
| Backend (FastAPI) | Railway / AWS (environnement staging) | `docker build` + push image + redémarrage service |
| Workers (parsing/email) | Railway / AWS (même environnement) | Idem backend |
| Migrations BDD | Exécutées avant le backend | `alembic upgrade head` |

**Workflow CD staging** (fichier `.github/workflows/cd-staging.yml`) – déclenché sur `push` vers `develop` :

```yaml
name: CD Staging

on:
  push:
    branches: [ develop ]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4

      # Frontend (Vercel)
      - name: Deploy frontend to Vercel (staging)
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID_STAGING }}
          vercel-args: '--prod'

      # Backend & workers (Railway/AWS)
      - name: Login to Railway
        run: railway login --token ${{ secrets.RAILWAY_TOKEN }}
      - name: Deploy backend to Railway (staging)
        run: railway up --service backend --environment staging
      - name: Run migrations
        run: railway run --service backend alembic upgrade head
      - name: Deploy worker parsing
        run: railway up --service worker-parsing --environment staging
```

**Post‑déploiement** : une notification est envoyée sur Slack (ou autre canal) avec l’URL du staging et le statut.

### 2.4.3. Déploiement sur Production (semi‑automatique)

**Objectif** : Livrer une version validée et taguée en production, après validation humaine.

**Prérequis** :
- Le code doit être fusionné dans `main` via une pull request approuvée.
- Un tag sémantique (`v1.0.0`, `v1.0.1`, etc.) doit être créé sur `main`.

**Déclencheur** : Création d’un tag sur `main`.

**Workflow CD production** (fichier `.github/workflows/cd-production.yml`) :

```yaml
name: CD Production

on:
  push:
    tags:
      - 'v*'   # ex: v1.0.0, v2.1.3

jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4

      # Frontend (Vercel production)
      - name: Deploy frontend to Vercel (prod)
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID_PROD }}
          vercel-args: '--prod'

      # Backend & workers (AWS / Railway prod)
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: eu-west-3
      - name: Login to Amazon ECR
        run: aws ecr get-login-password | docker login --username AWS --password-stdin ${{ secrets.ECR_REGISTRY }}
      - name: Build and push backend image
        run: |
          docker build -t ${{ secrets.ECR_REGISTRY }}/ats-backend:${{ github.ref_name }} ./backend
          docker push ${{ secrets.ECR_REGISTRY }}/ats-backend:${{ github.ref_name }}
      - name: Update ECS service
        run: aws ecs update-service --cluster ats-prod --service backend --force-new-deployment --image ${{ secrets.ECR_REGISTRY }}/ats-backend:${{ github.ref_name }}
      - name: Run migrations (production)
        run: aws ecs run-task --cluster ats-prod --task-definition migration-task --overrides '{"containerOverrides":[{"name":"migrate","command":["alembic","upgrade","head"]}]}'
```

**Validation manuelle** : Optionnellement, on peut ajouter une étape `environment: production` qui nécessite une approbation manuelle dans GitHub Actions.

### 2.4.4. Gestion des migrations de base de données

| Environnement | Moment d’exécution | Rollback possible ? |
|---------------|--------------------|----------------------|
| Staging | Avant le déploiement du backend (dans le workflow CD) | Oui (via `alembic downgrade -1`) |
| Production | Avant le déploiement (dans un job séparé, avec vérification) | Oui, mais doit être testé au préalable en staging |

**Recommandations** :
- Les migrations doivent être **rétrocompatibles** (ajout de colonnes nullable, nouvelles tables sans suppression).
- Toujours tester la migration sur staging avant production.
- En cas d’échec de migration en production, le déploiement est interrompu.

### 2.4.5. Stratégie de rollback

| Composant | Méthode de rollback |
|-----------|---------------------|
| Frontend (Vercel) | Utiliser l’interface Vercel pour revenir à un déploiement précédent (instantané) |
| Backend (ECS / Railway) | Re-déployer l’image du tag précédent (`vX.Y.Z-1`) |
| Base de données | Exécuter `alembic downgrade -1` (nécessite d’avoir préparé le downgrade) |
| Workers | Redémarrer avec l’ancienne image Docker |

**Procédure** : un document interne décrit les étapes (moins de 5 minutes pour un rollback complet).

### 2.4.6. Monitoring post‑déploiement

Après chaque déploiement (staging ou production), un job de vérification s’exécute :

```yaml
- name: Health check
  run: |
    curl --fail --retry 3 --retry-delay 5 https://staging.ats.exemple.com/health || exit 1
```

En cas d’échec, une notification est envoyée et le déploiement est marqué comme échoué (mais pas de rollback automatique en MVP).

**Cette stratégie CD permet de livrer rapidement tout en gardant la maîtrise sur la production.**

---
Voici la rédaction de la **sous‑étape 2.5 – Stratégie de rollback et de monitoring** pour l’étape 5.

---

## 2.5. Stratégie de rollback et de monitoring

**Objectif** : Prévoir les procédures et outils permettant de revenir rapidement à un état stable en cas d’incident post‑déploiement, et de surveiller la santé des environnements (staging, production) pour détecter les anomalies.

### 2.5.1. Stratégie de rollback

#### Principes généraux

- Tout déploiement doit être **réversible** en moins de 5 minutes.
- On privilégie un **rollback applicatif** (revenir à la version précédente) plutôt qu’un rollback base de données (plus risqué).
- Les migrations de base de données doivent être **rétrocompatibles** (ex: ajout de colonne nullable, nouvelle table) pour permettre au code ancien de fonctionner sans erreur.

#### Rollback par composant

| Composant | Méthode de rollback | Délai estimé | Prérequis |
|-----------|---------------------|--------------|-----------|
| **Frontend (Vercel)** | Interface Vercel : « Revert to previous deployment » | 1 minute | Aucun (interface web) |
| **Backend (AWS ECS)** | Redéployer la tâche avec l’image Docker du tag précédent (ex: `v1.2.0` → `v1.1.0`) | 2‑3 minutes | Images taggées conservées dans ECR |
| **Workers (parsing/email)** | Même procédure que backend | 2‑3 minutes | Idem |
| **Base de données (PostgreSQL)** | Migration descendante (`alembic downgrade -1`) ou restauration d’un dump | 5‑10 minutes (dump) / 1 minute (downgrade) | Script de downgrade testé ; dumps quotidiens |

#### Procédure de rollback (production)

1. **Détection** : alerte monitoring ou signalement utilisateur.
2. **Décision** : un responsable technique autorise le rollback.
3. **Exécution** (selon le composant) :
   - Frontend : rollback via Vercel.
   - Backend : lancer le workflow GitHub Action dédié (ou commande AWS CLI) en spécifiant le tag précédent.
   - Base de données : si la migration applicative est incompatible, exécuter `alembic downgrade` après avoir arrêté le backend.
4. **Vérification** : sonder l’endpoint `/health` et exécuter un test de non‑régression rapide.
5. **Communication** : informer l’équipe (Slack, email).

**Workflow GitHub Action pour rollback backend** (exemple) :

```yaml
name: Rollback Backend Production

on:
  workflow_dispatch:
    inputs:
      target_tag:
        description: 'Tag to rollback to (ex: v1.2.0)'
        required: true

jobs:
  rollback:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy previous image to ECS
        run: |
          aws ecs update-service --cluster ats-prod --service backend \
            --task-definition ats-backend --image ${{ secrets.ECR_REGISTRY }}/ats-backend:${{ github.event.inputs.target_tag }}
```

### 2.5.2. Monitoring (surveillance)

#### Niveaux de monitoring

| Niveau | Outil | Fréquence | Seuils d’alerte |
|--------|-------|-----------|------------------|
| **Disponibilité** (uptime) | UptimeRobot / Better Uptime | Toutes les 5 minutes | 2 échecs consécutifs → alerte |
| **Performance API** | Middleware FastAPI + logs | Temps réel | P95 > 1s (alerte) |
| **File d’attente** (Redis) | Commande `LLEN` (script Python ou cron) | Toutes les minutes | Longueur > 100 jobs |
| **Erreurs applicatives** | Sentry (intégré à FastAPI) | En continu | Nouvelle erreur non ignorée → alerte |
| **Base de données** | Métriques RDS (CloudWatch) / pg_stat | 1 minute | CPU > 80%, connexions > 80% max |
| **Stockage CV** (S3) | Monitoring AWS | 5 minutes | Erreurs 4xx/5xx > 10 par heure |

#### Mise en œuvre (MVP)

- **Sentry** : ajout du SDK Python dans FastAPI pour capturer les exceptions.
- **Health endpoint** : `/health` retourne `200 OK` si base de données et Redis répondent.
- **Script de monitoring de la queue** : un petit script Python (ou worker dédié) qui envoie une alerte Slack si la queue dépasse 100.

**Exemple de fonction de health check** (FastAPI) :

```python
@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        redis_client.ping()
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=503, detail="Service unavailable")
```

#### Alertes et notifications

| Canal | Usage | Destinataires |
|-------|-------|----------------|
| Slack (canal #alerts) | Alertes automatiques (monitoring, CI/CD, rollback) | Toute l’équipe technique |
| Email (support@) | Alertes critiques (prod down) | Lead tech + responsable |
| SMS (optionnel V2) | Urgence absolue | Lead tech |

**Exemple de notification Slack** (via webhook) :

```json
{
  "text": "⚠️ *Production* - Queue parsing > 100 jobs. Action requise."
}
```

### 2.5.3. Tableau de bord simplifié (MVP)

On peut utiliser un tableau de bord basé sur **Grafana Cloud** (niveau gratuit) avec des métriques :
- Temps de réponse API (P95).
- Taux d’erreur HTTP (4xx, 5xx).
- Longueur de la file d’attente.
- Utilisation CPU/mémoire des conteneurs.

**Alternative légère** : utiliser les graphes intégrés de Railway ou AWS CloudWatch (pas de tableau de bord dédié).

### 2.5.4. Procédure d’incident (runbook)

| Étape | Action | Responsable |
|-------|--------|--------------|
| 1 | Alerte reçue (Slack / email) | On-call |
| 2 | Consulter les logs (Sentry, CloudWatch, Railway logs) | On-call |
| 3 | Diagnostiquer : problème applicatif, infrastructure ou dépendance externe | On-call |
| 4 | Appliquer la solution : correction rapide (hotfix) ou rollback | On-call + lead |
| 5 | Documenter l’incident (causes, actions, prévention) | Équipe |

**Ce plan de rollback et de monitoring assure une résilience minimale pour le MVP, tout en restant simple à mettre en œuvre.**

---

**L’étape 5 (Plan de déploiement) est maintenant complète avec toutes ses sous‑étapes (2.1 à 2.5).**

---

Voici le **plan pour l’étape 6 – Organisation du travail local vs production**.

L’objectif est de définir comment l’équipe de développement organise son travail entre l’environnement local (chaque développeur) et la production (environnement réel), en passant par les environnements intermédiaires (test, staging). On aborde les aspects de configuration, de synchronisation des données, de gestion des secrets, et les bonnes pratiques pour éviter les décalages entre les environnements.

---

# Plan d’exécution – Étape 6 : Organisation du travail local vs production

## 1. Objectif de l’étape
- Décrire le **flux de travail typique** d’un développeur (de la machine locale à la mise en production).
- Définir comment **synchroniser** les configurations, les dépendances et les données entre les environnements.
- Établir des **bonnes pratiques** pour éviter les surprises (ex: « ça marche sur ma machine »).
- Préciser les **outils** et les **scripts** facilitant la reproduction des environnements.

## 2. Démarche en 5 sous‑étapes

### 2.1. Environnement de développement local (détaillé)
- **Prérequis** : Docker, Docker Compose, Node.js (pour le front), Python (pour le back).
- **Clonage et initialisation** : `git clone`, `cp .env.example .env`.
- **Lancement** : `docker-compose up -d` pour lancer la base, Redis, backend, workers.
- **Seed de données** : script `./scripts/seed_local.sh` pour peupler avec des offres et candidatures fictives.
- **Accès** :
  - Frontend local : `http://localhost:3000`
  - API locale : `http://localhost:8000/docs`
  - PGAdmin (optionnel) : `http://localhost:5050`

### 2.2. Gestion des différences de configuration
- **Fichiers `.env`** : un fichier par environnement (`.env.local`, `.env.staging`, `.env.production`) jamais versionnés.
- **Variables différenciées** :
  - URLs (`FRONTEND_URL`, `API_URL`)
  - Niveaux de log (`DEBUG=true` en local, `false` en prod)
  - Services externes (mock en local, réel en prod)
- **Utilisation de `direnv`** (optionnel) pour charger automatiquement le bon `.env` selon le dossier.

### 2.3. Stratégie de données : développement vs production
- **Local** : données fictives (fixtures) – reproductibles, effaçables.
- **Staging** : données anonymisées issues de production (script d’anonymisation).
- **Production** : données réelles (jamais copiées en local pour des raisons RGPD).
- **Script d’anonymisation** : exemple en Python qui remplace les noms, emails, IP, supprime les CV.

### 2.4. Synchronisation des migrations et du schéma
- **Local** : `alembic upgrade head` après chaque pull de `develop`.
- **Staging** : migrations exécutées automatiquement par la CI/CD.
- **Production** : migrations exécutées manuellement via un job CI/CD (avec approbation).
- **Règle d’or** : Ne jamais modifier la base de production directement. Toute migration doit être testée localement puis en staging.

### 2.5. Bonnes pratiques pour éviter l’écart local/prod
- **Dockeriser tout** : même l’environnement de développement (backend, worker) pour coller à la production.
- **Utiliser les mêmes versions** : Python, Node.js, PostgreSQL, Redis – versionnées dans `.tool-versions` (asdf) ou dans les Dockerfiles.
- **Vérification pré-commit** : linter, formatteur, tests unitaires.
- **Test d’intégration local** : possibilité de lancer les mêmes tests que la CI en local (via `make test`).
- **Documentation** : un `README.md` détaillant les commandes de setup, les variables d’environnement et la procédure de mise à jour.

## 3. Livrables de l’étape 6

| Livrable | Format | Description |
|----------|--------|-------------|
| **Guide de setup local** | Markdown (`README.md`) | Étapes détaillées pour lancer l’environnement de développement |
| **Scripts d’initialisation** | Shell / Python | `./scripts/bootstrap.sh`, `./scripts/seed_local.py` |
| **Exemple de fichier `.env.local`** | Texte | Variables typiques pour le développement |
| **Script d’anonymisation** | Python | `./scripts/anonymize_prod_dump.py` pour préparer des données staging |
| **Documentation des différences** | Markdown | Tableau récapitulatif des différences entre local/staging/prod |

## 4. Prochaine action concrète


Voici la rédaction de la **sous‑étape 1 – Objectif de l’étape** pour l’organisation du travail local vs production.

---

## 1. Objectif de l’étape

L’objectif de l’étape **« Organisation du travail local vs production »** est de formaliser le flux de travail quotidien des développeurs, depuis leur machine locale jusqu’à la mise en production, en garantissant la reproductibilité et la fiabilité des environnements. Concrètement, il s’agit de :

### 1.1. Décrire le flux de travail typique d’un développeur

- De la création d’une branche locale à l’exécution des tests, en passant par le lancement de l’application complète (front, back, base de données, workers) via Docker.
- Jusqu’à l’intégration dans `develop`, le déploiement automatique sur staging, puis la mise en production via un tag.
- Ce flux doit être documenté, simple et rapide (moins de 5 minutes pour un nouveau contributeur).

### 1.2. Définir comment synchroniser les configurations, dépendances et données

- **Configurations** : utilisation de fichiers `.env` versionnés en exemple (`.env.example`) et chargement automatique des bonnes variables par environnement.
- **Dépendances** : fixation des versions (Python, Node, PostgreSQL, Redis) via Dockerfiles ou fichiers de version (`.tool-versions`, `package-lock.json`, `requirements.txt`).
- **Données** : script de seed pour le local (données fictives) et script d’anonymisation pour le staging (à partir d’un dump de production). Jamais de données réelles en local.

### 1.3. Établir des bonnes pratiques pour éviter les écarts (« ça marche sur ma machine »)

- **Dockeriser l’environnement de développement** (backend, workers, base de données, Redis) pour coller à la production.
- **Utiliser les mêmes versions** de tous les services localement et en production.
- **Automatiser les vérifications** (lint, tests, migrations) avant chaque commit via hooks Git ou CI.
- **Documenter** les procédures de mise à jour (migrations, nouvelles variables d’environnement).

### 1.4. Préciser les outils et scripts facilitant la reproduction

- **Outils** : Docker Compose, Git, make (ou tâches npm), `pre-commit`, `direnv` (optionnel).
- **Scripts** :
  - `bootstrap.sh` : clone, installe les dépendances, crée les fichiers `.env`, lance les containers.
  - `seed_local.py` : peuple la base locale avec des données de test réalistes.
  - `anonymize_prod_dump.py` : nettoie un dump de production pour créer un jeu de staging.
  - `run_tests_locally.sh` : exécute les mêmes tests que la CI en local.

**En résumé** : cette étape vise à rendre l’environnement de développement aussi proche que possible de la production, à réduire les frictions et à garantir que ce qui fonctionne localement fonctionnera aussi en staging et en production.

---
Voici la rédaction de la **sous‑étape 2.1 – Environnement de développement local (détaillé)** pour l’étape 6.

---

## 2. Démarche en 5 sous‑étapes

### 2.1. Environnement de développement local (détaillé)

**Objectif** : Fournir aux développeurs un environnement de travail complet, isolé et reproductible, leur permettant de coder, tester et exécuter l’ensemble de l’application (frontend, backend, base de données, workers) sur leur machine.

#### 2.1.1. Prérequis

Avant de commencer, le développeur doit avoir installé sur sa machine :

| Outil | Version minimale | Utilité |
|-------|------------------|---------|
| **Docker** | v20.10+ | Conteneurisation des services (base de données, Redis, backend, workers) |
| **Docker Compose** | v2.0+ | Orchestration des conteneurs |
| **Node.js** (optionnel pour le front si exécution hors Docker) | v20+ | Pour exécuter le frontend en mode développement (hot reload) |
| **Python** (optionnel pour le back hors Docker) | 3.11+ | Pour exécuter le backend localement (alternative au conteneur) |
| **Git** | v2.30+ | Clonage du dépôt |
| **Make** (recommandé) | – | Simplification des commandes récurrentes |

**Recommandation** : Utiliser Docker pour tous les services (y compris backend et front) afin d’éviter les différences d’environnement. Node.js et Python ne sont alors nécessaires que pour les IDE et les linters.

#### 2.1.2. Clonage et initialisation

```bash
# Cloner le dépôt
git clone https://github.com/organisation/ats-platform.git
cd ats-platform

# Copier le fichier d’exemple des variables d’environnement
cp .env.example .env

# (Optionnel) Éditer .env pour ajuster les ports ou les mots de passe
# Par défaut, les valeurs conviennent au développement local
```

**Contenu minimal de `.env.example`** :

```ini
# Base de données
POSTGRES_DB=ats_dev
POSTGRES_USER=ats
POSTGRES_PASSWORD=devpass

# Backend
DATABASE_URL=postgresql://ats:devpass@postgres:5432/ats_dev
REDIS_URL=redis://redis:6379
SECRET_KEY=dev_secret_key_unsafe_do_not_use_in_production

# Frontend (si exécution séparée)
REACT_APP_API_URL=http://localhost:8000

# Workers
PARSING_QUEUE=parsing_jobs
EMAIL_QUEUE=email_jobs
```

#### 2.1.3. Lancement de l’environnement

**Avec Docker Compose (recommandé)** :

```bash
# Construire et lancer tous les services (base, Redis, backend, workers)
docker-compose up -d

# Suivre les logs (optionnel)
docker-compose logs -f
```

**Sans Docker (pour le frontend uniquement)** :

```bash
cd front
npm install
npm start   # Lance le serveur de développement React sur http://localhost:3000
```

**Services lancés** :

| Service | Conteneur | Port exposé (local) | Accès |
|---------|-----------|---------------------|-------|
| PostgreSQL | `ats-postgres` | 5432 | `localhost:5432` |
| Redis | `ats-redis` | 6379 | `localhost:6379` |
| Backend (FastAPI) | `ats-backend` | 8000 | `http://localhost:8000` |
| Worker parsing | `ats-worker-parsing` | – | – |
| Worker email | `ats-worker-email` | – | – |
| Frontend (si inclus) | `ats-front` | 3000 | `http://localhost:3000` |

#### 2.1.4. Peuplement des données (seed)

Un script permet de créer des données fictives réalistes pour tester l’interface.

```bash
# Exécuter le script de seed (dans le conteneur backend ou localement)
docker exec -it ats-backend python scripts/seed_local.py
```

**Contenu du script `scripts/seed_local.py`** (exemple) :
- Création de 2 offres (ex: « Développeur Python », « Responsable Marketing ») avec critères pondérés.
- Création de 20 candidatures fictives (noms, emails, scores aléatoires, étapes diverses).
- Liaison des CV factices (fichiers `.txt` vides ou faux PDF).

**Alternative** : utiliser `docker-compose exec backend python scripts/seed_local.py`.

Le script doit être **idempotent** : s’il est exécuté plusieurs fois, il nettoie d’abord les données existantes (ou les ignore si déjà présentes).

#### 2.1.5. Accès aux services

| Service | URL | Identifiants (par défaut) |
|---------|-----|---------------------------|
| **Frontend (React)** | `http://localhost:3000` | Pas d’authentification (recruteur factice) ou recruteur@example.com / devpass |
| **API (FastAPI)** | `http://localhost:8000` | – |
| **Documentation interactive** | `http://localhost:8000/docs` | – |
| **PGAdmin (optionnel)** | `http://localhost:5050` | email: admin@example.com / mdp: admin (défini dans docker-compose) |
| **Redis Commander (optionnel)** | `http://localhost:8081` | – |

**Vérification du bon fonctionnement** :

```bash
# Tester l’API
curl http://localhost:8000/health
# Devrait retourner {"status":"ok"}

# Tester le front (si lancé)
open http://localhost:3000
```

#### 2.1.6. Commandes utiles (Makefile)

Pour simplifier, on peut ajouter un `Makefile` à la racine :

```makefile
.PHONY: up down logs seed clean

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

seed:
	docker-compose exec backend python scripts/seed_local.py

clean:
	docker-compose down -v
	rm -rf front/node_modules backend/__pycache__
```

**Utilisation** : `make up`, `make seed`, `make logs`.

**Cet environnement local permet de travailler exactement comme en production (mêmes versions, mêmes services), tout en étant rapide à initialiser et à reproductible.**

---
Voici la rédaction de la **sous‑étape 2.2 – Gestion des différences de configuration** pour l’étape 6.

---

## 2.2. Gestion des différences de configuration

**Objectif** : Permettre à l’application de s’exécuter correctement dans des environnements aux caractéristiques différentes (local, staging, production) sans modifier le code, en externalisant la configuration via des variables d’environnement.

### 2.2.1. Principe général : « Configuration as Code »

- Toute valeur qui varie selon l’environnement (URLs, clés API, mots de passe, niveau de logs, etc.) est stockée dans une **variable d’environnement**.
- Aucune configuration spécifique à un environnement n’est figée dans le code source.
- Les secrets (mots de passe, clés API) ne sont jamais versionnés.

### 2.2.2. Fichiers `.env` par environnement

| Environnement | Fichier | Versionné ? | Contenu typique |
|---------------|---------|-------------|------------------|
| Local | `.env` (ou `.env.local`) | Non (ignoré par `.gitignore`) | URLs locales, secrets factices, DEBUG=true |
| Staging | `.env.staging` | Non (mais documentation dans `.env.example`) | URLs staging, clés API de test, DEBUG=false |
| Production | `.env.production` | Non (géré par le gestionnaire de secrets de l’hébergeur) | URLs réelles, secrets forts, DEBUG=false |

**Fichier versionné** : `.env.example` (ou `.env.dist`) contenant toutes les variables nécessaires avec des exemples de valeurs (non sensibles). Chaque développeur copie ce fichier pour créer son `.env` local.

**Exemple de `.env.example`** :

```ini
# Backend
DEBUG=true
DATABASE_URL=postgresql://user:pass@localhost:5432/ats
REDIS_URL=redis://localhost:6379
SECRET_KEY=change_me_in_production
FRONTEND_URL=http://localhost:3000

# Services externes
SENDGRID_API_KEY=SG.mock_key
AWS_ACCESS_KEY_ID=mock
AWS_SECRET_ACCESS_KEY=mock
AWS_S3_BUCKET=ats-local-bucket

# Workers
PARSING_QUEUE=parsing_jobs
EMAIL_QUEUE=email_jobs
```

### 2.2.3. Variables différenciées par environnement

| Variable | Local | Staging | Production |
|----------|-------|---------|-------------|
| `DEBUG` | `true` | `false` | `false` |
| `DATABASE_URL` | postgresql://ats:devpass@postgres:5432/ats_dev | URL staging (RDS) | URL production (RDS) |
| `REDIS_URL` | redis://redis:6379 | URL Redis staging | URL Redis production |
| `FRONTEND_URL` | http://localhost:3000 | https://staging.ats.exemple.com | https://ats.exemple.com |
| `SECRET_KEY` | `dev_secret_key` (fixe) | Secret aléatoire (staging) | Secret aléatoire fort (production) |
| `SENDGRID_API_KEY` | clé factice (pas d’envoi réel) | clé de test (envoi en sandbox) | clé réelle |
| `AWS_S3_BUCKET` | `ats-cv-local` | `ats-cv-staging` | `ats-cv-prod` |

### 2.2.4. Chargement des variables dans l’application

**Backend (FastAPI)** : utilisation de `pydantic-settings` (ou `python-dotenv` pour les tests).

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    debug: bool = False
    database_url: str
    redis_url: str
    secret_key: str
    frontend_url: str
    sendgrid_api_key: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_s3_bucket: str
    parsing_queue: str = "parsing_jobs"
    email_queue: str = "email_jobs"

    class Config:
        env_file = ".env"  # automatiquement chargé
        env_file_encoding = "utf-8"

settings = Settings()
```

**Frontend (React)** : les variables exposées au navigateur doivent commencer par `REACT_APP_` (CRA) ou `VITE_` (Vite). Exemple :

```bash
REACT_APP_API_URL=http://localhost:8000
REACT_APP_SENTRY_DSN=
```

### 2.2.5. Utilisation de `direnv` (optionnel mais pratique)

`direnv` charge automatiquement les variables d’environnement lorsque l’on entre dans le répertoire du projet.

**Configuration** :

```bash
# Installer direnv (via brew, apt, etc.)
# Créer un fichier .envrc à la racine
echo "source_env .env" > .envrc
direnv allow
```

Désormais, chaque fois que l’on `cd` dans le projet, les variables du fichier `.env` sont automatiquement exportées dans le shell.

### 2.2.6. Gestion des secrets en staging et production

| Environnement | Solution |
|---------------|----------|
| **Staging** | Variables définies dans l’interface de la plateforme d’hébergement (Railway / Heroku / Vercel). Pas de fichier `.env` sur le serveur. |
| **Production** | Même principe, avec en plus un gestionnaire de secrets dédié (AWS Secrets Manager, GitHub Secrets pour la CI/CD). |

**Exemple pour Railway** : les variables sont ajoutées via l’interface web ou la CLI :

```bash
railway variables set SECRET_KEY="prod_secret_strong" DATABASE_URL="postgresql://..."
```

### 2.2.7. Bonnes pratiques

- **Ne jamais** versionner les fichiers `.env`, `.env.local`, `.env.staging`, `.env.production`.
- **Toujours** versionner `.env.example` (ou `.env.dist`) à jour.
- **Documenter** dans le `README.md` la liste des variables nécessaires et comment les obtenir.
- **Valider** au démarrage de l’application que les variables critiques sont présentes (ex: `SECRET_KEY` non vide, `DATABASE_URL` valide).
- **En production**, utiliser des secrets forts et les faire tourner régulièrement (rotation).

**Cette organisation garantit que l’application se comporte de manière prévisible quel que soit l’environnement, sans risque de fuite de secrets.**

---
Voici la rédaction de la **sous‑étape 2.3 – Stratégie de données : développement vs production** pour l’étape 6.

---

## 2.3. Stratégie de données : développement vs production

**Objectif** : Définir comment les données sont gérées dans chaque environnement (local, staging, production) pour garantir à la fois la confidentialité (RGPD) et la pertinence des tests, sans jamais exposer de données réelles en dehors de la production.

### 2.3.1. Principes généraux

| Environnement | Nature des données | Origine | Confidentialité |
|---------------|--------------------|---------|------------------|
| **Local** | Données fictives (fixtures) | Scripts de seed | Aucune donnée réelle |
| **Staging** | Données anonymisées (copie de production nettoyée) | Dump de production anonymisé | Données réelles mais anonymisées (noms, emails, IPs supprimés / remplacés) |
| **Production** | Données réelles des candidats et recruteurs | Saisie utilisateur | Hautement confidentielle (RGPD) |

**Règle d’or** : Aucune donnée réelle ne doit jamais se trouver sur la machine d’un développeur ou dans l’environnement de staging sans anonymisation préalable.

### 2.3.2. Environnement local : données fictives (fixtures)

**Objectif** : Permettre aux développeurs de travailler avec un jeu de données réaliste mais entièrement synthétique, reproductible et sans risque.

**Mécanisme** : script `scripts/seed_local.py` (ou `seed_local.sh`) qui :

1. Nettoie les tables existantes (sauf les références statiques comme les templates d’email par défaut).
2. Crée :
   - 2 à 5 offres d’emploi (titres, descriptions, critères pondérés, seuils d’alerte).
   - 20 à 50 candidatures (noms, emails fictifs, scores aléatoires, étapes variées).
   - Pour chaque candidature, un fichier CV factice (fichier `.txt` contenant « Ceci est un CV factice » ou un vrai petit PDF généré).
   - Des historiques d’actions et notes internes aléatoires.
3. Insère des utilisateurs (recruteurs) de test.

**Exemple de génération de noms fictifs** :

```python
import faker
fake = Faker('fr_FR')
nom = fake.name()
email = fake.email()
```

**Stockage des CV factices** : des fichiers placés dans `storage/mock_cvs/` sont copiés et renommés pour correspondre aux candidatures.

**Avantages** :
- Rapide à recréer (quelques secondes).
- Permet de tester tous les cas de figure (scores bas, hauts, étapes variées).
- Pas de risque de fuite de données personnelles.

### 2.3.3. Environnement staging : données anonymisées issues de production

**Objectif** : Disposer d’un volume de données réaliste (structure, répartition des scores, flux) pour les tests d’intégration et de recette, sans exposer d’informations personnelles.

**Processus** :

1. **Extraction** : Un dump (sauvegarde) de la base de données de production est réalisé (par exemple via `pg_dump`).
2. **Anonymisation** : Un script `scripts/anonymize_prod_dump.py` est exécuté sur le dump pour :
   - Remplacer les `nom_candidat` par des valeurs génériques (`Candidat_123`, `Candidat_456`).
   - Remplacer les `email` par des adresses fictives (`candidat_123@example.com`).
   - Supprimer ou anonymiser les `ip` et `user_agent`.
   - Supprimer les fichiers CV réels (remplacer par des CV factices dans le stockage associé).
   - Anonymiser les notes internes (supprimer les références personnelles).
   - (Optionnel) Conserver les scores, les dates (mais décaler les dates récentes pour ne pas refléter la réalité).
3. **Chargement** : Le dump anonymisé est chargé dans la base de données de staging.
4. **Fréquence** : hebdomadaire ou à la demande (avant une campagne de tests importante).

**Exemple de script d’anonymisation (SQL)** :

```sql
UPDATE candidature SET
  nom_candidat = 'Candidat_' || id,
  email = 'candidat_' || id || '@example.com',
  ip = '0.0.0.0',
  user_agent = 'anonymized'
WHERE id > 0;
```

Pour les fichiers CV : on supprime les fichiers réels du bucket S3 staging et on les remplace par un fichier factice (ex: `cv_fictif.pdf`).

**Attention** : Le script d’anonymisation ne doit pas être exécuté sur la production. Il s’applique sur une copie.

### 2.3.4. Environnement production : données réelles

- **Sauvegarde** : dumps quotidiens (automatisés) stockés chiffrés (ex: via AWS RDS snapshots, ou `pg_dump` + chiffrement GPG).
- **Accès** : seul le personnel autorisé (lead tech, DBA) peut accéder à la base de production en lecture (via un outil comme pgAdmin ou une connexion sécurisée).
- **Rétention** : Les données personnelles des candidats sont conservées 2 ans après la dernière action, puis supprimées (batch automatique).

### 2.3.5. Scripts recommandés

| Script | Emplacement | Utilisation |
|--------|-------------|--------------|
| `seed_local.py` | `scripts/` | Peupler la base locale de données fictives |
| `anonymize_prod_dump.py` | `scripts/` | Anonymiser un dump de production pour staging |
| `refresh_staging.sh` | `scripts/` | Automatiser : télécharger le dump, l’anonymiser, le charger en staging, remplacer les CV |
| `purge_old_data.py` | `scripts/` | Supprimer les candidatures de plus de 2 ans (production) |

### 2.3.6. Isolation des fichiers CV

- **Local** : stockage dans un volume Docker (`./storage/cvs`) – fichiers factices.
- **Staging** : bucket S3 dédié (`ats-cv-staging`) contenant uniquement des CV anonymisés ou factices.
- **Production** : bucket S3 séparé (`ats-cv-prod`) avec les vrais CV, accès restreint et URLs signées.

### 2.3.7. Bonnes pratiques

- **Ne jamais** copier la base de production directement en staging sans anonymisation.
- **Documenter** le processus d’anonymisation dans le README.
- **Tester** régulièrement le script d’anonymisation sur un petit sous-ensemble.
- **Utiliser des variables d’environnement** pour basculer entre les modes (ex: `USE_MOCK_STORAGE=true` en local).

**Cette stratégie garantit la conformité RGPD tout en offrant des environnements de test réalistes et sécurisés.**

---

Voici la rédaction de la **sous‑étape 2.4 – Synchronisation des migrations et du schéma** pour l’étape 6.

---

## 2.4. Synchronisation des migrations et du schéma

**Objectif** : Permettre de faire évoluer le schéma de la base de données (ajout de tables, colonnes, modifications) de manière contrôlée, séquentielle et réversible, sur tous les environnements (local, staging, production), sans perte de données ni rupture de service.

### 2.4.1. Outillage : Alembic (pour SQLAlchemy)

Le projet utilise **Alembic** (outil de migration de base de données pour Python/SQLAlchemy). Les migrations sont versionnées dans le dépôt Git.

- Fichiers de migration : `backend/migrations/versions/`.
- Fichier de configuration : `alembic.ini` (avec paramètres adaptés à chaque environnement).

### 2.4.2. Principes généraux

| Règle | Description |
|-------|-------------|
| **Une migration = une version** | Chaque changement de schéma donne lieu à un script de migration (upgrade) et son rollback (downgrade). |
| **Idempotence** | Appliquer plusieurs fois la même migration ne doit pas provoquer d’erreur. |
| **Rétrocompatibilité** | Les migrations doivent permettre au code ancien de fonctionner encore (pas de suppression de colonne sans préavis). |
| **Test systématique** | Toute migration est testée en local puis en staging avant production. |
| **Jamais de migration automatique sur production** | Le déploiement en production exécute les migrations de manière contrôlée (manuel ou via pipeline avec approbation). |

### 2.4.3. Workflow de création d’une migration

1. **Développeur** : modifie les modèles SQLAlchemy (ajout d’une colonne, nouvelle table, etc.).
2. **Génération automatique** (depuis le conteneur backend) :
   ```bash
   docker-compose exec backend alembic revision --autogenerate -m "ajout de la colonne xyz"
   ```
3. **Vérification** : le développeur examine le fichier généré (`versions/xxxx_ajout_colonne_xyz.py`) et ajuste si nécessaire (ex: valeurs par défaut, contraintes conditionnelles).
4. **Test local** : appliquer la migration sur la base locale :
   ```bash
   docker-compose exec backend alembic upgrade head
   ```
5. **Tester le rollback** :
   ```bash
   docker-compose exec backend alembic downgrade -1
   ```
6. **Commit** : le développeur commit le fichier de migration avec son code.

### 2.4.4. Application des migrations par environnement

| Environnement | Moment d’exécution | Mode | Responsabilité |
|---------------|--------------------|------|----------------|
| **Local** | Manuel, après chaque `git pull` | `alembic upgrade head` | Développeur |
| **CI (tests)** | Automatique avant les tests d’intégration | `alembic upgrade head` sur base éphémère | Pipeline CI |
| **Staging** | Automatique lors du déploiement (après build, avant démarrage backend) | `alembic upgrade head` | Pipeline CD (staging) |
| **Production** | Semi‑automatique (déclenché par le pipeline, mais avec validation humaine) | `alembic upgrade head` | Pipeline CD (prod) après approbation |

**Exemple d’étape dans GitHub Actions (staging)** :

```yaml
- name: Run migrations (staging)
  run: |
    docker-compose exec backend alembic upgrade head
  env:
    DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}
```

### 2.4.5. Règles pour les migrations rétrocompatibles

| Type de changement | Rétrocompatible ? | Exemple | Recommandation |
|--------------------|-------------------|---------|----------------|
| Ajout d’une colonne nullable | Oui | `ALTER TABLE candidature ADD COLUMN notes TEXT;` | Sans risque |
| Ajout d’une colonne non nullable avec défaut | Oui | `ADD COLUMN active BOOLEAN DEFAULT TRUE NOT NULL;` | Sans risque |
| Création d’une nouvelle table | Oui | `CREATE TABLE ...` | Sans risque |
| Suppression d’une colonne | Non (rupture pour ancien code) | `DROP COLUMN old_field` | Prévoir plusieurs étapes : d’abord rendre nullable, puis supprimer après que le code ne l’utilise plus |
| Renommage de colonne | Risqué | `ALTER TABLE ... RENAME COLUMN a TO b` | À éviter en MVP ; préférer ajouter nouvelle colonne, migrer les données, puis supprimer l’ancienne |
| Changement de type de colonne | Parfois possible si compatible | `INT` → `BIGINT` | Peut nécessiter une migration en plusieurs étapes |

### 2.4.6. Gestion des migrations en équipe

- **Fichiers de migration** : ils doivent être commités avant la fusion de la feature branch.
- **Conflits** : si deux développeurs créent des migrations avec le même identifiant (révision), Alembic détecte un conflit. Solution : rebaser la branche et générer une nouvelle migration après avoir pris en compte celle de `develop`.
- **Ordre d’exécution** : Alembic utilise un numéro de révision (horodatage) pour ordonner les migrations. Il n’y a donc pas de risque d’exécution dans le désordre si les migrations sont correctement générées.

### 2.4.7. Migration sur production : procédure pas à pas

1. Le pipeline de CD production est déclenché par la création d’un tag (ex: `v1.2.0`).
2. Une étape **manuelle** (approbation) est requise pour exécuter les migrations (par sécurité).
3. Une fois approuvée, le pipeline exécute :
   ```bash
   alembic upgrade head
   ```
4. Si la migration réussit, le backend est redémarré avec la nouvelle version.
5. Si la migration échoue (ex: contrainte violée), le pipeline s’arrête et alerte l’équipe. Aucun déploiement n’est effectué.

**Exemple de job avec environnement protégé** :

```yaml
deploy-prod:
  environment: production
  steps:
    - name: Approve and run migrations
      run: alembic upgrade head
```

### 2.4.8. Procédure de rollback de migration

Si une migration en production cause un problème :

- **Option 1** : Si la migration est **rétrocompatible**, on peut simplement déployer la version précédente du code (qui ignore la nouvelle colonne). La migration reste appliquée mais n’est pas utilisée.
- **Option 2** : Exécuter un downgrade :
  ```bash
  alembic downgrade -1
  ```
  Cela nécessite que le script de downgrade ait été écrit et testé. C’est à privilégier si l’ancien code ne peut pas fonctionner avec le nouveau schéma.

**Règle** : Toute migration doit fournir une méthode `downgrade()` (Alembic la génère automatiquement pour les opérations simples ; pour les opérations complexes, il faut l’écrire manuellement).

### 2.4.9. Vérification de l’état des migrations

Alembic permet de vérifier si la base est à jour :

```bash
alembic current   # montre la révision actuelle
alembic history   # liste les migrations appliquées
```

Dans le tableau de bord d’administration (V2), on pourra afficher la version du schéma.

### 2.4.10. Bonnes pratiques

- **Tester systématiquement** les migrations sur une copie de staging avant production.
- **Ne jamais modifier** une migration déjà commitée et poussée sur `develop` (créer une nouvelle migration corrective).
- **Utiliser des migrations transactionnelles** (PostgreSQL supporte DDL transactionnel) : si une migration échoue, elle est annulée.
- **Documenter** dans le README la procédure pour appliquer les migrations localement.

**Cette stratégie garantit que tous les environnements restent synchronisés et que les évolutions du schéma sont maîtrisées, testées et réversibles.**

---

Voici la rédaction de la **sous‑étape 2.5 – Bonnes pratiques pour éviter l’écart local/prod** pour l’étape 6.

---

## 2.5. Bonnes pratiques pour éviter l’écart local/prod

**Objectif** : Éliminer les différences entre l’environnement de développement local et la production, afin de réduire le risque de bugs inattendus (« ça marche sur ma machine ») et d’accélérer la livraison.

### 2.5.1. Utiliser Docker partout (même en développement)

- **Conteneuriser le backend et les workers** : leur environnement d’exécution (système, dépendances, versions) est strictement identique localement, en staging et en production.
- **Utiliser Docker Compose pour orchestrer** : base de données, Redis, backend, workers, voire frontend.
- **Bannir les installations « à la main »** : tout nouveau développeur doit pouvoir lancer `docker-compose up` et avoir un environnement complet sans configuration supplémentaire.

**À faire** :
- Le `Dockerfile` de développement peut être le même que celui de production (ou en hériter).
- Utiliser des volumes pour le code source (hot reload) et les fichiers statiques.

### 2.5.2. Fixer les versions de toutes les dépendances

| Composant | Fichier de version |
|-----------|---------------------|
| Backend (Python) | `requirements.txt` (avec versions exactes, ex: `fastapi==0.115.0`) |
| Frontend (Node) | `package-lock.json` (ou `yarn.lock`) |
| Base de données | Version de l’image Docker (ex: `postgres:15`) |
| Redis | Image Docker (ex: `redis:7`) |
| Outils système | `Dockerfile` avec `apt-get install` de versions spécifiques |

**Outil recommandé** : `pip-tools` pour générer `requirements.txt` à partir de `requirements.in`, ou `poetry` / `pipenv`.

### 2.5.3. Appliquer les mêmes hooks et vérifications en local qu’en CI

**Objectif** : détecter les erreurs de lint, de formatage ou de tests avant même de pousser le code.

- **Hooks Git** (via `pre-commit`) :
  ```yaml
  # .pre-commit-config.yaml
  repos:
    - repo: local
      hooks:
        - id: flake8
          name: flake8
          entry: flake8 backend/
          language: system
        - id: black
          name: black
          entry: black --check backend/
          language: system
        - id: eslint
          name: eslint
          entry: npm run lint
          files: ^front/
          language: node
  ```
- **Makefile** pour exécuter les mêmes commandes que la CI :
  ```makefile
  ci-lint:  # appelé par le hook et par GitHub Actions
  	docker-compose run --rm backend flake8 .
  	docker-compose run --rm front npm run lint
  ci-test:
  	docker-compose run --rm backend pytest
  	docker-compose run --rm front npm test
  ```

### 2.5.4. Éviter les chemins absolus et les configurations implicites

- **Variables d’environnement** pour tout paramètre variable (ports, URLs, chemins de stockage).
- **Ne jamais coder en dur** un chemin comme `/home/user/projet/data`. Utiliser `os.getenv()` ou `settings`.
- **Fichiers de configuration** : les valeurs par défaut doivent être adaptées à Docker (ex: `DATABASE_URL=postgresql://ats:devpass@postgres:5432/ats_dev`).

### 2.5.5. Mocker les services externes en local, mais utiliser les vrais en staging/prod

| Service | Local (mock) | Staging / Prod |
|---------|--------------|----------------|
| Envoi d’emails | Logger seulement (pas de vrai SMTP) | SendGrid / AWS SES |
| Stockage CV | Système de fichiers local (volume Docker) | S3 |
| Paiement (future V2) | Mode sandbox | Mode réel |

**Exemple** : en développement, on peut désactiver l’envoi réel d’emails en utilisant un backend factice (`smtp://localhost:1025` avec MailHog).

### 2.5.6. Tester les migrations en local avant chaque déploiement

- Avant de pousser une branche, toujours exécuter `alembic upgrade head` localement.
- Tester également `alembic downgrade -1` pour vérifier la réversibilité.
- Utiliser une base de données locale **propre** (recréée avec `docker-compose down -v`) pour éviter les résidus.

### 2.5.7. Utiliser des scripts d’intégration continue en local

Les mêmes commandes que la CI doivent pouvoir être exécutées localement. Par exemple :

```bash
# Exécuter le même lint que GitHub Actions
make ci-lint

# Exécuter les tests unitaires et d’intégration
make ci-test

# Vérifier le build des images Docker
make ci-docker-build
```

### 2.5.8. Documenter les différences connues

Malgré tous ces efforts, certaines différences peuvent persister (ex: OS sous-jacent, performances réseau). Il faut les documenter dans un fichier `KNOWN_DIFFERENCES.md` :

| Différence | Impact | Contournement |
|------------|--------|----------------|
| Système de fichiers (Linux vs macOS) | Sensibilité à la casse | Utiliser des volumes Docker avec des noms cohérents |
| Résolution DNS dans Docker | `localhost` vs `postgres` | Utiliser les noms de services définis dans `docker-compose.yml` |
| Débits réseau (S3 local vs réel) | Tests de performance biaisés | Utiliser un bucket S3 factice (MinIO) en local |

### 2.5.9. Mettre en place un environnement de staging identique à la production

- **Mêmes versions** d’OS (Linux), de base de données, de Redis, de Python, Node.
- **Même fournisseur cloud** (ex: AWS) avec des services managés (RDS, ElastiCache) plutôt que des conteneurs artisanaux.
- **Mêmes variables d’environnement** (sauf les secrets bien sûr).

**Si staging ressemble exactement à production, alors « ça marche en staging » équivaut à « ça marchera en production ».**

### 2.5.10. Checklist avant de dire « fini »

Avant de fusionner une fonctionnalité dans `develop`, le développeur doit vérifier :

- [ ] Le code passe les tests en local (`make ci-test`).
- [ ] Les migrations s’appliquent et se rétropédalent sans erreur.
- [ ] L’application démarre avec `docker-compose up` sans erreur.
- [ ] Les variables d’environnement sont documentées dans `.env.example`.
- [ ] Aucun chemin absolu ou configuration codée en dur n’est présent.
- [ ] Les mocks sont utilisés pour les services externes (emails, stockage).

**Cette liste de bonnes pratiques, appliquée rigoureusement, élimine la grande majorité des écarts entre local et production.**

---

**L’étape 6 (Organisation du travail local vs prod) est désormais complète.**
