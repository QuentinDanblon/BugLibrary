# Mobile Static Analysis

## Goals

- Extract API hosts and paths  
- Find hardcoded secrets (report exposure; rotate expectation)  
- Map deep links and exported entry points  
- Note debuggable/backup flags (often low severity alone)  

## Android (high level)

- Manifest: exported activities/receivers/services/providers  
- Strings/resources for URLs  
- Network security config  
- Flutter/React Native bundles may hold JS-like routes  

## iOS (high level)

- Info.plist URL schemes  
- Embedded config plists  
- Swift/ObjC string extraction  

## Secret handling ethics

If you find live cloud keys: **report urgently**, do not spend quota, do not access foreign data.

## FR

Extraire hosts, secrets (signaler sans abuser), deep links, exports. Clés cloud live = urgence, pas d’exploration abusive.
