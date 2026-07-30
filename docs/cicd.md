# Pipeline CI/CD — Vue d'ensemble

Ce pipeline orchestre l'intégration continue de l'application selon la séquence suivante :  
**Lint → Test → Build, Scan & Push**

---

### 1. Lint

On vérifie le code source de manière statique (sans l'exécuter) à l'aide de **Ruff**.  
C'est l'étape la plus rapide et la moins coûteuse en ressources : elle est placée en tout début de pipeline selon le principe de **Fail-Fast**. Il est inutile d'exécuter des tests ou de builder une image Docker si le code ne respecte pas les standards de qualité ou comporte des erreurs de syntaxe.

---

### 2. Test

L'application est testée via son jeu de tests unitaires et d'intégration (`test_main.py`). Cette étape s'assure que les fonctionnalités principales de l'API / du service répondent correctement avant tout packaging.

---

### 3. Build, Scan & Push (Job Unique)

Cette phase est regroupée dans **un seul job CI** pour des raisons architecturales : le daemon Docker utilisé est isolé à l'environnement de ce job (`Docker-in-Docker / dind`). Séparer le build et le push dans des jobs distincts nécessiterait de re-puller l'image intermédiaire depuis la registry dans le second job, entraînant des I/O inutiles et un ralentissement du pipeline.

Au sein de ce job :
1. **Authentification** : Connexion sécurisée à la Container Registry en utilisant `--password-stdin` (voir section *Sécurité*).
2. **Build** : Construction de l'image Docker à partir du `Dockerfile`.
3. **Tagging** : Tag de l'image avec le SHA du commit Git (`$CI_COMMIT_SHORT_SHA`) afin d'assurer l'**immutabilité** des déploiements et une **traçabilité** exacte entre le code et l'image produite.
4. **Scan Sécurité** : Analyse des vulnérabilités via Trivy.
5. **Push** : Publication de l'image auditée sur la registry.

---

### 4. Sécurité & Analyse des Vulnérabilités

- **Authentification sécurisée** : La connexion à la registry Docker s'effectue via `echo "$CI_JOB_TOKEN" | docker login -u "$CI_REGISTRY_USER" --password-stdin $CI_REGISTRY`. L'option `--password-stdin` garantit que le jeton d'authentification ne passe jamais en argument de ligne de commande, évitant toute fuite dans la table des processus (`ps`).
- **Analyse d'image** : Le scan de sécurité a lieu **après le build et strictement avant le push** sur la registry afin d'éviter la propagation d'images vulnérables.

L'outil **Trivy** est exécuté pour analyser deux couches distinctes :
- **L'image de base (Système)** : Analyse des paquets de l'OS (ex: paquets Debian/Alpine).
- **Les dépendances applicatives** : Analyse des packages Python (`requirements.txt`).

#### Stratégie de contrôle à deux niveaux :
1. **Passage informatif** : Détection exhaustive de toutes les CVE (de `LOW` à `CRITICAL`) pour l'audit et la visibilité dans les logs du pipeline, sans bloquer le job.
2. **Quality Gate (Bloquant)** : Détection ciblée des vulnérabilités critiques (`CRITICAL`). 
   - Utilisation de l'option `--ignore-unfixed` pour ne pas bloquer le pipeline si aucun correctif n'est encore disponible par les éditeurs.

---

### 5. Choix d'Architecture & Trade-offs

- **Isolation (dind vs Socket Docker)** : Utilisation du service `docker:dind` pour garantir un environnement de build totalement isolé, évitant de partager le socket du host CI (`/var/run/docker.sock`) et réduisant les risques d'élévation de privilèges sur les runners.
- **Factorisation YAML (DRY)** : Utilisation d'ancres YAML (`&` / `*`) et du bloc `default:` dans GitLab CI pour réutiliser la configuration des images et des variables sans duplication.

---

### 6. Dette Technique Assumée

- **Image de base & CVE Système** : L'utilisation d'une image de base standard génère quelques CVE système connues (ex: dépendances Perl/Debian) qui ne disposent pas encore de correctifs (`unfixed`).
- **Évolution prévue** : Migration future vers une image de base plus sobre (*Distroless* ou *Alpine*) pour réduire la surface d'attaque et éliminer les paquets système inutiles en production.