# Smart Starter VTherm

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Intégration Home Assistant pour Versatile Thermostat (VTherm). Démarre le chauffage en avance de façon intelligente pour garantir la température cible exacte à l'heure planifiée, en tenant compte du slope thermique, de la température extérieure et du planning.

## 🌟 Fonctionnalités

- **Calcul intelligent du temps de préchauffage** : Détermine automatiquement quand démarrer le chauffage pour atteindre la température cible à l'heure exacte
- **Prise en compte des conditions extérieures** : Adapte le calcul en fonction de la température extérieure
- **Modélisation thermique** : Utilise le "slope thermique" (vitesse de chauffe) de votre pièce
- **Service Home Assistant** : Facile à intégrer dans vos automatisations
- **Capteurs dédiés** : Expose la durée de préchauffage et l'heure de démarrage optimale
- **Interface de configuration** : Configuration via l'interface utilisateur Home Assistant

## 📋 Prérequis

- Home Assistant 2023.1.0 ou supérieur
- Versatile Thermostat (recommandé mais pas obligatoire)
- Capteurs de température (intérieure et extérieure)

## 🚀 Installation

### Via HACS (recommandé)

1. Ouvrez HACS dans votre Home Assistant
2. Allez dans "Intégrations"
3. Cliquez sur les trois points en haut à droite et sélectionnez "Dépôts personnalisés"
4. Ajoutez l'URL : `https://github.com/RastaChaum/SmartStarterVTherm`
5. Sélectionnez la catégorie "Intégration"
6. Cliquez sur "Télécharger"
7. Redémarrez Home Assistant

### Installation manuelle

1. Copiez le dossier `custom_components/smart_starter_vtherm` dans votre dossier `custom_components` de Home Assistant
2. Redémarrez Home Assistant

## ⚙️ Configuration

### Via l'interface utilisateur

1. Allez dans **Configuration** → **Intégrations**
2. Cliquez sur **+ Ajouter une intégration**
3. Recherchez "Smart Starter VTherm"
4. Suivez les instructions de configuration :
   - **Nom** : Nom de votre instance
   - **Capteur de température actuelle** (optionnel) : Entité de température de la pièce
   - **Entité de température cible** (optionnel) : Thermostat ou input_number
   - **Capteur de température extérieure** (optionnel) : Température extérieure
   - **Pente thermique** : Vitesse de chauffe en °C/h (par défaut : 2.0)

## 📊 Utilisation

### Service : `smart_starter_vtherm.calculate_start_time`

Calcule l'heure de démarrage optimale pour atteindre la température cible.

**Paramètres :**
- `current_temp` (requis) : Température actuelle en °C
- `target_temp` (requis) : Température cible en °C
- `outdoor_temp` (requis) : Température extérieure en °C
- `target_time` (requis) : Heure cible (format : "2024-01-15 07:00:00")
- `thermal_slope` (optionnel) : Pente thermique en °C/h (défaut : 2.0)

**Exemple d'appel de service :**

```yaml
service: smart_starter_vtherm.calculate_start_time
data:
  current_temp: 18.5
  target_temp: 21.0
  outdoor_temp: 5.0
  target_time: "2024-01-15 07:00:00"
  thermal_slope: 2.5
```

### Capteurs

L'intégration crée automatiquement deux capteurs :

1. **Preheat Duration** : Durée de préchauffage nécessaire (en minutes)
2. **Start Time** : Heure de démarrage optimale (timestamp)

### Exemple d'automatisation

```yaml
automation:
  - alias: "Démarrage intelligent du chauffage"
    trigger:
      - platform: time_pattern
        minutes: "/5"  # Vérifie toutes les 5 minutes
    action:
      - service: smart_starter_vtherm.calculate_start_time
        data:
          current_temp: "{{ states('sensor.salon_temperature') }}"
          target_temp: 21.0
          outdoor_temp: "{{ states('sensor.outdoor_temperature') }}"
          target_time: "{{ states('sensor.scheduler_next_time') }}"
          thermal_slope: 2.0
      - condition: template
        value_template: "{{ states('sensor.smart_starter_vtherm_start_time') <= now() }}"
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.versatile_thermostat
        data:
          hvac_mode: heat
```

## 🧮 Logique de calcul

Le calcul prend en compte :

1. **Différence de température (ΔT)** : `target_temp - current_temp`
2. **Facteur extérieur** : Impact de la température extérieure sur la vitesse de chauffe
   - Formule : `outdoor_factor = 1 + (20 - outdoor_temp) * 0.05`
   - À 20°C extérieur : facteur = 1.0 (pas d'impact)
   - À 0°C extérieur : facteur = 2.0 (chauffe deux fois plus lente)
   - À -10°C extérieur : facteur = 2.5
3. **Pente thermique effective** : `effective_slope = thermal_slope / outdoor_factor`
4. **Durée de préchauffage** : `duration = ΔT / effective_slope` (en heures, converti en minutes)
5. **Heure de démarrage** : `start_time = target_time - duration`

### Exemple de calcul

**Conditions :**
- Température actuelle : 18°C
- Température cible : 21°C
- Température extérieure : 5°C
- Pente thermique : 2.0°C/h
- Heure cible : 07:00

**Calcul :**
1. ΔT = 21 - 18 = 3°C
2. outdoor_factor = 1 + (20 - 5) * 0.05 = 1.75
3. effective_slope = 2.0 / 1.75 = 1.14°C/h
4. duration = 3 / 1.14 = 2.63 heures = 158 minutes
5. start_time = 07:00 - 158 min = 04:22

**Résultat : Démarrer le chauffage à 04:22 pour atteindre 21°C à 07:00**

## 🔧 Déterminer votre pente thermique

La pente thermique représente la vitesse à laquelle votre pièce se réchauffe. Pour la déterminer :

1. Notez la température initiale de votre pièce
2. Démarrez le chauffage à pleine puissance
3. Après 1 heure, notez la nouvelle température
4. La différence est votre pente thermique en °C/h

Exemple : 18°C → 20°C après 1h = pente de 2.0°C/h

**Facteurs influençant la pente thermique :**
- Isolation de la pièce
- Puissance du radiateur
- Volume de la pièce
- Type de chauffage

## 🐛 Dépannage

### Le service ne calcule pas correctement

- Vérifiez que tous les paramètres sont corrects
- Assurez-vous que la pente thermique correspond à votre installation
- Consultez les logs Home Assistant pour plus de détails

### Les capteurs ne se mettent pas à jour

- Vérifiez que le service a été appelé au moins une fois
- Les capteurs sont mis à jour lors de l'événement `smart_starter_vtherm_calculation_complete`

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Soumettre des pull requests

## 📝 Licence

Ce projet est sous licence MIT.

## 👏 Remerciements

- [Versatile Thermostat](https://github.com/jmcollin78/versatile_thermostat) pour l'inspiration
- La communauté Home Assistant
