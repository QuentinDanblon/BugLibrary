# 07 — Binary Analysis & Reverse Engineering

## Contexte

Moins fréquent en bug bounty pur (davantage en pentest hardware/firmware ou programmes spécifiques desktop/CTF-like), mais à très haut payout quand applicable (agents desktop, clients VPN, firmware IoT, applications de sécurité elles-mêmes).

## Setup et outils de base

| Outil | Usage |
|---|---|
| Ghidra (gratuit, NSA) | Désassemblage/décompilation, analyse statique de binaires |
| IDA Pro / IDA Free | Référence historique, décompilateur Hex-Rays puissant |
| Binary Ninja | Alternative moderne, API Python solide pour scripting |
| x64dbg / WinDbg | Debug dynamique Windows |
| GDB + GEF/pwndbg | Debug dynamique Linux, exploitation binaire |
| Frida | Instrumentation dynamique cross-platform (voir aussi 05-Mobile-Hunting) |
| radare2 / rizin | Analyse légère scriptable en ligne de commande |
| Binwalk | Extraction de firmware, identification de filesystems embarqués |
| QEMU (mode user/system) | Émulation d'architectures pour firmware (ARM/MIPS) sans hardware physique |

## Analyse statique — première passe

```bash
file binary_target
strings -n 8 binary_target | grep -iE "password|key|token|http|debug"
checksec --file=binary_target   # protections actives : NX, PIE, RELRO, Stack Canary, ASLR
```

**Signaux à chercher immédiatement :**
- Absence de protections modernes (pas de PIE, pas de stack canary) → surface d'exploitation mémoire plus large.
- Chaînes de format de debug/logs laissées en build release (fuite d'info sur la structure interne).
- Fonctions dangereuses statiquement liées (`strcpy`, `sprintf`, `system`, `gets`) — pistes pour buffer overflow/injection de commande.

## Firmware IoT — méthodologie

```bash
# Extraction du filesystem depuis une image firmware
binwalk -e firmware.bin

# Analyse du filesystem extrait
grep -r "password" squashfs-root/etc/
find squashfs-root/ -name "*.key" -o -name "*.pem"

# Émulation pour analyse dynamique (approche FirmAE / qemu manuel)
qemu-arm-static -L squashfs-root/ squashfs-root/usr/bin/binaire_cible
```

**Vecteurs fréquents firmware :**
- Credentials hardcodés (souvent visibles directement en `strings` sur les fichiers de config extraits).
- Services réseau exposés par défaut sans authentification (telnet, interfaces de debug UART/JTAG laissées actives).
- Mécanismes de mise à jour firmware non signés/non vérifiés (possibilité d'injecter un firmware malveillant si le flow d'update est exploitable à distance).
- API de gestion locale (souvent HTTP non chiffré) avec des vulnérabilités web classiques (voir section 03) appliquées à une interface embarquée.

## Memory Corruption — bases pour bug bounty avec composante binaire

> ℹ️ Le développement d'exploits memory corruption complets (ROP chains, heap exploitation) est un domaine à part entière. Cette section couvre le nécessaire pour **identifier et documenter** une vulnérabilité en contexte bug bounty (souvent suffisant : crash reproductible + analyse de la cause + preuve de contrôle du flux d'exécution), pas un cours complet d'exploit dev.

| Classe de vulnérabilité | Signal de détection |
|---|---|
| Stack buffer overflow | Fonctions `strcpy`/`sprintf`/`gets` sur des buffers de taille fixe alimentés par une entrée utilisateur non bornée |
| Heap overflow / Use-After-Free | Fuzzing avec ASAN activé révèle un crash sur accès mémoire invalide après `free()` |
| Format string | Utilisateur contrôle directement ou partiellement le premier argument d'une fonction `printf`-like |
| Integer overflow → buffer overflow | Calcul de taille de buffer basé sur une entrée utilisateur sans vérification de dépassement avant allocation |

### Fuzzing pour découverte de crash

```bash
# AFL++ — fuzzing guidé par couverture de code, référence actuelle
afl-fuzz -i corpus_initial/ -o findings/ -- ./binaire_cible @@

# libFuzzer (intégré à un harness écrit pour la cible, avec ASAN/UBSAN)
clang++ -fsanitize=fuzzer,address harness.cpp -o fuzzer
./fuzzer corpus/
```

> 💡 **Pro tip :** Pour un programme de bug bounty ciblant un binaire/produit desktop, un simple crash reproductible avec **stack trace claire montrant une corruption mémoire** (ASAN output) est déjà un rapport valide et souvent payé — tu n'as pas toujours besoin de pousser jusqu'à une PoC RCE complète pour obtenir une sévérité Haute, mais démontrer l'exploitabilité (contrôle du RIP/PC, écrasement d'un pointeur de fonction) augmente significativement le payout.

## Analyse dynamique avec Frida (cross-platform)

```javascript
// Exemple : hooker une fonction pour observer/modifier ses arguments à l'exécution
Interceptor.attach(Module.findExportByName(null, "validate_license"), {
  onEnter: function(args) {
    console.log("Appel validate_license, arg0: " + args[0].readCString());
  },
  onLeave: function(retval) {
    console.log("Retour original: " + retval);
    retval.replace(1); // forcer un retour "valide" pour tester la logique en aval
  }
});
```

## Comment confirmer l'impact

- Crash reproductible : fournir le binaire d'entrée exact (input fuzzing minimisé), la stack trace ASAN/debugger, et les étapes de reproduction exactes.
- RCE : démonstration de contrôle du flux d'exécution (ex: écrasement d'une adresse de retour avec une valeur contrôlée, visible dans le debugger) — exécution de code arbitraire seulement si strictement nécessaire et autorisé par le scope.
- Firmware : preuve d'accès (credentials extraits, service exposé identifié) sans action destructrice sur un device physique de production s'il y en a un dans le scope.

## Références

- Ghidra / NSA documentation officielle
- `AFL++` documentation et techniques de harnessing
- "The Shellcoder's Handbook" (référence historique toujours pertinente sur les fondamentaux)
- OWASP Firmware Security Testing Methodology
- HackTricks — Reversing, Binary Exploitation
