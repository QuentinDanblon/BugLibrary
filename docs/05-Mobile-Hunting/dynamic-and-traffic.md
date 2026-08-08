# Dynamic Analysis & Traffic

## Setup principles

- Dedicated test device/emulator  
- Separate Google/Apple test accounts  
- Proxy only in-scope hosts when possible  
- Log correlation IDs for reports  

## WebView risks

- JavaScript bridges  
- Mixed content  
- Open file / intent URLs  

## Deep links

Test whether deep links trigger authenticated actions without re-auth or can inject parameters into WebViews.

## FR

Device de test dédié, proxy scopé, WebViews et deep links prioritaires.
